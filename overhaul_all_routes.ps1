
$files = Get-ChildItem "*-private-jet-cost.html" | Where-Object { 
    $_.Name -notmatch "abudhabi-to-doha|doha-to-abudhabi|beijing-to-seoul|seoul-to-beijing" 
}

# Common City Data Map (Extension Point)
$cityData = @{
    "abudhabi" = @{ name = "Abu Dhabi"; type = "Executive Hub"; airports = "Bateen Executive (AZI)" }
    "doha" = @{ name = "Doha"; type = "Strategic/Business"; airports = "Doha International (OTBD)" }
    "beijing" = @{ name = "Beijing"; type = "Sovereign/Diplomatic"; airports = "Capital (PEK)" }
    "seoul" = @{ name = "Seoul"; type = "High-Tech/Financial"; airports = "Gimpo (GMP)" }
    "london" = @{ name = "London"; type = "Global Financial"; airports = "Farnborough (FAB), Biggin Hill (BQH)" }
    "newyork" = @{ name = "New York"; type = "Global Power"; airports = "Teterboro (TEB), White Plains (HPN)" }
    "miami" = @{ name = "Miami"; type = "Elite Leisure"; airports = "Opa-locka (OPF)" }
    "aspen" = @{ name = "Aspen"; type = "Luxury Alpine"; airports = "Pitkin County (ASE)" }
    "bahamas" = @{ name = "Bahamas"; type = "Island Sanctuary"; airports = "Nassau Lynden Pindling (NAS)" }
    "bali" = @{ name = "Bali"; type = "Exclusive Resort"; airports = "Ngurah Rai (DPS)" }
    "melbourne" = @{ name = "Melbourne"; type = "Financial/Cultural"; airports = "Tullamarine (MEL), Essendon (MEB)" }
    "perth" = @{ name = "Perth"; type = "Industrial/Luxe"; airports = "Perth International (PER)" }
    "sydney" = @{ name = "Sydney"; type = "Harbor City"; airports = "Kingsford Smith (SYD)" }
    "brisbane" = @{ name = "Brisbane"; type = "Gateway"; airports = "Brisbane (BNE)" }
    "amsterdam" = @{ name = "Amsterdam"; type = "Trade/Design"; airports = "Schiphol (AMS)" }
    "barcelona" = @{ name = "Barcelona"; type = "Mediterranean Hub"; airports = "El Prat (BCN)" }
    "cabo" = @{ name = "Cabo San Lucas"; type = "Beach Elite"; airports = "Cabo San Lucas (CSL)" }
    "losangeles" = @{ name = "Los Angeles"; type = "Entertainment/Wealth"; airports = "Van Nuys (VNY)" }
    "cancun" = @{ name = "Cancun"; type = "Riviera Maya"; airports = "Cancun (CUN)" }
    "dallas" = @{ name = "Dallas"; type = "Energy/Commerce"; airports = "Love Field (DAL)" }
    "chicago" = @{ name = "Chicago"; type = "Industrial Force"; airports = "Midway (MDW)" }
}

function Get-CityName($slug) {
    if ($cityData.ContainsKey($slug)) { return $cityData[$slug].name }
    return $slug.psbase.ToString().ToUpper()[0] + $slug.psbase.ToString().Substring(1)
}

function Get-CityType($slug) {
    if ($cityData.ContainsKey($slug)) { return $cityData[$slug].type }
    return "Premium Destination"
}

function Get-Airports($slug) {
    if ($cityData.ContainsKey($slug)) { return $cityData[$slug].airports }
    return "$slug Private Terminal"
}

