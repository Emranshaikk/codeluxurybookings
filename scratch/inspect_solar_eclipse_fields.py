from bs4 import BeautifulSoup
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

path = "solar-eclipse-balearic-islands-private-yacht.html"
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')
forms = soup.find_all('form')
for idx, form in enumerate(forms):
    print(f"Form {idx+1}: ID={form.get('id')} | onsubmit={form.get('onsubmit')}")
    inputs = form.find_all(['input', 'select', 'textarea'])
    for inp in inputs:
        print(f"  Tag: {inp.name} | ID: {inp.get('id')} | Name: {inp.get('name')} | Type: {inp.get('type')}")
    print("-" * 40)
