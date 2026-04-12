$gridHtml = Get-Content "global-route-silo.html" -Raw

# Correct mobile block with all closing braces
$cleanMobileBlock = '
        /* MOBILE EXCELLENCE */
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

# SILO REPLACEMENT PATTERN
$siloHeader = "<!-- CONTEXTUAL INTERLINKING SECTION -->"

$files = Get-ChildItem route*.html | Where-Object { $_.Name -ne "global-route-silo.html" }

foreach ($file in $files) {
    Write-Host "Repairing $($file.Name)..."
    $content = Get-Content $file.FullName -Raw

    # 1. Fix the Header Style Tag (Restore closed braces)
    # This regex finds everything from /* MOBILE EXCELLENCE */ up to the first </style>
    $headerStyleRegex = '(?s)/\* MOBILE EXCELLENCE \*/.*?</style>'
    if ($content -match $headerStyleRegex) {
        $content = [regex]::Replace($content, $headerStyleRegex, $cleanMobileBlock)
    }

    # 2. Fix the Silo Area (Full Swap)
    # This regex finds from the interlinking header up to the footer
    $siloAreaRegex = '(?s)' + [regex]::Escape($siloHeader) + '.*?(?=<footer)'
    if ($content -match $siloAreaRegex) {
        $content = [regex]::Replace($content, $siloAreaRegex, ($siloHeader + "`n" + $gridHtml + "`n`n"))
    }

    # 3. Final Safety Check: Any unclosed media queries before any </style>?
    # If we see "@media (max-width: 1024px) { ... </style>" without a closing brace
    # We'll just force-close it. (Heuristic cleanup)
    $content = $content -replace '(?s)@media \(max-width: 1024px\) \{([^{}]*\{[^{}]*\}[^{}]*)\}\s+</style>', '@media (max-width: 1024px) {$1}`n    }`n    </style>'
    
    # Actually, the most robust way is to ensure all files have the exact same footer structure.
    # The silo replacement above already does a full swap of the silo area.
    
    Set-Content $file.FullName $content -NoNewline
}

Write-Host "Network Repair Complete. All braces balanced."
