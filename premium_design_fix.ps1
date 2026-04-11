# Elite Luxury Bookings - PIXEL-PERFECT STANDARDIZATION
# This script uses the PRECISE premium form design from the homepage

$premiumFormTemplate = @"
    <div class="glass-panel" style="padding: 4rem; border: 1px solid var(--glass-border); background: rgba(20, 20, 20, 0.8); border-radius: 30px; box-shadow: 0 50px 120px rgba(0,0,0,0.9); margin: 4rem auto; max-width: 900px; backdrop-filter: blur(30px);">
        <div style="text-align: center; margin-bottom: 4rem;">
            <h2 class="serif gold-text" style="font-size: 3.5rem; margin-bottom: 1rem; font-weight: 300;">Request Private Proposal</h2>
            <p style="color: var(--text-muted); font-size: 1rem; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 1rem;">Discreet & Confidential Aviation Service</p>
            <div style="width: 60px; height: 2px; background: var(--primary-gold); margin: 0 auto; opacity: 0.6;"></div>
        </div>

        <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: flex; flex-direction: column; gap: 2.5rem;">
            <input type="hidden" name="_target" value="[[SOURCE_NAME]]">
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem;" class="form-grid">
                <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                    <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-gold);">Full Name *</label>
                    <input type="text" name="name" required placeholder="John Doe" style="background: transparent; border: none; border-bottom: 1px solid rgba(255,255,255,0.2); padding: 1rem 0; color: #fff; font-size: 1.1rem; outline: none; transition: border-color 0.4s;">
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                    <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-gold);">WhatsApp / Phone *</label>
                    <input type="tel" name="phone" required placeholder="+1 234 567 8900" style="background: transparent; border: none; border-bottom: 1px solid rgba(255,255,255,0.2); padding: 1rem 0; color: #fff; font-size: 1.1rem; outline: none; transition: border-color 0.4s;">
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-gold);">Private Email *</label>
                <input type="email" name="email" required placeholder="client@exclusive.com" style="background: transparent; border: none; border-bottom: 1px solid rgba(255,255,255,0.2); padding: 1rem 0; color: #fff; font-size: 1.1rem; outline: none; transition: border-color 0.4s;">
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem;" class="form-grid">
                <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                    <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-gold);">Departure City *</label>
                    <input type="text" name="departure" required placeholder="e.g. Dubai, DXB" style="background: transparent; border: none; border-bottom: 1px solid rgba(255,255,255,0.2); padding: 1rem 0; color: #fff; font-size: 1.1rem; outline: none; transition: border-color 0.4s;">
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                    <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-gold);">Destination City *</label>
                    <input type="text" name="destination" required placeholder="e.g. London, LHR" style="background: transparent; border: none; border-bottom: 1px solid rgba(255,255,255,0.2); padding: 1rem 0; color: #fff; font-size: 1.1rem; outline: none; transition: border-color 0.4s;">
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                <label style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-gold);">Aviation & Mission Requirements</label>
                <textarea name="requirements" rows="4" placeholder="Flight date, passenger count, aircraft preference..." style="background: transparent; border: 1px solid rgba(255,255,255,0.1); padding: 1.5rem; color: #fff; font-size: 1.1rem; outline: none; border-radius: 12px; resize: none; transition: border-color 0.4s;"></textarea>
            </div>

            <div style="text-align: center; margin-top: 1rem;">
                <button type="submit" class="btn btn-gold" style="width: 100%; padding: 1.8rem; font-size: 1.2rem; border-radius: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 5px; border: none; cursor: pointer; transition: all 0.4s;">
                    Secure Private Proposal
                </button>
                <p style="margin-top: 1.5rem; color: var(--text-muted); font-size: 0.8rem; letter-spacing: 1.5px; opacity: 0.6;">A dedicated concierge will respond personally within 30 minutes.</p>
            </div>
        </form>
    </div>
"@

$htmlFiles = Get-ChildItem -Filter *.html

foreach ($file in $htmlFiles) {
    if ($file.Name -eq "index.html") { continue }
    
    Write-Host "Re-Standardizing $($file.Name)..."
    $content = Get-Content $file.FullName -Raw

    # 1. Standardize Lead Engine with PREMIUM style
    $sourceName = $file.BaseName -replace '-private-jet-cost', '' -replace '-', ' '
    $routeLeadForm = $premiumFormTemplate -replace '\[\[SOURCE_NAME\]\]', "Inquiry: $sourceName"

    # Replace any previous lead form wrapper or Valens placeholder
    if ($content -match '(?s)<div class="glass-panel" style="padding: 3.5rem;.*?</div>\s*</form>\s*</div>') {
         $oldFormPattern = '(?s)<div class="glass-panel" style="padding: 3.5rem;.*?</div>\s*</form>\s*</div>'
         $content = [regex]::Replace($content, $oldFormPattern, $routeLeadForm)
    } elseif ($content -match '(?s)<!-- ELB_VALENS_WIDGET_START -->.*?<!-- ELB_VALENS_WIDGET_END -->') {
         $valensPattern = '(?s)<!-- ELB_VALENS_WIDGET_START -->.*?<!-- ELB_VALENS_WIDGET_END -->'
         $content = [regex]::Replace($content, $valensPattern, $routeLeadForm)
    }

    # 2. Add dynamic CSS fix for form-grid responsive behavior if not exists
    if ($content -notmatch 'form-grid \{') {
        $responsiveFix = "@media (max-width: 768px) { .form-grid { grid-template-columns: 1fr !important; gap: 2rem !important; } }"
        $content = $content.Replace("</style>", "$responsiveFix`n    </style>")
    }

    Set-Content $file.FullName $content
}

Write-Host "Premium Design Lock: DEPLOYED."
