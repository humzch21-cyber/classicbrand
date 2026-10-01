"""New order flow: 1) choose series → 2) add products → 3) checkout."""
from pages import heading


def steps(current):
    items = [("new-order.html", "Choose a series"), ("new-order-products.html", "Add products"), ("new-order-checkout.html", "Checkout")]
    out = ['<nav class="steps" aria-label="Order steps">']
    for i, (href, label) in enumerate(items, 1):
        state = "done" if i < current else "current" if i == current else ""
        mark = '<svg class="icon" width="12" height="12"><use href="#i-check"/></svg>' if i < current else str(i)
        tag = "a" if i < current else "span"
        attr = f' href="{href}"' if i < current else ""
        out.append(f'<{tag} class="step {state}"{attr}><i>{mark}</i>{label}</{tag}>')
        if i < 3:
            out.append('<span class="step-sep"></span>')
    out.append('</nav>')
    return "".join(out)


# ---------------------------------------------------------------- Step 1
def series_page(menu):
    content = heading("New order · Step 1 of 3", "Choose a series", "Pick the product line, then the series and colour you want to order. Every SKU in the next step belongs to the series you choose here.") + steps(1) + '''
<section class="type-select" id="lineChooser" aria-label="Choose product line" hidden>
  <a class="type-card" href="?line=kitchen" data-line="kitchen">
    <span class="type-icon"><svg class="icon"><use href="#i-kitchen"/></svg></span>
    <span><strong>Kitchen</strong><small>Fundamentals, Trends Limited, Trends Select, Econoline, Euroline</small></span>
    <svg class="icon" style="color:var(--muted)"><use href="#i-chevron"/></svg>
  </a>
  <a class="type-card" href="?line=vanity" data-line="vanity">
    <span class="type-icon"><svg class="icon"><use href="#i-vanity"/></svg></span>
    <span><strong>Vanity</strong><small>Configurator, or Evolution I / II / III, Crush and Fundamentals</small></span>
    <svg class="icon" style="color:var(--muted)"><use href="#i-chevron"/></svg>
  </a>
  <a class="type-card" href="new-order-vanity-top.html?series=vanity-top" data-line="vanity-top">
    <span class="type-icon"><svg class="icon"><use href="#i-counter"/></svg></span>
    <span><strong>Vanity top</strong><small>Quartz &amp; sintered stone tops · pick the top, then the size · drilling and cuts per top</small></span>
    <svg class="icon" style="color:var(--muted)"><use href="#i-chevron"/></svg>
  </a>
</section>
<div class="line-tabs" role="tablist" aria-label="Product line" id="lineTabs" hidden>
  <a class="line-tab" role="tab" href="?line=kitchen" data-line="kitchen"><svg class="icon"><use href="#i-kitchen"/></svg>Kitchen</a>
  <a class="line-tab" role="tab" href="?line=vanity" data-line="vanity"><svg class="icon"><use href="#i-vanity"/></svg>Vanity</a>
  <a class="line-tab" role="tab" href="new-order-vanity-top.html?series=vanity-top" data-line="vanity-top"><svg class="icon"><use href="#i-counter"/></svg>Vanity top</a>
</div>
<a class="cross-link" id="crossLink" href="new-order-vanity-top.html?series=vanity-top" hidden><svg class="icon"><use href="#i-counter"/></svg><span><strong>Need a vanity top too?</strong><small>Quartz and sintered stone tops, sized to these vanities</small></span><svg class="icon chev"><use href="#i-chevron"/></svg></a>
<div class="series-grid" id="seriesGrid"></div>
<p class="lede" id="seriesNote" style="margin-top:22px;font-size:12px"></p>

<div class="confirm-layer" id="vanityAsk" aria-hidden="true">
  <div class="confirm-dialog" role="alertdialog" aria-modal="true" aria-labelledby="vanityAskTitle" aria-describedby="vanityAskDesc">
    <div class="confirm-mark"><svg class="icon" width="22" height="22"><use href="#i-vanity"/></svg></div>
    <h2 id="vanityAskTitle">How would you like to build this vanity order?</h2>
    <p id="vanityAskDesc">The 3D configurator walks you through series, size, finish, top and hardware. You can also pick a series here and add SKUs directly.</p>
    <div class="confirm-actions stack" style="margin-top:18px">
      <a class="primary-button" href="https://classicbrand.ca/3d-bathroom-cabinet-configurator/" target="_blank" rel="noopener"><svg class="icon"><use href="#i-external"/></svg><span>Use the 3D configurator<small>Opens classicbrand.ca in a new tab · guided selection with pricing</small></span></a>
      <a class="secondary-button" href="new-order.html?line=vanity"><svg class="icon"><use href="#i-file"/></svg><span>Choose from the series list<small>Browse SKUs and set quantities yourself</small></span></a>
      <button class="quiet-button" id="vanityAskClose" type="button" style="align-self:flex-end">Cancel</button>
    </div>
  </div>
</div>'''
    script = r'''<script>
(() => {
  const { $, $$ } = Portal;
  const { SERIES, LINE_LABEL, BOX_COLORS, seriesTitle, products, pageFor } = Catalog;
  const params = new URLSearchParams(location.search);
  if (params.get('line') === 'vanity-top' || params.get('line') === 'countertop') { location.replace('new-order-vanity-top.html?series=vanity-top'); return; }
  const line = LINE_LABEL[params.get('line')] ? params.get('line') : null;
  $('#crossLink').hidden = line !== 'vanity';
  $('#lineChooser').hidden = !!line;
  $('#lineTabs').hidden = !line;
  $$('.line-tab').forEach(t => t.classList.toggle('active', t.dataset.line === line));
  if (line) {
    document.title = `${LINE_LABEL[line]} series — Classic Brand Cabinetry`;
    $('h1').textContent = `Choose a ${LINE_LABEL[line].toLowerCase()} series`;
  } else {
    $('h1').textContent = 'What are you ordering?';
    $('.lede').textContent = 'Start by choosing the product line. Kitchen opens the cabinet series, Vanity lets you use the 3D configurator or pick a vanity series, Vanity top goes straight to the tops.';
  }

  /* Vanity: ask whether to use the configurator */
  const ask = $('#vanityAsk');
  const openAsk = () => { ask.classList.add('open'); ask.setAttribute('aria-hidden', 'false'); ask.querySelector('a').focus(); };
  const closeAsk = () => { ask.classList.remove('open'); ask.setAttribute('aria-hidden', 'true'); };
  $$('.line-tab[data-line="vanity"], #lineChooser [data-line="vanity"]').forEach(el => el.addEventListener('click', e => { e.preventDefault(); openAsk(); }));
  $('#vanityAskClose').addEventListener('click', closeAsk);
  ask.addEventListener('click', e => { if (e.target === ask) closeAsk(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && ask.classList.contains('open')) closeAsk(); });
  if (params.get('ask') === '1') openAsk();

  const boxDots = (s) => s.box ? `<span class="box-dots" title="Box colours: ${s.box.join(', ')}">${s.box.map(b => { const c = BOX_COLORS.find(x => x.code === b); return `<i style="background:${c.color}"></i>`; }).join('')}</span>` : '';
  const badge = (s) => s.badge ? `<span class="series-badge">${s.badge}</span>` : s.quoteOnly ? `<span class="series-badge soft">Pricing on request</span>` : '';

  $('#seriesGrid').innerHTML = !line ? '' : SERIES.filter(s => s.line === line).map(s => {
    const count = products(s).length;
    const visual = s.image ? `<img src="${s.image}" alt="${seriesTitle(s)}" loading="lazy">` : `<span class="door ${s.door}"><span class="pull"></span></span>`;
    return `<a class="series-card" href="${pageFor(s)}" style="--swatch:${s.color};--frame:${s.frame}">
      <div class="swatch">${visual}${badge(s)}</div>
      <div class="series-body">
        <span class="series-family">${LINE_LABEL[line]} series</span>
        <span class="series-name">${s.name || s.family}</span>
        ${s.blurb ? `<span class="item-meta">${s.blurb}</span>` : ''}
        <div class="series-meta"><span>${count} SKUs${s.box ? ' · ' : ''}${boxDots(s)}</span><span class="series-cta">Select<svg class="icon"><use href="#i-chevron"/></svg></span></div>
      </div>
    </a>`;
  }).join('');

  $('#seriesNote').textContent = !line ? '' : line === 'kitchen'
    ? 'Choose a kitchen series to open its SKU list. Colours and box options are selected in the next step.'
    : 'Vanity series and pricing follow the April 2026 price books. Prefer a guided path? Open the 3D configurator from the Vanity tab.';
})();
</script>'''
    return content, script


