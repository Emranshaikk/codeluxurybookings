$files = Get-ChildItem "route*.html" | Select-Object -ExpandProperty Name

$authorityTriad = @"
    <!-- MASTER TRIAD: SECTIONS (BOOKINGS + COST BREAKDOWN) -->
    <section class="section-padding">
        <div class="container">
            <div class="seo-content" style="max-width: 900px; margin: 0 auto;">
                <h2 class="serif">Private Jet Bookings: Logistics for Elite Missions</h2>
                <p>Securing elite <strong>private jet bookings</strong> for this corridor requires sophisticated coordination between global aviation authorities and our 24/7 aviation desk. Every manifest is managed with complete discretion, from securing preferred slots at executive airports like Farnborough or Biggin Hill to providing discreet chauffeur transfers at your destination.</p>
                <p>When you initiate your booking, you gain access to a curated fleet of ARGUS-rated aircraft, ensuring the highest safety protocols for your family or executive ensemble. Whether you require a rapid-response Light Jet or an Ultra-Long-Range Heavy Jet, our procurement team ensures absolute reliability.</p>
                <h3 class="serif" style="margin-top: 2rem;">The Booking Procedure</h3>
                <ul class="luxury-list">
                    <li><strong>Instant Appraisal:</strong> Multi-quote proposals tailored to your passenger payload.</li>
                    <li><strong>Asset Selection:</strong> Choose between Light, Midsize, or Heavy jet configurations.</li>
                    <li><strong>Concierge Sync:</strong> Integrated catering, secure communications, and ground logistics.</li>
                </ul>
            </div>
        </div>
    </section>

    <section class="section-padding" style="background: var(--graphene);">
        <div class="container">
            <div class="seo-content" style="max-width: 900px; margin: 0 auto;">
                <h2 class="serif">Private Jet Flight Cost Breakdown</h2>
                <p>Calculating the precise <strong>private jet flight cost</strong> requires analyzing tactical variables such as positioning fees, fuel surcharges, and international ground handling. We recommend leveraging our proprietary operator network to source fleet repositioning discounts, often reducing the cost for this route by up to 50%.</p>
                <div class="glass-panel" style="padding: 2.5rem; margin: 2rem 0;">
                    <h4 class="gold-text" style="margin-top:0;">Technical Cost Components</h4>
                    <ul style="list-style: none; margin-top: 1rem; line-height: 1.8;">
                        <li>• <strong>VIP Terminal Handling:</strong> Access to exclusive GenAv terminals.</li>
                        <li>• <strong>Tactical Routing:</strong> Automated flight planning for maximum efficiency.</li>
                        <li>• <strong>Empty Leg Alignment:</strong> Strategic cost reduction for flexible departures.</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <div id="footer-silo-target"></div>
"@

foreach ($f in $files) {
    if (Test-Path $f) {
        $content = Get-Content $f -Raw
        
        # 1. Update Title and Description to Master Authority v2
        # Use (?s) to handle multiline tags
        $content = $content -replace '(?s)<title>.*?</title>', "<title>Private Jet cost (Bookings + Flight Cost Breakdown)</title>"
        $content = $content -replace '(?s)<meta name="description".*?>', '<meta name="description" content="Secure the elite private jet cost for this corridor. 2-hour luxury performance from VIP terminals. Ultimate Master Authority bookings.">'
        
        # 2. Inject Authority Triad before the Footer/Internal Linking (only if not already present)
        if ($content -notmatch "MASTER TRIAD: SECTIONS") {
            if ($content -match "<!-- INTERNAL LINKING SECTION -->") {
                $content = $content -replace "<!-- INTERNAL LINKING SECTION -->", ($authorityTriad + "`r`n`r`n    <!-- INTERNAL LINKING SECTION -->")
            } elseif ($content -match "<footer") {
                $content = $content -replace "<footer", ($authorityTriad + "`r`n`r`n    <footer")
            }
            Write-Host "Injected Authority Triad into $f"
        } else {
            Write-Host "Authority Triad already present in $f, updating SEO meta only."
        }
        
        Set-Content $f $content
        Write-Host "Updated $f to Master Authority v2"
    }
}
