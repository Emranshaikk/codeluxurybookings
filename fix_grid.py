import os

css_path = r"c:\Users\imran\OneDrive\Desktop\ELB code\assets\css\style.css"

grid_styles = """
/* --- GRID 2 AND LUXURY LIST FIX --- */
.grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
}
@media (max-width: 1024px) {
    .grid-2 {
        grid-template-columns: 1fr;
    }
}
ul.luxury-list {
    list-style-type: none !important;
    padding-left: 0;
}
ul.luxury-list li {
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
}
ul.luxury-list li::before {
    content: '✓' !important;
    color: var(--primary-gold);
    font-weight: bold;
    font-family: Arial, sans-serif;
}
"""

with open(css_path, "a", encoding="utf-8") as f:
    f.write(grid_styles)
print("Grid and List styles updated.")
