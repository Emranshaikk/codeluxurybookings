# Elite Luxury Bookings - Silo Link Synchronizer (Trailing Slash Version)
# This script updates the global silo with the new, premium 'private-jet-cost/' URLs.

$siloPath = "global-route-silo/index.html"
if (Test-Path $siloPath) {
    $content = Get-Content $siloPath -Raw
    # Regex: href="route([a-z]+)to([a-z]+)\.html" -> href="/$1-to-$2-private-jet-cost/"
    $newContent = $content -replace 'href="route([a-z]+)to([a-z]+)\.html"', 'href="/$1-to-$2-private-jet-cost/"'
    Set-Content $siloPath $newContent
    Write-Host "Global Jet Silo Links Updated in: $siloPath"
} else {
    Write-Warning "Silo not found: $siloPath"
}
