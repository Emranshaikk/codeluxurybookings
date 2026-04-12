$gridHtml = Get-Content "global-route-silo.html" -Raw

# Get all route files
$files = Get-ChildItem route*.html | Where-Object { $_.Name -ne "global-route-silo.html" }

foreach ($file in $files) {
    Write-Host "-------------------------------------------"
    Write-Host "Processing $($file.Name)..."
    $content = Get-Content $file.FullName -Raw
    
    # --- PHASE 1: REPAIR ---
    # 1. Restore Select Tag if missing
    $depGroupPattern = '(?s)(<div class="form-group">\s*<label[^>]*for="departure"[^>]*>.*?</label>)\s*(?!<select)'
    if ($content -match $depGroupPattern) {
        $selectTag = '
                                <select class="form-control" id="departure" name="departure" required>
                                    <option value="EGLF" selected>London Farnborough (EGLF)</option>
                                    <option value="EGKB">London Biggin Hill (EGKB)</option>
                                    <option value="EGGW">London Luton (EGGW)</option>
                                    <option value="EGSS">London Stansted (EGSS)</option>
                                    <option value="EGLL">London Heathrow (EGLL)</option>
                                </select>'
        # Use '$1' to prevent PowerShell variable expansion of the regex backreference
        $replacement = '$1' + "`n" + $selectTag
        $content = [regex]::Replace($content, $depGroupPattern, $replacement)
        Write-Host "  - Restored missing Departure Select tag."
    }

    # 2. Fix Footer
    $footerSearch = 'class="section-padding" style="background: #000; border-top: 1px solid rgba(255,255,255,0.05); text-align: center;">'
    if ($content.Contains($footerSearch) -and -not $content.Contains("<footer " + $footerSearch)) {
        $content = $content.Replace($footerSearch, "<footer " + $footerSearch)
        Write-Host "  - Repaired Footer tag."
    }

    # 3. Mobile CSS & Structure Repair (The "17 Problems" Fix)
    # Strategy: 1. Remove all malformed media query fragments first.
    # 2. Re-inject clean styles.
    
    # regex for any media query fragment (zombie) that was left over from broken replaces
    $brokenZombies = '(?s)\s+\.hero h1 \{ font-size: clamp\(2rem, 8vw, 3.5rem\); line-height: 1.2; \}.*?\.btn \{ width: 100%; margin-bottom: 1rem; \}\s+\}'
    $content = $content -replace $brokenZombies, ""
    
    # Fix extra braces that are dangling before </style>
    $content = $content -replace '(?s)\}\s+\}\s+</style>', "}`n        }`n    </style>" 
    # Wait, better: remove any '}' that follows a '}' if it's right before </style>
    $content = $content -replace '(?s)\}\s+\}\s+</style>', "}`n    </style>"

    # 4. Consolidate Mobile CSS
    $newMobileBlock = '@media (max-width: 768px) {
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
        }'

    # Robust regex for media queries with nested blocks
    $nestedMobilePattern = '(?s)@media \(max-width: 768px\) \{(?:[^{}]*\{[^{}]*\})*[^{}]*\}'
    
    if ($content -match $nestedMobilePattern) {
        # Update the first one
        $content = [regex]::Replace($content, $nestedMobilePattern, $newMobileBlock, 1)
        # Clean any others from the head
        if ($content -match "(?s)(.*)(<!-- CONTEXTUAL INTERLINKING SECTION -->)(.*)") {
            $head = $Matches[1]; $silo = $Matches[2]; $tail = $Matches[3]
            $head = $head -replace $nestedMobilePattern, ""
            $content = $head + $silo + $tail
        }
        Write-Host "  - Sanitized and Updated Mobile CSS."
    }

    # --- PHASE 2: INTERLINKING ---
    $sectionHeader = "<!-- CONTEXTUAL INTERLINKING SECTION -->"
    if ($content.Contains($sectionHeader)) {
        $pattern = "(?s)" + [regex]::Escape($sectionHeader) + ".*?(?=<footer)"
        $content = [regex]::Replace($content, $pattern, ($sectionHeader + "`n" + $gridHtml + "`n`n"))
    }

    Set-Content $file.FullName $content -NoNewline

    # --- PHASE 3: REVERSE GENERATION ---
    if ($file.Name -match "route(.+)to(.+)\.html") {
        $from = $Matches[1]; $to = $Matches[2]
        $reverseName = "route$($to)to$($from).html"
        
        # IDEMPOTENCY: Only reverse if it's currently a "Forward" route
        $expectedCanonical = "https://eliteluxurybookings.com/$from-to-$to-private-jet-cost/"
        if ($content.Contains($expectedCanonical)) {
             Write-Host "  - Scaling Forward -> Reverse: $reverseName"
             $rev = $content
             
             $fromP = $from.Substring(0,1).ToUpper() + $from.Substring(1)
             $toP = $to.Substring(0,1).ToUpper() + $to.Substring(1)
             
             # Swap strings
             $rev = $rev -replace "(?i)$fromP to $toP", "SWAP_P"
             $rev = $rev -replace "(?i)$toP to $fromP", "$fromP to $toP"
             $rev = $rev.Replace("SWAP_P", "$toP to $fromP")
             
             $rev = $rev -replace "(?i)$from to $to", "SWAP_L"
             $rev = $rev -replace "(?i)$to to $from", "$from to $to"
             $rev = $rev.Replace("SWAP_L", "$to to $from")
             
             $rev = $rev -replace "(?i)$from-to-$to", "SWAP_S"
             $rev = $rev -replace "(?i)$to-to-$from", "$from-to-$to"
             $rev = $rev.Replace("SWAP_S", "$to-to-$from")

             # Swap Form Options
             if ($rev -match '(?s)(<select[^>]*id="departure"[^>]*>)(.*?)(</select>)') {
                  $dInner = $Matches[2]
                  if ($rev -match '(?s)(<select[^>]*id="arrival"[^>]*>)(.*?)(</select>)') {
                      $aInner = $Matches[2]
                      $rev = $rev.Replace($dInner, "FORM_MARKER")
                      $rev = $rev.Replace($aInner, $dInner)
                      $rev = $rev.Replace("FORM_MARKER", $aInner)
                  }
             }
             
             # Swap Canonical
             $revSlug = "$to-to-$from-private-jet-cost"
             $rev = $rev -replace '<link rel="canonical" href=".*?">', ('<link rel="canonical" href="https://eliteluxurybookings.com/' + $revSlug + '/">')
             
             Set-Content $reverseName $rev -NoNewline
        }
    }
}
Write-Host "Master Scaling v9 Complete."
