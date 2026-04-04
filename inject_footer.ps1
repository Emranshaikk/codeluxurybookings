# inject_footer.ps1
# Replaces the minimal footer across all HTML files with the full premium footer
# Includes: Blog, Contact, WhatsApp row, copyright line
# Skips files that already have the upgraded footer

$newFooter = @'
    <footer>
        <div class="container" style="max-width:1300px; margin:0 auto; padding:0 2rem;">

            <!-- Footer Top: Brand + Nav -->
            <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:flex-start; gap:3rem; padding:5rem 0 3rem; border-bottom:1px solid rgba(212,175,55,0.1);">

                <!-- Brand Column -->
                <div style="flex:1; min-width:220px;">
                    <div style="font-family:'Cormorant Garamond',serif; font-size:2rem; color:#fff; margin-bottom:1rem;">Elite <span style="color:#D4AF37;">Luxury</span></div>
                    <p style="color:rgba(255,255,255,0.5); font-size:0.9rem; line-height:1.7; max-width:260px;">Curating world-class luxury experiences through our global partner network. Private Jets. Yachts. Villas.</p>
                    <a href="https://wa.me/918801079030" target="_blank" style="display:inline-flex; align-items:center; gap:0.6rem; margin-top:1.5rem; background:#25D366; color:#fff; padding:0.75rem 1.5rem; border-radius:8px; text-decoration:none; font-size:0.82rem; font-weight:600; text-transform:uppercase; letter-spacing:1.5px; transition:all 0.3s;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 20px rgba(37,211,102,0.3)'" onmouseout="this.style.transform=''; this.style.boxShadow=''">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326z"/></svg>
                        WhatsApp Concierge
                    </a>
                </div>

                <!-- Services Column -->
                <div style="min-width:160px;">
                    <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:2px; color:#D4AF37; margin-bottom:1.2rem; font-weight:600;">Services</div>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:0.75rem;">
                        <li><a href="/elite-private-jet-charter/" style="color:rgba(255,255,255,0.55); text-decoration:none; font-size:0.88rem; transition:color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.55)'">✈ Private Jets</a></li>
                        <li><a href="/luxury-yacht-rentals/" style="color:rgba(255,255,255,0.55); text-decoration:none; font-size:0.88rem; transition:color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.55)'">⛵ Luxury Yachts</a></li>
                        <li><a href="/luxury-villa-rentals/" style="color:rgba(255,255,255,0.55); text-decoration:none; font-size:0.88rem; transition:color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.55)'">🏛 Exclusive Villas</a></li>
                    </ul>
                </div>

                <!-- Popular Guides Column -->
                <div style="min-width:180px;">
                    <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:2px; color:#D4AF37; margin-bottom:1.2rem; font-weight:600;">Popular Guides</div>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:0.75rem;">
                        <li><a href="/private-jet-rental-prices/" style="color:rgba(255,255,255,0.55); text-decoration:none; font-size:0.88rem; transition:color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.55)'">Jet Rental Prices</a></li>
                        <li><a href="/empty-leg-flights-discount/" style="color:rgba(255,255,255,0.55); text-decoration:none; font-size:0.88rem; transition:color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.55)'">Empty Leg Deals</a></li>
                        <li><a href="/types-of-private-jets/" style="color:rgba(255,255,255,0.55); text-decoration:none; font-size:0.88rem; transition:color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.55)'">Types of Jets</a></li>
                        <li><a href="/guide-to-mediterranean-yacht-charter/" style="color:rgba(255,255,255,0.55); text-decoration:none; font-size:0.88rem; transition:color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.55)'">Mediterranean Charter</a></li>
                        <li><a href="/luxury-villas/" style="color:rgba(255,255,255,0.55); text-decoration:none; font-size:0.88rem; transition:color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.55)'">Luxury Villa Guide</a></li>
                    </ul>
                </div>

                <!-- Company Column -->
                <div style="min-width:140px;">
                    <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:2px; color:#D4AF37; margin-bottom:1.2rem; font-weight:600;">Company</div>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:0.75rem;">
                        <li><a href="/blog/" style="color:rgba(255,255,255,0.55); text-decoration:none; font-size:0.88rem; transition:color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.55)'">Blog</a></li>
                        <li><a href="/contact/" style="color:rgba(255,255,255,0.55); text-decoration:none; font-size:0.88rem; transition:color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.55)'">Contact Us</a></li>
                        <li><a href="https://wa.me/918801079030" target="_blank" style="color:rgba(255,255,255,0.55); text-decoration:none; font-size:0.88rem; transition:color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.55)'">WhatsApp</a></li>
                    </ul>
                </div>

            </div>

            <!-- Footer Bottom: Copyright -->
            <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; padding:2rem 0; gap:1rem;">
                <p style="color:rgba(255,255,255,0.3); font-size:0.82rem; letter-spacing:0.5px;">© 2026 Elite Luxury Bookings. All rights reserved. Global Concierge Service.</p>
                <div style="display:flex; gap:2rem;">
                    <a href="/elite-private-jet-charter/" style="color:rgba(255,255,255,0.3); font-size:0.78rem; text-decoration:none; text-transform:uppercase; letter-spacing:1px;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.3)'">Private Jets</a>
                    <a href="/luxury-yacht-rentals/" style="color:rgba(255,255,255,0.3); font-size:0.78rem; text-decoration:none; text-transform:uppercase; letter-spacing:1px;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.3)'">Yachts</a>
                    <a href="/blog/" style="color:rgba(255,255,255,0.3); font-size:0.78rem; text-decoration:none; text-transform:uppercase; letter-spacing:1px;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.3)'">Blog</a>
                    <a href="/contact/" style="color:rgba(255,255,255,0.3); font-size:0.78rem; text-decoration:none; text-transform:uppercase; letter-spacing:1px;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='rgba(255,255,255,0.3)'">Contact</a>
                </div>
            </div>

        </div>
    </footer>
