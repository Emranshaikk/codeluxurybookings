$gridHtml = Get-Content "global-route-silo.html" -Raw

# Get all route files
$files = Get-ChildItem route*.html | Where-Object { $_.Name -ne "global-route-silo.html" }

foreach ($file in $files) {
    Write-Host "Processing $($file.Name)..."
    $content = Get-Content $file.FullName -Raw
    
    # --- PHASE 1: SANITY REPAIR & CLEANUP ---
    # Fix residual v4 placeholders if any exist
    if ($content -contains "DEPOPT_PLACEHOLDER") {
        # Heuristic: try to find the other select to restore options
        if ($content -match '(?s)<select[^>]*id="arrival"[^>]*>(.*?)</select>') {
             $arrInner = $Matches[1]
             $content = $content.Replace("DEPOPT_PLACEHOLDER", $arrInner)
             Write-Host "  - Repaired residual DEPOPT_PLACEHOLDER."
        }
    }

    # Fix Mangled Footer (Case: Missing <footer tag)
    $footerSearch = ' class="section-padding" style="background: #000; border-top: 1px solid rgba(255,255,255,0.05); text-align: center;">'
    if ($content -match "(?s)\s+$([regex]::Escape($footerSearch))" -and $content -notmatch "<footer$([regex]::Escape($footerSearch))") {
        $content = $content -replace "(?s)\s+class=""section-padding"" style=""background: #000; border-top: 1px solid rgba\(255,255,255,0\.05\); text-align: center;"">", ("`n<footer" + $footerSearch)
        Write-Host "  - Restored missing <footer tag."
    }

    # Fix Missing Departure Label
    $depGroupNoLabel = '(?s)(<div class="form-group">)\s*(<select[^>]*id="departure")'
    if ($content -match $depGroupNoLabel) {
        $depLabel = '<label class="form-label" for="departure">Departure Airport</label>'
        $content = $content -replace $depGroupNoLabel, ("$1`n                                $depLabel`n                                $2")
        Write-Host "  - Restored missing Departure Label."
    }

    # --- PHASE 2: MOBILE OPTIMIZATION (Multiline Regex Fix) ---
    $mobileCss = '
        @media (max-width: 768px) {
            .section-padding { padding: 3rem 0; }
            .hero h1 { font-size: clamp(2rem, 8vw, 3.5rem); line-height: 1.2; }
            .hero-sub { font-size: 1.1rem; padding: 0 1rem; }
            .form-wrapper { padding: 1.25rem !important; border-radius: 15px; }
            .container { padding: 0 1rem; }
            .grid-2 { gap: 1.5rem; }
            .benefit-card { padding: 1.5rem; }
            .form-grid { gap: 1rem; }
            h2 { font-size: 2.2rem !important; }
        }
    '
    $oldMediaPattern = '(?s)@media \(max-width: 768px\) \{.*?padding: 4rem 0;.*?\}'
    if ($content -match $oldMediaPattern) {
         $content = $content -replace $oldMediaPattern, $mobileCss
         Write-Host "  - Injected Mobile Optimization CSS."
    }

    # --- PHASE 3: INTERLINKING ---
    $sectionHeader = "<!-- CONTEXTUAL INTERLINKING SECTION -->"
    if ($content -match [regex]::Escape($sectionHeader)) {
        $pattern = "(?s)$([regex]::Escape($sectionHeader)).*?(?=<footer)"
        $content = $content -replace $pattern, ("$sectionHeader`n$gridHtml`n")
    }

    # Save source updates
    Set-Content $file.FullName $content -NoNewline
    
    # --- PHASE 4: REVERSE ROUTE GENERATION ---
    if ($file.Name -match "route(.+)to(.+)\.html") {
        $from = $Matches[1]; $to = $Matches[2]
        $reverseName = "route$($to)to$($from).html"
        
        Write-Host "  - Scaling: $reverseName"
        $rev = $content
        
        # --- Comprehensive String Swaps (JS + Body) ---
        $fromP = $from.Substring(0,1).ToUpper() + $from.Substring(1)
        $toP = $to.Substring(0,1).ToUpper() + $to.Substring(1)
        
        # We perform swaps on ALL text to catch JS fragments
        # 1. Reverse "City to City"
        $rev = $rev -replace "(?i)$fromP to $toP", "TEMP_HOLDER_P"
        $rev = $rev -replace "(?i)$toP to $fromP", "$fromP to $toP"
        $rev = $rev.Replace("TEMP_HOLDER_P", "$toP to $fromP")
        
        # 2. Reverse "city to city"
        $rev = $rev -replace "(?i)$from to $to", "TEMP_HOLDER_L"
        $rev = $rev -replace "(?i)$to to $from", "$from to $to"
        $rev = $rev.Replace("TEMP_HOLDER_L", "$to to $from")
        
        # 3. Reverse "city-to-city"
        $rev = $rev -replace "(?i)$from-to-$to", "TEMP_HOLDER_S"
        $rev = $rev -replace "(?i)$to-to-$from", "$from-to-$to"
        $rev = $rev.Replace("TEMP_HOLDER_S", "$to-to-$from")

        # --- ROCK SOLID FORM SWAP ---
        $depRegex = '(?s)(<select[^>]*id="departure"[^>]*>)(.*?)(</select>)'
        $arrRegex = '(?s)(<select[^>]*id="arrival"[^>]*>)(.*?)(</select>)'
        
        if ($rev -match $depRegex) {
            $dI = $Matches[2]
            if ($rev -match $arrRegex) {
                $aI = $Matches[2]
                
                # Use sub-placeholders that won't conflict with labels
                $rev = $rev.Replace($dI, "INTERNAL_DEP_MARKER")
                $rev = $rev.Replace($aI, $dI)
                $rev = $rev.Replace("INTERNAL_DEP_MARKER", $aI)
                Write-Host "    - Reversed Form."
            }
        }

        # --- CANONICAL ---
        $slug = "$($to)-to-$($from)-private-jet-cost"
        $rev = $rev -replace '<link rel="canonical" href=".*?">', ('<link rel="canonical" href="https://eliteluxurybookings.com/' + $slug + '/">')

        Set-Content $reverseName $rev -NoNewline
    }
}

Write-Host "Master Scaling v6 Complete."
