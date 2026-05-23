import re

FOOTER_CSS = """        /* ===== MASTER FOOTER (INJECTED SITE-WIDE) ===== */
        .footer { background: #000 !important; padding: 5rem 0 3rem !important; border-top: 1px solid rgba(212, 175, 55, 0.1) !important; margin-top: 5rem !important; text-align: left !important; }
        .footer-grid { display: grid !important; grid-template-columns: 2fr 1fr 1fr !important; gap: 4rem !important; padding-bottom: 4rem !important; border-bottom: 1px solid rgba(212, 175, 55, 0.1) !important; text-align: left !important; }
        .footer-brand { text-align: left !important; }
        .footer-brand h2 { font-family: 'Cormorant Garamond', serif !important; font-size: 2.2rem !important; margin-bottom: 1.5rem !important; color: #fff !important; text-align: left !important; }
        .footer-brand p { font-family: 'Inter', sans-serif !important; font-size: 0.9rem !important; line-height: 1.8 !important; max-width: 380px !important; margin-bottom: 2rem !important; color: rgba(255, 255, 255, 0.7) !important; text-align: left !important; }
        .footer-socials { display: flex !important; gap: 1.5rem !important; justify-content: flex-start !important; }
        .footer-socials a { color: rgba(255, 255, 255, 0.6) !important; transition: 0.3s !important; font-size: 1.5rem !important; }
        .footer-socials a:hover { color: #D4AF37 !important; }
        .footer-col { text-align: left !important; }
        .footer-col h4 { color: #D4AF37 !important; text-transform: uppercase !important; letter-spacing: 2px !important; font-size: 0.9rem !important; margin-bottom: 2rem !important; text-align: left !important; }
        .footer-col ul { list-style: none !important; padding: 0 !important; margin: 0 !important; text-align: left !important; }
        .footer-col ul li { margin-bottom: 1rem !important; text-align: left !important; }
        .footer-col ul li a { color: rgba(255, 255, 255, 0.8) !important; text-decoration: none !important; transition: 0.3s !important; font-size: 0.95rem !important; }
        .footer-col ul li a:hover { color: #D4AF37 !important; padding-left: 5px !important; }
        .footer-bottom { display: flex !important; justify-content: space-between !important; align-items: center !important; padding-top: 3rem !important; color: rgba(255, 255, 255, 0.4) !important; font-size: 0.85rem !important; }
        .footer-legal { display: flex !important; gap: 2rem !important; }
        .footer-legal a { color: inherit !important; text-decoration: none !important; }
        @media (max-width: 992px) { 
            .footer-grid { grid-template-columns: 1fr 1fr !important; } 
            .footer-brand { grid-column: span 2 !important; } 
        }
        @media (max-width: 600px) { 
            .footer-grid { grid-template-columns: 1fr !important; } 
            .footer-brand { grid-column: span 1 !important; text-align: center !important; } 
            .footer-brand h2 { text-align: center !important; }
            .footer-brand p { text-align: center !important; margin: 0 auto 2rem auto !important; }
            .footer-socials { justify-content: center !important; }
            .footer-col { text-align: center !important; }
            .footer-col h4 { text-align: center !important; }
            .footer-col ul { text-align: center !important; }
            .footer-col ul li { text-align: center !important; }
            .footer-bottom { flex-direction: column !important; gap: 2rem !important; text-align: center !important; } 
        }"""

def fix_template(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Clean out all blocks containing the header string
    pattern = re.compile(r'/\*\s*===\s*MASTER FOOTER \(INJECTED SITE-WIDE\)\s*===\s*\*/.*?(?=\n\s*(?:</style>|\Z))', re.DOTALL)
    content = pattern.sub('', content)

    # 2. Find the last </style> tag in the file
    last_style_idx = content.rfind('</style>')
    if last_style_idx == -1:
        print(f"Error: No </style> tag found in {path}")
        return False

    # 3. Inject exactly one clean copy of FOOTER_CSS before the last </style>
    new_content = content[:last_style_idx] + FOOTER_CSS + "\n    " + content[last_style_idx:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully cleaned and updated template: {path}")
    return True

def main():
    fix_template('_template_master.html')
    fix_template('_template_blog_master.html')

if __name__ == '__main__':
    main()
