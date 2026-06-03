import os

files = [
    "caribbean-private-island-rental.html",
    "maldives-private-island-rental.html",
    "luxury-private-island-rental.html"
]

directory = r"c:\Users\imran\OneDrive\Desktop\ELB code"

for filename in files:
    path = os.path.join(directory, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        print(f"--- File: {filename} ---")
        # Check for wa-float element
        has_el = "class=\"wa-float\"" in content or "class='wa-float'" in content or "class=wa-float" in content
        print(f"Has wa-float HTML element: {has_el}")
        
        # Check for </style>
        if "</style>" in content:
            print("Contains </style> tag")
        else:
            print("No </style> tag found")
