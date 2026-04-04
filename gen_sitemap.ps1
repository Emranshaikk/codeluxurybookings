# Elite Luxury Bookings - Master Dynamic Sitemap Generator
# This script crawls your folder architecture to ensure 100% SEO coverage.

$domain = "https://eliteluxurybookings.com"
$sitemapXml = '<?xml version="1.0" encoding="UTF-8"?>' + "`n"
$sitemapXml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "`n"

# 1. Add Homepage
$sitemapXml += "  <url>`n"
$sitemapXml += "    <loc>$domain/</loc>`n"
$sitemapXml += "    <changefreq>daily</changefreq>`n"
$sitemapXml += "    <priority>1.0</priority>`n"
$sitemapXml += "  </url>`n"

# 2. Add all Content Folders (Excluding system and hidden)
$dirs = Get-ChildItem -Directory | Where-Object { 
    $_.Name -notmatch '^\.|^_|^global' -and 
    (Test-Path "$($_.FullName)/index.html") 
}

foreach ($dir in $dirs) {
    $slug = $dir.Name
    $sitemapXml += "  <url>`n"
    $sitemapXml += "    <loc>$domain/$slug/</loc>`n"
    $sitemapXml += "    <changefreq>weekly</changefreq>`n"
    $sitemapXml += "    <priority>0.8</priority>`n"
    $sitemapXml += "  </url>`n"
}

$sitemapXml += "</urlset>"

# Save as the standard sitemap.xml
Set-Content "sitemap.xml" $sitemapXml -Encoding UTF8
Write-Host "Success: Master Dynamic Sitemap Generated (Standard: sitemap.xml)"
