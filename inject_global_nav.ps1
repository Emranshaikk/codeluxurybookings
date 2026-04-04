
# Injected Nav Engine (v4 - Final Restoration)

$navStart = "<!-- ELB_NAV_START -->"
$navEnd = "<!-- ELB_NAV_END -->"
$cssStart = "<!-- ELB_CSS_START -->"
$cssEnd = "<!-- ELB_CSS_END -->"
$jsStart = "<!-- ELB_JS_START -->"
$jsEnd = "<!-- ELB_JS_END -->"

$navHTML = @"
$navStart
    <nav class="global-nav" id="elbGlobalNav">
        <div class="container global-nav-inner">
            <a href="/" class="nav-brand">Elite Luxury <span class="nav-gold">Bookings</span></a>
            <ul class="nav-links">
                <li class="nav-dropdown">
                    <a href="/elite-private-jet-charter/">Private Jets</a>
                    <div class="dropdown-menu">
                        <a href="/elite-private-jet-charter/">Jet Charters Overview</a>
                        <a href="/private-jet-rental-prices/">Rental Prices</a>
                        <a href="/types-of-private-jets/">Types of Jets</a>
                        <a href="/empty-leg-flights-discount/">Empty Leg Deals</a>
                        <a href="/private-jet-for-business-travel/">Business Travel</a>
                    </div>
                </li>
                <li class="nav-dropdown">
                    <a href="/luxury-yacht-rentals/">Luxury Yachts</a>
                    <div class="dropdown-menu">
                        <a href="/luxury-yacht-rentals/">Yacht Charter Overview</a>
                        <a href="/luxury-yacht-rentals/renting-catamaran/">Catamaran Rentals</a>
                        <a href="/luxury-yacht-rentals/best-sailing-yacht-charter/">Sailing Yachts</a>
                        <a href="/luxury-yacht-rentals/bareboat-charter-guide/">Bareboat Guide</a>
                        <a href="/luxury-yacht-rentals/guide-to-mediterranean-yacht-charter/">Mediterranean Guide</a>
                    </div>
                </li>
                <li class="nav-dropdown">
                    <a href="/luxury-villa-rentals/">Exclusive Villas</a>
                    <div class="dropdown-menu">
                        <a href="/luxury-villa-rentals/">Villa Rentals Overview</a>
                        <a href="/luxury-villas/">Luxury Villa Guide</a>
                    </div>
                </li>
                <li><a href="/blog/">Blog</a></li>
            </ul>
            <div class="nav-cta">
                <a href="https://wa.me/918801079030" class="btn btn-gold" target="_blank">WhatsApp</a>
            </div>
            <div class="nav-hamburger" id="navHamburger" onclick="toggleMobileMenu()">
                <span></span><span></span><span></span>
            </div>
        </div>
    </nav>
    <div class="mobile-menu" id="elbMobileMenu">
        <a href="/elite-private-jet-charter/">✈ Private Jets</a>
        <a href="/luxury-yacht-rentals/">⛵ Luxury Yachts</a>
        <a href="/luxury-villa-rentals/">🏛 Exclusive Villas</a>
        <a href="/blog/">📖 Blog</a>
        <a href="/contact/">📧 Contact</a>
        <a href="https://wa.me/918801079030" class="mobile-cta" target="_blank">WhatsApp Concierge →</a>
    </div>
$navEnd
"@

