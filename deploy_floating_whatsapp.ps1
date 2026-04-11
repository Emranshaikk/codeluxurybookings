$files = Get-ChildItem -Path . -Filter *.html
foreach ($file in $files) {
    Write-Host "Applying Floating Gold WhatsApp to $($file.Name)..."
    $content = Get-Content $file.FullName -Raw
    
    # 1. Remove the nav button (matches either 'Direct Concierge' or the SVG variant I just added)
    $content = $content -replace '<a href="https://wa.me/918801079030" class="btn btn-gold btn-sm" style="display: flex; align-items: center; gap: 8px;">\s*<svg.*?>\s*<path.*?>\s*</svg>\s*<span>WhatsApp</span>\s*</a>', ''
    $content = $content -replace '<a href="https://wa.me/918801079030" class="btn btn-gold btn-sm">Direct Concierge</a>', ''

    # 2. Add Floating Button CSS to the head
    $floatStyles = "`n        /* Floating WhatsApp Button */
        .wa-float {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 54px;
            height: 54px;
            background: linear-gradient(135deg, #D4AF37, #B8860B);
            color: #000 !important;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 0 5px rgba(212, 175, 55, 0.1);
            z-index: 999999;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            text-decoration: none !important;
        }
        .wa-float:hover {
            transform: scale(1.1) rotate(5deg);
            box-shadow: 0 15px 40px rgba(212, 175, 55, 0.4);
        }
        @media (max-width: 768px) {
            .wa-float { bottom: 20px; right: 20px; width: 48px; height: 48px; }
        }"
    
    if ($content -notmatch 'wa-float') {
        $content = $content -replace '(#D4AF37;)\s*\}', "$1 }$floatStyles"
    }

    # 3. Add Floating Button HTML before </body>
    $floatHtml = '<!-- FLOATING WHATSAPP -->
    <a href="https://wa.me/918801079030" class="wa-float" target="_blank" aria-label="WhatsApp">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 16 16">
            <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z" />
        </svg>
    </a>'
    
    if ($content -notmatch 'wa-float') {
        $content = $content -replace '</body>', "$floatHtml`n</body>"
    }

    Set-Content $file.FullName $content -NoNewline
}
Write-Host "Floating Gold WhatsApp successfully deployed site-wide."
