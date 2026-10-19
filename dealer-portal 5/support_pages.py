"""Dealer support pages — the "Support for retailers" pages of classicbrand.ca, rebuilt inside the portal.

Source pages (main website):
  support-retailers-customer-support   → support.html
  support-retailers-delivery-service   → support-delivery.html
  support-retailers-assembly-service   → support-assembly.html
  support-retailers-assembly-video     → support-videos.html
  support-retailers-product-replacement → support-replacement.html
  support-retailers-inventory-checking → inventory.html (already in the portal)
"""

MAIN = "https://classicbrand.ca/"


def heading(kicker, title, lede, source):
    return f'''
<section class="page-heading">
  <div>
    <p class="kicker">{kicker}</p>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
  <div class="heading-actions"><a class="quiet-button" href="{MAIN}{source}" target="_blank" rel="noopener"><svg class="icon"><use href="#i-external"/></svg>Same page on classicbrand.ca</a></div>
</section>'''


# Tiles shown on every support page so dealers can move between them without the sidebar (mobile)
SUPPORT_LINKS = [
    ("support.html", "i-headset", "Customer support", "Your CSR and what dealers receive"),
    ("support-delivery.html", "i-truck", "Delivery service", "Delivery, pickup and loading"),
    ("support-assembly.html", "i-tool", "Assembly service", "Cabinets delivered assembled"),
    ("support-videos.html", "i-play", "Assembly videos", "Step-by-step assembly"),
    ("support-replacement.html", "i-swap", "Product replacement", "Damaged or defective parts"),
    ("inventory.html", "i-layers", "Inventory checking", "Stock pages by colour code"),
]


def support_tabs(active):
    return '<nav class="support-tabs" aria-label="Dealer support pages">' + "".join(
        f'<a class="support-tab{" active" if href == active else ""}" href="{href}"{" aria-current=\"page\"" if href == active else ""}><svg class="icon"><use href="#{icon}"/></svg>{name}</a>'
        for href, icon, name, _ in SUPPORT_LINKS) + '</nav>'


# ---------------------------------------------------------------- Customer support
DEALER_BENEFITS = [
    ("i-book", "Price books", "Electronic and hard copy"),
    ("i-catalog", "Electronic catalogs", "Every series, door style and finish"),
    ("i-palette", "2020 design libraries", "For your designers' layouts"),
    ("i-cart", "Online ordering system", "This portal"),
    ("i-file", "Excel order forms", "For offline order preparation"),
    ("i-swatch", "High-resolution images", "For your marketing"),
    ("i-user", "Outside sales representatives", "Visits and product training"),
    ("i-headset", "In-house customer service team", "Orders, changes and questions"),
    ("i-home", "Corporate showroom", "Bring your clients"),
    ("i-tag", "Authorized dealer network only", "No direct sales to end users"),
    ("i-edit", "Design support", "Provided through dealers"),
    ("i-truck", "Delivery within 170 km", "On Classic Brand trucks"),
]


def customer_support(menu):
    content = heading("Dealer support", "Customer support",
                      "Fast answers on enquiries and orders, help choosing products and running promotions, and problem solving when something goes wrong.",
                      "support-retailers-customer-support") + support_tabs("support.html") + '''
<div class="support-grid">
  <section class="order-card">
    <div class="order-card-head"><div><span class="step-label">Your CSR</span><h3>Customer service representative</h3></div></div>
    <div class="order-card-body">
      <div class="confirm-details" style="margin:0;font-size:12px">
        <div><span>Name</span><strong data-sap="csr_name">Aria</strong></div>
        <div><span>Email</span><strong><a href="mailto:support@classicbrand.ca" data-sap="csr_email">support@classicbrand.ca</a></strong></div>
        <div><span>Phone</span><strong data-sap="csr_phone">905 232 4660 ext. 214</strong></div>
        <div><span>Work hours</span><strong>Mon–Fri · 8:00–17:00 ET</strong></div>
      </div>
    </div>
  </section>
  <section class="order-card">
    <div class="order-card-head"><div><span class="step-label">Before you write</span><h3>Common requests</h3></div></div>
    <div class="order-card-body">
      <a class="start-option" href="orders.html?status=draft"><span class="start-icon"><svg class="icon"><use href="#i-edit"/></svg></span><span><strong>Check a draft quote before placing</strong><small>Send the Q-number; the team reviews configuration and pricing</small></span><svg class="icon"><use href="#i-chevron"/></svg></a>
      <a class="start-option" href="support-replacement.html"><span class="start-icon"><svg class="icon"><use href="#i-swap"/></svg></span><span><strong>Damaged or defective product</strong><small>Request a replacement part with photos</small></span><svg class="icon"><use href="#i-chevron"/></svg></a>
      <a class="start-option" href="invoices.html"><span class="start-icon"><svg class="icon"><use href="#i-invoice"/></svg></span><span><strong>Billing or invoice question</strong><small>Quote the INV-number from My invoices</small></span><svg class="icon"><use href="#i-chevron"/></svg></a>
    </div>
  </section>
</div>

<section class="panel support-section">
  <header class="support-section-head"><span class="step-label">Partnership</span><h2>What every Classic Brand dealer receives</h2></header>
  <div class="benefit-grid">''' + "".join(
        f'<div class="benefit"><span class="benefit-icon"><svg class="icon"><use href="#{i}"/></svg></span><span><strong>{t}</strong><small>{d}</small></span></div>'
        for i, t, d in DEALER_BENEFITS) + '''</div>
</section>'''
    return content, ""


