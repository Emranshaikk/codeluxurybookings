# Elite Luxury Bookings - Yacht Silo Link Synchronizer
# This script ensures yacht links are consistent with the premium, extension-less URL pattern.

$siloPath = "global-yacht-silo.html"
$content = Get-Content $siloPath -Raw

# Replace "/slug/" with "slug" (removing both slashes for clean internal links)
$newContent = $content -replace 'href="/([^/]+)/"', 'href="$1"'

Set-Content $siloPath $newContent
Write-Host "Global Yacht Silo Links Synchronized."
