Get-ChildItem -Path "$PSScriptRoot" -Filter *.html | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # 1. Clean up the Desktop Nav (Jets -> Yachts -> Villas -> Blog -> Contact)
    $cleanDesktop = '<ul class="nav-links">
                <li><a href="/elite-private-jet-charter.html">Private Jets</a></li>
                <li><a href="/luxury-yacht-rentals.html">Yachts</a></li>
                <li><a href="/luxury-villa-rentals.html">Villas</a></li>
                <li><a href="/blog.html">Blog</a></li>
                <li><a href="/contact.html">Contact</a></li>'
    
    # Regex to catch any variant of the list before the links end
    $content = $content -replace '(?s)<ul class="nav-links">.*?<li><a href="/blog.html"', $cleanDesktop

    # 2. Clean up Footer (Jets -> Yachts -> Villas -> Blog)
    $cleanFooterList = '<ul style="list-style:none; display:flex; flex-direction:column; gap:1rem; padding:0; margin:0;">
                        <li><a href="/elite-private-jet-charter.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Private Jets</a></li>
                        <li><a href="/luxury-yacht-rentals.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Luxury Yachts</a></li>
                        <li><a href="/luxury-villa-rentals.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Luxury Villas</a></li>
                        <li><a href="/blog.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Blog</a></li>'

    $content = $content -replace '(?s)<ul style="list-style:none; display:flex; flex-direction:column; gap:1rem; padding:0; margin:0;">.*?<li><a href="/blog.html"', $cleanFooterList

    Set-Content $_.FullName $content
}
