# Audit script to check for Formspree lead forms on route pages
$routeFiles = Get-ChildItem -Filter *-private-jet-cost.html
$missingCount = 0

foreach ($file in $routeFiles) {
    if (!(Select-String -Path $file.FullName -Pattern "formspree.io/f/xwvwanlj" -Quiet)) {
        Write-Host "MISSING Formspree in: $($file.Name)"
        $missingCount++
    }
}

if ($missingCount -eq 0) {
    Write-Host "Success: All route pages have the Formspree lead form."
} else {
    Write-Host "Found $missingCount pages missing Formspree."
}
