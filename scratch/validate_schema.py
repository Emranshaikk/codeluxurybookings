import json
import re

def validate_schemas(file_path):
    print(f"Validating JSON-LD schemas in: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find all <script type="application/ld+json">...</script> blocks
    schema_pattern = re.compile(r'<script\s+type="application/ld\+json"\s*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
    matches = schema_pattern.findall(html_content)
    
    if not matches:
        print("No JSON-LD schemas found!")
        return False

    success = True
    for i, schema_text in enumerate(matches):
        try:
            # Clean and parse JSON
            cleaned_text = schema_text.strip()
            data = json.loads(cleaned_text)
            print(f"Schema Block {i+1}: SUCCESS (Valid JSON)")
            # Print top level keys or types
            if isinstance(data, dict):
                print(f"  Type: {data.get('@type', data.get('@context'))}")
            elif isinstance(data, list):
                print(f"  List of {len(data)} items")
        except json.JSONDecodeError as e:
            print(f"Schema Block {i+1}: FAIL (Invalid JSON)")
            print(f"  Error: {e}")
            # Print context around error
            lines = schema_text.splitlines()
            line_no = e.lineno
            print("Context of failure:")
            start = max(0, line_no - 4)
            end = min(len(lines), line_no + 4)
            for idx in range(start, end):
                prefix = ">>> " if idx == line_no - 1 else "    "
                print(f"{prefix}{idx+1}: {lines[idx]}")
            success = False
            
    return success

if __name__ == "__main__":
    validate_schemas("luxury-yacht-charter-for-family-vacation.html")
