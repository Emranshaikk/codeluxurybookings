# Elite Luxury Bookings - Bulk Purge & Standardization Script
# Target: Purge Yacht/Villa content, Remove Valens, Standardize Lead Capture

$cleanNav = @"
            <ul class="nav-links">
                <li><a href="/elite-private-jet-charter.html">Private Jets</a></li>
                <li><a href="/blog.html">Blog</a></li>
                <li><a href="/contact.html">Contact</a></li>
            </ul>
"@

$cleanMobileMenu = @"
    <div class="mobile-menu" id="elbMobileMenu">
        <a href="/elite-private-jet-charter.html">Private Jets</a>
        <a href="/blog.html">Articles & News</a>
        <a href="/contact.html">Contact Us</a>
        <a href="https://wa.me/918801079030" class="mobile-cta">WhatsApp Concierge</a>
    </div>
"@

$leadFormTemplate = @"
            <div class="glass-panel" style="padding: 3rem; border: 1px solid var(--primary-gold); background: #000; border-radius: 24px; box-shadow: 0 40px 100px rgba(0,0,0,0.8);">
                <div style="text-align: center; margin-bottom: 3rem;">
                    <h2 class="serif gold-text" style="font-size: 2.5rem; margin-bottom: 1rem;">Global Charter Inquiry</h2>
                    <p style="color: var(--text-muted); text-transform: uppercase; letter-spacing: 3px; font-size: 0.8rem;">24/7 Concierge Dispatch</p>
                </div>
                <form action="https://formspree.io/f/xwvwanlj" method="POST">
                    <input type="hidden" name="_subject" value="GLOBAL INQUIRY: Private Jet Charter">
                    <input type="hidden" name="Source" value="[[SOURCE_NAME]]">
                    <div class="form-grid">
                        <div class="form-group">
                            <label>Full Name</label>
                            <input type="text" name="name" class="form-control" placeholder="e.g. James Harrington" required>
                        </div>
                        <div class="form-group">
                            <label>WhatsApp / Phone</label>
                            <input type="tel" name="phone" class="form-control" placeholder="+44 7XXX XXXXXX" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Email Address</label>
                        <input type="email" name="email" class="form-control" placeholder="client@privatemail.com" required>
                    </div>
                    <div class="form-grid">
                        <div class="form-group">
                            <label>Departure City</label>
                            <input type="text" name="from" class="form-control" placeholder="City or Code" required>
                        </div>
                        <div class="form-group">
                            <label>Destination City</label>
                            <input type="text" name="to" class="form-control" placeholder="City or Code" required>
                        </div>
                    </div>
                    <div class="form-grid">
                        <div class="form-group">
                            <label>Preferred Date</label>
                            <input type="date" name="date" class="form-control" style="color-scheme: dark;">
                        </div>
                        <div class="form-group">
                            <label>Passengers</label>
                            <input type="number" name="pax" class="form-control" placeholder="Quantity">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Special Requirements</label>
                        <textarea name="message" class="form-control" rows="3" placeholder="Aircraft preference, catering, or urgent dispatch needs..." style="resize: none;"></textarea>
                    </div>
                    <button type="submit" class="btn btn-gold" style="width: 100%; padding: 1.5rem; font-size: 1.1rem; border-radius: 12px; margin-top: 1rem; background: linear-gradient(135deg, #D4AF37, #B8860B); color: #000 !important;">
                        Submit Confidential Inquiry
                    </button>
                </form>
            </div>
"@

$htmlFiles = Get-ChildItem -Filter *.html

foreach ($file in $htmlFiles) {
    Write-Host "Processing $($file.Name)..."
    $content = Get-Content $file.FullName -Raw

    # 1. Purge Legacy Nav Links
    $navPattern = '(?s)<ul class="nav-links">.*?</ul>'
    $content = [regex]::Replace($content, $navPattern, $cleanNav)

    # 2. Purge Mobile Menu
    $mobilePattern = '(?s)<div class="mobile-menu" id="elbMobileMenu">.*?</div>'
    $content = [regex]::Replace($content, $mobilePattern, $cleanMobileMenu)

    # 3. Purge Valens Widget and Replace with Formspree
    if ($content -match 'ELB_VALENS_WIDGET_START') {
        $sourceName = $file.BaseName -replace '-private-jet-cost', '' -replace '-', ' '
        if ($file.Name -eq "index.html") { $sourceName = "Homepage" }
        elseif ($file.Name -eq "elite-private-jet-charter.html") { $sourceName = "Aviation Hub" }
        
        $routeLeadForm = $leadFormTemplate -replace '\[\[SOURCE_NAME\]\]', "Route: $sourceName"
        
        $valensPattern = '(?s)<!-- ELB_VALENS_WIDGET_START -->.*?<!-- ELB_VALENS_WIDGET_END -->'
        $content = [regex]::Replace($content, $valensPattern, $routeLeadForm)
    }

    # 4. Standalone Valens cleanup (if widget missing but mentions exist)
    $content = $content -replace 'Elite Luxury Bookings \| Powered by Valens Core', 'Elite Luxury Bookings | Concierge Dispatch Worldwide'
    $content = $content -replace 'valens_api_bridge.js', ''

    # 5. Clean up Yacht/Villa mentions in footers/headers (Safe replacements)
    $content = $content -replace 'luxury yacht rentals, and exclusive villa bookings', 'and discrete aviation coordination'
    $content = $content -replace 'bespoke travel planning across private jets, luxury yachts, and exclusive villa retreats', 'bespoke aviation coordination and elite jet charter'
    $content = $content -replace 'jets ⋅ yachts ⋅ villas', 'Private Jets'
    
    # Remove footer link block for Yacht/Villa if present in standard pattern
    # More surgical footer purge
    $content = $content -replace '<a href="/luxury-yacht-rentals/".*?Maritime</a>', ''
    $content = $content -replace '<a href="luxury-villa-rentals.html".*?Villas</a>', ''
    $content = $content -replace '<a href="/luxury-villa-rentals.html".*?Villas</a>', ''
    
    # 6. Final cleanup of empty lines/gaps created by purges
    $content = $content -replace '\n\s*\n\s*\n', "`n`n"

    Set-Content $file.FullName $content
}

Write-Host "Site-wide audit and cleanup completed."
