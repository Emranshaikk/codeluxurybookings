Get-ChildItem -Path "$PSScriptRoot" -Filter *.html | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # Define the absolute target blocks for Header and Footer
    $perfectHeaderNav = '<ul class="nav-links">
                <li><a href="/elite-private-jet-charter.html">Private Jets</a></li>
                <li><a href="/luxury-yacht-rentals.html">Yachts</a></li>
                <li><a href="/luxury-villa-rentals.html">Villas</a></li>
                <li><a href="/blog.html">Blog</a></li>
                <li><a href="/contact.html">Contact</a></li>
            </ul>'

    $perfectFooterNav = '<ul style="list-style:none; display:flex; flex-direction:column; gap:1rem; padding:0; margin:0;">
                        <li><a href="/elite-private-jet-charter.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Private Jets</a></li>
                        <li><a href="/luxury-yacht-rentals.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Luxury Yachts</a></li>
                        <li><a href="/luxury-villa-rentals.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Luxury Villas</a></li>
                        <li><a href="/blog.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Blog</a></li>
                    </ul>'

    # Regex to surgically swap the entire UL blocks
    $content = $content -replace '(?s)<ul class="nav-links">.*?</ul>', $perfectHeaderNav
    $content = $content -replace '(?s)<ul style="list-style:none; display:flex; flex-direction:column; gap:1rem; padding:0; margin:0;">.*?</ul>', $perfectFooterNav

    Set-Content $_.FullName $content
}
