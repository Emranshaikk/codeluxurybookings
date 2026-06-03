import os
import re

files = [
    "all-inclusive-private-island-rental.html",
    "bahamas-private-island-rental.html",
    "caribbean-private-island-rental.html",
    "exclusive-private-island-rental.html",
    "luxury-private-island-rental.html",
    "maldives-private-island-rental.html",
    "private-island-for-rent.html"
]

directory = r"c:\Users\imran\OneDrive\Desktop\ELB code"

style_override = """
        /* Floating WhatsApp Button Override */
        .wa-float {
            position: fixed !important;
            bottom: 30px !important;
            right: 30px !important;
            background: #25D366 !important;
            color: #FFF !important;
            width: 60px !important;
            height: 60px !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            z-index: 100000 !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s ease !important;
            text-decoration: none !important;
        }

        .wa-float:hover {
            transform: scale(1.1) !important;
            background: #128C7E !important;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4) !important;
        }

        .wa-float svg {
            width: 32px !important;
            height: 32px !important;
            fill: currentColor !important;
            display: block !important;
        }
"""

for filename in files:
    path = os.path.join(directory, filename)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        # Check if style override is already present
        if "Floating WhatsApp Button Override" in content:
            print(f"{filename}: Override already present.")
            continue
            
        if "</style>" in content:
            # Inject right before the closing </style> tag
            content = content.replace("</style>", style_override + "\n    </style>")
            
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
            except UnicodeEncodeError:
                with open(path, 'w', encoding='latin-1') as f:
                    f.write(content)
            print(f"Fixed {filename} successfully!")
        else:
            print(f"ERROR: {filename} does not contain </style> tag!")
    else:
        print(f"{filename} not found.")
