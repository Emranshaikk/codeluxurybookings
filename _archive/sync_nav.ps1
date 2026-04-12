Get-ChildItem -Path "$PSScriptRoot" -Filter *.html | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # Skip if already updated
    if ($content -like "*luxury-villa-rentals.html*") { return }

    # 1. Update Desktop Nav Links
    $oldDesktop = '<li><a href="/elite-private-jet-charter.html">Private Jets</a></li>'
    $newDesktop = '<li><a href="/elite-private-jet-charter.html">Private Jets</a></li>\n                <li><a href="/luxury-villa-rentals.html">Villas</a></li>'
    
    # 2. Update Mobile Menu Links
    $oldMobile = '<a href="/elite-private-jet-charter.html">✈ Private Jets</a>'
    $newMobile = '<a href="/elite-private-jet-charter.html">✈ Private Jets</a>\n        <a href="/luxury-villa-rentals.html">🏡 Luxury Villas</a>'

    $content = $content -replace [regex]::Escape($oldDesktop), $newDesktop
    $content = $content -replace [regex]::Escape($oldMobile), $newMobile

    Set-Content $_.FullName $content
}
