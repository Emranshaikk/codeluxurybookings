import os
import re

def fix_blog_index():
    path = "c:\\Users\\imran\\OneDrive\\Desktop\\ELB code\\blog\\index.html"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Identify all route links and add 'route-card' class
        # route links usually look like: *-to-*-private-jet-cost
        # We also ensure category matches 'private jets'
        
        def route_replacer(match):
            href = match.group(1)
            # Add 'route-card' class to the link
            return f'<a href="{href}" class="blog-card route-card"'
            
        pattern = r'<a href="(/[^"]+to-[^"]+private-jet-cost/)" class="blog-card"'
        content = re.sub(pattern, route_replacer, content)
        
        # 2. Inject the missing filterPosts function and Image Fallback script
        script_code = """
    <script>
        function filterPosts(category) {
            const cards = document.querySelectorAll('.blog-card');
            const btns = document.querySelectorAll('.filter-btn');
            
            // Update active button
            btns.forEach(btn => {
                if(btn.innerText.toLowerCase() === category.toLowerCase()) {
                    btn.classList.add('active');
                } else if(category === 'all' && btn.innerText.toLowerCase() === 'all articles') {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });

            cards.forEach(card => {
                const cardCat = card.getAttribute('data-category').toLowerCase();
                const isRoute = card.classList.contains('route-card');
                
                if (category === 'all') {
                    // EXCLUDE route pages from the 'All Articles' view to keep it clean
                    if (isRoute) {
                        card.style.display = 'none';
                    } else {
                        card.style.display = 'block';
                    }
                } else {
                    // Show standard matches
                    if (cardCat === category.toLowerCase()) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                }
            });
        }

        // Apply Premium Fallback Images on Load
        document.addEventListener('DOMContentLoaded', () => {
            const images = document.querySelectorAll('.blog-card img');
            const fallbacks = {
                'private jets': 'https://images.pexels.com/photos/7233354/pexels-photo-7233354.jpeg?auto=compress&cs=tinysrgb&w=800',
                'yachts': 'https://images.pexels.com/photos/163236/luxury-yacht-ocean-sea-163236.jpeg?auto=compress&cs=tinysrgb&w=800',
                'villas': 'https://images.pexels.com/photos/208736/pexels-photo-208736.jpeg?auto=compress&cs=tinysrgb&w=800'
            };

            images.forEach(img => {
                const card = img.closest('.blog-card');
                const cat = card.getAttribute('data-category').toLowerCase();
                
                // If it's the generic pexels placeholder 7233354 without the w=800 param, 
                // it might be a missing specific image. Replace with category defaults.
                if (img.src.includes('7233354') && !img.src.includes('w=800')) {
                    if (fallbacks[cat]) {
                        img.src = fallbacks[cat];
                    }
                }
            });
            
            // Initial filter run to clean 'All Articles' view
            filterPosts('all');
        });
    </script>
"""
        # Inject before </body>
        if "</body>" in content:
            content = content.replace("</body>", f"{script_code}</body>")
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Successfully fixed blog index categorization and injected filter engine.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_blog_index()
