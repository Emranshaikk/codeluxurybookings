
# Clean up Yacht and Villa content as per previous instructions
$pathsToRemove = @(
    "luxury-yacht-rentals",
    "luxury-villa-rentals.html",
    "luxury-villas.html",
    "elite-private-jet-charter"
)

foreach ($path in $pathsToRemove) {
    if (Test-Path $path) {
        Write-Host "Removing $path..."
        Remove-Item -Path $path -Recurse -Force
    }
}

# Update Navigation in all HTML files
$htmlFiles = Get-ChildItem -Path . -Filter "*.html" -Recurse

foreach ($file in $htmlFiles) {
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    
    # 1. Update Navigation UL
    $newNav = @"
            <ul class="nav-links">
                <li><a href="/elite-private-jet-charter.html">Private Jets</a></li>
                <li><a href="/blog.html">Blog</a></li>
                <li><a href="/contact.html">Contact</a></li>
            </ul>
"@
    
    if ($content -match '(?s)<ul class="nav-links">.*?</ul>') {
        $content = [regex]::Replace($content, '(?s)<ul class="nav-links">.*?</ul>', $newNav)
    }

    # 2. Update Mobile Menu
    $newMobile = @"
    <div class="mobile-menu" id="elbMobileMenu">
        <a href="/elite-private-jet-charter.html">Private Jets</a>
        <a href="/blog.html">Articles & News</a>
        <a href="/contact.html">Contact Us</a>
        <a href="https://wa.me/918801079030" class="mobile-cta">WhatsApp Concierge</a>
    </div>
"@
    
    if ($content -match '(?s)<div class="mobile-menu" id="elbMobileMenu">.*?</div>') {
        $content = [regex]::Replace($content, '(?s)<div class="mobile-menu" id="elbMobileMenu">.*?</div>', $newMobile)
    }

    # 3. Update Footer
    $newFooterLinks = @"
            <div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; margin-bottom: 2.5rem;">
                <a href="/elite-private-jet-charter.html" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;">Aviation</a>
                <a href="/blog.html" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;">Blog</a>
                <a href="/contact.html" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 0.9rem; letter-spacing: 1.5px; text-transform: uppercase;">Contact</a>
            </div>
"@

    if ($content -match '(?s)<div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; margin-bottom: 2.5rem;">.*?</div>') {
        $content = [regex]::Replace($content, '(?s)<div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap; margin-bottom: 2.5rem;">.*?</div>', $newFooterLinks)
    }

    [System.IO.File]::WriteAllText($file.FullName, $content, (New-Object System.Text.UTF8Encoding $false))
}
