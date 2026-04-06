import os
import re

filepath = r'c:\Users\imran\OneDrive\Desktop\ELB code\luxury-villa-rentals\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix duplicated style tag
content = content.replace("<style>\n<style>", "<style>")
content = content.replace("<style>\r\n<style>", "<style>")

# 2. Add an immersive Hero Background Image replacing the flat gradient
hero_pattern = r'\.hero-parallax-bg\s*\{[^}]*\}'
new_hero_css = """.hero-parallax-bg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(to bottom, rgba(5,5,5,0.4) 0%, rgba(5,5,5,1) 100%), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80') center/cover no-repeat;
            z-index: -1;
            will-change: transform;
            animation: zoomBg 25s infinite alternate linear;
        }

        @keyframes zoomBg {
            from { transform: scale(1); filter: contrast(1); }
            to { transform: scale(1.05); filter: contrast(1.1); }
        }"""
content = re.sub(hero_pattern, new_hero_css, content)

# 3. Add Premium Image Backgrounds to the Destination Cards
# We match the <div class="glass-panel" followed by the inline style and insert a background image.

# Amalfi
content = re.sub(
    r'<div class="glass-panel"\s*style="padding:\s*2\.5rem;\s*text-align:\s*center;\s*border-top:\s*2px\s*solid\s*var\(--primary-gold\);\s*display:\s*flex;\s*flex-direction:\s*column;\s*justify-content:\s*flex-start;\s*gap:\s*0\.5rem;\s*height:\s*100%;">',
    '<div class="glass-panel card" style="padding: 2.5rem; text-align: center; border-top: 2px solid var(--primary-gold); background: linear-gradient(to top, rgba(5,5,5,0.95), rgba(5,5,5,0.2)), url(\'https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?auto=format&fit=crop&w=800&q=80\') center/cover; display: flex; flex-direction: column; justify-content: flex-start; gap: 0.5rem; height: 100%; transition: transform 0.4s ease;">',
    content, count=1
)

# St. Barts
content = re.sub(
    r'<div class="glass-panel"\s*style="padding:\s*2\.5rem;\s*text-align:\s*center;\s*border-top:\s*2px\s*solid\s*var\(--primary-gold\);\s*display:\s*flex;\s*flex-direction:\s*column;\s*justify-content:\s*flex-start;\s*gap:\s*0\.5rem;\s*height:\s*100%;">',
    '<div class="glass-panel card" style="padding: 2.5rem; text-align: center; border-top: 2px solid var(--primary-gold); background: linear-gradient(to top, rgba(5,5,5,0.95), rgba(5,5,5,0.2)), url(\'https://images.unsplash.com/photo-1589394815804-964ce052dfce?auto=format&fit=crop&w=800&q=80\') center/cover; display: flex; flex-direction: column; justify-content: flex-start; gap: 0.5rem; height: 100%; transition: transform 0.4s ease;">',
    content, count=1
)

# Aspen
content = re.sub(
    r'<div class="glass-panel"\s*style="padding:\s*2\.5rem;\s*text-align:\s*center;\s*border-top:\s*2px\s*solid\s*var\(--primary-gold\);\s*display:\s*flex;\s*flex-direction:\s*column;\s*justify-content:\s*flex-start;\s*gap:\s*0\.5rem;\s*height:\s*100%;">',
    '<div class="glass-panel card" style="padding: 2.5rem; text-align: center; border-top: 2px solid var(--primary-gold); background: linear-gradient(to top, rgba(5,5,5,0.95), rgba(5,5,5,0.2)), url(\'https://images.unsplash.com/photo-1516086550756-32db2f0b701c?auto=format&fit=crop&w=800&q=80\') center/cover; display: flex; flex-direction: column; justify-content: flex-start; gap: 0.5rem; height: 100%; transition: transform 0.4s ease;">',
    content, count=1
)

# Dubai
content = re.sub(
    r'<div class="glass-panel"\s*style="padding:\s*2\.5rem;\s*text-align:\s*center;\s*border-top:\s*2px\s*solid\s*var\(--primary-gold\);\s*display:\s*flex;\s*flex-direction:\s*column;\s*justify-content:\s*flex-start;\s*gap:\s*0\.5rem;\s*height:\s*100%;">',
    '<div class="glass-panel card" style="padding: 2.5rem; text-align: center; border-top: 2px solid var(--primary-gold); background: linear-gradient(to top, rgba(5,5,5,0.95), rgba(5,5,5,0.2)), url(\'https://images.unsplash.com/photo-1520653609805-4c07883d6a2f?auto=format&fit=crop&w=800&q=80\') center/cover; display: flex; flex-direction: column; justify-content: flex-start; gap: 0.5rem; height: 100%; transition: transform 0.4s ease;">',
    content, count=1
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Redesign applied successfully.")