$navCSS = @"
<style>
$cssStart
    /* ===== GLOBAL NAVIGATION (V4 - ULTRA) ===== */
    .global-nav { position:fixed; top:0; left:0; right:0; background:rgba(5,5,5,0.98); backdrop-filter:blur(24px); -webkit-backdrop-filter:blur(24px); border-bottom:1px solid rgba(212,175,55,0.2); z-index:99999; }
    .global-nav-inner { display:flex; align-items:center; justify-content:space-between; height:72px; gap:1rem; max-width:1400px; margin:0 auto; padding:0 2rem; box-sizing: border-box; }
    .nav-brand { font-family:'Cormorant Garamond',serif; font-size:1.75rem; font-weight:600; color:#fff !important; text-decoration:none !important; white-space:nowrap; }
    .nav-gold { color:#D4AF37 !important; }
    .nav-links { display:flex; align-items:center; gap:0.25rem; list-style:none; flex:1; justify-content:center; margin:0; padding:0; }
    .nav-links li { list-style: none !important; }
    .nav-links a { color:rgba(255,255,255,0.7) !important; text-decoration:none !important; font-size:0.82rem; text-transform:uppercase; letter-spacing:1.5px; padding:0.5rem 0.9rem; border-radius:6px; transition:all 0.4s; font-family: 'Inter', sans-serif !important; }
    .nav-links a:hover { color:#D4AF37 !important; background: rgba(212,175,55,0.05); }
    .nav-dropdown { position:relative; }
    .nav-dropdown > a::after { content:' \25be' !important; font-size:0.7rem; opacity: 0.7; }
    .dropdown-menu { position:absolute; top:calc(100% + 8px); left:0; background:#0a0a0a; border:1px solid rgba(212,175,55,0.15); border-radius:12px; padding:0.75rem; min-width:240px; opacity:0; visibility:hidden; transform:translateY(-8px); transition:all 0.4s; box-shadow:0 20px 40px rgba(0,0,0,0.8); z-index:100; }
    .nav-dropdown:hover .dropdown-menu { opacity:1 !important; visibility:visible !important; transform:translateY(0) !important; }
    .dropdown-menu a { display:block !important; padding:0.7rem 1.2rem !important; color:rgba(255,255,255,0.7) !important; border-radius:8px; font-size:0.85rem !important; text-transform: none !important; }
    .dropdown-menu a:hover { color:#D4AF37 !important; background:rgba(212,175,55,0.08) !important; }
    .nav-cta { display:flex; gap:0.6rem; align-items:center; flex-shrink:0; }
    .nav-hamburger { display:none; flex-direction:column; gap:5px; cursor:pointer; padding:0.5rem; z-index: 100001; }
    .nav-hamburger span { display:block; width:24px; height:2px; background:rgba(255,255,255,0.8); border-radius:2px; transition:all 0.4s; }
    .nav-hamburger.open span:nth-child(1) { transform:rotate(45deg) translate(5px,5px); background:#D4AF37; }
    .nav-hamburger.open span:nth-child(2) { opacity:0; }
    .nav-hamburger.open span:nth-child(3) { transform:rotate(-45deg) translate(5px,-5px); background:#D4AF37; }
    .mobile-menu { display:none; position:fixed; top:0; left:0; right:0; bottom:0; background:#050505; padding:72px 2rem 2rem; z-index:100000; flex-direction:column; gap:0.5rem; overflow-y: auto; }
    .mobile-menu.open { display:flex !important; }
    .mobile-menu a { color:rgba(255,255,255,0.8) !important; text-decoration:none !important; font-size:1.1rem; text-transform:uppercase; letter-spacing:2px; padding:1.2rem 0; border-bottom:1px solid rgba(255,255,255,0.05); }
    .mobile-menu a:hover { color:#D4AF37 !important; }
    .mobile-cta { margin-top:2rem; text-align:center; background:linear-gradient(135deg,#D4AF37,#B8860B); color:#000 !important; border-radius:8px; padding:1.2rem !important; font-weight:700; letter-spacing:2px; }
    @media (max-width:1024px) { .nav-links { display:none !important; } .nav-hamburger { display:flex !important; } }
    body { padding-top: 72px !important; }
$cssEnd
</style>
"@

$navJS = @"
$jsStart
    <script>
    function toggleMobileMenu() {
        var menu = document.getElementById('elbMobileMenu');
        var burger = document.getElementById('navHamburger');
        if (menu && burger) { menu.classList.toggle('open'); burger.classList.toggle('open'); }
    }
    </script>
$jsEnd
"@

# REPLACEMENT LOGIC
$htmlFiles = Get-ChildItem -Path . -Filter "index.html" -Recurse
foreach ($file in $htmlFiles) {
    if ($file.FullName -match '\.git' -or $file.FullName -match 'node_modules') { continue }
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)

    # 1. Broad Cleanup of ANYTHING that looks like our old nav/css/js
    $content = $content -replace '(?s)<!-- ELB_NAV_START -->.*?<!-- ELB_NAV_END -->', ""
    $content = $content -replace '(?s)<!-- ELB_CSS_START -->.*?<!-- ELB_CSS_END -->', ""
    $content = $content -replace '(?s)<!-- ELB_JS_START -->.*?<!-- ELB_JS_END -->', ""
    $content = $content -replace '(?s)<nav class="global-nav".*?</nav>', ""
    $content = $content -replace '(?s)<div class="mobile-menu".*?</div>', ""
    $content = $content -replace '(?s)/\* ===== GLOBAL NAVIGATION.*?\}', ""
    $content = $content -replace '(?s)<script>\s*function toggleMobileMenu\(\).*?</script>', ""
    
    # 2. Cleanup specific duplicate CTA buttons (like the Get Quote fixed button)
    $content = $content -replace '(?s)<a href="#quote" style="position: fixed;.*?Get Quote</a>', ""
    $content = $content -replace '(?s)<!-- 7\. STICKY CTA BUTTON -->.*?</a>', ""

    # 3. Injection
    $content = $content -replace '</head>', "`n$navCSS`n</head>"
    $content = $content -replace '<body[^>]*>', "`$0`n$navHTML"
    $content = $content -replace '</body>', "`n$navJS`n</body>"

    # 4. Save
    $utf8WithoutBom = New-Object System.Text.UTF8Encoding $false
    [System.IO.File]::WriteAllText($file.FullName, $content, $utf8WithoutBom)
}

Write-Host "Site-wide Harmonization Complete."
