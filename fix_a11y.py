import os
import glob
import re

files_changed = 0

for filepath in glob.glob("*.html"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    old_content = content
    
    # 1. Footer contrast
    content = content.replace(
        "color:rgba(255,255,255,0.5); font-size:0.95rem; line-height:1.8; max-width:300px;",
        "color:rgba(255,255,255,0.7); font-size:0.95rem; line-height:1.8; max-width:300px;"
    )
    content = content.replace(
        "color:rgba(255,255,255,0.35); font-size:0.85rem; letter-spacing:0.5px;",
        "color:rgba(255,255,255,0.6); font-size:0.85rem; letter-spacing:0.5px;"
    )

    # 2. Form in _template_master.html (has class="form-label")
    content = re.sub(r'<label class="form-label">Departure Airport</label>\s*<select class="form-control" id="departure"', r'<label class="form-label" for="departure">Departure Airport</label>\n                                <select class="form-control" id="departure"', content)
    content = re.sub(r'<label class="form-label">Arrival Airport</label>\s*<select class="form-control" id="arrival"', r'<label class="form-label" for="arrival">Arrival Airport</label>\n                                <select class="form-control" id="arrival"', content)
    content = re.sub(r'<label class="form-label">Travel Date</label>\s*<input type="date" class="form-control" id="travel_date"', r'<label class="form-label" for="travel_date">Travel Date</label>\n                                <input type="date" class="form-control" id="travel_date"', content)
    content = re.sub(r'<label class="form-label">Departure Time</label>\s*<input type="time" class="form-control" id="travel_time"', r'<label class="form-label" for="travel_time">Departure Time</label>\n                                <input type="time" class="form-control" id="travel_time"', content)
    
    content = re.sub(r'<label class="form-label">Passengers</label>\s*<input type="number" class="form-control" name="passengers"', r'<label class="form-label" for="passengers">Passengers</label>\n                                <input type="number" class="form-control" id="passengers" name="passengers"', content)
    content = re.sub(r'<label class="form-label">Full Name</label>\s*<input type="text" class="form-control" name="fullName"', r'<label class="form-label" for="fullName">Full Name</label>\n                                <input type="text" class="form-control" id="fullName" name="fullName"', content)
    content = re.sub(r'<label class="form-label">Private Email</label>\s*<input type="email" class="form-control" name="email"', r'<label class="form-label" for="email">Private Email</label>\n                                <input type="email" class="form-control" id="email" name="email"', content)
    content = re.sub(r'<label class="form-label">Contact Number</label>\s*<input type="tel" class="form-control" name="contact"', r'<label class="form-label" for="contact">Contact Number</label>\n                                <input type="tel" class="form-control" id="contact" name="contact"', content)

    # 3. Form in Route Pages (has <label> without class)
    # Full Name
    content = re.sub(r'<label>Full Name</label>\s*<input type="text" name="name" class="form-control"', r'<label for="name">Full Name</label>\n                            <input type="text" id="name" name="name" class="form-control"', content)
    # WhatsApp / Phone
    content = re.sub(r'<label>WhatsApp / Phone</label>\s*<input type="tel" name="phone" class="form-control"', r'<label for="phone">WhatsApp / Phone</label>\n                            <input type="tel" id="phone" name="phone" class="form-control"', content)
    # Email Address
    content = re.sub(r'<label>Email Address</label>\s*<input type="email" name="email" class="form-control"', r'<label for="email">Email Address</label>\n                        <input type="email" id="email" name="email" class="form-control"', content)
    # Travel Date
    content = re.sub(r'<label>Travel Date</label>\s*<input type="date" name="travel_date" class="form-control"', r'<label for="travel_date">Travel Date</label>\n                            <input type="date" id="travel_date" name="travel_date" class="form-control"', content)
    # Passengers
    content = re.sub(r'<label>Passengers</label>\s*<input type="number" name="passengers" class="form-control"', r'<label for="passengers">Passengers</label>\n                            <input type="number" id="passengers" name="passengers" class="form-control"', content)
    # Aircraft Class
    content = re.sub(r'<label>Aircraft Class Preference</label>\s*<select name="aircraft_class" class="form-control">', r'<label for="aircraft_class">Aircraft Class Preference</label>\n                        <select id="aircraft_class" name="aircraft_class" class="form-control">', content)
    # Message
    content = re.sub(r'<label>Specific Requirements</label>\s*<textarea name="message" class="form-control"', r'<label for="message">Specific Requirements</label>\n                        <textarea id="message" name="message" class="form-control"', content)

    if content != old_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        files_changed += 1

print(f"Updated {files_changed} files.")
