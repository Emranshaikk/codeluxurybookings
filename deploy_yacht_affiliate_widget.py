import os
import re

# THE STANDARDIZED MOBILE-OPTIMIZED YACHTING WIDGET
YACHT_WIDGET_HTML = r"""
        <!-- ELB_YACHTING_AFFILIATE_WIDGET_START -->
        <div class="yachting-affiliate-container" style="margin: 3rem auto; max-width: 350px; text-align: center; background: rgba(255,255,255,0.02); padding: 1rem; border-radius: 15px; border: 1px solid rgba(212,175,55,0.15); box-shadow: 0 15px 45px rgba(0,0,0,0.4); overflow: hidden;">
            <p style="color: var(--primary-gold); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem; font-weight: 600;">Explore Global Yacht Fleet</p>
            <a href="https://www.yachting.com/en-gb?AffiliateID=elbookings&amp;BannerID=1729a6e6" target="_top" style="display: block; border-radius: 10px; overflow: hidden;">
                <img src="//affiliate.yachting.com/accounts/default1/ne6ayxbkog/1729a6e6.png" alt="Exclusive Yacht Charter" title="Book Premium Yachts" width="320" height="1200" style="width:100%; height:auto; display:block; transition: transform 0.5s ease;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'" />
            </a>
            <img style="border:0" src="https://affiliate.yachting.com/scripts/ne6ayxikog?AffiliateID=elbookings&amp;BannerID=1729a6e6" width="1" height="1" alt="" />
            <p style="color: rgba(255,255,255,0.4); font-size: 0.65rem; margin-top: 1rem; letter-spacing: 1px;">Official Maritime Partner of Elite Luxury Bookings</p>
        </div>
        <style>
            @media (max-width: 768px) {
                .yachting-affiliate-container {
                    max-width: 100% !important;
                    margin: 2rem 1rem !important;
                    border-radius: 12px !important;
                }
            }
        </style>
        <!-- ELB_YACHTING_AFFILIATE_WIDGET_END -->
"""

def deploy_yacht_widget():
    count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == 'index.html':
                 path = os.path.join(root, file)
                 if any(x in root for x in ['node_modules', '.git', 'assets']): continue
                 
                 with open(path, 'r', encoding='utf-8') as f:
                     content = f.read()
                 
                 # ONLY target Yacht pages
                 is_yacht = 'luxury-yacht-rentals' in root or 'yacht' in root.lower() or 'Yacht' in content
                 if not is_yacht: continue
                 
                 # Safety: Don't touch Aviation or Villa pages unless they specifically mention Yachts
                 if ('private-jet' in root or 'luxury-villa-rentals' in root) and 'Yacht' not in root.lower():
                     continue

                 original = content
                 
                 # 1. If it's a blog post (has sidebar), put it in the sidebar
                 if 'blog-sidebar' in content:
                     # Remove old widget first
                     content = re.sub(r'<!-- ELB_YACHTING_WIDGET_START -->.*?<!-- ELB_YACHTING_WIDGET_END -->', '', content, flags=re.DOTALL)
                     content = content.replace('<aside class="blog-sidebar">', '<aside class="blog-sidebar">\n' + YACHT_WIDGET_HTML)
                 
                 # 2. For Category/Hub pages, put it after the primary content or hero
                 elif 'hero-mini-form' in content:
                     content = content.replace('</div>\n            </div>\n        </div>\n    </header>', '</div>\n            </div>\n        </div>\n' + YACHT_WIDGET_HTML + '\n    </header>')
                 
                 # 3. Fallback: After header if no sidebar or mini-form
                 elif '</header>' in content and 'ELB_YACHTING_AFFILIATE_WIDGET_START' not in content:
                     content = content.replace('</header>', '</header>\n' + YACHT_WIDGET_HTML, 1)

                 if content != original:
                     with open(path, 'w', encoding='utf-8') as f:
                         f.write(content)
                     count += 1
                     print(f"Yacht Widget Deployed: {path}")

    print(f"\nElite Yachting.com Affiliate System deployed to {count} maritime pages.")

if __name__ == "__main__":
    deploy_yacht_widget()
