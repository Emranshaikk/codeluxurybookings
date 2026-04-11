$files = Get-ChildItem -Path . -Filter *.html
foreach ($file in $files) {
    Write-Host "Updating WhatsApp color for $($file.Name)..."
    $content = Get-Content $file.FullName -Raw
    
    # Update to WhatsApp Green
    if ($content -match 'wa-float') {
        $content = $content -replace 'background: linear-gradient\(135deg, #D4AF37, #B8860B\);', 'background: linear-gradient(135deg, #25D366, #128C7E);'
        $content = $content -replace 'color: #000 !important;', 'color: #fff !important;'
        $content = $content -replace 'rgba\(212, 175, 55, 0\.1\)', 'rgba(37, 211, 102, 0.1)'
        $content = $content -replace 'rgba\(212, 175, 55, 0\.4\)', 'rgba(37, 211, 102, 0.4)'
        Set-Content $file.FullName $content -NoNewline
    }
}
Write-Host "WhatsApp Brand Green successfully deployed site-wide."
