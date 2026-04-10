$files = Get-ChildItem -Path . -Filter *.html
foreach ($file in $files) {
    Write-Host "Optimizing mobile for $($file.Name)..."
    $content = Get-Content $file.FullName -Raw
    
    # 1. Add .form-grid class if missing
    if ($content -notmatch '\.form-grid') {
        $content = $content -replace '(#D4AF37;)\s*\}', "$1 }`n`n        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }"
    }

    # 2. Update Mobile Media Query Block
    $targetBlock = '@media (max-width: 768px) {'
    $newMobileRules = '@media (max-width: 768px) {
            .hero { padding: 6rem 0 3rem !important; }
            .hero h1 { font-size: 2.2rem !important; line-height: 1.1; padding: 0 1rem; }
            .hero-sub { font-size: 1rem !important; padding: 0 1.5rem; }
            .grid-2, .grid-3 { grid-template-columns: 1fr !important; gap: 2.5rem !important; }
            .section-padding { padding: 4rem 1rem !important; }
            .aviation-search-engine { padding: 1.5rem !important; margin: 1rem !important; }
            .form-grid { grid-template-columns: 1fr !important; gap: 1rem !important; }
            .nav-brand { font-size: 1.3rem !important; }
            .btn-gold { padding: 0.6rem 1rem !important; font-size: 0.7rem !important; }
        }'

    # Replace the existing block precisely
    if ($content -match '@media\s*\(max-width:\s*768px\)\s*\{[^}]*(\.aviation-search-engine[^}]*\}[^}]*|[^}]*)\}') {
        $content = $content -replace '@media\s*\(max-width:\s*768px\)\s*\{[^}]*\}', $newMobileRules
    }

    Set-Content $file.FullName $content -NoNewline
}
Write-Host "Site-wide mobile optimization complete."
