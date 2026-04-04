$gridHtml = Get-Content "global-route-silo.html" -Raw

# Get all route files
$files = Get-ChildItem route*.html | Where-Object { $_.Name -ne "global-route-silo.html" }

foreach ($file in $files) {
    Write-Host "-------------------------------------------"
    Write-Host "Processing $($file.Name)..."
    $content = Get-Content $file.FullName -Raw
    
    # --- PHASE 1: COMPREHENSIVE REPAIR (IN-PLACE) ---
    # 1. Restore Select Tag if missing (due to legacy replacement bugs)
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
        $content = $content -replace $depGroupPattern, ('$1' + "`n" + $selectTag)
        Write-Host "  - Restored missing Departure Select tag."
    }

    # 2. Fix Footer (Case: Space prefix/missing <footer)
    $footerSearch = 'class="section-padding" style="background: #000; border-top: 1px solid rgba(255,255,255,0.05); text-align: center;">'
    if ($content -match "(?s)\s+$([regex]::Escape($footerSearch))" -and $content -notmatch "<footer\s+$([regex]::Escape($footerSearch))") {
        $content = $content -replace "(?s)\s+class=""section-padding"" style=""background: #000; border-top: 1px solid rgba\(255,255,255,0\.05\); text-align: center;"">", ("`n    <footer " + $footerSearch)
        Write-Host "  - Repaired Footer tag."
    }

    # 3. Clean up "Zombie" CSS blocks (Dangling styles outside @media queries or duplicates)
    $zombiePattern = '(?s)\s+\.hero h1 \{ font-size: clamp\(2rem, 8vw, 3.5rem\); line-height: 1.2; \}.*?\.btn \{ width: 100%; margin-bottom: 1rem; \}\s+\}'
    $content = $content -replace $zombiePattern, ""
    
    # 4. Inject/Update Mobile CSS (Consolidation)
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

    # Regex that correctly matches media queries with multiple nested braces
    $existingMobileReg = '(?s)@media \(max-width: 768px\) \{(?:[^{}]*\{[^{}]*\})*[^{}]*\}'
    
    if ($content -match $existingMobileReg) {
        # Replace the first one (usually in <head>), keep the others if they belong to something else?
        $content = [regex]::Replace($content, $existingMobileReg, $newMobileBlock, 1)
        # Remove any others that might be in the head part
        if ($content -match "(?s)(.*)(<!-- CONTEXTUAL INTERLINKING SECTION -->)(.*)") {
            $headPart = $Matches[1]; $midPart = $Matches[2]; $tailPart = $Matches[3]
            $headPart = $headPart -replace $existingMobileReg, ""
            $content = $headPart + $midPart + $tailPart
        }
        Write-Host "  - Sanitized and Updated Mobile CSS."
    }

    # --- PHASE 2: IDEMPOTENT SCAFFOLDING ---
    # Ensure Interlinking is fresh
    $sectionHeader = "<!-- CONTEXTUAL INTERLINKING SECTION -->"
    if ($content -match [regex]::Escape($sectionHeader)) {
        $pattern = "(?s)$([regex]::Escape($sectionHeader)).*?(?=<footer)"
        $content = $content -replace $pattern, ("$sectionHeader`n$gridHtml`n`n")
    }

    Set-Content $file.FullName $content -NoNewline

    # --- PHASE 3: SELECTIVE REVERSE GENERATION ---
    # Only reverse if the file is a "Source" (Forward) route
    # We define sources as files that have "london" as the DEPARTURE or follow a pattern.
    # Safe heuristic: only generate reverse if it doesn't exist OR if we are forcing it.
    if ($file.Name -match "route(.+)to(.+)\.html") {
        $from = $Matches[1]; $to = $Matches[2]
        $reverseName = "route$($to)to$($from).html"
        
        # Check if we should generate/refresh the reverse
        # Heuristic: If 'from' is london, it's likely a primary source.
        # Or just do all, but make sure we don't reverse an already reversed file.
        
        # Check Canonical vs Filename to see if it's already correct
        $expectedCanonical = "https://eliteluxurybookings.com/$from-to-$to-private-jet-cost/"
        $canonicalPattern = '<link rel="canonical" href="' + [regex]::Escape($expectedCanonical) + '"/?>'
        
        if ($content -match $canonicalPattern) {
             Write-Host "  - Forward Route: $from to $to. Generating/Updating Reverse: $reverseName"
             $rev = $content
             
             $fromP = $from.Substring(0,1).ToUpper() + $from.Substring(1)
             $toP = $to.Substring(0,1).ToUpper() + $to.Substring(1)
             
             # Reverse Text
             $rev = $rev -replace "(?i)$fromP to $toP", "MARKER_P"
             $rev = $rev -replace "(?i)$toP to $fromP", "$fromP to $toP"
             $rev = $rev.Replace("MARKER_P", "$toP to $fromP")
             
             $rev = $rev -replace "(?i)$from to $to", "MARKER_L"
             $rev = $rev -replace "(?i)$to to $from", "$from to $to"
             $rev = $rev.Replace("MARKER_L", "$to to $from")
             
             $rev = $rev -replace "(?i)$from-to-$to", "MARKER_S"
             $rev = $rev -replace "(?i)$to-to-$from", "$from-to-$to"
             $rev = $rev.Replace("MARKER_S", "$to-to-$from")

             # Reverse Form (Robust Inner Swap)
             if ($rev -match '(?s)(<select[^>]*id="departure"[^>]*>)(.*?)(</select>)') {
                 $dI = $Matches[2]
                 if ($rev -match '(?s)(<select[^>]*id="arrival"[^>]*>)(.*?)(</select>)') {
                     $aI = $Matches[2]
                     $rev = $rev.Replace($dI, "INTERNAL_SWAP_MARKER")
                     $rev = $rev.Replace($aI, $dI)
                     $rev = $rev.Replace("INTERNAL_SWAP_MARKER", $aI)
                     Write-Host "    - Reversed Form Options."
                 }
             }
             
             # Reverse Canonical
             $revSlug = "$to-to-$from-private-jet-cost"
             $rev = $rev -replace '<link rel="canonical" href=".*?">', ('<link rel="canonical" href="https://eliteluxurybookings.com/' + $revSlug + '/">')
             
             Set-Content $reverseName $rev -NoNewline
        } else {
             Write-Host "  - Already a Reverse Route (Skipping Scaling)."
        }
    }
}
Write-Host "Master Scaling v8 Complete."
