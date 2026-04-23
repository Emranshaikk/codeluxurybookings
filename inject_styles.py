import os

premium_css = """
        /* --- PREMIUM FLEET CARD REDESIGN --- */
        .fleet-card {
            padding: 3.5rem 2.5rem !important;
            background: rgba(10, 10, 10, 0.85) !important;
            border: 1px solid rgba(212, 175, 55, 0.2) !important;
            border-radius: 24px !important;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            text-align: center;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            backdrop-filter: blur(20px);
        }

        .fleet-card:hover {
            transform: translateY(-12px);
            border-color: #D4AF37 !important;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.7);
            background: rgba(15, 15, 15, 0.95) !important;
        }

        .fleet-card .type {
            font-family: 'Cormorant Garamond', serif !important;
            font-size: 2.4rem !important;
            color: #D4AF37 !important;
            margin-bottom: 1.5rem;
            font-weight: 500;
            letter-spacing: 1.5px;
            line-height: 1.2;
        }

        .fleet-card .desc {
            font-size: 1.1rem !important;
            color: rgba(255, 255, 255, 0.8) !important;
            line-height: 1.8 !important;
            margin: 0;
            font-family: 'Inter', sans-serif !important;
        }
"""

def inject():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    count = 0
    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'fleet-card' in content and 'PREMIUM FLEET CARD REDESIGN' not in content:
            if '</style>' in content:
                new_content = content.replace('</style>', premium_css + '\n    </style>')
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
    print(f"Successfully updated {count} files.")

if __name__ == "__main__":
    inject()