# ---------------------------------------------------------------- Step 2 (shared pieces)
SIDE_SUMMARY = """
    <aside class="panel side-summary" id="sideSummary" aria-label="Selected products">
      <div class="cat-head">Selected <span id="sideCount" class="cat-count"></span></div>
      <div class="side-summary-list" id="sideList"></div>
      <div class="side-summary-foot">
        <div><span class="item-meta">Subtotal</span><strong id="sideTotal">$0.00</strong></div>
        <button class="table-action primary" id="sideOpen">View summary</button>
      </div>
    </aside>"""

CART_BAR = """
    <div class="cart-bar" id="cartBar">
      <div class="cart-summary">
        <div><span>Items in cart</span><strong id="cartCount">0</strong></div>
        <div><span>Subtotal · dealer price</span><strong id="cartTotal">$0.00</strong></div>
        <div id="cartSeries" style="font-size:11px"></div>
      </div>
      <div class="cart-actions">
        <a class="secondary-button" href="new-order.html" id="changeSeries">Change series</a>
        <button class="secondary-button" id="clearCart">Clear</button>
        <button class="primary-button" id="viewSummary"><svg class="icon"><use href="#i-cart"/></svg>View summary &amp; checkout<svg class="icon"><use href="#i-chevron"/></svg></button>
      </div>
    </div>"""

SUMMARY_DRAWER = """
<div class="drawer-layer" id="summaryDrawer" aria-hidden="true">
  <aside class="drawer" role="dialog" aria-modal="true" aria-labelledby="summaryTitle">
    <header class="drawer-head">
      <div><span class="step-label">Order summary</span><h3 id="summaryTitle">Selected products</h3></div>
      <button class="icon-button" id="closeSummary" aria-label="Close summary"><svg class="icon"><use href="#i-close"/></svg></button>
    </header>
    <div class="drawer-body" id="summaryBody"></div>
    <div class="assembly-bar" id="assemblyBar">
      <span class="assembly-label">Assembly Required <span class="req">*</span></span>
      <label class="assembly-choice"><input type="radio" name="assembly" value="yes"><span>Yes</span></label>
      <label class="assembly-choice"><input type="radio" name="assembly" value="no"><span>No</span></label>
      <span class="assembly-hint" id="assemblyHint">Choose one to continue to checkout</span>
    </div>
    <footer class="drawer-foot">
      <div><span class="item-meta">Subtotal · dealer price</span><strong id="summaryTotal" style="display:block;font-family:Manrope,sans-serif;font-size:20px">$0.00</strong></div>
      <div class="foot-actions"><button class="secondary-button" id="summaryContinue">Keep adding</button><a class="primary-button disabled" id="summaryCheckout" href="new-order-checkout.html" aria-disabled="true">Checkout<svg class="icon"><use href="#i-chevron"/></svg></a></div>
    </footer>
  </aside>
</div>"""

