
import os
import re

def audit_links():
    # 1. Get all valid local directories
    with open('tmp_all_dirs.txt', 'r', encoding='utf-8') as f:
        valid_dirs = set(line.strip().lower() for line in f if line.strip())
    
    # Add home and core files
    valid_dirs.add('') # root
    valid_dirs.add('index.html')
    valid_dirs.add('sitemap.xml')
    valid_dirs.add('robots.txt')

    broken_links = []
    checked_files = 0
    total_links_found = 0

    # 2. Iterate through all html files
    for root, dirs, files in os.walk('.'):
        # Skip git and assets
        if '.git' in root or 'assets' in root:
            continue
            
        for file in files:
            if file.endswith('.html'):
                checked_files += 1
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
                    continue

                # Find all href="..."
                links = re.findall(r'href=["\'](.*?)["\']', content)
                for link in links:
                    total_links_found += 1
                    
                    # Strip domain if present
                    clean_link = link.replace('https://eliteluxurybookings.com', '')
                    
                    # Only check internal links
                    if clean_link.startswith('http') or clean_link.startswith('mailto:') or clean_link.startswith('tel:') or clean_link.startswith('#'):
                        continue
                    
                    # Clean up path to just the folder name or filename
                    # e.g., /london-to-nice-private-jet-cost/ -> london-to-nice-private-jet-cost
                    path_parts = [p for p in clean_link.split('/') if p]
                    
                    if not path_parts:
                        # Root link (/) is always valid
                        continue
                    
                    target = path_parts[0].lower()
                    
                    # Check if the first level exists in our valid_dirs
                    if target not in valid_dirs:
                        broken_links.append({
                            'source_file': filepath,
                            'broken_href': link,
                            'target_part': target
                        })

    # 3. Save report
    report = f"# Link Integrity Audit Report\n\n"
    report += f"- Total Files Checked: {checked_files}\n"
    report += f"- Total Links Found: {total_links_found}\n"
    report += f"- Total Broken Links Identified: {len(broken_links)}\n\n"

    if broken_links:
        report += "### Broken Internal Links Found\n\n"
        report += "| Source File | Broken Link | Missing Folder |\n"
        report += "| :--- | :--- | :--- |\n"
        # Only show first 100 for brevity in report if there are many
        for bl in broken_links[:100]:
            report += f"| {bl['source_file']} | `{bl['broken_href']}` | `{bl['target_part']}` |\n"
            
        if len(broken_links) > 100:
            report += f"\n*...and {len(broken_links) - 100} more broken links.*"
    else:
        report += "### ✅ No Broken Internal Links Found!\n\nAll internal links point to valid destination folders."

    with open('broken_links_report.md', 'w', encoding='utf-8') as f:
        f.write(report)

if __name__ == "__main__":
    audit_links()
