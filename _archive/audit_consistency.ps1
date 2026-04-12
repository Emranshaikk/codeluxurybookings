
$htmlFiles = Get-ChildItem -Path . -Filter "*.html" -Recurse
$report = @()

foreach ($file in $htmlFiles) {
    if ($file.Name -match "audit_") { continue }
    $content = Get-Content $file.FullName -Raw
    
    $hasGA = $content -match "G-J56D1LJLFM"
    $hasLogo = $content -match "Elite Luxury <span class=.nav-gold.>Bookings</span>" -or $content -match "Elite Luxury <span style=.color:#D4AF37;.>Bookings</span>"
    $favicon = "Missing"
    if ($content -match 'href=["''](?:\/)?favicon\.png["'']') { $favicon = "Root" }
    elseif ($content -match 'href=["''](?:\/)?assets\/images\/favicon\.png["'']') { $favicon = "Assets" }

    $report += [PSCustomObject]@{
        Page = $file.Name
        HasGA = $hasGA
        HasBranding = $hasLogo
        Favicon = $favicon
    }
}

$report | Export-Csv -Path "pre_deployment_audit.csv" -NoTypeInformation
$report | Group-Object HasGA, HasBranding, Favicon | Select-Object Name, Count | Write-Host