# Category tree renderer shared by both step-2 pages (plain items, expandable children, and link items)
TREE_JS = r"""
  const countFor = (id, isSub) => all.filter(p => id === 'all' || (isSub ? p.sub === id : p.cat === id)).length;
  function renderTree() {
    $('#catTree').innerHTML = `<div class="cat-head">${TREE_TITLE}</div>` + cats.filter(c => c.link || countFor(c.id) > 0).map(c => {
      if (c.link) return `<a class="cat-item cat-link" href="${c.link}">${c.name}<span class="cat-count">colour → size</span><svg class="icon chev"><use href="#i-chevron"/></svg></a>`;
      const kids = (c.children || []).filter(k => countFor(k.id, true) > 0);
      const expanded = c.id === cat;
      return `<button class="cat-item${c.id === cat ? ' active' : ''}${expanded && kids.length ? ' expanded' : ''}" data-cat="${c.id}">${c.name}<span class="cat-count">${countFor(c.id)}</span>${kids.length ? '<svg class="icon chev"><use href="#i-chevron"/></svg>' : ''}</button>` +
        (kids.length ? `<div class="cat-children${expanded ? ' open' : ''}">${kids.map(k => `<button class="cat-child${sub === k.id ? ' active' : ''}" data-cat="${c.id}" data-sub="${k.id}">${k.name}<span class="cat-count">${countFor(k.id, true)}</span></button>`).join('')}</div>` : '');
    }).join('');
    $$('#catTree [data-cat]').forEach(b => b.addEventListener('click', () => { cat = b.dataset.cat; sub = b.dataset.sub || null; shown = PAGE; renderTree(); renderTable(); window.scrollTo({ top: $('.shop-layout').offsetTop - 90, behavior: 'smooth' }); }));
  }
"""


