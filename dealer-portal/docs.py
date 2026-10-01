"""Document library definitions, card renderer, and placeholder file generation."""
import pathlib, zipfile, io

ROOT = pathlib.Path(__file__).parent
DOC_DIR = ROOT / "assets/docs"

REAL_PRICE_BOOK = "quick-reference-bathroom-price-book-august-2026.pdf"

# cover: ("image", path) or (palette, icon, caption)
SERIES_BOOKS = [
    {"title": "Price books by series", "note": "April 01 2026 editions. Quote from these.", "docs": [
        {"file": "crush-price-book-april-2026.pdf", "name": "Crush Price Book", "desc": "Crush vanities CRU24–CRU72D, linen cabinets and matching countertops.", "edition": "April 01 2026", "cover": ("image", "assets/covers/pricebook-crush-apr-2026.jpg", "portrait"), "badge": "Current"},
        {"file": "fundamentals-price-book-april-2026.pdf", "name": "Fundamentals Price Book", "desc": "Fundamentals vanities, drawer bases, wall and medicine cabinets, make-up table drawers and mirrors.", "edition": "April 01 2026", "cover": ("image", "assets/covers/pricebook-fundamentals-apr-2026.jpg", "portrait"), "badge": "Current"},
        {"file": "evolution-price-book-april-2026.pdf", "name": "Evolution Price Book", "desc": "Evolution I, Evolution II and Evolution III vanities with legs and full panel.", "edition": "April 01 2026", "cover": ("image", "assets/covers/pricebook-evolution-apr-2026.jpg", "portrait"), "badge": "Current"},
        {"file": "contempo-price-book-april-2026.pdf", "name": "Contempo Price Book", "desc": "Contempo slab-front vanities with legs and full panel, plus linen cabinets.", "edition": "April 01 2026", "cover": ("image", "assets/covers/pricebook-contempo-apr-2026.jpg", "portrait"), "badge": "Current"},
        {"file": "all-in-one-bathroom-cabinetry-price-book-april-2026.pdf", "name": "All-in-One Bathroom Cabinetry Price Book", "desc": "Every bathroom series in one book: Crush, Fundamentals, Evolution and Contempo vanities, linen cabinets, mirrors and countertops.", "edition": "April 01 2026", "cover": ("image", "assets/covers/pricebook-all-in-one-bathroom-apr-2026.jpg", "portrait"), "badge": "Current"},
    ]},
]

# Catalog and Design library temporarily mirror the price book page.
DOCS = {"price-book": SERIES_BOOKS, "catalog": SERIES_BOOKS, "design-library": SERIES_BOOKS}


def human_size(n):
    return f"{n / 1024 / 1024:.1f} MB" if n >= 1024 * 1024 else f"{max(1, round(n / 1024))} KB"


def doc_card(d):
    path = DOC_DIR / d["file"]
    kind = d.get("kind", "pdf").upper()
    # Placeholder files are tiny; show only the format until the published file replaces them.
    size = human_size(path.stat().st_size) if path.exists() and path.stat().st_size > 20_000 else None
    pages = d.get("pages")
    if d["cover"][0] == "image":
        cover = f'<img src="{d["cover"][1]}" alt="" loading="lazy">'
        cover_cls = " portrait" if len(d["cover"]) > 2 and d["cover"][2] == "portrait" else ""
    else:
        palette, icon, caption = d["cover"]
        cover = f'<span class="cover-mark"><svg class="icon"><use href="#{icon}"/></svg><span>{caption}</span></span>'
        cover_cls = " " + palette
    badge = f'<span class="doc-badge{" soft" if d.get("badge_soft") else ""}">{d["badge"]}</span>' if d.get("badge") else ""
    meta = [f'<span><svg class="icon"><use href="#i-calendar"/></svg>{d["edition"]}</span>', f'<span><svg class="icon"><use href="#i-file"/></svg>{kind}{" · " + size if size else ""}</span>']
    if pages:
        meta.append(f'<span><svg class="icon"><use href="#i-pages"/></svg>{pages} pages</span>')
    href = f'assets/docs/{d["file"]}'
    open_btn = "" if kind == "ZIP" else f'<a class="table-action" href="{href}" target="_blank" rel="noopener"><svg class="icon" width="14" height="14"><use href="#i-external"/></svg>Open</a>'
    return f'''<article class="doc-card">
  <div class="doc-cover{cover_cls}">{cover}{badge}</div>
  <div class="doc-body">
    <h3>{d["name"]}</h3>
    <p>{d["desc"]}</p>
    <div class="doc-meta">{"".join(meta)}</div>
    <div class="doc-actions">
      <a class="table-action primary" href="{href}" download data-download-note="{d["file"]}"><svg class="icon" width="14" height="14"><use href="#i-download"/></svg>Download</a>
      {open_btn}
    </div>
  </div>
</article>'''


# ---------------------------------------------------------------- placeholder files
def make_placeholder_pdf(path, title, subtitle):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor
    c = canvas.Canvas(str(path), pagesize=letter)
    w, h = letter
    c.setFillColor(HexColor("#181611")); c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setFillColor(HexColor("#e4cea4"))
    c.setFont("Helvetica", 11); c.drawCentredString(w / 2, h - 90, "C L A S S I C   B R A N D   C A B I N E T R Y")
    c.setFont("Helvetica-Bold", 26); c.drawCentredString(w / 2, h / 2 + 30, title)
    c.setFont("Helvetica", 13); c.drawCentredString(w / 2, h / 2, subtitle)
    c.setFillColor(HexColor("#ffffff")); c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, 80, "Placeholder document — replace this file with the published PDF of the same name.")
    c.drawCentredString(w / 2, 66, "assets/docs/" + path.name)
    c.showPage(); c.save()


def make_placeholder_zip(path, title):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.txt", f"{title}\n\nPlaceholder package — replace assets/docs/{path.name} with the published catalog files.\n")


def ensure_placeholders():
    DOC_DIR.mkdir(parents=True, exist_ok=True)
    (DOC_DIR / "invoices").mkdir(exist_ok=True)
    for group in DOCS.values():
        for sec in group:
            for d in sec["docs"]:
                p = DOC_DIR / d["file"]
                if p.exists():
                    continue
                if d.get("kind") == "zip":
                    make_placeholder_zip(p, d["name"])
                else:
                    make_placeholder_pdf(p, d["name"].replace("&amp;", "&"), d["edition"])
    for inv in ["INV-30412", "INV-30398", "INV-30371", "INV-30355", "INV-30340", "INV-30322", "INV-30301", "INV-30288"]:
        p = DOC_DIR / "invoices" / f"{inv}.pdf"
        if not p.exists():
            make_placeholder_pdf(p, f"Invoice {inv}", "Dealer CB-20418 · Classic Brand Cabinetry")


if __name__ == "__main__":
    ensure_placeholders()
    print("placeholders ready")
