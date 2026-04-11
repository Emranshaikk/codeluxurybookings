$premiumForm = @'
            <div class="glass-panel" style="padding: 4rem; border: 1px solid var(--glass-border); background: rgba(10, 10, 10, 0.9); border-radius: 30px; box-shadow: 0 50px 120px rgba(0,0,0,0.9); margin: 3rem auto; max-width: 900px; backdrop-filter: blur(30px);">
                <div style="text-align: center; margin-bottom: 4rem;">
                    <h2 class="serif gold-text" style="font-size: 3.5rem; margin-bottom: 1rem; font-weight: 300;">Request Private Proposal</h2>
                    <p style="color: var(--text-muted); font-size: 1rem; text-transform: uppercase; letter-spacing: 4px; margin-bottom: 2rem;">Discreet & Confidential Aviation Dispatch</p>
                    <div style="width: 80px; height: 1px; background: var(--primary-gold); margin: 0 auto; opacity: 0.4;"></div>
                </div>

                <form action="https://formspree.io/f/xwvwanlj" method="POST" style="display: flex; flex-direction: column; gap: 2.5rem;">
                    <input type="hidden" name="_target" value="Inquiry: [[SOURCE_NAME]]">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem;" class="form-grid">
                        <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                            <label style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-gold);">Full Name *</label>
                            <input type="text" name="name" required placeholder="John Doe" style="background: transparent; border: none; border-bottom: 1px solid rgba(255,255,255,0.15); padding: 1.2rem 0; color: #fff; font-size: 1.15rem; outline: none; transition: border-color 0.4s; font-family: 'Inter', sans-serif;">
                        </div>
                        <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                            <label style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-gold);">WhatsApp / Phone *</label>
                            <input type="tel" name="phone" required placeholder="+1 234 567 8900" style="background: transparent; border: none; border-bottom: 1px solid rgba(255,255,255,0.15); padding: 1.2rem 0; color: #fff; font-size: 1.15rem; outline: none; transition: border-color 0.4s; font-family: 'Inter', sans-serif;">
                        </div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                        <label style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-gold);">Private Email *</label>
                        <input type="email" name="email" required placeholder="client@exclusive.com" style="background: transparent; border: none; border-bottom: 1px solid rgba(255,255,255,0.15); padding: 1.2rem 0; color: #fff; font-size: 1.15rem; outline: none; transition: border-color 0.4s; font-family: 'Inter', sans-serif;">
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem;" class="form-grid">
                        <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                            <label style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-gold);">Departure City *</label>
                            <input type="text" name="departure" required placeholder="Origin City" style="background: transparent; border: none; border-bottom: 1px solid rgba(255,255,255,0.15); padding: 1.2rem 0; color: #fff; font-size: 1.15rem; outline: none; transition: border-color 0.4s; font-family: 'Inter', sans-serif;">
                        </div>
                        <div style="display: flex; flex-direction: column; gap: 0.8rem;">
                            <label style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-gold);">Destination City *</label>
                            <input type="text" name="destination" required placeholder="Arrival City" style="background: transparent; border: none; border-bottom: 1px solid rgba(255,255,255,0.15); padding: 1.2rem 0; color: #fff; font-size: 1.15rem; outline: none; transition: border-color 0.4s; font-family: 'Inter', sans-serif;">
                        </div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 1rem;">
                        <label style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; color: var(--primary-gold);">Aviation & Mission Requirements</label>
                        <textarea name="requirements" rows="3" placeholder="Flight date, passenger count, or aircraft preference..." style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 1.5rem; color: #fff; font-size: 1.1rem; outline: none; border-radius: 12px; resize: none; transition: all 0.4s; font-family: 'Inter', sans-serif;"></textarea>
                    </div>
                    <div style="text-align: center; margin-top: 1rem;">
                        <button type="submit" class="btn btn-gold" style="width: 100%; padding: 1.8rem; font-size: 1.25rem; border-radius: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 5px; border: none; cursor: pointer; transition: all 0.4s; background: linear-gradient(135deg, #D4AF37, #B8860B); color: #000 !important;">Secure Private Proposal</button>
                        <p style="margin-top: 2rem; color: var(--text-muted); font-size: 0.85rem; letter-spacing: 2px; opacity: 0.7;">A dedicated concierge will respond personally within 30 minutes.</p>
                    </div>
                </form>
            </div>
'@

Get-ChildItem -Path "$PSScriptRoot" -Filter *.html | ForEach-Object {
    if ($_.Name -eq 'index.html') { return }
    $content = Get-Content $_.FullName -Raw
    
    # BRUTE FORCE MATCH: Target the UNIQUE ID of the broken form
    # It has padding: 3rem and the text 'Global Charter Inquiry'
    $formPattern = '(?s)<div class="glass-panel" style="padding: 3rem;.*?Global Charter Inquiry.*?</form>\s*</div>'
    $source = $_.BaseName -replace '-private-jet-cost', ''
    $finalForm = $premiumForm.Replace('[[SOURCE_NAME]]', $source)
    
    if ($content -match $formPattern) {
        $content = [regex]::Replace($content, $formPattern, $finalForm)
        Write-Host "FIXED FORM: $($_.Name)"
    }

    # PURGE Green and Enforce Brand Gold
    $content = $content.Replace('background: linear-gradient(135deg, #25D366, #128C7E)', 'background: linear-gradient(135deg, #D4AF37, #B8860B)')
    $content = $content.Replace('color: #25D366', 'color: #D4AF37')
    
    Set-Content $_.FullName $content
}
