import os
import re

def minify_css(css_content):
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # Remove extra spaces/tabs/newlines
    css_content = re.sub(r'\s+', ' ', css_content)
    # Remove spaces around punctuation
    css_content = re.sub(r'\s*([\{\};:,])\s*', r'\1', css_content)
    # Remove final semicolon in rules
    css_content = re.sub(r';\}', '}', css_content)
    return css_content.strip()

def optimize_font_awesome(html_content):
    # Match FontAwesome stylesheet link tags
    # <link rel="stylesheet" href="...font-awesome..."> or similar
    def replace_fa(match):
        tag = match.group(0)
        # Skip if already async
        if 'media="print"' in tag or "media='print'" in tag:
            return tag
        
        # Remove any existing media attribute
        tag_clean = re.sub(r'\s+media=["\'][^"\']*["\']', '', tag)
        
        # Replace rel="stylesheet" or inject the media/onload attributes
        if 'rel="stylesheet"' in tag_clean:
            return tag_clean.replace('rel="stylesheet"', 'rel="stylesheet" media="print" onload="this.media=\'all\'"')
        elif "rel='stylesheet'" in tag_clean:
            return tag_clean.replace("rel='stylesheet'", "rel='stylesheet' media='print' onload='this.media=\"all\"'")
        else:
            # Inject before the closing bracket
            if tag_clean.endswith('/>'):
                return tag_clean[:-2] + ' media="print" onload="this.media=\'all\'"/>'
            else:
                return tag_clean[:-1] + ' media="print" onload="this.media=\'all\'">'

    return re.sub(r'<link[^>]*href="[^"]*font-awesome[^"]*"[^>]*>', replace_fa, html_content)

def optimize_google_fonts(html_content):
    # Defer Google Fonts stylesheets in HTML files
    def replace_gf(match):
        tag = match.group(0)
        # Skip if already async or is preload/preconnect
        if 'media="print"' in tag or "media='print'" in tag or 'rel="preload"' in tag or 'rel="preconnect"' in tag:
            return tag
        
        # Remove existing media attribute
        tag_clean = re.sub(r'\s+media=["\'][^"\']*["\']', '', tag)
        
        if 'rel="stylesheet"' in tag_clean:
            return tag_clean.replace('rel="stylesheet"', 'rel="stylesheet" media="print" onload="this.media=\'all\'"')
        elif "rel='stylesheet'" in tag_clean:
            return tag_clean.replace("rel='stylesheet'", "rel='stylesheet' media='print' onload='this.media=\"all\"'")
        else:
            if tag_clean.endswith('/>'):
                return tag_clean[:-2] + ' media="print" onload="this.media=\'all\'"/>'
            else:
                return tag_clean[:-1] + ' media="print" onload="this.media=\'all\'">'

    # Match all link tags containing fonts.googleapis.com
    def check_link(match):
        tag = match.group(0)
        if 'fonts.googleapis.com' in tag and ('rel="stylesheet"' in tag or "rel='stylesheet'" in tag):
            return replace_gf(match)
        return tag

    return re.sub(r'<link[^>]*>', check_link, html_content)

def optimize_index_hero(html_content):
    # Optimize the hero image URL width to w=1200
    old_url = 'https://images.unsplash.com/photo-1540962351504-03099e0a754b?w=1800&q=80'
    new_url = 'https://images.unsplash.com/photo-1540962351504-03099e0a754b?w=1200&q=80'
    
    # 1. Rescale background image in styles
    html_content = html_content.replace(old_url, new_url)
    
    # 2. Inject preload tag at the top of the <head> tag
    preload_tag = f'\n    <link rel="preload" href="{new_url}" as="image">'
    if preload_tag not in html_content:
        html_content = re.sub(r'(<head\b[^>]*>)', r'\1' + preload_tag, html_content)
        
    return html_content

def run_optimization():
    directory = '.'
    
    # 1. Minify CSS
    css_path = os.path.join(directory, 'style.css')
    min_css_path = os.path.join(directory, 'style.min.css')
    
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        orig_size = len(css_content)
        minified_content = minify_css(css_content)
        min_size = len(minified_content)
        
        with open(min_css_path, 'w', encoding='utf-8') as f:
            f.write(minified_content)
            
        print(f"Minified CSS: {orig_size} bytes -> {min_size} bytes ({((orig_size - min_size)/orig_size)*100:.1f}% savings)")
    else:
        print("Warning: style.css not found!")
        
    # 2. Optimize all HTML files
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    files_updated = 0
    
    for filename in html_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # A. Replace references to style.css with style.min.css
        # Replace variations with or without leading slash, single or double quotes
        content = content.replace('href="/style.css"', 'href="/style.min.css"')
        content = content.replace("href='/style.css'", "href='/style.min.css'")
        content = content.replace('href="style.css"', 'href="/style.min.css"')
        content = content.replace("href='style.css'", "href='/style.min.css'")
        
        # B. Optimize FontAwesome (asynchronously load)
        content = optimize_font_awesome(content)
        
        # C. Optimize Google Fonts (asynchronously load stylesheet)
        content = optimize_google_fonts(content)
        
        # D. Optimize Homepage (index.html) hero image preload/scale
        if filename == 'index.html':
            content = optimize_index_hero(content)
            
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            files_updated += 1
            
    print(f"Successfully optimized {files_updated} / {len(html_files)} HTML files.")

if __name__ == '__main__':
    run_optimization()
