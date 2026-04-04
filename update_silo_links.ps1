# Elite Luxury Bookings - Silo Link Synchronizer
# This script updates the global silo with the new, premium 'private-jet-cost' URLs.

$siloPath = "global-route-silo.html"
$content = Get-Content $siloPath -Raw

# Regex: href="route([a-z]+)to([a-z]+)\.html" -> href="$1-to-$2-private-jet-cost"
# Note: We remove .html because our .htaccess handles extensionless URLs perfectly.
$newContent = $content -replace 'href="route([a-z]+)to([a-z]+)\.html"', 'href="$1-to-$2-private-jet-cost"'

Set-Content $siloPath $newContent
Write-Host "Global Jet Silo Links Updated to Premium Format."
