# Elite Luxury Bookings - Professional Site-Wide Standardization Script
# Source of Truth: index.html (Restored Version)

$masterNav = @"
    <!-- ELB_NAV_START -->
    <nav class="global-nav">
        <div class="container global-nav-inner">
            <a href="/" class="nav-brand">Elite Luxury <span class="nav-gold">Bookings</span></a>
            <ul class="nav-links">
                <li><a href="/elite-private-jet-charter.html">Private Jets</a></li>
                <li><a href="/blog.html">Blog</a></li>
                <li><a href="/contact.html">Contact</a></li>
            </ul>
            <div class="nav-cta"><a href="https://wa.me/918801079030" class="btn btn-gold" target="_blank">WhatsApp</a>
            </div>
            <div class="nav-hamburger" id="navHamburger" onclick="toggleMobileMenu()"><span></span><span></span><span></span></div>
        </div>
    </nav>
    <div class="mobile-menu" id="elbMobileMenu">
        <a href="/elite-private-jet-charter.html">✈ Private Jets</a>
        <a href="/blog.html">📰 Blog</a>
        <a href="/contact.html">📞 Contact</a>
        <a href="https://wa.me/918801079030" class="mobile-cta" target="_blank">WhatsApp Concierge →</a>
    </div>
    <!-- ELB_NAV_END -->
"@

$leadFormTemplate = @"
            <div class="glass-panel" style="padding: 3.5rem; border: 1px solid var(--primary-gold); background: #000; border-radius: 28px; box-shadow: 0 40px 100px rgba(0,0,0,0.8); margin: 3rem auto; max-width: 900px;">
                <div style="text-align: center; margin-bottom: 3rem;">
                    <h2 class="serif gold-text" style="font-size: 2.8rem; margin-bottom: 1rem;">Global Charter Inquiry</h2>
                    <p style="color: var(--text-muted); text-transform: uppercase; letter-spacing: 3px; font-size: 0.85rem;">24/7 Elite Concierge Dispatch</p>
                </div>
                <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: flex; flex-direction: column; gap: 1.5rem;">
                    <input type="hidden" name="_subject" value="GLOBAL INQUIRY: Private Jet Charter">
                    <input type="hidden" name="Source" value="[[SOURCE_NAME]]">
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;" class="form-grid">
                        <div class="form-group">
                            <label style="display: block; font-size: 0.75rem; color: var(--primary-gold); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.8rem; font-weight: 700;">Full Name</label>
                            <input type="text" name="name" class="form-control" placeholder="e.g. James Harrington" required style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); padding: 1.2rem; color: #fff; border-radius: 8px;">
                        </div>
                        <div class="form-group">
                            <label style="display: block; font-size: 0.75rem; color: var(--primary-gold); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.8rem; font-weight: 700;">WhatsApp / Phone</label>
                            <input type="tel" name="phone" class="form-control" placeholder="+44 7XXX XXXXXX" required style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); padding: 1.2rem; color: #fff; border-radius: 8px;">
                        </div>
                    </div>

                    <div class="form-group">
                        <label style="display: block; font-size: 0.75rem; color: var(--primary-gold); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.8rem; font-weight: 700;">Private Email Address</label>
                        <input type="email" name="email" class="form-control" placeholder="client@exclusive.com" required style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); padding: 1.2rem; color: #fff; border-radius: 8px;">
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;" class="form-grid">
                        <div class="form-group">
                            <label style="display: block; font-size: 0.75rem; color: var(--primary-gold); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.8rem; font-weight: 700;">Hub of Origin</label>
                            <input type="text" name="from" class="form-control" placeholder="Departure City" required style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); padding: 1.2rem; color: #fff; border-radius: 8px;">
                        </div>
                        <div class="form-group">
                            <label style="display: block; font-size: 0.75rem; color: var(--primary-gold); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.8rem; font-weight: 700;">Destination Hub</label>
                            <input type="text" name="to" class="form-control" placeholder="Arrival City" required style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); padding: 1.2rem; color: #fff; border-radius: 8px;">
                        </div>
                    </div>

                    <div class="form-group">
                        <label style="display: block; font-size: 0.75rem; color: var(--primary-gold); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.8rem; font-weight: 700;">Special Mission Requirements</label>
                        <textarea name="message" class="form-control" rows="3" placeholder="Aircraft preference, security detail, or urgent dispatch requirements..." style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid var(--glass-border); padding: 1.2rem; color: #fff; border-radius: 8px; resize: none;"></textarea>
                    </div>

                    <button type="submit" class="btn btn-gold" style="width: 100%; padding: 1.5rem; font-size: 1.2rem; border-radius: 12px; margin-top: 1rem; background: linear-gradient(135deg, #D4AF37, #B8860B); color: #000 !important; font-weight: 800; text-transform: uppercase; letter-spacing: 4px; border: none; cursor: pointer;">
                        Secure Confidential Proposal
                    </button>
                    <p style="text-align: center; color: var(--text-muted); font-size: 0.75rem; letter-spacing: 1px;">Elite Luxury Bookings | NDA Backed Coordination</p>
                </form>
            </div>
"@

$cssTokens = @"
        :root {
            --primary-gold: #D4AF37;
            --deep-black: #050505;
            --graphene: #1A1A1A;
            --glass-bg: rgba(255, 255, 255, 0.02);
            --glass-border: rgba(212, 175, 55, 0.15);
            --text-main: #FFFFFF;
            --text-muted: rgba(255, 255, 255, 0.6);
            --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
"@

$htmlFiles = Get-ChildItem -Filter *.html

foreach ($file in $htmlFiles) {
    if ($file.Name -eq "index.html") { continue }
    
    Write-Host "Standardizing $($file.Name)..."
    $content = Get-Content $file.FullName -Raw

    # 1. Standardize CSS Tokens
    $cssPattern = '(?s):root \{.*?\}'
    $content = [regex]::Replace($content, $cssPattern, $cssTokens)

    # 2. Standardize Navigation Hook
    $navPattern = '(?s)<!-- ELB_NAV_START -->.*?<!-- ELB_NAV_END -->'
    $content = [regex]::Replace($content, $navPattern, $masterNav)

    # 3. Purge Valens Widget and replace with Master Lead Engine
    if ($content -match 'ELB_VALENS_WIDGET_START') {
        $sourceName = $file.BaseName -replace '-private-jet-cost', '' -replace '-', ' '
        $routeLeadForm = $leadFormTemplate -replace '\[\[SOURCE_NAME\]\]', "Route: $sourceName"
        $valensPattern = '(?s)<!-- ELB_VALENS_WIDGET_START -->.*?<!-- ELB_VALENS_WIDGET_END -->'
        $content = [regex]::Replace($content, $valensPattern, $routeLeadForm)
    }

    # 4. Standardize Logo Identity
    $logoPattern = '(?s)<a href="/" class="nav-brand">.*?</a>'
    $content = [regex]::Replace($content, $logoPattern, '<a href="/" class="nav-brand">Elite Luxury <span class="nav-gold">Bookings</span></a>')

    # 5. Fix internal links to use standard .html
    $content = $content -replace '/elite-private-jet-charter/', '/elite-private-jet-charter.html'
    $content = $content -replace '/luxury-yacht-rentals/', '/luxury-yacht-rentals.html'
    $content = $content -replace '/luxury-villa-rentals/', '/luxury-villa-rentals.html'

    Set-Content $file.FullName $content
}

Write-Host "Site-wide standardization and design lock completed successfully."
