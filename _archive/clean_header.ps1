Get-ChildItem -Path "$PSScriptRoot" -Filter *.html | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # Precise multi-line or single-line removal of the Desktop Nav CTA
    $content = $content -replace '(?s)<div class="nav-cta">.*?https://wa.me/.*?WhatsApp.*?</div>', ''
    
    # Precise removal of the Mobile Nav CTA
    $content = $content -replace '<a href="https://wa.me/.*?" class="mobile-cta".*?>.*?</a>', ''

    Set-Content $_.FullName $content
}
