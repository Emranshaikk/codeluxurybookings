import xml.etree.ElementTree as ET

ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")
tree = ET.parse('sitemap.xml')
root = tree.getroot()
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

seen = set()
to_remove = []

for url_tag in root.findall('ns:url', namespace):
    loc = url_tag.find('ns:loc', namespace).text
    if loc in seen:
        to_remove.append(url_tag)
    else:
        seen.add(loc)

for url_tag in to_remove:
    root.remove(url_tag)

tree.write('sitemap.xml', encoding='UTF-8', xml_declaration=True)

print(f"Cleaned sitemap.xml. Removed {len(to_remove)} duplicate entries.")
