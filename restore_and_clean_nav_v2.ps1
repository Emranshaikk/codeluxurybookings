
$cleanNav = @"
<!-- ELB_NAV_START -->
    <nav class="global-nav">
        <div class="container global-nav-inner">
            <a href="/" class="nav-brand"><span class="nav-gold">Elite</span> Luxury Bookings</a>
            <ul class="nav-links">
                <li><a href="/elite-private-jet-charter.html">Private Jets</a></li>
                <li><a href="/luxury-yacht-rentals/">Yacht Charter</a></li>
                <li><a href="/luxury-villa-rentals.html">Villas</a></li>
                <li><a href="/blog.html">Blog</a></li>
                <li><a href="/contact.html">Contact</a></li>
            </ul>
            <div class="nav-cta">
                <a href="https://wa.me/918801079030" class="btn btn-gold btn-sm">Direct Concierge</a>
                <div class="nav-hamburger" id="navHamburger" onclick="toggleMobileMenu()">
                    <span></span><span></span><span></span>
                </div>
            </div>
        </div>
    </nav>
    <div class="mobile-menu" id="elbMobileMenu">
        <a href="/elite-private-jet-charter.html">Private Jets</a>
        <a href="/luxury-yacht-rentals/">Luxury Yachts</a>
        <a href="/luxury-villa-rentals.html">Exclusive Villas</a>
        <a href="/blog.html">Articles & News</a>
        <a href="/contact.html">Contact Us</a>
        <a href="https://wa.me/918801079030" class="mobile-cta">WhatsApp Concierge</a>
    </div>
<!-- ELB_NAV_END -->
"@

$files = @(
    "types-of-private-jets.html", 
    "private-jet-rental-prices.html", 
    "empty-leg-flights-discount.html", 
    "private-jet-for-business-travel.html"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)
        
        if ($content -match '(?s)<!-- ELB_NAV_START -->.*?<!-- ELB_NAV_END -->') {
            $content = $content -replace '(?s)<!-- ELB_NAV_START -->.*?<!-- ELB_NAV_END -->', $cleanNav
            [System.IO.File]::WriteAllText($file, $content, (New-Object System.Text.UTF8Encoding $false))
            Write-Host "Cleaned navigation in $file"
        }
        else {
            Write-Host "No ELB markers found in $file - skipping to avoid corruption"
        }
    }
}
