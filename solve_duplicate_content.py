import os
import re
import hashlib

def format_city(city_raw):
    city_map = {
        'losangeles': 'Los Angeles',
        'newyork': 'New York',
        'sanfrancisco': 'San Francisco',
        'abudhabi': 'Abu Dhabi',
        'goldcoast': 'Gold Coast',
        'lasvegas': 'Las Vegas',
        'hongkong': 'Hong Kong',
        'turksandcaicos': 'Turks and Caicos',
        'buenosaires': 'Buenos Aires',
        'saopaulo': 'Sao Paulo',
        'capetown': 'Cape Town'
    }
    return city_map.get(city_raw, city_raw.replace('-', ' ').title())

def solve_duplicate_content():
    html_files = [f for f in os.listdir('.') if f.endswith('-private-jet-cost.html')]
    print(f"Processing {len(html_files)} route files...")

    # Spintax templates for Hero Sub
    hero_subs = [
        "Reclaim your time and experience absolute privacy. We curate and coordinate world-class luxury experiences through our global partner network, engineering seamless transitions from {origin} to {dest} with precision timing.",
        "Elevate your journey from {origin} to {dest} with unparalleled privacy and bespoke concierge services. Our elite aviation partners ensure that every aspect of your flight is executed with flawless precision.",
        "Bypass commercial congestion entirely. Our exclusive jet charter network guarantees absolute discretion and world-class luxury as you transition smoothly from {origin} to {dest}.",
        "Experience the pinnacle of private aviation. We coordinate sophisticated travel logistics from {origin} to {dest}, ensuring high-net-worth individuals arrive refreshed and completely unbothered.",
        "Your time is your ultimate luxury. Our dedicated dispatchers arrange bespoke flight paths from {origin} to {dest}, providing a discrete, secure, and exceptional journey tailored entirely to you.",
        "Step onto the tarmac and leave the world behind. We curate highly confidential and luxurious jet charters connecting {origin} to {dest}, utilizing only Wyvern and ARGUS certified aircraft.",
        "Seamless global mobility tailored for the elite. Our concierge coordinates every nuance of your departure from {origin} to your arrival in {dest}, ensuring zero delays and ultimate comfort.",
        "Redefining executive travel. From {origin} to {dest}, we provide rapid dispatch capabilities, off-market aircraft access, and a strictly confidential flight environment for our discerning clients.",
        "Luxury is in the details. Our aviation experts orchestrate perfectly timed departures from {origin} to {dest}, allowing you to conduct business or relax in absolute solitude at 40,000 feet.",
        "Uncompromised safety and sophisticated service. We connect {origin} to {dest} through elite private FBOs, giving you a completely private and highly efficient travel experience."
    ]

    # Spintax templates for Flight Performance
    flight_performances = [
        "The {origin} to {dest} corridor is a vital luxury transit route. By utilizing private aviation, travelers bypass commercial congestion entirely, reclaiming hours of valuable time.",
        "Flying privately from {origin} to {dest} ensures absolute discretion and unmatched time efficiency. Direct routing and exclusive terminal access eliminate the frictions of commercial travel.",
        "For high-net-worth individuals, the journey between {origin} and {dest} demands the utmost in privacy. Our curated jet charter guarantees a seamless departure and a perfectly timed arrival.",
        "The strategic route connecting {origin} and {dest} is highly sought after by corporate executives and VIPs. Private charter allows for dynamic scheduling that revolves entirely around your agenda.",
        "Navigating from {origin} to {dest} has never been more refined. By departing through dedicated FBOs, our clients experience an uninterrupted flow from ground transport directly to the aircraft.",
        "Air travel between {origin} and {dest} requires logistical precision. Our elite aviation network provides tailored aircraft solutions that optimize speed, range, and cabin comfort for this specific flight path.",
        "Whether for critical business engagements or leisure, the {origin} to {dest} flight path benefits immensely from private aviation, offering zero baggage delays, no security lines, and total peace of mind.",
        "Our clients traveling from {origin} to {dest} expect nothing less than perfection. Private jet charters transform this route into a luxurious sanctuary, complete with bespoke catering and high-speed connectivity.",
        "The distance between {origin} and {dest} is effortlessly bridged by our premium fleet. Private charters drastically reduce total travel time, providing a secure and productive environment in the sky.",
        "Executing a flawless flight from {origin} to {dest} requires unparalleled expertise. Our team curates the ideal aircraft for this specific mission, balancing high-end luxury with absolute operational safety."
    ]

    files_changed = 0

    for filename in html_files:
        # Extract cities
        match = re.match(r'([a-z]+)-to-([a-z]+)-private-jet-cost\.html', filename)
        if not match:
            continue
            
        origin_raw = match.group(1)
        dest_raw = match.group(2)
        
        origin = format_city(origin_raw)
        dest = format_city(dest_raw)

        # Consistent hash based on filename so templates remain static upon reruns
        hash_val = int(hashlib.md5(filename.encode('utf-8')).hexdigest(), 16)
        t_index = hash_val % 10
        
        hero_text = hero_subs[t_index].format(origin=origin, dest=dest)
        perf_text = flight_performances[t_index].format(origin=origin, dest=dest)

        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        old_content = content

        # Replace Hero Sub text while preserving style and tags
        # Regex looks for <p class="hero-sub" ... > (anything) </p>
        content = re.sub(
            r'(<p class="hero-sub"[^>]*>)(.*?)(</p>)',
            lambda m: f"{m.group(1)}\n                {hero_text}{m.group(3)}",
            content,
            flags=re.IGNORECASE | re.DOTALL
        )

        # Replace Flight Performance text while preserving style and tags
        # Regex looks for <h3 ...>Flight Performance</h3> followed by whitespace and a <p ...>(anything)</p>
        content = re.sub(
            r'(<h3[^>]*>Flight Performance</h3>\s*<p[^>]*>)(.*?)(</p>)',
            lambda m: f"{m.group(1)}{perf_text}{m.group(3)}",
            content,
            flags=re.IGNORECASE | re.DOTALL
        )

        if content != old_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            files_changed += 1

    print(f"Duplicate content resolved in {files_changed} files.")

if __name__ == "__main__":
    solve_duplicate_content()
