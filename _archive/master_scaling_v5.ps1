$gridHtml = Get-Content "global-route-silo.html" -Raw

# Get all route files
$files = Get-ChildItem route*.html | Where-Object { $_.Name -ne "global-route-silo.html" }

foreach ($file in $files) {
    Write-Host "Processing $($file.Name)..."
    $content = Get-Content $file.FullName -Raw
    
    # --- PHASE 1: SANITY REPAIR ---
    # Fix Mangled Footer (Case: Missing <footer tag)
    $footerSearch = ' class="section-padding" style="background: #000; border-top: 1px solid rgba(255,255,255,0.05); text-align: center;">'
    if ($content -match "\s+$([regex]::Escape($footerSearch))" -and $content -notmatch "<footer$([regex]::Escape($footerSearch))") {
        # Use regex to find it even with variable leading whitespace
        $content = $content -replace "\s+class=""section-padding"" style=""background: #000; border-top: 1px solid rgba\(255,255,255,0\.05\); text-align: center;"">", ('<footer' + $footerSearch)
        Write-Host "  - Restored missing <footer tag."
    }

    # Fix Missing Departure Label
    $depGroupNoLabel = '(?s)(<div class="form-group">)\s*(<select[^>]*id="departure")'
    if ($content -match $depGroupNoLabel) {
        $depLabel = '<label class="form-label" for="departure">Departure Airport</label>'
        $content = $content -replace $depGroupNoLabel, ("$1`n                                $depLabel`n                                $2")
        Write-Host "  - Restored missing Departure Label."
    }

    # --- PHASE 2: MOBILE OPTIMIZATION ---
    # Injected fluid font sizes and tight mobile padding
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
    if ($content -match "@media \(max-width: 768px\) \{.*?padding: 4rem 0;.*?\}") {
         $content = $content -replace "@media \(max-width: 768px\) \{.*?padding: 4rem 0;.*?\}", $mobileCss
    }

    # --- PHASE 3: INTERLINKING ---
    $sectionHeader = "<!-- CONTEXTUAL INTERLINKING SECTION -->"
    if ($content -match [regex]::Escape($sectionHeader)) {
        # Update existing section safely
        $pattern = "(?s)$([regex]::Escape($sectionHeader)).*?(?=<footer)"
        $content = $content -replace $pattern, ("$sectionHeader`n$gridHtml`n")
    }

    # Save source file updates
    Set-Content $file.FullName $content -NoNewline
    
    # --- PHASE 4: REVERSE ROUTE GENERATION ---
    if ($file.Name -match "route(.+)to(.+)\.html") {
        $from = $Matches[1]; $to = $Matches[2]
        $reverseName = "route$($to)to$($from).html"
        
        Write-Host "  - Generating/Refreshing: $reverseName"
        $rev = $content
        
        # --- Robust String Swaps ---
        $fromPretty = $from.Substring(0,1).ToUpper() + $from.Substring(1)
        $toPretty = $to.Substring(0,1).ToUpper() + $to.Substring(1)
        
        # Case insensitive regex swaps with placeholders
        $rev = $rev -replace "(?i)$fromPretty to $toPretty", "REVSWAP_CAPS"
        $rev = $rev -replace "(?i)$toPretty to $fromPretty", "$fromPretty to $toPretty"
        $rev = $rev.Replace("REVSWAP_CAPS", "$toPretty to $fromPretty")
        
        $rev = $rev -replace "(?i)$from-to-$to", "REVSWAP_SLUG"
        $rev = $rev -replace "(?i)$to-to-$from", "$from-to-$to"
        $rev = $rev.Replace("REVSWAP_SLUG", "$to-to-$from")

        # --- REVERSE FORM OPTIONS (Rock Solid Implementation) ---
        if ($rev -match '(?s)(<select[^>]*id="departure"[^>]*>)(.*?)(</select>)') {
            $depTag = $Matches[1]; $depInner = $Matches[2]
            if ($rev -match '(?s)(<select[^>]*id="arrival"[^>]*>)(.*?)(</select>)') {
                $arrTag = $Matches[1]; $arrInner = $Matches[2]
                
                # We swap ONLY the inner contents
                # 1. Place a unique marker for departure contents
                $rev = $rev.Replace($depInner, "DEP_CONTENT_MARKER")
                # 2. Replace arrival contents with departure contents
                $rev = $rev.Replace($arrInner, $depInner)
                # 3. Replace marker with arrival contents
                $rev = $rev.Replace("DEP_CONTENT_MARKER", $arrInner)
                Write-Host "    - Reversed Form Selections."
            }
        }

        # --- UPDATE SELF-CANONICAL ---
        $canonicalUrl = "https://eliteluxurybookings.com/$($to)-to-$($from)-private-jet-cost/"
        $rev = $rev -replace '<link rel="canonical" href=".*?">', ('<link rel="canonical" href="' + $canonicalUrl + '">')

        Set-Content $reverseName $rev -NoNewline
    }
}

Write-Host "Success: All pages repaired, mobile-optimized, and scaled."
