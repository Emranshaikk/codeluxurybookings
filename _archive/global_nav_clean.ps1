
$newNavUl = @"
            <ul class="nav-links">
                <li><a href="/elite-private-jet-charter.html">Private Jets</a></li>
                <li><a href="/luxury-yacht-rentals/">Yacht Charter</a></li>
                <li><a href="/luxury-villa-rentals.html">Villas</a></li>
                <li><a href="/blog.html">Blog</a></li>
                <li><a href="/contact.html">Contact</a></li>
            </ul>
"@

$htmlFiles = Get-ChildItem -Path . -Filter "*.html"

foreach ($file in $htmlFiles) {
    # Skip index.html as per user locking request
    if ($file.Name -eq "index.html") { 
        Write-Host "Skipping locked home page: $($file.Name)"
        continue 
    }

    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    
    # 1. Replace the entire nav-links UL block
    if ($content -match '(?s)<ul class="nav-links">.*?</ul>') {
        $content = [regex]::Replace($content, '(?s)<ul class="nav-links">.*?</ul>', $newNavUl)
        
        # 2. Cleanup associated CSS if it exists in ELB_STYLE blocks
        # Specifically targeting dropdown related styles that are no longer needed
        $content = $content -replace '(?s)\.nav-dropdown\s*\{.*?\}', ''
        $content = $content -replace '(?s)\.dropdown-menu\s*\{.*?\}', ''
        $content = $content -replace '(?s)\.nav-dropdown:hover.*?\}', ''
        $content = $content -replace '(?s)\.dropdown-menu a\s*\{.*?\}', ''
        
        [System.IO.File]::WriteAllText($file.FullName, $content, (New-Object System.Text.UTF8Encoding $false))
        Write-Host "Cleaned navigation and CSS in $($file.Name)"
    }
}
