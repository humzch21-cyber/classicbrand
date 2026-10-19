#!/usr/bin/env python3
"""Generates the dealer portal pages from a shared shell so the topbar and sidebar stay identical."""
import base64, pathlib, importlib

ROOT = pathlib.Path(__file__).parent
LOGO_URI = "data:image/png;base64," + base64.b64encode((ROOT / "assets/classicbrand-logo.png").read_bytes()).decode()

ICONS = """
<svg class="sr-only" aria-hidden="true" focusable="false">
  <symbol id="i-grid" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></symbol>
  <symbol id="i-file" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h6"/></symbol>
  <symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></symbol>
  <symbol id="i-user" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></symbol>
  <symbol id="i-help" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M9.7 9a2.5 2.5 0 1 1 4 2c-.9.7-1.7 1.2-1.7 2.5M12 17h.01"/></symbol>
  <symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></symbol>
  <symbol id="i-bell" viewBox="0 0 24 24"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M10 21h4"/></symbol>
  <symbol id="i-cart" viewBox="0 0 24 24"><path d="M3 4h2l2.2 10.2a2 2 0 0 0 2 1.6h7.8a2 2 0 0 0 2-1.6L20.5 8H6"/><circle cx="10" cy="20" r="1"/><circle cx="18" cy="20" r="1"/></symbol>
  <symbol id="i-chevron" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></symbol>
  <symbol id="i-down" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></symbol>
  <symbol id="i-edit" viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L8 18l-4 1 1-4z"/></symbol>
  <symbol id="i-printer" viewBox="0 0 24 24"><path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></symbol>
  <symbol id="i-close" viewBox="0 0 24 24"><path d="m6 6 12 12M18 6 6 18"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path d="m5 12 4 4L19 6"/></symbol>
  <symbol id="i-tag" viewBox="0 0 24 24"><path d="M20 13 13 20a2 2 0 0 1-3 0l-6-6a2 2 0 0 1 0-3V4h7a2 2 0 0 1 1.4.6l7.6 7.6a1 1 0 0 1 0 .8Z"/><circle cx="8.5" cy="8.5" r="1"/></symbol>
  <symbol id="i-calendar" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></symbol>
  <symbol id="i-box" viewBox="0 0 24 24"><path d="m12 3 9 5-9 5-9-5zM3 8v9l9 5 9-5V8M12 13v9"/></symbol>
  <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
  <symbol id="i-logout" viewBox="0 0 24 24"><path d="M10 17l5-5-5-5M15 12H3M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/></symbol>
  <symbol id="i-book" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><path d="M9 7h7M9 11h5"/></symbol>
  <symbol id="i-catalog" viewBox="0 0 24 24"><path d="M2 4h6a4 4 0 0 1 4 4v12a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v12a3 3 0 0 1 3-3h7z"/></symbol>
  <symbol id="i-palette" viewBox="0 0 24 24"><path d="M12 3a9 9 0 1 0 0 18c1.4 0 2-.8 2-1.8 0-.6-.3-1-.3-1.5 0-1 .8-1.7 1.8-1.7H17a4 4 0 0 0 4-4c0-5-4-9-9-9z"/><circle cx="7.5" cy="11.5" r="1"/><circle cx="10.5" cy="7.5" r="1"/><circle cx="15" cy="7.5" r="1"/></symbol>
  <symbol id="i-download" viewBox="0 0 24 24"><path d="M12 4v11M7 10l5 5 5-5M4 19h16"/></symbol>
  <symbol id="i-home" viewBox="0 0 24 24"><path d="m3 11 9-7 9 7"/><path d="M5 10v10h14V10M10 20v-6h4v6"/></symbol>
  <symbol id="i-truck" viewBox="0 0 24 24"><path d="M3 6h11v10H3zM14 9h4l3 3.5V16h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></symbol>
  <symbol id="i-tool" viewBox="0 0 24 24"><path d="M14.5 6.5a4 4 0 0 0 5 5L12 19a2.1 2.1 0 0 1-3-3l7.5-7.5"/><path d="M14.5 6.5 17 4l3 3-2.5 2.5"/></symbol>
  <symbol id="i-swap" viewBox="0 0 24 24"><path d="M4 8h13l-3.5-3.5M20 16H7l3.5 3.5"/></symbol>
  <symbol id="i-headset" viewBox="0 0 24 24"><path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="13" width="4" height="6" rx="1.5"/><rect x="17" y="13" width="4" height="6" rx="1.5"/><path d="M19 19c0 1.5-2 2.5-5 2.5"/></symbol>
  <symbol id="i-play" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="m10 8.5 5.5 3.5-5.5 3.5z"/></symbol>
  <symbol id="i-back" viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6"/></symbol>
  <symbol id="i-cube" viewBox="0 0 24 24"><path d="m12 3 8 4.5v9L12 21l-8-4.5v-9z"/><path d="m4 7.5 8 4.5 8-4.5M12 12v9"/></symbol>
  <symbol id="i-external" viewBox="0 0 24 24"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></symbol>
  <symbol id="i-kitchen" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="1.5"/><path d="M3 12h18M12 3v9M8 16h2M14 16h2"/></symbol>
  <symbol id="i-vanity" viewBox="0 0 24 24"><rect x="3" y="9" width="18" height="11" rx="1.5"/><path d="M3 13h18M12 13v7M8 4v5M16 4v5M8 4h8"/><circle cx="12" cy="6.5" r="1"/></symbol>
  <symbol id="i-invoice" viewBox="0 0 24 24"><path d="M6 2h12v20l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h4"/></symbol>
  <symbol id="i-pages" viewBox="0 0 24 24"><path d="M8 3h9l4 4v11a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M17 3v4h4M4 7v13a2 2 0 0 0 2 2h11"/></symbol>
  <symbol id="i-swatch" viewBox="0 0 24 24"><path d="M4 3h6v14a3 3 0 0 1-6 0z"/><path d="m10 8 4.2-4.2 4.3 4.3L10 16.5M13.5 21H21v-6h-4"/><circle cx="7" cy="17" r="1"/></symbol>
  <symbol id="i-layers" viewBox="0 0 24 24"><path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5M3 17l9 5 9-5"/></symbol>
  <symbol id="i-cab-wall" viewBox="0 0 24 24"><rect x="7" y="2.5" width="10" height="19" rx="1"/><path d="M12 2.5v19M10 11v3M14 11v3"/></symbol>
  <symbol id="i-cab-base" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="15" rx="1"/><path d="M3 9.5h18M12 9.5V20M9 14v2.5M15 14v2.5M2 21h20"/></symbol>
  <symbol id="i-cab-drawer" viewBox="0 0 24 24"><rect x="5" y="4" width="14" height="17" rx="1"/><path d="M5 9.5h14M5 15h14M10.5 6.75h3M10.5 12.25h3M10.5 18h3"/></symbol>
  <symbol id="i-cab-tall" viewBox="0 0 24 24"><rect x="7" y="2" width="10" height="20" rx="1"/><path d="M7 12h10M10 7v2M10 16v2"/></symbol>
  <symbol id="i-cab-vanity" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="13" rx="1"/><path d="M2 5h20M8 7v13M16 7v13M8 11.5h8M5 12.5v2M19 12.5v2"/></symbol>
  <symbol id="i-cab-legs" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="11" rx="1"/><path d="M3 3.5h18M12 5v11M9 9.5v2M15 9.5v2M5 16v5M19 16v5"/></symbol>
  <symbol id="i-mirror" viewBox="0 0 24 24"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="m8.5 16 7-9"/></symbol>
  <symbol id="i-counter" viewBox="0 0 24 24"><path d="M2 9h20v4H2z"/><path d="M8 13v7M16 13v7M12 5v4"/></symbol>
  <symbol id="i-panel" viewBox="0 0 24 24"><rect x="9" y="2" width="6" height="20" rx=".8"/><path d="M12 2v20"/></symbol>
  <symbol id="i-door" viewBox="0 0 24 24"><rect x="6" y="2" width="12" height="20" rx="1"/><rect x="8.5" y="4.5" width="7" height="15" rx=".5"/><path d="M14 12h.01"/></symbol>
  <symbol id="i-glass" viewBox="0 0 24 24"><rect x="6" y="2" width="12" height="20" rx="1"/><path d="m8.5 13 6-8M9.5 19l7-10"/></symbol>
  <symbol id="i-hardware" viewBox="0 0 24 24"><rect x="2.5" y="8" width="19" height="3.2" rx="1.6"/><path d="M6.5 11.2v4.3M17.5 11.2v4.3M4.8 15.5h3.4M15.8 15.5h3.4"/></symbol>
  <symbol id="i-trash" viewBox="0 0 24 24"><path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13M10 11v6M14 11v6"/></symbol>
  <symbol id="i-zip" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M10 6h2M10 9h2M10 12h2M10 15h2M10 18h2"/></symbol>
</svg>
"""

