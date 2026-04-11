Get-ChildItem -Path "$PSScriptRoot" -Filter *.html | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # 1. Define the Standard Premium WhatsApp Button CSS
    $waStyle = "`n        .wa-float { position: fixed; bottom: 30px; right: 30px; background: #25D366; color: #fff; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 100000; box-shadow: 0 10px 25px rgba(0,0,0,0.3); transition: all 0.3s; }`n        .wa-float:hover { transform: scale(1.1); background: #128C7E; }`n"
    
    # 2. Inject CSS if it's missing the .wa-float definition
    if ($content -notlike "*.wa-float *") {
        $content = $content -replace "</style>", "$waStyle</style>"
    } else {
        # If it exists but might have been turned gold, force it back to green
        $content = $content -replace '\.wa-float\s*\{[^}]*?background:[^;]+', '.wa-float { position: fixed; bottom: 30px; right: 30px; background: #25D366'
    }

    # 3. Ensure the anchor itself has the class if it's just a raw link
    if ($content -like "*wa.me*" -and $content -notlike "*class=`"wa-float`"*") {
        $content = $content -replace '<a href="https://wa.me/918801079030"', '<a href="https://wa.me/918801079030" class="wa-float"'
    }

    Set-Content $_.FullName $content
}