def products_page(menu):
    content = heading("New order · Step 2 of 3", "Add products", "Browse the series by category, filter by box colour and set quantities. Items are held in your cart until you check out or clear them.") + steps(2) + """
<div class="shop-toolbar">
  <div class="series-pill" id="seriesPill"></div>
  <a class="cross-link compact" id="crossLink" href="new-order-vanity-top.html?series=vanity-top" hidden><svg class="icon"><use href="#i-counter"/></svg><span><strong>Add a vanity top</strong><small>Quartz &amp; sintered stone · sized to these vanities</small></span><svg class="icon chev"><use href="#i-chevron"/></svg></a>
  <label class="search-box" style="width:320px">
    <svg class="icon" width="16" height="16"><use href="#i-search"/></svg>
    <span class="sr-only">Search products</span>
    <input id="productSearch" type="search" placeholder="Type to search SKU or description">
  </label>
</div>

<div class="shop-layout" style="margin-top:16px">
  <div class="shop-side">
    <aside class="panel cat-tree" id="catTree" aria-label="Product categories"></aside>""" + SIDE_SUMMARY + """
  </div>

  <div class="shop-main">
    <section class="panel filter-card" id="doorFilter" hidden>
      <div class="filter-label">Door Style</div>
      <div class="filter-options" id="doorOptions"></div>
    </section>
    <section class="panel filter-card" id="colorFilter" hidden>
      <div class="filter-label" id="colorLabel">Door Color</div>
      <div class="filter-options" id="colorOptions"></div>
    </section>
    <section class="panel filter-card" id="boxFilter" hidden>
      <div class="filter-label">Box Color</div>
      <div class="filter-options" id="boxOptions"></div>
    </section>

    <section class="panel orders-panel">
      <div class="table-scroll">
        <table class="data-table product-table">
          <thead><tr><th>Image</th><th>Sku</th><th>Price</th><th>Short description</th><th>Stock</th><th>Add to cart</th></tr></thead>
          <tbody id="productBody"></tbody>
        </table>
      </div>
      <div class="empty-state" id="emptyState"><strong>No products match</strong>Try another category, clear the box colour filter or search a different SKU.</div>
      <div class="load-more" id="loadMore"><span id="loadStatus"></span></div>
    </section>
""" + CART_BAR + """
  </div>
</div>

<div class="confirm-layer" id="configLayer" aria-hidden="true">
  <form class="confirm-dialog config-dialog" id="configForm" role="dialog" aria-modal="true" aria-labelledby="configTitle" novalidate>
    <header class="config-head">
      <div><span class="step-label">Configure before adding</span><h2 id="configTitle">SKU</h2><p id="configDesc"></p></div>
      <button class="icon-button" type="button" id="configClose" aria-label="Close"><svg class="icon"><use href="#i-close"/></svg></button>
    </header>
    <div class="config-grid">
      <label class="config-row" id="legsRow"><span>Legs <b class="req">*</b></span><select name="legs"></select></label>
      <label class="config-row"><span>Knobs</span><select name="knob"><option value="">None</option></select></label>
      <label class="config-row"><span>Knob location</span><select name="knobLoc" disabled><option value="">Choose an item</option></select></label>
      <label class="config-row"><span>Handles</span><select name="handle"><option value="">None</option></select></label>
      <label class="config-row"><span>Handle location</span><select name="handleLoc" disabled><option value="">Choose an item</option></select></label>
      <label class="config-row"><span>Hardware instruction <b class="req">*</b></span><select name="instruction" required></select></label>
      <label class="config-row"><span>Customer tag</span><input name="tag" type="text" maxlength="12" placeholder="1 to 12 characters"></label>
      <label class="config-row"><span>Qty</span><div class="qty"><button type="button" data-step="-1" aria-label="Decrease">−</button><input name="qty" type="number" min="1" max="99" value="1"><button type="button" data-step="1" aria-label="Increase">+</button></div></label>
    </div>
    <p class="config-error" id="configError" hidden></p>
    <div class="confirm-actions"><div class="config-price" id="configPrice"></div><button class="secondary-button" type="button" id="configCancel">Cancel</button><button class="primary-button" type="submit"><svg class="icon"><use href="#i-cart"/></svg>Add to cart</button></div>
  </form>
</div>
""" + SUMMARY_DRAWER
    script = r"""<script>
(() => {
  const { $, $$, money, toast } = Portal;
  const C = Catalog;
  const params = new URLSearchParams(location.search);
  const series = C.seriesById(params.get('series')) || C.SERIES[1];
  if (!params.get('series') || series.flow) { location.replace(params.get('series') && series.flow ? C.pageFor(series) : `new-order-products.html?series=${series.id}`); return; }
  let door = C.doorOf(series, params.get('door'));
  let color = C.colorOf(series, params.get('color'));
  const isVanity = series.line === 'vanity';
  const reload = () => { if (door && color && !C.colorsFor(series, door).includes(color)) color = C.colorsFor(series, door)[0]; all = C.products(series, color && color.code, door && door.id); };
  let all; reload();
  const cats = C.CATEGORIES[series.line];
  const TREE_TITLE = `${series.line === 'vanity' ? 'Bathroom' : C.LINE_LABEL[series.line]} categories`;
  const PAGE = 20;                       // rows appended per scroll step
  let cat = 'all', sub = null, shown = PAGE, boxes = new Set(), query = '';
  $('#changeSeries').href = `new-order.html?line=${series.line}`;
  $('#crossLink').hidden = series.line !== 'vanity';

  const doorLabel = () => door && series.doors.length > 1 ? `${door.name} (${door.style})` : '';
  function renderPill() {
    document.title = `${C.seriesTitle(series)}${color ? ' · ' + color.name : ''} — Add products — Classic Brand Cabinetry`;
    const detail = isVanity ? [doorLabel(), color && color.name].filter(Boolean).join(' · ') : (color ? `${color.name} · SKU prefix ${color.code}-` : '');
    $('#seriesPill').innerHTML = `<span class="mini-swatch" style="--swatch:${color ? color.swatch : series.color}"></span><span>${C.seriesTitle(series)}${detail ? ` <small>· ${detail}</small>` : ''} <small>· ${C.LINE_LABEL[series.line]}</small></span><a href="new-order.html?line=${series.line}">Change</a>`;
  }
  const syncUrl = () => { const url = new URL(location.href); if (color) url.searchParams.set('color', color.code); if (door && series.doors.length > 1) url.searchParams.set('door', door.id); history.replaceState(null, '', url); };

  /* Door style selector (vanity series with more than one door) */
  if (series.doors && series.doors.length > 1) {
    $('#doorFilter').hidden = false;
    const renderDoors = () => {
      $('#doorOptions').innerHTML = series.doors.map(d => `<button type="button" class="color-option door-option${door && d.id === door.id ? ' active' : ''}" data-door="${d.id}"><span class="door-chip ${series.door === 'fluted' ? 'fluted' : d.slab ? 'slab' : /narrow/i.test(d.style) ? 'narrow' : /step|bevel/i.test(d.style) ? 'raised' : 'shaker'}" style="--swatch:${color ? color.swatch : '#eee'}"><i></i></span><span>${d.name}<small>${d.style}</small></span></button>`).join('');
      $$('#doorOptions .door-option').forEach(b => b.addEventListener('click', () => {
        door = C.doorOf(series, b.dataset.door); reload(); shown = PAGE; syncUrl();
        renderDoors(); renderColors(); renderPill(); renderTree(); renderTable();
      }));
    };
    window.renderDoors = renderDoors;
  }

  /* Colour selector: kitchen colours swap the SKU prefix; vanity colours are recorded on the cart line */
  let renderColors = () => {};
  if (series.colors) {
    $('#colorFilter').hidden = false;
    $('#colorLabel').textContent = isVanity ? 'Colour' : 'Door Color';
    renderColors = () => {
      const list = C.colorsFor(series, door);
      const groups = [...new Set(list.map(c => c.group || ''))];
      $('#colorOptions').innerHTML = groups.map(g => (groups.length > 1 ? `<span class="opt-group">${g}</span>` : '') + list.filter(c => (c.group || '') === g).map(c => `<button type="button" class="color-option${isVanity ? ' swatch-option' : ''}${color && c.code === color.code ? ' active' : ''}" data-color="${c.code}" style="--swatch:${c.swatch};--frame:${c.frame || c.swatch}">${isVanity ? '<span class="colour-cube"></span>' : `<span class="door-chip ${c.door}"><i></i></span>`}<span>${c.name}${isVanity ? (c.note ? `<small>${c.note}</small>` : (/^[A-Z]{2,4}$/.test(c.code) ? `<small>${c.code}</small>` : '')) : `<small>${c.code}-</small>`}</span></button>`).join('')).join('');
      $$('#colorOptions .color-option').forEach(b => b.addEventListener('click', () => {
        color = C.colorOf(series, b.dataset.color); reload(); shown = PAGE; syncUrl();
        if (window.renderDoors) window.renderDoors();
        renderColors(); renderPill(); renderTree(); renderTable();
      }));
    };
  }
  if (window.renderDoors) window.renderDoors();
  renderColors();
  renderPill();
""" + TREE_JS + r"""
  /* Box colour filter (kitchen only) */
  if (series.box) {
    $('#boxFilter').hidden = false;
    $('#boxOptions').innerHTML = C.BOX_COLORS.filter(b => series.box.includes(b.code)).map(b => `<label class="box-option"><input type="checkbox" value="${b.code}"><span class="box-cube" style="--swatch:${b.color}"></span><span>${b.code}<small>${b.name}</small></span></label>`).join('');
    $$('#boxOptions input').forEach(i => i.addEventListener('change', () => { i.checked ? boxes.add(i.value) : boxes.delete(i.value); shown = PAGE; renderTable(); }));
  }

  $('#productSearch').addEventListener('input', e => { query = e.target.value.trim().toLowerCase(); shown = PAGE; renderTable(); });

  const THUMB = OrderSummary.THUMB;
  const stockCell = (n) => n === 0 ? '<span class="stock out">Backorder</span>' : n > 10 ? '<span class="stock in">&gt;10</span>' : `<span class="stock low">${n} left</span>`;

  function filtered() {
    return all.filter(p => (cat === 'all' || p.cat === cat) && (!sub || p.sub === sub) && (!boxes.size || !p.box || boxes.has(p.box)) && (!query || (p.sku + ' ' + p.desc).toLowerCase().includes(query)));
  }

  /* Vanity cabinets are configured (legs, knobs, handles, hardware instruction) before they go in the cart */
  const needsConfig = (p) => isVanity && !p.generic && ['van-legs', 'van-panel', 'linen', 'vwall', 'vbase'].includes(p.cat);
  const inCartHtml = (sku) => { const n = C.qtyOfSku(sku); return n ? `<span class="in-cart-note"><span class="type-chip in-cart">${n} in cart</span><button type="button" class="row-remove">Remove</button></span>` : ''; };
  function rowHtml(p) {
    const price = p.dealer == null ? '<span class="price-cell quote">On request</span>' : `${money(p.dealer)}<small>MSRP ${money(p.msrp)}</small>${p.assembly != null ? `<small class="asm">Assembly +${money(p.assembly)}</small>` : ''}`;
    return `<tr data-sku="${p.sku}">
      <td><span class="product-thumb"><svg class="icon"><use href="#${THUMB[p.img] || 'i-box'}"/></svg></span></td>
      <td class="sku-cell">${p.sku}${p.box ? `<small>Box · ${p.box}</small>` : ''}${p.variant ? `<small>${p.variant}</small>` : ''}</td>
      <td class="price-cell">${price}</td>
      <td style="font-size:13px">${p.desc}</td>
      <td>${stockCell(p.stock)}</td>
      <td>${needsConfig(p) ? `<div class="row-add"><button type="button" class="table-action primary configure-line"><svg class="icon" width="14" height="14"><use href="#i-hardware"/></svg>Configure</button><span class="config-hint">${p.cat === 'van-legs' && series.book ? 'Legs, knobs &amp; handles' : 'Knobs, handles &amp; install'}</span></div>` : `<div class="row-add"><input class="row-tag" type="text" maxlength="12" placeholder="Customer tag" aria-label="Customer tag for ${p.sku}"><div class="qty"><button type="button" data-step="-1" aria-label="Decrease">−</button><input type="number" min="1" max="99" value="1" aria-label="Quantity for ${p.sku}"><button type="button" data-step="1" aria-label="Increase">+</button></div><button type="button" class="table-action primary add-line"><svg class="icon" width="14" height="14"><use href="#i-cart"/></svg>Add</button></div>`}<div class="in-cart-wrap">${inCartHtml(p.sku)}</div></td>
    </tr>`;
  }
  function wireRow(row) {
    const p = all.find(x => x.sku === row.dataset.sku);
    const refreshNote = () => { $('.in-cart-wrap', row).innerHTML = inCartHtml(p.sku); wireRemove(); };
    const wireRemove = () => { const r = $('.row-remove', row); if (r) r.addEventListener('click', () => { C.removeSku(p.sku); summary.refresh(); refreshNote(); }); };
    wireRemove();
    const cfg = $('.configure-line', row);
    if (cfg) { cfg.addEventListener('click', () => openConfig(p, refreshNote)); return; }
    const input = $('.qty input', row);
    $$('[data-step]', row).forEach(b => b.addEventListener('click', () => { input.value = Math.max(1, Math.min(99, Number(input.value) + Number(b.dataset.step))); }));
    $('.add-line', row).addEventListener('click', () => {
      const n = Math.max(1, Math.min(99, Number(input.value) || 1));
      const tag = $('.row-tag', row).value;
      C.addUnits(p, series, n, null, tag);
      summary.refresh(); refreshNote();
      $('.row-tag', row).value = ''; input.value = 1;
    });
    $('.row-tag', row).addEventListener('keydown', e => { if (e.key === 'Enter') $('.add-line', row).click(); });
  }

  /* Scroll loading: the first 20 rows render at once, more append as the list end scrolls into view */
  function renderTable() {
    const list = filtered();
    const body = $('#productBody');
    body.innerHTML = list.slice(0, shown).map(rowHtml).join('');
    $$('tr', body).forEach(wireRow);
    $('#emptyState').classList.toggle('visible', list.length === 0);
    $('.table-scroll').style.display = list.length ? '' : 'none';
    updateLoadStatus(list);
  }
  function appendMore() {
    const list = filtered();
    if (shown >= list.length) return;
    const next = list.slice(shown, shown + PAGE);
    shown += next.length;
    const body = $('#productBody');
    const frag = document.createElement('tbody'); frag.innerHTML = next.map(rowHtml).join('');
    [...frag.children].forEach(tr => { body.appendChild(tr); wireRow(tr); });
    updateLoadStatus(list);
  }
  function updateLoadStatus(list) {
    const more = shown < list.length;
    $('#loadStatus').innerHTML = list.length ? `Showing ${Math.min(shown, list.length)} of ${list.length} SKUs${more ? ' · <em>scroll for more</em>' : ''}` : '';
    $('#loadMore').classList.toggle('done', !more);
  }
  new IntersectionObserver(entries => { if (entries.some(e => e.isIntersecting)) appendMore(); }, { rootMargin: '400px 0px' }).observe($('#loadMore'));

  /* Configuration dialog: vanity option, knobs / handles with location, hardware instruction, tag, qty */
  const layer = $('#configLayer'), form = $('#configForm');
  let cfgProduct = null, cfgDone = null;
  const fill = (sel, list, placeholder) => {
    const groups = [...new Set(list.map(o => o.group || ''))];
    sel.innerHTML = (placeholder ? `<option value="">${placeholder}</option>` : '') + groups.map(g => { const opts = list.filter(o => (o.group || '') === g).map(o => `<option value="${o.code}">${o.name}</option>`).join(''); return g ? `<optgroup label="${g}">${opts}</optgroup>` : opts; }).join('');
  };
  function openConfig(p, done) {
    cfgProduct = p; cfgDone = done;
    const o = C.hardwareOptions(series, p);
    $('#configTitle').textContent = p.sku;
    $('#configDesc').textContent = `${p.desc}${p.variant ? ' · ' + p.variant : ''}`;
    $('#legsRow').hidden = !o.legs; if (o.legs) fill(form.legs, o.legs, 'Choose an item');
    fill(form.knob, o.knobs, 'None'); fill(form.handle, o.handles, 'None');
    fill(form.knobLoc, o.locations, 'Choose an item'); fill(form.handleLoc, o.locations, 'Choose an item');
    fill(form.instruction, o.instructions, 'Choose an item');
    form.knobLoc.disabled = true; form.handleLoc.disabled = true; form.tag.value = ''; form.qty.value = 1;
    $('#configError').hidden = true; $$('.config-row.invalid', form).forEach(r => r.classList.remove('invalid'));
    updatePrice();
    layer.classList.add('open'); layer.setAttribute('aria-hidden', 'false'); (o.legs ? form.legs : form.knob).focus();
  }
  const closeConfig = () => { layer.classList.remove('open'); layer.setAttribute('aria-hidden', 'true'); };
  const updatePrice = () => { if (!cfgProduct) return; const n = Math.max(1, Number(form.qty.value) || 1); $('#configPrice').innerHTML = cfgProduct.dealer == null ? 'Priced on request' : `<strong>${money(cfgProduct.dealer * n)}</strong><small>${n} × ${money(cfgProduct.dealer)}${cfgProduct.assembly != null ? ` · assembly +${money(cfgProduct.assembly)} each if assembled` : ''}</small>`; };
  form.knob.addEventListener('change', () => { form.knobLoc.disabled = !form.knob.value; if (!form.knob.value) form.knobLoc.value = ''; });
  form.handle.addEventListener('change', () => { form.handleLoc.disabled = !form.handle.value; if (!form.handle.value) form.handleLoc.value = ''; });
  $$('[data-step]', form).forEach(b => b.addEventListener('click', () => { form.qty.value = Math.max(1, Math.min(99, Number(form.qty.value) + Number(b.dataset.step))); updatePrice(); }));
  form.qty.addEventListener('change', updatePrice);
  form.addEventListener('change', e => { const row = e.target.closest('.config-row'); if (row && e.target.value) row.classList.remove('invalid'); if (!$('.config-row.invalid', form)) $('#configError').hidden = true; });
  $('#configClose').addEventListener('click', closeConfig); $('#configCancel').addEventListener('click', closeConfig);
  layer.addEventListener('click', e => { if (e.target === layer) closeConfig(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && layer.classList.contains('open')) closeConfig(); });
  form.addEventListener('submit', e => {
    e.preventDefault();
    const missing = [];
    const need = (field, label) => { const row = form[field].closest('.config-row'); const bad = !form[field].value; row.classList.toggle('invalid', bad); if (bad) missing.push(label); };
    if (!$('#legsRow').hidden) need('legs', 'Legs'); need('instruction', 'Hardware instruction');
    if (form.knob.value) need('knobLoc', 'Knob location'); else form.knobLoc.closest('.config-row').classList.remove('invalid');
    if (form.handle.value) need('handleLoc', 'Handle location'); else form.handleLoc.closest('.config-row').classList.remove('invalid');
    if (missing.length) { const err = $('#configError'); err.hidden = false; err.textContent = `Please choose: ${missing.join(', ')}.`; return; }
    const hardware = { legs: $('#legsRow').hidden ? null : form.legs.value, knob: form.knob.value || null, knobLoc: form.knob.value ? form.knobLoc.value : null, handle: form.handle.value || null, handleLoc: form.handle.value ? form.handleLoc.value : null, instruction: form.instruction.value };
    const n = Math.max(1, Math.min(99, Number(form.qty.value) || 1));
    C.addUnits(cfgProduct, series, n, null, form.tag.value, hardware);
    summary.refresh(); if (cfgDone) cfgDone(); closeConfig();
  });

  /* Summary drawer, "Selected" panel and cart bar (shared module) */
  const summary = OrderSummary.init({ onClear: renderTable });

  renderTree(); renderTable();
})();
</script>"""
    return content, script