NAV = [
    ("Workspace", [
        ("index.html",     "i-grid",    "Overview",     None),
        ("orders.html",    "i-file",    "Orders",       '<span class="nav-count" data-count="orders">12</span>'),
        ("new-order.html", "i-plus",    "New order",    None),
        ("https://classicbrand.ca/3d-bathroom-cabinet-configurator/", "i-cube", "Vanity configurator", '<svg class="icon nav-ext"><use href="#i-external"/></svg>'),
        ("invoices.html",  "i-invoice", "My invoices",  '<span class="nav-count alert">1</span>'),
    ]),
    ("Documents", [
        ("price-book.html",     "i-book",    "Price book",     None),
        ("catalog.html",        "i-catalog", "Catalog",        None),
        ("design-library.html", "i-palette", "Design library", None),
    ]),
    # Dealer support mirrors the "Support for retailers" pages of classicbrand.ca, so dealers never leave the portal for them
    ("Dealer support", [
        ("support.html",             "i-headset", "Customer support",    None),
        ("support-delivery.html",    "i-truck",   "Delivery service",    None),
        ("support-assembly.html",    "i-tool",    "Assembly service",    None),
        ("support-videos.html",      "i-play",    "Assembly videos",     None),
        ("support-replacement.html", "i-swap",    "Product replacement", None),
        ("inventory.html",           "i-layers",  "Inventory checking",  None),
    ]),
]


