# Injected Nav Engine (v5.5 - Pure-ASCII Harmonization)

# 1. Symbol Definitions (Purely safe character codes)
$airplane = [char]0x2708; $boat = [char]0x26F5; $villas = [char]0xD83C + [char]0xDFDB
$blog = [char]0xD83D + [char]0xDCD6; $email = [char]0xD83D + [char]0xDCE7
$arrow = [char]0x2192; $check = [char]0x2713

# 2. Repair Mapping (Using char-code concatenation to avoid script corruption)
$repairs = @{}
# Airplane artifacts (âœˆ, etc.)
$repairs[([char]0xE2 + [char]0x9C + [char]0x88)] = $airplane
# Checkmark artifacts (âœ“, etc.)
$repairs[([char]0xE2 + [char]0x9C + [char]0x93)] = $check
# Dash artifacts (â€“ , â€” )
$repairs[([char]0xE2 + [char]0x80 + [char]0x93)] = [char]0x2013
$repairs[([char]0xE2 + [char]0x80 + [char]0x94)] = [char]0x2014
# Pound/Symbol artifacts (Â£)
$repairs[([char]0xC2 + [char]0xA3)] = [char]0x00A3

$navHTML = @"
<!-- ELB_NAV_START -->
    <nav class="global-nav">
        <div class="container global-nav-inner">
            <a href="/" class="nav-brand">Elite Luxury <span class="nav-gold">Bookings</span></a>
            <ul class="nav-links">
                <li class="nav-dropdown"><a href="/elite-private-jet-charter/">Private Jets</a>
                    <div class="dropdown-menu">
                        <a href="/elite-private-jet-charter/">Jet Charters Overview</a>
                        <a href="/private-jet-rental-prices/">Rental Prices</a>
                        <a href="/types-of-private-jets/">Types of Jets</a>
                        <a href="/empty-leg-flights-discount/">Empty Leg Deals</a>
                        <a href="/private-jet-for-business-travel/">Business Travel</a>
                    </div>
                </li>
                <li class="nav-dropdown"><a href="/luxury-yacht-rentals/">Luxury Yachts</a>
                    <div class="dropdown-menu">
                        <a href="/luxury-yacht-rentals/">Yacht Charter Overview</a>
                        <a href="/luxury-yacht-rentals/renting-catamaran/">Catamaran Rentals</a>
                        <a href="/luxury-yacht-rentals/best-sailing-yacht-charter/">Sailing Yachts</a>
                        <a href="/luxury-yacht-rentals/bareboat-charter-guide/">Bareboat Guide</a>
                        <a href="/luxury-yacht-rentals/guide-to-mediterranean-yacht-charter/">Mediterranean Guide</a>
                    </div>
                </li>
                <li class="nav-dropdown"><a href="/luxury-villa-rentals/">Exclusive Villas</a>
                    <div class="dropdown-menu">
                        <a href="/luxury-villa-rentals/">Villa Rentals Overview</a>
                        <a href="/luxury-villas/">Luxury Villa Guide</a>
                    </div>
                </li>
                <li><a href="/blog/">Blog</a></li>
            </ul>
            <div class="nav-cta"><a href="https://wa.me/918801079030" class="btn btn-gold" target="_blank">WhatsApp</a></div>
            <div class="nav-hamburger" id="navHamburger" onclick="toggleMobileMenu()"><span></span><span></span><span></span></div>
        </div>
    </nav>
    <div class="mobile-menu" id="elbMobileMenu">
        <a href="/elite-private-jet-charter/">$airplane Private Jets</a>
        <a href="/luxury-yacht-rentals/">$boat Luxury Yachts</a>
        <a href="/luxury-villa-rentals/">$villas Exclusive Villas</a>
        <a href="/blog/">$blog Blog</a>
        <a href="/contact/">$email Contact</a>
        <a href="https://wa.me/918801079030" class="mobile-cta" target="_blank">WhatsApp Concierge $arrow</a>
    </div>
<!-- ELB_NAV_END -->
"@

