$gridHtml = Get-Content "global-route-silo.html" -Raw

# Get all route files
$files = Get-ChildItem route*.html | Where-Object { $_.Name -ne "global-route-silo.html" }

foreach ($file in $files) {
    Write-Host "Processing $($file.Name)..."
    
    # 1. Update/Inject Interlinking Grid
    $content = Get-Content $file.FullName -Raw
    $originalLength = $content.Length
    
    # Mobile Optimization Injection (Ensuring responsive design tokens)
    # We'll update the style block to be more mobile-friendly
    $mobileCss = '
        @media (max-width: 768px) {
            .section-padding { padding: 3rem 0; }
            .hero h1 { font-size: clamp(2rem, 8vw, 3.5rem); line-height: 1.2; }
            .hero-sub { font-size: 1.1rem; padding: 0 1rem; }
            .form-wrapper { padding: 1.5rem !important; border-radius: 15px; }
            .container { padding: 0 1.25rem; }
            .grid-2 { gap: 2rem; }
            .benefit-card { padding: 1.5rem; }
        }
    '
    
    # Inject mobile CSS if not present
    if ($content -notmatch [regex]::Escape(".hero h1 { font-size: clamp")) {
         $content = $content -replace "(@media \(max-width: 768px\) \{.*?padding: 4rem 0;.*?\})", $mobileCss
    }

    # Interlinking Injection
    $sectionHeader = "<!-- CONTEXTUAL INTERLINKING SECTION -->"
    $footerTag = "<footer"
    
    if ($content -notmatch [regex]::Escape($sectionHeader)) {
        if ($content -match $footerTag) {
            $content = $content -replace "$footerTag", "$sectionHeader`n$gridHtml`n$footerTag"
        }
    } else {
        # Replace existing section
        $content = $content -replace "(?s)$([regex]::Escape($sectionHeader)).*?(?=$footerTag)", "$sectionHeader`n$gridHtml`n"
    }

    if ($originalLength -ne $content.Length) {
        Set-Content $file.FullName $content -NoNewline
    }
    
    # 2. Logic to Generate/Refresh Reverse Route
    if ($file.Name -match "route(.+)to(.+)\.html") {
        $from = $Matches[1]
        $to = $Matches[2]
        $reverseName = "route$($to)to$($from).html"
        
        Write-Host "Refreshing Reverse Route: $reverseName"
        $rev = $content # Start with the updated source content
        
        # --- Pre-calculate Pretty Names ---
        $fromPretty = $from.Substring(0,1).ToUpper() + $from.Substring(1)
        $toPretty = $to.Substring(0,1).ToUpper() + $to.Substring(1)
        
        # --- COMPREHENSIVE TEXT SWAPS (Robust Placeholder Logic) ---
        # Caps
        $rev = $rev -replace "$fromPretty to $toPretty", "TEMPSWAP_CAPS"
        $rev = $rev -replace "$toPretty to $fromPretty", "$fromPretty to $toPretty"
        $rev = $rev -replace "TEMPSWAP_CAPS", "$toPretty to $fromPretty"
        # Lower
        $rev = $rev -replace "$from to $to", "TEMPSWAP_LOWER"
        $rev = $rev -replace "$to to $from", "$from to $to"
        $rev = $rev -replace "TEMPSWAP_LOWER", "$to to $from"
        # Slug
        $rev = $rev -replace "$from-to-$to", "TEMPSWAP_SLUG"
        $rev = $rev -replace "$to-to-$from", "$from-to-$to"
        $rev = $rev -replace "TEMPSWAP_SLUG", "$to-to-$from"
        
        # --- FORM SELECT SWAP (Safest Method) ---
        if ($rev -match '(?s)(<select[^>]*id="departure"[^>]*>)(.*?)(</select>)') {
            $depFull = $Matches[0]; $depInner = $Matches[2];
            if ($rev -match '(?s)(<select[^>]*id="arrival"[^>]*>)(.*?)(</select>)') {
                $arrFull = $Matches[0]; $arrInner = $Matches[2];
                
                # Replace WITHOUT destroying the structure
                $rev = $rev.Replace($depFull, "DEPOPT_PLACEHOLDER")
                $rev = $rev.Replace($arrFull, $arrFull -replace [regex]::Escape($arrInner), $depInner.Replace('$', '$$'))
                $rev = $rev.Replace("DEPOPT_PLACEHOLDER", $depFull -replace [regex]::Escape($depInner), $arrInner.Replace('$', '$$'))
            }
        }

        # --- SEO AUDIT: Canonical Clean Up ---
        # Ensure only one canonical exists and points to self
        $rev = $rev -replace '<link rel="canonical" href=".*?">', ('<link rel="canonical" href="https://eliteluxurybookings.com/' + $reverseName.Replace('.html', '') + '/">')

        Set-Content $reverseName $rev -NoNewline
        Write-Host "  - Success: Refreshed $reverseName with Mobile SEO."
    }
}

Write-Host "Scaling, Repair, and Mobile Optimization Complete."
