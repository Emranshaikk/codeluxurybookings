import os
import re

def find_all_villa_routes():
    blog_index = "blog/index.html"
    try:
        with open(blog_index, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Regex to find links with data-category="villas"
        # The structure is: <a href="/..." class="..." data-category="villas" ...>
        # Or <a href="/..." data-category="villas" ...>
        
        links = re.findall(r'<a href="(/[^"]*/)"[^>]*data-category="villas"', content)
        
        if not links:
            # Try finding by looking for href following category
            links = re.findall(r'data-category="villas"[^>]*href="(/[^"]*/)"', content)

        if not links:
            # Final attempt: manual search for destination guides
            print("No direct category-based links found. Performing semantic search...")
            links = re.findall(r'href="(/[^"]*/?)"', content)
            villas = []
            for l in links:
                if any(k in l.lower() for k in ["villa", "estate", "st-tropez", "ibiza-luxury", "retreat"]):
                    villas.append(l)
            links = villas

        print(f"Discovered {len(links)} Potential Villa Destinations:")
        for l in links:
            print(f" - {l}")
            
    except Exception as e:
        print(f"Audit Error: {e}")

if __name__ == "__main__":
    find_all_villa_routes()