'@

# Also upgrade the old CSS for footer to add responsive wrap
$footerCssUpgrade = @'
    /* ===== UPGRADED FOOTER CSS ===== */
    footer { background: #000; border-top: 1px solid rgba(255,255,255,0.05); }
    @media (max-width: 768px) {
        footer > div > div:first-child { flex-direction: column; }
        footer > div > div:last-child { flex-direction: column; gap: 0.5rem; text-align: center; }
    }
'@

$skipDirs = @("blog", "contact")
$rootDir = (Get-Location).Path

$htmlFiles = Get-ChildItem -Path . -Filter "index.html" -Recurse | Where-Object {
    $dir = $_.DirectoryName
    # Skip root
    if ($dir -eq $rootDir) { return $false }
    # Skip blog/ contact/
    foreach ($skip in $skipDirs) {
        if ($dir -like "*\$skip") { return $false }
    }
    return $true
}

$count = 0
$skipped = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8

    # Skip if already has upgraded footer (detect by unique marker)
    if ($content -like "*Popular Guides*" -or $content -like "*footer-upgraded*") {
        $skipped++
        continue
    }

    # Replace entire <footer>...</footer> block
    # Use a regex that matches from <footer> to </footer>
    $newContent = $content -replace '(?s)<footer>.*?</footer>', $newFooter

    # Inject footer responsive CSS before </style> if not already present
    if ($newContent -notlike "*UPGRADED FOOTER CSS*") {
        $newContent = $newContent -replace '</style>', "$footerCssUpgrade`n    </style>"
    }

    Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
    $count++
    Write-Host "Footer upgraded -> $($file.Name) in $($file.DirectoryName | Split-Path -Leaf)"
}

Write-Host "`n✅ Done. Footer upgraded in $count pages. Skipped $skipped (already upgraded or excluded)."