# ---------------------------------------------------------------- Delivery service
def delivery(menu):
    methods = [
        ("i-home", "Pick up by dealer", "Free", "Collect at the Classic Brand dock during pickup hours."),
        ("i-truck", "CBC truck stand delivery", "Within 170 km", "Classic Brand truck, stand delivery to your address."),
        ("i-box", "Pick up by DC", "", "Released to your distribution centre."),
        ("i-file", "Pick up by third party", "", "Your carrier collects — put the carrier name on the PO."),
    ]
    content = heading("Dealer support", "Delivery service",
                      "Choose how each order leaves our warehouse when you place it. Classic Brand trucks deliver within 170 km of our head office.",
                      "support-retailers-delivery-service") + support_tabs("support-delivery.html") + '''
<section class="panel support-section">
  <header class="support-section-head"><span class="step-label">Shipping method</span><h2>Four ways to receive an order</h2><p>Picked at checkout, step 3 of a new order.</p></header>
  <div class="method-grid">''' + "".join(
        f'<div class="method-card"><span class="benefit-icon"><svg class="icon"><use href="#{i}"/></svg></span><strong>{t}</strong>{f"<span class=\"status ready\">{b}</span>" if b else ""}<small>{d}</small></div>'
        for i, t, b, d in methods) + '''</div>
</section>

<div class="support-grid">
  <section class="order-card">
    <div class="order-card-head"><div><span class="step-label">Load truck method</span><h3>How the order is loaded</h3></div></div>
    <div class="order-card-body">
      <div class="fact-list">
        <div><strong>Load product with skids</strong><small>Needs a dock or forklift at the destination.</small></div>
        <div><strong>Hand carry product with truck</strong><small>Loaded and unloaded piece by piece.</small></div>
      </div>
    </div>
  </section>
  <section class="order-card">
    <div class="order-card-head"><div><span class="step-label">Timing</span><h3>Ready date</h3></div></div>
    <div class="order-card-body">
      <ol class="step-list">
        <li><strong>Pick a shipping ready date</strong><small>At checkout, from the available dates.</small></li>
        <li><strong>Order desk confirms</strong><small>The confirmed date is emailed and shown on the order.</small></li>
        <li><strong>Inspect on arrival</strong><small>Report damage within 7 business days — <a href="support-replacement.html">request a replacement</a>.</small></li>
      </ol>
    </div>
  </section>
</div>'''
    return content, ""


