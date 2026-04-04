
# inject_global_nav.ps1
# Injects the premium global navigation bar and mobile menu into all blog post HTML files
# Skips: homepage (index.html at root), blog/index.html, contact/index.html (already have nav)

$navHTML = @"
    <!-- GLOBAL NAVIGATION -->
    <nav class="global-nav" id="globalNav">
        <div class="container global-nav-inner">
            <a href="/" class="nav-brand">Elite <span class="nav-gold">Luxury</span></a>
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
                        <a href="/renting-catamaran/">Catamaran Rentals</a>
                        <a href="/best-sailing-yacht-charter/">Sailing Yachts</a>
                        <a href="/bareboat-charter-guide/">Bareboat Guide</a>
                        <a href="/guide-to-mediterranean-yacht-charter/">Mediterranean Guide</a>
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
                <li><a href="/contact/">Contact</a></li>
            </ul>
            <div class="nav-cta">
                <a href="/contact/" class="btn btn-outline">Contact Us</a>
                <a href="https://wa.me/918801079030" class="btn btn-gold" target="_blank">WhatsApp</a>
            </div>
            <div class="nav-hamburger" id="navHamburger" onclick="toggleMobileMenu()">
                <span></span><span></span><span></span>
            </div>
        </div>
    </nav>
    <div class="mobile-menu" id="mobileMenu">
        <a href="/elite-private-jet-charter/">[Jet] Private Jets</a>
        <a href="/luxury-yacht-rentals/">[Yacht] Luxury Yachts</a>
        <a href="/luxury-villa-rentals/">[Villa] Exclusive Villas</a>
        <a href="/blog/">[Blog] Blog</a>
        <a href="/contact/">[Contact] Contact</a>
        <a href="https://wa.me/918801079030" class="mobile-cta" target="_blank">WhatsApp Concierge</a>
    </div>
"@

$navCSS = @"
    /* ===== GLOBAL NAVIGATION (Injected) ===== */
    .global-nav { position:fixed; top:0; left:0; right:0; background:rgba(5,5,5,0.96); backdrop-filter:blur(24px); -webkit-backdrop-filter:blur(24px); border-bottom:1px solid rgba(212,175,55,0.15); z-index:2000; box-shadow:0 4px 30px rgba(0,0,0,0.5); }
    .global-nav-inner { display:flex; align-items:center; justify-content:space-between; height:72px; gap:1rem; max-width:1400px; margin:0 auto; padding:0 2rem; }
    .nav-brand { font-family:'Cormorant Garamond',serif; font-size:1.5rem; font-weight:600; color:#fff; text-decoration:none; white-space:nowrap; flex-shrink:0; }
    .nav-gold { color:#D4AF37; }
    .nav-links { display:flex; align-items:center; gap:0.25rem; list-style:none; flex:1; justify-content:center; }
    .nav-links a { color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.82rem; text-transform:uppercase; letter-spacing:1.5px; padding:0.5rem 0.9rem; border-radius:6px; transition:all 0.4s; white-space:nowrap; }
    .nav-links a:hover { color:#D4AF37; }
    .nav-dropdown { position:relative; }
    .nav-dropdown > a::after { content:' \u25be'; font-size:0.7rem; }
    .dropdown-menu { position:absolute; top:calc(100% + 8px); left:0; background:#0f0f0f; border:1px solid rgba(212,175,55,0.15); border-radius:12px; padding:0.75rem; min-width:220px; opacity:0; visibility:hidden; transform:translateY(-8px); transition:all 0.4s; box-shadow:0 20px 40px rgba(0,0,0,0.6); z-index:100; }
    .nav-dropdown:hover .dropdown-menu { opacity:1; visibility:visible; transform:translateY(0); }
    .dropdown-menu a { display:block; padding:0.6rem 1rem; color:rgba(255,255,255,0.6) !important; border-radius:8px; font-size:0.82rem; letter-spacing:1px; }
    .dropdown-menu a:hover { color:#D4AF37 !important; background:rgba(212,175,55,0.06); }
    .nav-cta { display:flex; gap:0.6rem; align-items:center; flex-shrink:0; }
    .nav-hamburger { display:none; flex-direction:column; gap:5px; cursor:pointer; padding:0.5rem; }
    .nav-hamburger span { display:block; width:24px; height:2px; background:rgba(255,255,255,0.6); border-radius:2px; transition:all 0.4s; }
    .nav-hamburger.open span:nth-child(1) { transform:rotate(45deg) translate(5px,5px); background:#D4AF37; }
    .nav-hamburger.open span:nth-child(2) { opacity:0; }
    .nav-hamburger.open span:nth-child(3) { transform:rotate(-45deg) translate(5px,-5px); background:#D4AF37; }
    .mobile-menu { display:none; position:fixed; top:72px; left:0; right:0; background:rgba(5,5,5,0.98); backdrop-filter:blur(24px); border-bottom:1px solid rgba(212,175,55,0.15); padding:2rem; z-index:1999; flex-direction:column; gap:1rem; }
    .mobile-menu.open { display:flex; }
    .mobile-menu a { color:rgba(255,255,255,0.6); text-decoration:none; font-size:1rem; text-transform:uppercase; letter-spacing:2px; padding:0.75rem 0; border-bottom:1px solid rgba(255,255,255,0.05); transition:all 0.4s; }
    .mobile-menu a:hover { color:#D4AF37; }
    .mobile-cta { margin-top:1rem; text-align:center; background:linear-gradient(135deg,#D4AF37,#B8860B); color:#000 !important; border-radius:8px; padding:1rem; font-weight:600; letter-spacing:2px; border-bottom:none !important; }
    @media (max-width:900px) { .nav-links { display:none; } .nav-cta .btn-outline { display:none; } .nav-hamburger { display:flex; } }
    /* Push body content below fixed nav */
    body { padding-top: 72px !important; }
"@

$navJS = @"
    <script>
    function toggleMobileMenu() {
        var menu = document.getElementById('mobileMenu');
        var burger = document.getElementById('navHamburger');
        if (menu && burger) { menu.classList.toggle('open'); burger.classList.toggle('open'); }
    }
    </script>
"@

# Get all blog post index.html files — skip root, blog/, contact/ which already have nav
$skipDirs = @("blog", "contact", "_template_blog_master", "moneypage1", "moneypage2", "global-route-silo")
$rootIndex = Join-Path (Get-Location) "index.html"

$htmlFiles = Get-ChildItem -Path . -Filter "index.html" -Recurse | Where-Object {
    $dir = $_.DirectoryName
    $rootDir = (Get-Location).Path
    # Skip root index
    if ($dir -eq $rootDir) { return $false }
    # Skip specified dirs
    foreach ($skip in $skipDirs) {
        if ($dir -like "*\$skip*") { return $false }
    }
    return $true
}

$count = 0
foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8

    # Skip if nav already injected
    if ($content -like "*global-nav*") {
        Write-Host "SKIP (already has nav): $($file.FullName)"
        continue
    }

    # Inject CSS into <style> block (before closing </style>)
    $newContent = $content -replace '</style>', "$navCSS`n    </style>"

    # Inject nav HTML after <body>
    $newContent = $newContent -replace '<body>', "<body>`n$navHTML"

    # Inject JS before </body>
    $newContent = $newContent -replace '</body>', "$navJS`n</body>"

    Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
    $count++
    Write-Host "Injected nav -> $($file.FullName)"
}

Write-Host "`nDone. Global nav injected into $count pages."