def sidebar(active):
    parts = ['<aside class="sidebar" id="sidebar" aria-label="Portal navigation">',
             '<a class="nav-link mobile-switch" href="https://classicbrand.ca/"><svg class="icon"><use href="#i-home"/></svg>Back to main website</a>']
    for i, (label, items) in enumerate(NAV):
        if i:
            parts.append('<div class="sidebar-rule"></div>')
        parts.append(f'<p class="nav-label">{label}</p><nav class="nav-list">')
        for href, icon, text, extra in items:
            is_active = href == active or (href == "new-order.html" and active.startswith("new-order")) or (href == "orders.html" and active == "order.html")
            cls = "nav-link active" if is_active else "nav-link"
            aria = ' aria-current="page"' if is_active else ""
            ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
            parts.append(f'<a class="{cls}" href="{href}"{aria}{ext}><svg class="icon"><use href="#{icon}"/></svg>{text}{extra or ""}</a>')
        parts.append('</nav>')
    prof = ' class="active" aria-current="page"' if active == "profile.html" else ""
    parts.append('''<div class="dealer-card">
  <div class="dealer-name">Humphrey</div>
  <div class="dealer-id">Dealer ID · CB-20418</div>
  <div class="dealer-actions"><a href="profile.html"{prof}><svg class="icon" width="14" height="14"><use href="#i-user"/></svg>Profile</a><button id="signOut"><svg class="icon" width="14" height="14"><use href="#i-logout"/></svg>Sign out</button></div>
</div></aside>
<div class="sidebar-backdrop"></div>'''.replace("{prof}", prof))
    return "\n".join(parts)