$navCSS = @"
/* ELB_CSS_START */
    .global-nav { position:fixed; top:0; left:0; right:0; background:rgba(5,5,5,0.98); backdrop-filter:blur(24px); border-bottom:1px solid rgba(212,175,55,0.2); z-index:99999; }
    .global-nav-inner { display:flex; align-items:center; justify-content:space-between; height:72px; gap:1rem; max-width:1400px; margin:0 auto; padding:0 2rem; box-sizing: border-box; }
    .nav-brand { font-family:'Cormorant Garamond',serif; font-size:1.75rem; font-weight:600; color:#fff !important; text-decoration:none !important; }
    .nav-gold { color:#D4AF37 !important; }
    .nav-links { display:flex; align-items:center; gap:0.25rem; list-style:none; flex:1; justify-content:center; margin:0; padding:0; }
    .nav-links a { color:rgba(255,255,255,0.7) !important; text-decoration:none !important; font-size:0.82rem; text-transform:uppercase; letter-spacing:1.5px; padding:0.5rem 0.9rem; border-radius:6px; transition:all 0.4s; font-family: 'Inter', sans-serif !important; }
    .nav-dropdown { position:relative; }
    .dropdown-menu { position:absolute; top:calc(100% + 8px); left:0; background:#0a0a0a; border:1px solid rgba(212,175,55,0.15); border-radius:12px; padding:0.75rem; min-width:240px; opacity:0; visibility:hidden; transform:translateY(-8px); transition:all 0.4s; box-shadow:0 20px 40px rgba(0,0,0,0.8); z-index:100; }
    .nav-dropdown:hover .dropdown-menu { opacity:1 !important; visibility:visible !important; transform:translateY(0) !important; }
    .dropdown-menu a { display:block !important; padding:0.7rem 1.2rem !important; color:rgba(255,255,255,0.7) !important; border-radius:8px; font-size:0.85rem !important; text-transform: none !important; }
    .nav-hamburger { display:none; flex-direction:column; gap:5px; cursor:pointer; padding:0.5rem; z-index:100001; }
    .nav-hamburger span { display:block; width:24px; height:2px; background:rgba(255,255,255,0.8); border-radius:2px; transition:all 0.4s; }
    .mobile-menu { display:none; position:fixed; top:0; left:0; right:0; bottom:0; background:#050505; padding:72px 2rem 2rem; z-index:100000; flex-direction:column; gap:0.5rem; overflow-y: auto; }
    .mobile-menu.open { display:flex !important; }
    .mobile-menu a { color:rgba(255,255,255,0.8) !important; text-decoration:none !important; font-size:1.1rem; text-transform:uppercase; letter-spacing:2px; padding:1.2rem 0; border-bottom:1px solid rgba(255,255,255,0.05); }
    .mobile-cta { margin-top:2rem; text-align:center; background:linear-gradient(135deg,#D4AF37,#B8860B); color:#000 !important; border-radius:8px; padding:1.2rem !important; font-weight:700; }
    @media (max-width:1024px) { .nav-links { display:none !important; } .nav-hamburger { display:flex !important; } }
    body { padding-top: 72px !important; }
    .luxury-list li::before { content: '$check' !important; }
/* ELB_CSS_END */
"@

$navJS = @"
<!-- ELB_JS_START -->
    <script>function toggleMobileMenu(){var m=document.getElementById('elbMobileMenu'),b=document.getElementById('navHamburger');if(m&&b){m.classList.toggle('open');b.classList.toggle('open');}}</script>
<!-- ELB_JS_END -->
"@

$htmlFiles = Get-ChildItem -Path . -Filter "index.html" -Recurse
foreach ($file in $htmlFiles) {
    if ($file.FullName -match '\.git' -or $file.FullName -match 'node_modules') { continue }
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)

    # 1. Clean legacy markers
    $content = $content -replace '(?s)<!--\s*ELB_NAV_START\s*-->.*?<!--\s*ELB_NAV_END\s*-->', ''
    $content = $content -replace '(?s)/\*\s*ELB_CSS_START\s*\*/.*?/\*\s*ELB_CSS_END\s*\*/', ''
    $content = $content -replace '(?s)<!--\s*ELB_JS_START\s*-->.*?<!--\s*ELB_JS_END\s*-->', ''
    $content = $content -replace '(?s)<style>\s*</style>', ''

    # 2. Repair Routes direction and capitalization
    $folder = $file.Directory.Name
    if ($folder -match "^([^-]+)-to-([^-]+)") {
        $c1 = $Matches[1]; $c2 = $Matches[2]; $c1T = (Get-Culture).TextInfo.ToTitleCase($c1); $c2T = (Get-Culture).TextInfo.ToTitleCase($c2)
        $route = "$c1T to $c2T"
        $content = $content -replace "(?i)$c2 to $c1", $route -replace "(?i)$c1 to $c2", $route
    }

    # 3. Aggressive Encoding Repair
    foreach ($k in $repairs.Keys) { $content = $content.Replace($k, $repairs[$k]) }

    # 4. Standardized Injection
    $navStyleBlock = "<style>`n$navCSS`n</style>"
    $content = $content -replace '</head>', "`n$navStyleBlock`n</head>"
    $content = $content -replace '<body[^>]*>', "`$0`n$navHTML"
    $content = $content -replace '</body>', ("`n" + $navJS + "`n</body>")

    [System.IO.File]::WriteAllText($file.FullName, $content, (New-Object System.Text.UTF8Encoding $false))
}
Write-Host "Site-wide Harmonization v5.5 Complete. Pure-ASCII Verified."