# ---------------------------------------------------------------- Step 2b · Vanity tops (colour → size → top service)
def vanity_top_page(menu):
    content = heading("New order · Step 2 of 3", "Vanity tops", "Pick the top first — material, thickness and colour — then choose sizes below. Drilling and cut-to-size are chosen per top before it goes in the cart.") + steps(2) + """
<div class="shop-toolbar">
  <div class="series-pill" id="seriesPill"></div>
  <a class="cross-link compact" href="new-order.html?line=vanity"><svg class="icon"><use href="#i-vanity"/></svg><span><strong>Add vanities</strong><small>Choose a vanity series for these tops</small></span><svg class="icon chev"><use href="#i-chevron"/></svg></a>
  <label class="search-box" style="width:320px">
    <svg class="icon" width="16" height="16"><use href="#i-search"/></svg>
    <span class="sr-only">Search vanity tops</span>
    <input id="productSearch" type="search" placeholder="Search size or SKU, e.g. 31 or AGR31">
  </label>
</div>

<div class="shop-layout" style="margin-top:16px">
  <div class="shop-side">
    <aside class="panel cat-tree" id="catTree" aria-label="Vanity top categories"></aside>""" + SIDE_SUMMARY + """
  </div>

  <div class="shop-main">
    <section class="panel vt-section" id="colorSection">
      <header class="vt-head"><span class="vt-step">1</span><div><h3>Choose a top</h3><p>Material, thickness and colour · the code becomes the SKU prefix</p></div><span class="vt-chosen" id="colorChosen">No top selected</span></header>
      <div id="colorOptions"></div>
    </section>

    <section class="panel vt-section" id="sizeSection">
      <header class="vt-head"><span class="vt-step">2</span><div><h3>Choose a size</h3><p>Every top is a bundle: quartz top with the matching undermount sink. Tick the top services you need, add a customer tag, then add to cart.</p></div><span class="vt-chosen" id="sizeCount"></span></header>
      <div class="vt-locked" id="sizeLocked"><svg class="icon"><use href="#i-swatch"/></svg><div><strong>Pick a top above to load sizes and prices</strong><span>Sizes are the same for every top; SKUs and pricing appear once a top is selected.</span></div></div>
      <div class="vt-list" id="sizeList"></div>
      <div class="empty-state" id="emptyState"><strong>No sizes match</strong>Try another category or clear the search.</div>
    </section>
""" + CART_BAR + """
  </div>
</div>
""" + SUMMARY_DRAWER
    script = r"""<script>
(() => {
  const { $, $$, money, toast } = Portal;
  const C = Catalog;
  const params = new URLSearchParams(location.search);
  const series = C.seriesById('vanity-top');
  let color = C.colorOf(series, params.get('color'));            // null until the dealer picks one
  let all = C.products(series, color && color.code);
  const cats = C.CATEGORIES['vanity-top'];
  const TREE_TITLE = 'Vanity top categories';
  const PAGE = 500;                                               // the size list is short — no scroll loading needed
  let cat = 'all', sub = null, shown = PAGE, query = '';
  $('#changeSeries').href = 'new-order.html';
  $('#changeSeries').textContent = 'Change product line';

  function renderPill() {
    document.title = `Vanity tops${color ? ' · ' + color.name : ''} — Add products — Classic Brand Cabinetry`;
    $('#seriesPill').innerHTML = `${color ? `<img class="mini-top" src="${color.image}" alt="">` : `<span class="mini-swatch stone" style="--swatch:${series.color}"></span>`}<span>Vanity tops${color ? ` <small>· ${color.name} · ${color.short} · SKU prefix ${color.prefix}</small>` : ' <small>· quartz &amp; sintered stone</small>'}</span><a href="new-order.html">Change</a>`;
  }

  /* 1 · colour strip */
  function renderColors() {
    const groups = [...new Set(series.colors.map(c => c.group))];
    $('#colorOptions').innerHTML = groups.map(g => `<div class="stone-group"><div class="stone-group-name">${g}</div><div class="stone-options">${series.colors.filter(c => c.group === g).map(c => `<button type="button" class="stone-option${color && c.code === color.code ? ' active' : ''}" data-color="${c.code}"><img class="stone-img" src="${c.image}" alt="${c.name}" loading="lazy"><span class="stone-name">${c.name}${c.note ? ` <em>${c.note}</em>` : ''}<small>${c.prefix}${c.suffix ? ' · ' + c.suffix.slice(1) : ''}</small></span><span class="stone-check"><svg class="icon" width="12" height="12"><use href="#i-check"/></svg></span></button>`).join('')}</div></div>`).join('');
    $$('#colorOptions .stone-option').forEach(b => b.addEventListener('click', () => {
      color = C.colorOf(series, b.dataset.color);
      all = C.products(series, color.code);
      const url = new URL(location.href); url.searchParams.set('color', color.code); history.replaceState(null, '', url);
      renderColors(); renderPill(); renderTree(); renderTable();
      $('#sizeSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }));
    $('#colorChosen').textContent = color ? `${color.name} · ${color.short}` : 'No top selected';
    $('#colorChosen').classList.toggle('set', !!color);
  }
  renderColors(); renderPill();
""" + TREE_JS + r"""
  $('#productSearch').addEventListener('input', e => { query = e.target.value.trim().toLowerCase(); renderTable(); });

  const THUMB = OrderSummary.THUMB;
  const stockCell = (n) => n === 0 ? '<span class="stock out">Backorder</span>' : n > 10 ? '<span class="stock in">In stock</span>' : `<span class="stock low">${n} left</span>`;
  const filtered = () => all.filter(p => (cat === 'all' || p.cat === cat) && (!sub || p.sub === sub) && (!query || (p.sku + ' ' + p.desc).toLowerCase().includes(query)));

  /* 2 · size cards — each with top services, customer tag, quantity and Add to cart */
  function cardHtml(p) {
    const inCart = C.qtyOfSku(p.sku);
    const isTop = p.cat === 'vt-product';
    const services = isTop ? `<div class="vt-services"><span class="vt-label">Top service</span>${series.services.map(s => `<label class="svc-option"><input type="checkbox" value="${s.code}"><span>${s.code}<small>${s.name}</small></span></label>`).join('')}</div>` : '<div class="vt-services"><span class="vt-label">Top service</span><span class="item-meta">Not applicable</span></div>';
    return `<article class="vt-card${isTop ? ' has-services' : ''}" data-sku="${p.sku}">
      <div class="vt-main">
        <span class="product-thumb vt-thumb">${color && !p.generic ? `<img src="${color.image}" alt="">` : `<svg class="icon"><use href="#${THUMB[p.img] || 'i-box'}"/></svg>`}</span>
        <div class="vt-info">
          <div class="vt-sku">${p.sku}${inCart ? `<span class="type-chip in-cart">${inCart} in cart</span>` : ''}</div>
          <div class="vt-desc">${p.desc}</div>
          <div class="vt-meta">${p.width ? `<span>${p.width}″ wide · 22″ deep</span>` : ''}${color && !p.generic ? `<span>${color.name} · ${color.short}</span>` : ''}${stockCell(p.stock)}</div>
        </div>
        <div class="vt-price">${money(p.dealer)}<small>MSRP ${money(p.msrp)}</small></div>
      </div>
      <div class="vt-config">
        ${services}
        <div class="vt-actions">
          <input class="row-tag" type="text" maxlength="12" placeholder="Customer tag" aria-label="Customer tag for ${p.sku}">
          <div class="qty"><button type="button" data-step="-1" aria-label="Decrease">−</button><input type="number" min="1" max="99" value="1" aria-label="Quantity for ${p.sku}"><button type="button" data-step="1" aria-label="Increase">+</button></div>
          <button type="button" class="primary-button vt-add"><svg class="icon"><use href="#i-cart"/></svg>Add to cart</button>
        </div>
      </div>
    </article>`;
  }
  function wireCard(card) {
    const p = all.find(x => x.sku === card.dataset.sku);
    const qtyInput = $('.qty input', card);
    $$('[data-step]', card).forEach(b => b.addEventListener('click', () => { qtyInput.value = Math.max(1, Math.min(99, Number(qtyInput.value) + Number(b.dataset.step))); }));
    $('.vt-add', card).addEventListener('click', () => {
      const n = Math.max(1, Math.min(99, Number(qtyInput.value) || 1));
      const services = $$('.svc-option input:checked', card).map(i => i.value);
      const tag = $('.row-tag', card).value;
      C.addUnits(p, series, n, services, tag);
      summary.refresh();
      $('.row-tag', card).value = ''; qtyInput.value = 1;
      $('.vt-sku', card).innerHTML = `${p.sku}<span class="type-chip in-cart">${C.qtyOfSku(p.sku)} in cart</span>`;
    });
  }
  function renderTable() {
    const locked = !color;
    $('#sizeLocked').hidden = !locked;
    $('#sizeSection').classList.toggle('locked', locked);
    const list = locked ? [] : filtered();
    $('#sizeList').innerHTML = list.map(cardHtml).join('');
    $$('.vt-card', $('#sizeList')).forEach(wireCard);
    $('#emptyState').classList.toggle('visible', !locked && list.length === 0);
    $('#sizeCount').textContent = locked ? '' : `${list.length} size${list.length === 1 ? '' : 's'}`;
  }

  const summary = OrderSummary.init({ onClear: renderTable });
  renderTree(); renderTable();
})();
</script>"""
    return content, script


# ---------------------------------------------------------------- Step 3
from checkout_page import checkout_page  # noqa: E402