def shell(*, file, title, crumb, content, script="", head=""):
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Classic Brand dealer order portal — {crumb}">
  <title>{title} — Classic Brand Cabinetry</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&amp;family=Manrope:wght@400;500;600;700&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/portal.css">
  {head}
</head>
<body>
{ICONS}
<div class="app-shell">
  <header class="topbar">
    <a class="brand" href="index.html" aria-label="Classic Brand Cabinetry — Overview">
      <img src="{LOGO_URI}" alt="">
    </a>
    <button class="mobile-menu" aria-label="Open menu" aria-controls="sidebar" aria-expanded="false"><svg class="icon"><use href="#i-menu"/></svg></button>
    <div class="topbar-main">
      <div class="topbar-context"><span class="eyebrow">Dealer portal</span><span class="slash">/</span><strong>{crumb}</strong></div>
      <div class="top-actions">
        <nav class="portal-switch" aria-label="Switch site">
          <a href="https://classicbrand.ca/" class="ps-item"><svg class="icon"><use href="#i-home"/></svg><span>Main website</span></a>
          <span class="ps-item active" aria-current="page"><svg class="icon"><use href="#i-grid"/></svg><span>Dealer portal</span></span>
        </nav>
        <button class="top-action" aria-label="Notifications"><svg class="icon"><use href="#i-bell"/></svg></button>
        <a class="top-action" href="new-order.html" data-cart-link><svg class="icon"><use href="#i-cart"/></svg><span class="label">Cart · <span data-cart-count>0</span></span></a>
        <a class="avatar" href="profile.html" title="Profile" aria-label="Profile">H</a>
      </div>
    </div>
  </header>

{sidebar(file)}

  <main>
    <div class="page">
{content}
    </div>
  </main>
</div>

<div class="toast-region" id="toastRegion" aria-live="polite" aria-atomic="true"></div>
<script src="assets/sample-orders.js"></script>
<script src="assets/portal.js"></script>
<script src="assets/vanity-book.js"></script>
<script src="assets/catalog.js"></script>
<script src="assets/order-summary.js"></script>
{script}
</body>
</html>
'''


NEW_ORDER_MENU = '''
<div class="new-order-wrap">
  <button class="primary-button" id="newOrderButton" aria-expanded="false" aria-controls="orderMenu">
    <svg class="icon"><use href="#i-plus"/></svg>New order<svg class="icon" width="15" height="15"><use href="#i-down"/></svg>
  </button>
  <div class="order-menu" id="orderMenu" role="menu">
    <a role="menuitem" href="new-order.html?line=kitchen">
      <span class="menu-icon"><svg class="icon"><use href="#i-kitchen"/></svg></span>
      <span><strong>Kitchen</strong><small>Choose a series, then add cabinets</small></span>
      <svg class="icon"><use href="#i-chevron"/></svg>
    </a>
    <a role="menuitem" href="new-order.html?line=vanity">
      <span class="menu-icon"><svg class="icon"><use href="#i-vanity"/></svg></span>
      <span><strong>Vanity</strong><small>Choose a series, then add vanities</small></span>
      <svg class="icon"><use href="#i-chevron"/></svg>
    </a>
    <a role="menuitem" href="new-order-vanity-top.html?series=vanity-top">
      <span class="menu-icon"><svg class="icon"><use href="#i-counter"/></svg></span>
      <span><strong>Vanity top</strong><small>Quartz &amp; sintered stone tops · pick the top, then the size</small></span>
      <svg class="icon"><use href="#i-chevron"/></svg>
    </a>
    <a role="menuitem" href="new-order-products.html?series=hardware">
      <span class="menu-icon"><svg class="icon"><use href="#i-hardware"/></svg></span>
      <span><strong>Hardware</strong><small>Handles, knobs, LED and parts · standard and premium</small></span>
      <svg class="icon"><use href="#i-chevron"/></svg>
    </a>
  </div>
</div>'''


if __name__ == "__main__":
    pages = importlib.import_module("pages")
    for file, html in pages.build(shell, NEW_ORDER_MENU).items():
        (ROOT / file).write_text(html, encoding="utf-8")
        print("wrote", file)
