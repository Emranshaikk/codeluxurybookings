$gridHtml = Get-Content "global-route-silo.html" -Raw

# Get all route files
$files = Get-ChildItem route*.html | Where-Object { $_.Name -ne "global-route-silo.html" }

foreach ($file in $files) {
    Write-Host "Processing $($file.Name)..."
    $content = Get-Content $file.FullName -Raw
    
    # --- PHASE 1: REPAIR ---
    # Fix DEPOPT_PLACEHOLDER (Legacy v4 bug)
    if ($content.Contains("DEPOPT_PLACEHOLDER")) {
        if ($content -match '(?s)<select[^>]*id="arrival"[^>]*>(.*?)</select>') {
             $arrOptions = $Matches[1]
             $content = $content.Replace("DEPOPT_PLACEHOLDER", $arrOptions)
             Write-Host "  - Cleaned up residual DEPOPT_PLACEHOLDER."
        }
    }

    # Fix Footer (Case: Space prefix/missing <footer)
    $footerAttribs = 'class="section-padding" style="background: #000; border-top: 1px solid rgba(255,255,255,0.05); text-align: center;">'
    if ($content -match "(?s)\s+$([regex]::Escape($footerAttribs))" -and $content -notmatch "<footer\s+$([regex]::Escape($footerAttribs))") {
        $content = $content -replace "(?s)\s+class=""section-padding"" style=""background: #000; border-top: 1px solid rgba\(255,255,255,0\.05\); text-align: center;"">", ("`n    <footer " + $footerAttribs)
        Write-Host "  - Repaired Footer tag."
    }

    # --- PHASE 2: MOBILE CSS (Force Update) ---
    # Target the EXACT block structure from the viewed files
        
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

    if ($content.Contains(".section-padding { padding: 4rem 0; }")) {
        # Use simple string replacement for the block if possible, or broad regex
        $content = $content -replace '(?s)@media \(max-width: 768px\) \{.*?padding: 4rem 0;.*?\}', $newMobileBlock
        Write-Host "  - Injected Mobile Optimization CSS."
    }

    # --- PHASE 3: INTERLINKING ---
    $sectionHeader = "<!-- CONTEXTUAL INTERLINKING SECTION -->"
    if ($content -match [regex]::Escape($sectionHeader)) {
        $pattern = "(?s)$([regex]::Escape($sectionHeader)).*?(?=<footer)"
        $content = $content -replace $pattern, ("$sectionHeader`n$gridHtml`n`n")
    }

    Set-Content $file.FullName $content -NoNewline
    
    # --- PHASE 4: REGENERATE REVERSE ---
    if ($file.Name -match "route(.+)to(.+)\.html") {
        $f = $Matches[1]; $t = $Matches[2]
        $reverseName = "route$($t)to$($f).html"
        
        Write-Host "  - Scaling Reverse: $reverseName"
        $rev = $content
        
        $fp = $f.Substring(0,1).ToUpper() + $f.Substring(1)
        $tp = $t.Substring(0,1).ToUpper() + $t.Substring(1)
        
        # 1. Reverse Text (3-way swap)
        # Proper Case
        $rev = $rev -replace "(?i)$fp to $tp", "REVSWAP_MARKER_P"
        $rev = $rev -replace "(?i)$tp to $fp", "$fp to $tp"
        $rev = $rev.Replace("REVSWAP_MARKER_P", "$tp to $fp")
        
        # Lower Case
        $rev = $rev -replace "(?i)$f to $t", "REVSWAP_MARKER_L"
        $rev = $rev -replace "(?i)$t to $f", "$f to $t"
        $rev = $rev.Replace("REVSWAP_MARKER_L", "$t to $f")
        
        # Slug Case
        $rev = $rev -replace "(?i)$f-to-$t", "REVSWAP_MARKER_S"
        $rev = $rev -replace "(?i)$t-to-$f", "$f-to-$t"
        $rev = $rev.Replace("REVSWAP_MARKER_S", "$t-to-$f")

        # 2. Reverse Form Options (Robust Inner Swap)
        if ($rev -match '(?s)(<select[^>]*id="departure"[^>]*>)(.*?)(</select>)') {
            $dInner = $Matches[2]
            if ($rev -match '(?s)(<select[^>]*id="arrival"[^>]*>)(.*?)(</select>)') {
                $aInner = $Matches[2]
                
                # Perform the swap on the whole content to avoid placeholder collisions
                $rev = $rev.Replace($dInner, "FORM_INNER_SWAP_MARKER")
                $rev = $rev.Replace($aInner, $dInner)
                $rev = $rev.Replace("FORM_INNER_SWAP_MARKER", $aInner)
                Write-Host "    - Swapped Form Flights."
            }
        }

        # 3. Canonical Self-Fix
        $rev = $rev -replace '<link rel="canonical" href=".*?">', ('<link rel="canonical" href="https://eliteluxurybookings.com/' + $t + '-to-' + $f + '-private-jet-cost/">')

        Set-Content $reverseName $rev -NoNewline
    }
}

Write-Host "Master Scaling v7 Complete: Repair + Mobile + Scaling."
