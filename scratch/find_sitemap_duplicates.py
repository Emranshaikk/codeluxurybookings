import xml.etree.ElementTree as ET

tree = ET.parse('sitemap.xml')
root = tree.getroot()
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

urls = []
duplicates = []
seen = set()

for url_tag in root.findall('ns:url', namespace):
    loc = url_tag.find('ns:loc', namespace).text
    if loc in seen:
        duplicates.append(loc)
    else:
        seen.add(loc)
        urls.append(url_tag)

if duplicates:
    print(f"Found {len(duplicates)} duplicate URLs in sitemap:")
    for d in duplicates:
        print(d)
else:
    print("No duplicates found in sitemap.")