# ---------------------------------------------------------------- Assembly service
def assembly(menu):
    content = heading("Dealer support", "Assembly service",
                      "We assemble cabinets on request so they arrive ready to install. Assembly is completed within 10 business days.",
                      "support-retailers-assembly-service") + support_tabs("support-assembly.html") + '''
<div class="assembly-hero panel">
  <div class="assembly-stat"><strong>10</strong><span>business days<br>to assemble</span></div>
  <div class="assembly-stat"><strong>100%</strong><span>assembled and checked<br>before it ships</span></div>
  <div class="assembly-stat"><strong>Per piece</strong><span>assembly price shown<br>on every SKU</span></div>
</div>

<div class="support-grid">
  <section class="order-card">
    <div class="order-card-head"><div><span class="step-label">How to request it</span><h3>Three steps in the order flow</h3></div></div>
    <div class="order-card-body">
      <ol class="step-list">
        <li><strong>Add the cabinets</strong><small>Each SKU shows its assembly price under the dealer price.</small></li>
        <li><strong>Choose “Assembly required: Yes”</strong><small>In View summary &amp; checkout — it is never pre-selected.</small></li>
        <li><strong>Place the order</strong><small>Assembly is added to the total and the ready date allows for it.</small></li>
      </ol>
      <a class="primary-button" href="new-order.html" style="margin-top:18px;width:max-content"><svg class="icon"><use href="#i-plus"/></svg>Start a new order</a>
    </div>
  </section>
  <section class="order-card">
    <div class="order-card-head"><div><span class="step-label">What you get</span><h3>Accurate, fast, ready to install</h3></div></div>
    <div class="order-card-body">
      <div class="fact-list">
        <div><strong>Fully assembled boxes</strong><small>Built and squared in our facility.</small></div>
        <div><strong>Hardware as configured</strong><small>Vanity knobs and handles follow the hardware instruction you chose.</small></div>
        <div><strong>Prefer flat-pack?</strong><small>Choose “No” and the order ships flat-packed — see <a href="support-videos.html">assembly videos</a>.</small></div>
      </div>
    </div>
  </section>
</div>'''
    return content, ""


# ---------------------------------------------------------------- Assembly videos
# Each card opens the assembly video page on classicbrand.ca. To embed a video in the portal instead,
# add its YouTube id as the 4th value and the card plays it inline.
VIDEOS = [
    ("Kitchen", [
        ("Wall cabinet", "Box, back panel, shelves and hanging rail", "i-cab-wall", ""),
        ("Base cabinet", "Box, stretchers, adjustable legs and toe kick", "i-cab-base", ""),
        ("Drawer base", "Drawer boxes, soft-close slides and fronts", "i-cab-drawer", ""),
        ("Pantry cabinet", "Tall box, shelves and door alignment", "i-cab-tall", ""),
    ]),
    ("Vanity", [
        ("Vanity with legs", "Evolution vanity box, legs and drawers", "i-cab-legs", ""),
        ("Full-panel vanity", "Crush and Fundamentals vanities", "i-cab-vanity", ""),
        ("Linen cabinet", "Tall linen tower and shelves", "i-cab-tall", ""),
    ]),
    ("Doors & hardware", [
        ("Hinge adjustment", "Up, down, side-to-side and depth", "i-door", ""),
        ("Handles & knobs", "Drilling and fitting standard hardware", "i-hardware", ""),
    ]),
]


def videos(menu):
    page = MAIN + "support-retailers-assembly-video"
    body = "".join(
        f'<section class="panel support-section"><header class="support-section-head"><span class="step-label">{group}</span><h2>{group} assembly</h2></header><div class="video-grid">'
        + "".join(
            (f'<button type="button" class="video-card" data-yt="{yt}">' if yt else f'<a class="video-card" href="{page}" target="_blank" rel="noopener">')
            + f'<span class="video-thumb"><svg class="icon cab"><use href="#{icon}"/></svg><span class="video-play"><svg class="icon"><use href="#i-play"/></svg></span></span><span class="video-text"><strong>{title}</strong><small>{desc}</small></span>'
            + ('</button>' if yt else '</a>')
            for title, desc, icon, yt in items)
        + '</div></section>' for group, items in VIDEOS)
    content = heading("Dealer support", "Assembly videos",
                      "Step-by-step videos for flat-packed cabinets — share them with installers and clients.",
                      "support-retailers-assembly-video") + support_tabs("support-videos.html") + body + '''
<div class="confirm-layer" id="videoLayer" aria-hidden="true"><div class="confirm-dialog video-dialog" role="dialog" aria-modal="true" aria-label="Assembly video"><button class="icon-button" type="button" id="videoClose" aria-label="Close"><svg class="icon"><use href="#i-close"/></svg></button><div class="video-frame" id="videoFrame"></div></div></div>'''
    script = r'''<script>
(() => {
  const { $, $$ } = Portal;
  const layer = $('#videoLayer');
  const close = () => { layer.classList.remove('open'); $('#videoFrame').innerHTML = ''; };
  $$('.video-card[data-yt]').forEach(b => b.addEventListener('click', () => { $('#videoFrame').innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${b.dataset.yt}?autoplay=1" allow="autoplay; encrypted-media" allowfullscreen title="Assembly video"></iframe>`; layer.classList.add('open'); }));
  $('#videoClose').addEventListener('click', close);
  layer.addEventListener('click', e => { if (e.target === layer) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
})();
</script>'''
    return content, script


