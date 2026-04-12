$files = Get-ChildItem -Path . -Filter *.html
foreach ($file in $files) {
    Write-Host "Updating $($file.Name)..."
    $content = Get-Content $file.FullName -Raw
    
    # The new refined CSS for the button
    $newStyles = ".btn-gold {
            background: linear-gradient(135deg, #D4AF37, #B8860B);
            color: #000 !important;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            display: inline-block;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
        }

        .btn-gold:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
            filter: brightness(1.1);
        }

        .btn-sm {
            padding: 0.6rem 1.2rem;
            font-size: 0.75rem;
        }"

    # Use Regex to replace the entire old .btn-gold block with the new one + hover + sm variant
    if ($content -match '\.btn-gold\s*\{[^}]*\}') {
        $content = $content -replace '\.btn-gold\s*\{[^}]*\}', $newStyles
        Set-Content $file.FullName $content -NoNewline
    }
}
Write-Host "Site-wide button upgrade complete."
