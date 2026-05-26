import os

def check_nav_comments():
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('_') and f != 'old_blog.html']
    html_files.sort()
    
    missing_start = []
    missing_end = []
    
    for fname in html_files:
        with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        if '<!-- ELB_NAV_START -->' not in content:
            missing_start.append(fname)
        if '<!-- ELB_NAV_END -->' not in content:
            missing_end.append(fname)
            
    print(f"Audited {len(html_files)} files.")
    print(f"Missing ELB_NAV_START: {len(missing_start)}")
    for f in missing_start[:10]:
        print(f"  - {f}")
    if len(missing_start) > 10:
        print(f"  ... and {len(missing_start) - 10} more.")
        
    print(f"\nMissing ELB_NAV_END: {len(missing_end)}")
    for f in missing_end[:10]:
        print(f"  - {f}")
    if len(missing_end) > 10:
        print(f"  ... and {len(missing_end) - 10} more.")

if __name__ == '__main__':
    check_nav_comments()
