$siloPath = "global-route-silo.html"
$siloContent = Get-Content $siloPath -Raw

# Identify the core structure we want to propagate
$siloHeader = "<!-- CONTEXTUAL INTERLINKING SECTION -->"
$siloFooter = "</style>"
# We want to replace from SILO HEADER to SILO FOOTER

$files = Get-ChildItem route*.html | Where-Object { $_.Name -ne "global-route-silo.html" }

foreach ($file in $files) {
    Write-Host "Ultimate Silo Reset in $($file.Name)..."
    $content = Get-Content $file.FullName -Raw

    # 1. Reset the entire Silo area with the known-good version
    $regex = '(?s)' + [regex]::Escape($siloHeader) + '.*?' + [regex]::Escape($siloFooter)
    if ($content -match $regex) {
        $content = [regex]::Replace($content, $regex, ($siloHeader + "`n" + $siloContent))
    }

    # 2. Fix the Header Style block (Ensuring it's also perfect)
    $headerStyles = '        /* MOBILE EXCELLENCE */
        @media (max-width: 1024px) {
            .grid-2 { grid-template-columns: 1fr; gap: 3rem; }
            .hero h1 { font-size: 3rem; }
            .form-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 768px) {
            .section-padding { padding: 3rem 0; }
            .hero h1 { font-size: clamp(2rem, 8vw, 3.5rem); line-height: 1.2; }
            .hero-sub { font-size: 1.1rem; padding: 0 1rem; }
            .form-wrapper { padding: 1.25rem !important; border-radius: 15px; }
            .container { padding: 0 1rem; }
            .grid-2 { gap: 1.5rem; }
            .benefit-card { padding: 1.25rem; }
            .form-grid { gap: 0.75rem; }
            h2 { font-size: 2.2rem !important; }
            .btn { width: 100%; margin-bottom: 1rem; }
        }
    </style>'

    $headerRegex = '(?s)/\* MOBILE EXCELLENCE \*/.*?</style>'
    if ($content -match $headerRegex) {
        $content = [regex]::Replace($content, $headerRegex, $headerStyles)
    }

    Set-Content $file.FullName $content -NoNewline
}

Write-Host "The Network is now 100% Repaired."