foreach ($file in $files) {
    $name = $file.BaseName
    $parts = $name -split "-to-"
    if ($parts.Count -lt 2) { continue }
    
    $cityA_slug = $parts[0]
    $cityB_slug = $parts[1] -replace "-private-jet-cost", ""
    
    $cityA = Get-CityName $cityA_slug
    $cityB = Get-CityName $cityB_slug
    $cityAType = Get-CityType $cityA_slug
    $cityBType = Get-CityType $cityB_slug
    $airportsA = Get-Airports $cityA_slug
    $airportsB = Get-Airports $cityB_slug

    $template = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-J56D1LJLFM"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-J56D1LJLFM');</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Private Jet $cityA to $cityB Cost | Book & Charter Instantly</title>
    <meta name="description" content="Secure your private jet $cityA to $cityB with Elite Luxury Bookings. Direct access to 10,000+ aircraft and discrete VIP terminals. Request an elite quote now.">
    <link rel="icon" type="image/png" href="/favicon.png">
    <link rel="canonical" href="https://eliteluxurybookings.com/$name/">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Inter:wght@300;400;600&display=swap">
    <style>
        :root { --gold: #D4AF37; --black: #050505; --glass: rgba(255,255,255,0.03); --border: rgba(212,175,55,0.15); }
        body { background: var(--black); color: #fff; margin:0; font-family:'Inter',sans-serif; overflow-x:hidden; }
        .global-nav { position:fixed; top:0; left:0; right:0; background:rgba(5,5,5,0.98); backdrop-filter:blur(20px); border-bottom:1px solid var(--border); z-index:99999; }
        .nav-inner { max-width:1400px; margin:0 auto; padding:0 2rem; height:72px; display:flex; align-items:center; justify-content:space-between; }
        .nav-brand { font-family:'Cormorant Garamond',serif; font-size:1.7rem; font-weight:600; text-decoration:none; color:#fff; }
        .hero { padding: 9rem 0 5rem; text-align:center; background: radial-gradient(circle at top, rgba(212,175,55,0.05), transparent); }
        h1 { font-family:'Cormorant Garamond',serif; font-size:3.5rem; margin-bottom:1rem; }
        .hero-sub { color:rgba(255,255,255,0.6); max-width:800px; margin:0 auto 3rem; line-height:1.6; }
        .container { max-width:1200px; margin:0 auto; padding:0 2rem; }
        .glass-panel { background:rgba(15,15,15,0.6); border:1px solid var(--border); border-radius:20px; padding:3rem; backdrop-filter:blur(20px); }
        .btn-gold { background:linear-gradient(135deg,#D4AF37,#B8860B); color:#000; padding:1.2rem 2.5rem; border-radius:8px; font-weight:700; text-decoration:none; text-transform:uppercase; letter-spacing:2px; display:inline-block; transition:all 0.3s; }
        .btn-gold:hover { transform:translateY(-3px); box-shadow:0 10px 20px rgba(212,175,55,0.2); }
        .grid-2 { display:grid; grid-template-columns: 1fr 1fr; gap:3rem; margin:4rem 0; }
        .luxury-list { list-style:none; padding:0; }
        .luxury-list li { margin-bottom:1rem; display:flex; gap:1rem; align-items:flex-start; }
        .luxury-list li::before { content:'✦'; color:var(--gold); }
        @media (max-width:768px) { h1 { font-size:2.3rem; } .grid-2 { grid-template-columns:1fr; } }
    </style>
</head>
<body>
    <nav class="global-nav">
        <div class="nav-inner">
            <a href="/" class="nav-brand">ELITE <span style="color:var(--gold)">LUXURY</span></a>
            <a href="https://wa.me/918801079030" class="btn-gold" style="padding:0.6rem 1.2rem; font-size:0.75rem;">WhatsApp</a>
        </div>
    </nav>

    <header class="hero">
        <div class="container">
            <h1>$cityA to $cityB Private Jet Charter</h1>
            <p class="hero-sub">Experience the ultimate in bespoke aviation. Our curated service connects the $cityAType environment of $cityA with the $cityBType landscape of $cityB, ensuring absolute discretion and temporal freedom.</p>
            
            <div class="glass-panel" style="max-width:900px; margin:0 auto; border-color:var(--gold);">
                <h3 style="font-family:'Cormorant Garamond',serif; font-size:2rem; margin-top:0;">Request Elite Quote</h3>
                <p style="color:rgba(255,255,255,0.5); margin-bottom:2rem;">Direct Valens Dashboard Synchronisation</p>
                <form id="valensEngineForm" style="display:grid; gap:1.5rem;">
                    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:1rem;">
                        <input type="text" value="$cityA" readonly style="padding:1rem; background:rgba(0,0,0,0.3); border:1px solid var(--border); color:#fff; border-radius:8px;">
                        <input type="text" value="$cityB" readonly style="padding:1rem; background:rgba(0,0,0,0.3); border:1px solid var(--border); color:#fff; border-radius:8px;">
                        <input type="date" required style="padding:1rem; background:rgba(255,255,255,0.05); border:1px solid var(--border); color:#fff; border-radius:8px;">
                    </div>
                    <button type="submit" class="btn-gold" style="width:100%;">Search Global Fleet</button>
                </form>
            </div>
        </div>
    </header>

    <section class="container" style="padding-bottom:10rem;">
        <div class="grid-2">
            <div class="glass-panel">
                <h2 style="font-family:'Cormorant Garamond',serif; font-size:2.2rem;">Route Intelligence</h2>
                <p>Connecting $cityA and $cityB via private jet bypasses the friction of commercial hubs. Reclaim hours of high-value time while enjoying a sanctuary tailored to your exact specifications.</p>
                <ul class="luxury-list">
                    <li><strong>Departure:</strong> $airportsA</li>
                    <li><strong>Arrival:</strong> $airportsB</li>
                    <li><strong>VIP Transit:</strong> Dedicated FBO Handling</li>
                    <li><strong>Custom Planning:</strong> 24/7 Concierge Support</li>
                </ul>
            </div>
            <div class="glass-panel">
                <h2 style="font-family:'Cormorant Garamond',serif; font-size:2.2rem;">Fleet Availability</h2>
                <p>We provide immediate access to over 10,000 aircraft globally for the $cityA to $cityB corridor.</p>
                <div style="display:grid; gap:1rem; margin-top:2rem;">
                    <div style="border-bottom:1px solid var(--border); padding-bottom:1rem;">
                        <strong>Light Jets</strong><br><small style="color:rgba(255,255,255,0.5);">Phenom 300 / Citation CJ4 - Rapid Efficiency</small>
                    </div>
                    <div style="border-bottom:1px solid var(--border); padding-bottom:1rem;">
                        <strong>Midsize Jets</strong><br><small style="color:rgba(255,255,255,0.5);">Citation Latitude - Enhanced Comfort</small>
                    </div>
                    <div>
                        <strong>Heavy Jets</strong><br><small style="color:rgba(255,255,255,0.5);">Gulfstream G650 - Maximum Prestige</small>
                    </div>
                </div>
            </div>
        </div>

        <div class="glass-panel" style="text-align:center;">
            <h2 style="font-family:'Cormorant Garamond',serif; font-size:2.5rem;">The Elite Standard</h2>
            <p style="max-width:700px; margin:0 auto 2rem; color:rgba(255,255,255,0.6);">From bespoke catering to synchronized tarmac transfers, every mission between $cityA and $cityB is engineered for excellence. No missed connections, only seamless transitions.</p>
            <a href="https://wa.me/918801079030" class="btn-gold">Consult Flight Concierge</a>
        </div>
    </section>

    <footer style="padding:4rem 0; border-top:1px solid var(--border); text-align:center;">
        <p style="color:rgba(255,255,255,0.4); font-size:0.8rem; letter-spacing:1px;">&copy; ELITE LUXURY BOOKINGS - GLOBAL AVIATION NETWORK</p>
    </footer>

    <script src="/valens_api_bridge.js"></script>
    <script>
        document.getElementById('valensEngineForm').addEventListener('submit', function(e) {
            e.preventDefault();
            this.innerHTML = '<div style="padding:4rem; text-align:center;"><h3 style=\"color:var(--gold)\">Sync Successful</h3><p>A concierge is analyzing the fleet for you.</p></div>';
        });
    </script>
</body>
</html>
"@
    
    $template | Out-File -FilePath "$($file.FullName)" -Encoding utf8
    Write-Host "Processed: $($file.Name)"
}