# ---------------------------------------------------------------- Product replacement
def replacement(menu):
    content = heading("Dealer support", "Product replacement",
                      "Inspect cabinets when they arrive. Damaged or defective products must be claimed within 7 business days of receipt.",
                      "support-retailers-product-replacement") + support_tabs("support-replacement.html") + '''
<div class="checkout-grid">
  <div class="checkout-main">
    <section class="order-card" id="requestCard">
      <div class="order-card-head"><div><span class="step-label">New request</span><h3>Request a replacement</h3></div></div>
      <form class="order-card-body replace-form" id="replaceForm" novalidate>
        <div class="form-row">
          <div class="field" id="orderField"><label for="rOrder">Order # <span class="req">*</span></label><select id="rOrder"><option value="">Choose an order…</option></select></div>
          <div class="field" id="skuField"><label for="rSku">Product <span class="req">*</span></label><select id="rSku" disabled><option value="">Choose the order first</option></select></div>
        </div>
        <div class="form-row">
          <div class="field" id="issueField"><label for="rIssue">Issue <span class="req">*</span></label><select id="rIssue">
            <option value="">Choose one…</option>
            <option>Damaged in transit</option>
            <option>Cracked door or drawer-front frame / panel</option>
            <option>Cracked corner joint (door or drawer front)</option>
            <option>Manufacturing defect</option>
            <option>Missing part</option>
            <option>Wrong item received</option>
          </select></div>
          <div class="field"><label for="rQty">Pieces affected</label><input id="rQty" type="text" inputmode="numeric" value="1"></div>
        </div>
        <div class="field"><label for="rReceived">Date received <span class="req">*</span></label><input id="rReceived" type="date"><span class="field-hint" id="windowHint">Claims are accepted within 7 business days of receipt.</span></div>
        <div class="field"><label for="rNote">What happened <span class="field-hint">optional</span></label><textarea id="rNote" placeholder="Where the damage is, customer tag, anything the team should know"></textarea></div>
        <div class="field"><label for="rPhotos">Photos <span class="field-hint">label, damage close-up and the whole piece</span></label><label class="photo-drop" for="rPhotos"><svg class="icon"><use href="#i-download"/></svg><span id="photoText">Add photos</span></label><input id="rPhotos" type="file" accept="image/*" multiple hidden></div>
        <p class="config-error" id="replaceError" hidden></p>
        <button class="primary-button" type="submit" style="justify-self:start"><svg class="icon"><use href="#i-swap"/></svg>Submit request</button>
      </form>
      <div class="order-card-body replace-done" id="replaceDone" hidden>
        <div class="confirm-mark ok"><svg class="icon" width="22" height="22"><use href="#i-check"/></svg></div>
        <h3 id="doneTitle">Request sent</h3>
        <p id="doneText">Customer service reviews it and replies by email.</p>
        <button class="secondary-button" type="button" id="newRequest">Request another part</button>
      </div>
    </section>
    <section class="order-card">
      <div class="order-card-head"><div><span class="step-label">History</span><h3>Your requests</h3></div></div>
      <div class="order-card-body" id="requestList"></div>
    </section>
  </div>
  <aside class="checkout-side">
    <section class="order-card">
      <div class="order-card-head"><div><span class="step-label">Policy</span><h3>Replacement warranty</h3></div></div>
      <div class="order-card-body">
        <div class="fact-list">
          <div><strong>Replace or repair</strong><small>A defective part is replaced or repaired at Classic Brand's discretion. Installation and delivery costs are not covered.</small></div>
          <div><strong>7 business days</strong><small>Inspect on arrival and claim damaged or defective products within 7 business days of receipt.</small></div>
          <div><strong>Cracked frame or panel</strong><small>Doors and drawer fronts with a cracked frame or centre panel are replaced free of charge.</small></div>
          <div><strong>Cracked corner joint</strong><small>Under warranty, repaired free at our warehouse — even after installation.</small></div>
        </div>
      </div>
    </section>
  </aside>
</div>'''
    script = r'''<script>
(() => {
  const { $, $$, ORDERS, getOrder } = Portal;
  const KEY = 'cb-dealer-replacements';
  const read = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } };
  const write = (list) => { try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {} };
  const params = new URLSearchParams(location.search);
  const placed = ORDERS.filter(o => o.status !== 'draft');
  $('#rOrder').innerHTML += placed.map(o => `<option value="${o.id}">${o.id}${o.po ? ' · PO ' + o.po : ''}${o.name ? ' · ' + o.name : ''}</option>`).join('');
  function fillSkus() {
    const o = getOrder($('#rOrder').value);
    const sel = $('#rSku');
    sel.disabled = !o;
    sel.innerHTML = o ? '<option value="">Choose a product…</option>' + (o.items || []).map(i => `<option value="${i.sku}">${i.sku} · ${i.desc || ''}</option>`).join('') : '<option value="">Choose the order first</option>';
  }
  $('#rOrder').addEventListener('change', () => { fillSkus(); $('#orderField').classList.remove('invalid'); });
  if (params.get('order')) { $('#rOrder').value = params.get('order'); fillSkus(); }
  /* business days between the receipt date and today */
  const bizDays = (from) => { let d = new Date(from + 'T12:00'), n = 0; const today = new Date(); while (d < today) { d.setDate(d.getDate() + 1); if (d.getDay() % 6 && d <= today) n++; } return n; };
  $('#rReceived').max = new Date().toISOString().slice(0, 10);
  $('#rReceived').addEventListener('change', e => { const n = e.target.value ? bizDays(e.target.value) : 0; const late = n > 7; $('#windowHint').textContent = e.target.value ? (late ? `${n} business days ago — outside the 7-day window; customer service will review it.` : `${n} business day${n === 1 ? '' : 's'} ago — within the 7-day window.`) : 'Claims are accepted within 7 business days of receipt.'; $('#windowHint').classList.toggle('late', late); });
  $('#rPhotos').addEventListener('change', e => { const n = e.target.files.length; $('#photoText').textContent = n ? `${n} photo${n === 1 ? '' : 's'} added` : 'Add photos'; });
  function renderList() {
    const list = read();
    $('#requestList').innerHTML = list.length ? list.map(r => `<div class="request-row"><div><strong>${r.id}</strong><small>${r.order} · ${r.sku} · ${r.qty} pc</small></div><span>${r.issue}</span><span class="status submitted">Submitted</span><small>${r.date}</small></div>`).join('') : '<div class="side-empty">No replacement requests yet.</div>';
  }
  $('#replaceForm').addEventListener('submit', e => {
    e.preventDefault();
    const req = [['rOrder', 'Order #'], ['rSku', 'Product'], ['rIssue', 'Issue'], ['rReceived', 'Date received']];
    const missing = req.filter(([id]) => !$('#' + id).value);
    req.forEach(([id]) => $('#' + id).closest('.field').classList.toggle('invalid', !$('#' + id).value));
    if (missing.length) { $('#replaceError').hidden = false; $('#replaceError').textContent = `Please fill in: ${missing.map(m => m[1]).join(', ')}.`; return; }
    $('#replaceError').hidden = true;
    const list = read();
    const r = { id: 'RR-' + (2401 + list.length), order: $('#rOrder').value, sku: $('#rSku').value, qty: Math.max(1, parseInt($('#rQty').value, 10) || 1), issue: $('#rIssue').value, received: $('#rReceived').value, note: $('#rNote').value.trim(), photos: $('#rPhotos').files.length, date: new Date().toLocaleDateString('en-CA', { month: 'short', day: 'numeric', year: 'numeric' }) };
    write([r, ...list]);
    $('#doneTitle').textContent = `Request ${r.id} sent`;
    $('#doneText').textContent = `${r.qty} × ${r.sku} on order ${r.order} · ${r.issue}. Customer service reviews it and replies by email.`;
    $('#replaceForm').hidden = true; $('#replaceDone').hidden = false;
    renderList();
  });
  $('#replaceForm').addEventListener('change', e => { const f = e.target.closest('.field'); if (f && e.target.value) f.classList.remove('invalid'); });
  $('#newRequest').addEventListener('click', () => { $('#replaceForm').reset(); fillSkus(); $('#photoText').textContent = 'Add photos'; $('#windowHint').textContent = 'Claims are accepted within 7 business days of receipt.'; $('#replaceDone').hidden = true; $('#replaceForm').hidden = false; });
  renderList();
})();
</script>'''
    return content, script
