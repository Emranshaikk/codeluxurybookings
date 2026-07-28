import os

SAMPLE_FILES = [
    'houston-to-miami-private-jet-cost.html',
    'bahamas-to-newyork-private-jet-cost.html',
    'dallas-to-denver-private-jet-cost.html',
    'hawaii-to-losangeles-private-jet-cost.html',
    'dubai-to-sydney-private-jet-cost.html',
    'london-to-barcelona-private-jet-cost.html',
    'newyork-to-london-private-jet-cost.html'
]

def spot_check():
    print("=== SPOT CHECK RESULTS FOR 7 SAMPLE PAGES ===\n")
    
    for filename in SAMPLE_FILES:
        filepath = os.path.join('.', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        has_clean_ticker = '⚠️ Intelligence Alert:' in content and '?? Intelligence Alert:' not in content
        has_clean_menu = '✈ Private Jets' in content and '? Private Jets' not in content
        has_clean_breadcrumb = 'href="https://eliteluxurybookings.com/elite-private-jet-charter/"' in content
        no_gmail = 'contactshaikk@gmail.com' not in content
        no_product_schema = '"Product"' not in content and '"@type": "Product"' not in content
        no_local_biz = '"LocalBusiness"' not in content and '"@type": "LocalBusiness"' not in content
        has_status_box = '✨ Route Status: High-Availability Executive Corridors Open' in content
        has_range_warning = 'id="range-warning"' in content or 'routeDistance' in content
        
        all_passed = all([has_clean_ticker, has_clean_menu, has_clean_breadcrumb, no_gmail, no_product_schema, no_local_biz, has_status_box])
        
        status_str = "[PASS]" if all_passed else "[FAIL]"
        print(f"{status_str} File: {filename}")
        print(f"       Clean Ticker: {has_clean_ticker} | Clean Menu: {has_clean_menu}")
        print(f"       Correct Breadcrumb: {has_clean_breadcrumb} | No Gmail: {no_gmail}")
        print(f"       No Product Schema: {no_product_schema} | No LocalBusiness Schema: {no_local_biz}")
        print(f"       Status Box: {has_status_box} | Range Warning Enabled: {has_range_warning}\n")

if __name__ == '__main__':
    spot_check()
