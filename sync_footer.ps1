Get-ChildItem -Path "$PSScriptRoot" -Filter *.html | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # Define the Master Elite Footer
    $masterFooter = '    <footer style="background:#000; border-top:1px solid rgba(255,255,255,0.05); padding:6rem 0;">
        <div class="container">
            <div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:flex-start; gap:4rem; padding-bottom:3rem; border-bottom:1px solid rgba(212,175,55,0.1); text-align:left;">
                <div style="flex:1; min-width:280px; margin-bottom:2rem;">
                    <div style="font-family:''Cormorant Garamond'',serif; font-size:2.2rem; color:#fff; margin-bottom:1rem; line-height:1.2;">Elite Luxury <span style="color:#D4AF37;">Bookings</span></div>
                    <p style="color:rgba(255,255,255,0.5); font-size:0.95rem; line-height:1.8; max-width:300px;">Curating world-class luxury experiences through our global partner network. Private Jets. Yachts. Villas.</p>
                </div>
                <div style="min-width:160px; margin-bottom:2rem;">
                    <div style="font-size:0.8rem; text-transform:uppercase; letter-spacing:2.5px; color:#D4AF37; margin-bottom:1.5rem; font-weight:700;">Services</div>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:1rem; padding:0; margin:0;">
                        <li><a href="/elite-private-jet-charter.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Private Jets</a></li>
                        <li><a href="/luxury-villa-rentals.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Luxury Villas</a></li>
                        <li><a href="/blog.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Blog</a></li>
                    </ul>
                </div>
                <div style="min-width:140px; margin-bottom:2rem;">
                    <div style="font-size:0.8rem; text-transform:uppercase; letter-spacing:2.5px; color:#D4AF37; margin-bottom:1.5rem; font-weight:700;">Company</div>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:1rem; padding:0; margin:0;">
                        <li><a href="/contact.html" style="color:rgba(255,255,255,0.6); text-decoration:none; font-size:0.9rem; transition:color 0.3s;" onmouseover="this.style.color=''#D4AF37''" onmouseout="this.style.color=''rgba(255,255,255,0.6)''">Contact Us</a></li>
                    </ul>
                </div>
            </div>
            <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; padding-top:3rem; gap:1.5rem;">
                <p style="color:rgba(255,255,255,0.35); font-size:0.85rem; letter-spacing:0.5px;">&copy; 2026 Elite Luxury Bookings. All rights reserved. Global Concierge Service.</p>
            </div>
        </div>
    </footer>'

    # Regex to surgically replace the entire footer block
    $content = $content -replace '(?s)<footer.*?>.*?</footer>', $masterFooter

    Set-Content $_.FullName $content
}
