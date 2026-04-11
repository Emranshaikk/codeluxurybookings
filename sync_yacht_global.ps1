Get-ChildItem -Path "$PSScriptRoot" -Filter *.html | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # Skip the new yacht page itself as it's already built correctly
    if ($_.Name -eq "luxury-yacht-rentals.html") { return }

    # 1. Update Desktop Nav
    $oldDesktop = '<li><a href="/luxury-villa-rentals.html">Villas</a></li>'
    $newDesktop = '<li><a href="/luxury-villa-rentals.html">Villas</a></li>\n                <li><a href="/luxury-yacht-rentals.html">Yachts</a></li>'
    
    # 2. Update Mobile Menu
    $oldMobile = '<a href="/luxury-villa-rentals.html">🏡 Luxury Villas</a>'
    $newMobile = '<a href="/luxury-villa-rentals.html">🏡 Luxury Villas</a>\n        <a href="/luxury-yacht-rentals.html">⚓ Luxury Yachts</a>'

    # 3. Update Footer (Regex for precision)
    $oldFooterItem = '<li><a href="/luxury-villa-rentals.html"'
    $newFooterItem = '<li><a href="/luxury-yacht-rentals.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Luxury Yachts</a></li>\n                        <li><a href="/luxury-villa-rentals.html"'

    $content = $content -replace [regex]::Escape($oldDesktop), $newDesktop
    $content = $content -replace [regex]::Escape($oldMobile), $newMobile
    $content = $content -replace [regex]::Escape($oldFooterItem), $newFooterItem

    # Final newline fix for any injected \n
    $content = $content -replace '\\n', "`n"

    Set-Content $_.FullName $content
}
