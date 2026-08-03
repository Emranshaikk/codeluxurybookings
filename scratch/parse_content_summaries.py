import json
from bs4 import BeautifulSoup
import re

with open("scratch/extracted_raw_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

summary_report = []

def clean_text(text):
    if not text:
        return ""
    # remove excessive whitespace
    return re.sub(r'\s+', ' ', text).strip()

def extract_page_details(name, html):
    soup = BeautifulSoup(html, "html.parser")
    
    title = soup.title.string if soup.title else "No Title"
    h1 = soup.h1.get_text() if soup.h1 else "No H1"
    
    # Extract meta description
    meta_desc = "No Description"
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        meta_desc = meta.get("content")
        
    # Find h2s and h3s
    headers = []
    for h in soup.find_all(["h2", "h3"]):
        headers.append(f"{h.name}: {clean_text(h.get_text())}")
        
    # Extract any tables (often contains pricing)
    tables = []
    for i, t in enumerate(soup.find_all("table")):
        rows = []
        for r in t.find_all("tr"):
            cols = [clean_text(c.get_text()) for c in r.find_all(["td", "th"])]
            rows.append(" | ".join(cols))
        tables.append(f"Table {i+1}:\n" + "\n".join(rows))
        
    # Extract lists (often contains tips or itineraries)
    lists = []
    for l in soup.find_all(["ul", "ol"]):
        items = [clean_text(li.get_text()) for li in l.find_all("li")]
        # Only keep lists with meaningful items
        if len(items) >= 3 and any(len(it) > 30 for it in items):
            lists.append("\n".join([f"- {it}" for it in items[:10]]))
            
    # Extract FAQ questions and answers
    faqs = []
    # Look for accordion or FAQ structures (common class names: faq-question, faq-answer)
    faq_q = soup.find_all(class_=re.compile("faq-question|question", re.I))
    for q in faq_q:
        a = q.find_next(class_=re.compile("faq-answer|answer|content", re.I))
        if a:
            faqs.append(f"Q: {clean_text(q.get_text())}\nA: {clean_text(a.get_text())}")
            
    # Fallback FAQ check: if no class-based FAQs, look for structured schema
    if not faqs:
        scripts = soup.find_all("script", type="application/ld+json")
        for s in scripts:
            try:
                js = json.loads(s.string)
                if js.get("@type") == "FAQPage" or "FAQPage" in str(js):
                    for item in js.get("mainEntity", []):
                        q = item.get("name")
                        a = item.get("acceptedAnswer", {}).get("text")
                        if q and a:
                            # Strip html from answer
                            a_clean = clean_text(BeautifulSoup(a, "html.parser").get_text())
                            faqs.append(f"Q: {q}\nA: {a_clean}")
            except Exception:
                continue

    return {
        "title": clean_text(title),
        "h1": clean_text(h1),
        "description": clean_text(meta_desc),
        "headers": headers,
        "tables": tables,
        "lists": lists,
        "faqs": faqs
    }

report_str = ""

for key, val in sorted(data.items()):
    if key in ["private-boat-trip-mallorca-to-formentera.html", "mallorca-to-ibiza-private-boat.html"]:
        # Summarize canonical
        details = extract_page_details(key, val["content"])
        header_text = f"=========================================\nCANONICAL: {key}\n=========================================\n"
        report_str += header_text
        report_str += f"Title: {details['title']}\n"
        report_str += f"H1: {details['h1']}\n"
        report_str += f"Description: {details['description']}\n\n"
        report_str += "Headers:\n" + "\n".join(details['headers'][:10]) + "\n\n"
        if details['tables']:
            report_str += "Tables:\n" + "\n\n".join(details['tables']) + "\n\n"
        if details['faqs']:
            report_str += "FAQs:\n" + "\n\n".join(details['faqs'][:5]) + "\n\n"
        report_str += "\n"
    else:
        # Summarize non-canonical
        details = extract_page_details(key, val["content"])
        header_text = f"=========================================\nNON-CANONICAL: {key} (from {val['branch']} - {val['path']})\n=========================================\n"
        report_str += header_text
        report_str += f"Title: {details['title']}\n"
        report_str += f"H1: {details['h1']}\n"
        report_str += f"Description: {details['description']}\n\n"
        
        # Summarize unique value
        report_str += "Key Headers:\n" + "\n".join(details['headers'][:5]) + "\n\n"
        
        if details['tables']:
            report_str += "Tables/Pricing Info:\n" + "\n\n".join(details['tables']) + "\n\n"
            
        report_str += "Lists/Itinerary/Tips:\n"
        for idx, l in enumerate(details['lists'][:3]):
            report_str += f"List {idx+1}:\n{l}\n\n"
            
        if details['faqs']:
            report_str += "FAQs:\n" + "\n\n".join(details['faqs']) + "\n\n"
            
        report_str += "\n"

with open("scratch/content_merges_summary.txt", "w", encoding="utf-8") as out:
    out.write(report_str)

print("Saved summaries to scratch/content_merges_summary.txt")
