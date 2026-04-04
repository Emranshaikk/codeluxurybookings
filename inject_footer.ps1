# inject_footer.ps1
# Replaces any footer block across all HTML files with the full premium footer
# Updates: Fixed brand name, encoding-safe entities, and improved alignment

$newFooter = @'
    <footer>
        <div class="container" style="max-width:1300px; margin:0 auto; padding:0 2rem;">

            <!-- Footer Top: Brand + Nav -->
            <div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:flex-start; gap:4rem; padding:5rem 0 3rem; border-bottom:1px solid rgba(212,175,55,0.1); text-align:left;">

                <!-- Brand Column -->
                <div style="flex:1; min-width:280px; margin-bottom:2rem;">
                    <div style="font-family:''Cormorant Garamond'',serif; font-size:2.2rem; color:#fff; margin-bottom:1rem; line-height:1.2;">Elite Luxury <span style="color:#D4AF37;">Bookings</span></div>
                    <p style="color:rgba(255,255,255,0.5); font-size:0.95rem; line-height:1.8; max-width:300px;">Curating world-class luxury experiences through our global partner network. Private Jets. Yachts. Villas.</p>
                    <a href="https://wa.me/918801079030" target="_blank" style="display:inline-flex; align-items:center; gap:0.6rem; margin-top:2rem; background:#25D366; color:#fff; padding:0.9rem 1.8rem; border-radius:12px; text-decoration:none; font-size:0.85rem; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; transition:all 0.3s; box-shadow: 0 10px 20px rgba(37,211,102,0.15);" onmouseover="this.style.transform=''translateY(-3px)''; this.style.boxShadow=''0 15px 30px rgba(37,211,102,0.25)''" onmouseout="this.style.transform=''''; this.style.boxShadow=''0 10px 20px rgba(37,211,102,0.15)''">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16"><path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326z"/></svg>
                        WhatsApp Concierge
                    </a>
                </div>

                <!-- Services Column -->
                <div style="min-width:160px; margin-bottom:2rem;">
                    <div style="font-size:0.8rem; text-transform:uppercase; letter-spacing:2.5px; color:#D4AF37; margin-bottom:1.5rem; font-weight:700;">Services</div>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:1rem; padding:0; margin:0;">
                        <li><a href="/elite-private-jet-charter/" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Private Jets</a></li>
                        <li><a href="/luxury-yacht-rentals/" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Luxury Yachts</a></li>
                        <li><a href="/luxury-villa-rentals/" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Exclusive Villas</a></li>
                    </ul>
                </div>

                <!-- Popular Guides Column -->
                <div style="min-width:180px; margin-bottom:2rem;">
                    <div style="font-size:0.8rem; text-transform:uppercase; letter-spacing:2.5px; color:#D4AF37; margin-bottom:1.5rem; font-weight:700;">Popular Guides</div>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:1rem; padding:0; margin:0;">
                        <li><a href="/private-jet-rental-prices/" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Jet Rental Prices</a></li>
                        <li><a href="/empty-leg-flights-discount/" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Empty Leg Deals</a></li>
                        <li><a href="/types-of-private-jets/" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Types of Jets</a></li>
                        <li><a href="/guide-to-mediterranean-yacht-charter/" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Mediterranean Charter</a></li>
                        <li><a href="/luxury-villas/" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Luxury Villa Guide</a></li>
                    </ul>
                </div>

                <!-- Company Column -->
                <div style="min-width:140px; margin-bottom:2rem;">
                    <div style="font-size:0.8rem; text-transform:uppercase; letter-spacing:2.5px; color:#D4AF37; margin-bottom:1.5rem; font-weight:700;">Company</div>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:1rem; padding:0; margin:0;">
                        <li><a href="/blog/" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Blog</a></li>
                        <li><a href="/contact/" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Contact Us</a></li>
                        <li><a href="https://wa.me/918801079030" target="_blank" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">WhatsApp</a></li>
                    </ul>
                </div>

            </div>

            <!-- Footer Bottom: Copyright -->
            <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; padding:3rem 0; gap:1.5rem;">
                <p style="color:rgba(255,255,255,0.35); font-size:0.85rem; letter-spacing:0.5px;">&copy; 2026 Elite Luxury Bookings. All rights reserved. Global Concierge Service.</p>
                <div style="display:flex; gap:2rem; flex-wrap:wrap;">
                    <a href="/elite-private-jet-charter/" style="color:rgba(255,255,255,0.35); text-decoration:none; font-size:0.8rem; text-transform:uppercase; letter-spacing:1.5px;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.35)''">Private Jets</a>
                    <a href="/luxury-yacht-rentals/" style="color:rgba(255,255,255,0.35); text-decoration:none; font-size:0.8rem; text-transform:uppercase; letter-spacing:1.5px;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.35)''">Yachts</a>
                    <a href="/blog/" style="color:rgba(255,255,255,0.35); text-decoration:none; font-size:0.8rem; text-transform:uppercase; letter-spacing:1.5px;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.35)''">Blog</a>
                    <a href="/contact/" style="color:rgba(255,255,255,0.35); text-decoration:none; font-size:0.8rem; text-transform:uppercase; letter-spacing:1.5px;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.35)''">Contact</a>
                </div>
            </div>

        </div>
    </footer>
'@

# Also upgrade the old CSS for footer to add responsive wrap
$footerCssUpgrade = @'
    /* ===== UPGRADED FOOTER CSS ===== */
    footer { background: #000; border-top: 1px solid rgba(255,255,255,0.05); }
    @media (max-width: 900px) {
        footer > div > div:first-child { justify-content: flex-start !important; gap: 2rem !important; }
    }
    @media (max-width: 600px) {
        footer > div > div:first-child { flex-direction: column !important; align-items: center !important; text-align: center !important; }
        footer > div > div:first-child > div { width: 100% !important; max-width: 100% !important; }
        footer > div > div:last-child { flex-direction: column !important; text-align: center !important; }
    }
'@

$rootDir = (Get-Location).Path

# Get ALL index.html files
$htmlFiles = Get-ChildItem -Path . -Filter "index.html" -Recurse

$count = 0

foreach ($file in $htmlFiles) {
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)

    # Use a regex that matches <footer ...> ... </footer>
    $newContent = $content -replace '(?s)<footer.*?>.*?</footer>', $newFooter

    # Inject footer responsive CSS before </style>
    if ($newContent -notlike "*UPGRADED FOOTER CSS*") {
        $newContent = $newContent -replace '</style>', "$footerCssUpgrade`n    </style>"
    } else {
        # Update existing CSS block if found
        $newContent = $newContent -replace '(?s)/\* ===== UPGRADED FOOTER CSS ===== \*/.*?\}(?=\n\s*</style>|\s*</style>)', $footerCssUpgrade
    }

    [System.IO.File]::WriteAllText($file.FullName, $newContent, (New-Object System.Text.UTF8Encoding $false))
    $count++
    Write-Host "Footer upgraded -> $($file.Name) in $($file.DirectoryName | Split-Path -Leaf)"
}

Write-Host "`n✅ Done. Footer updated in $count pages."
