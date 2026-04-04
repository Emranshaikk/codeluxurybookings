$template = Get-Content "_template_master.html" -Raw
$grid = Get-Content "global-route-silo.html" -Raw

# 1. ICAO/Option Lookup for Core Cities (Ensuring Quality)
$icaoLookup = @{
    "london" = '<option value="EGLF" selected>London Farnborough (EGLF)</option><option value="EGKB">London Biggin Hill (EGKB)</option><option value="EGGW">London Luton (EGGW)</option><option value="EGSS">London Stansted (EGSS)</option>';
    "ibiza" = '<option value="LEIB" selected>Ibiza Airport (LEIB)</option>';
    "paris" = '<option value="LFPB" selected>Paris Le Bourget (LFPB)</option>';
    "nice" = '<option value="LFMN" selected>Nice Côte d''Azur (LFMN)</option>';
    "miami" = '<option value="KOPF" selected>Miami Opa-Locka (KOPF)</option><option value="KFXE">Fort Lauderdale Exec (KFXE)</option>';
    "newyork" = '<option value="KTEB" selected>Teterboro (KTEB)</option><option value="KHPN">Westchester County (KHPN)</option>';
    "nyc" = '<option value="KTEB" selected>Teterboro (KTEB)</option>';
    "dubai" = '<option value="OMDB" selected>Dubai International (OMDB)</option><option value="OMDW">Al Maktoum (OMDW)</option>';
    "geneva" = '<option value="LSGG" selected>Geneva Cointrin (LSGG)</option>';
    "milan" = '<option value="LIML" selected>Milan Linate (LIML)</option>';
    "monaco" = '<option value="LNMC" selected>Monaco Heliport (LNMC)</option>';
    "barcelona" = '<option value="LEBL" selected>Barcelona El Prat (LEBL)</option>';
    "madrid" = '<option value="LEMD" selected>Madrid Barajas (LEMD)</option>';
    "malta" = '<option value="LMML" selected>Malta International (LMML)</option>';
    "mykonos" = '<option value="LGMK" selected>Mykonos Airport (LGMK)</option>';
    "santorini" = '<option value="LGSR" selected>Santorini Airport (LGSR)</option>';
    "marrakesh" = '<option value="GMMX" selected>Marrakesh Menara (GMMX)</option>';
    "palma" = '<option value="LEPA" selected>Palma de Mallorca (LEPA)</option>';
}

$files = Get-ChildItem route*to*.html | Where-Object { $_.Name -ne "_template_master.html" -and $_.Name -ne "global-route-silo.html" }

foreach ($file in $files) {
    if ($file.Name -match "route(.+)to(.+)\.html") {
        $from = $Matches[1]; $to = $Matches[2]
        Write-Host "Migrating $($file.Name)..."
        
        $fromP = $from.Substring(0,1).ToUpper() + $from.Substring(1)
        $toP = $to.Substring(0,1).ToUpper() + $to.Substring(1)
        
        # Hydrate Template
        $newContent = $template
        $newContent = $newContent.Replace("{{FROM_P}}", $fromP)
        $newContent = $newContent.Replace("{{TO_P}}", $toP)
        $newContent = $newContent.Replace("{{FROM_L}}", $from)
        $newContent = $newContent.Replace("{{TO_L}}", $to)
        $newContent = $newContent.Replace("{{FOOTER_SILO}}", $grid)
        
        # Handle Options
        $depOps = if ($icaoLookup.ContainsKey($from)) { $icaoLookup[$from] } else { "<option value='LOCAL' selected>$fromP Executive Terminal</option>" }
        $arrOps = if ($icaoLookup.ContainsKey($to)) { $icaoLookup[$to] } else { "<option value='LOCAL' selected>$toP Executive Terminal</option>" }
        
        $newContent = $newContent.Replace("{{DEPARTURE_OPTIONS}}", $depOps)
        $newContent = $newContent.Replace("{{ARRIVAL_OPTIONS}}", $arrOps)
        
        Set-Content $file.FullName $newContent -NoNewline
    }
}
Write-Host "Migration Complete. All files are now synchronized with the Master Template."
