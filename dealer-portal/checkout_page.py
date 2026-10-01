"""New order · Step 3 — Place order (mirrors the original Classic Brand checkout: address, shipping methods, load truck method, PO number)."""
from pages import heading
from order_pages import steps

CONTENT = """
<div class="checkout-grid" id="orderForm">
  <div class="checkout-main">
    <section class="order-card">
      <div class="order-card-head">
        <div><span class="step-label">Order contents</span><h3 id="itemsTitle">Items in this order</h3></div>
        <a class="quiet-button" id="addMore" href="new-order.html"><svg class="icon" width="15" height="15"><use href="#i-plus"/></svg>Add more items</a>
      </div>
      <div class="assembly-bar" id="assemblyBar">
        <span class="assembly-label">Assembly Required</span>
        <strong id="assemblyView">—</strong>
        <span class="assembly-hint" id="assemblyHint"></span>
        <span class="assembly-tag" id="customerTagView"></span>
      </div>
      <div class="order-card-body checkout-items" id="lineItems"></div>
    </section>

    <section class="order-card">
      <div class="order-card-head"><div><span class="step-label">Shipping address</span><h3>Ship to</h3></div><button class="quiet-button" id="changeAddress">Change address</button></div>
      <div class="order-card-body">
        <div class="address-card">
          <span class="addr-check"><svg class="icon" width="14" height="14"><use href="#i-check"/></svg></span>
          <strong>Humphrey &middot; Dealer CB-20418</strong>
          3095 Universal Drive<br>Mississauga, Ontario<br>Canada
          <div class="addr-phone">905 232 4660</div>
        </div>
      </div>
    </section>

    <section class="order-card">
      <div class="order-card-head"><div><span class="step-label">Shipping methods</span><h3>Ready date &amp; delivery</h3></div><span class="status submitted">Required to place</span></div>
      <div class="order-card-body">
        <div class="field" style="margin-bottom:16px">
          <label for="customDate">Shipping ready date &ndash; estimated <span class="req">*</span></label>
          <div class="date-strip" id="dateStrip" aria-label="Available shipping ready dates"></div>
          <label class="custom-date" style="display:flex;margin-top:10px"><span>Or choose another date</span><input id="customDate" type="date"></label>
        </div>

        <div class="field">
          <label>Shipping method <span class="req">*</span></label>
          <div class="ship-methods" id="shipMethods">
            <label class="ship-method"><input type="radio" name="ship" value="dealer" data-fee="0" checked><span class="ship-price">0.00</span><span class="ship-free">Free</span><span>Pick up by dealer<small>Collect at the Classic Brand dock during pickup hours</small></span></label>
            <label class="ship-method"><input type="radio" name="ship" value="cbc-truck" data-fee="0"><span class="ship-price">0.00</span><span></span><span>CBC truck stand delivery<small>Classic Brand truck &middot; stand delivery to the address above</small></span></label>
            <label class="ship-method"><input type="radio" name="ship" value="dc" data-fee="0"><span class="ship-price">0.00</span><span></span><span>Pick up by DC<small>Released to your distribution centre</small></span></label>
            <label class="ship-method"><input type="radio" name="ship" value="third-party" data-fee="0"><span class="ship-price">0.00</span><span></span><span>Pick up by third party<small>Your carrier collects &middot; carrier name on the PO</small></span></label>
          </div>
        </div>

        <div class="field" style="margin-top:16px">
          <label for="loadMethod">Load truck method <span class="req">*</span></label>
          <select id="loadMethod" required>
            <option value="">Select how the order should be loaded&hellip;</option>
            <option value="skids">Load product with skids</option>
            <option value="hand">Hand carry product with truck</option>
          </select>
          <div class="field-hint">Skids need a dock or forklift at the destination; hand carry is loaded piece by piece.</div>
        </div>
      </div>
    </section>

  </div>

  <aside class="checkout-side">
    <section class="order-card summary-card">
      <h3>Order summary</h3>
      <div class="summary-line"><span>Cart subtotal <span id="sumCount"></span></span><span id="sumMerch">&mdash;</span></div>
      <div class="summary-line"><span>MSRP value</span><span id="sumMsrp">&mdash;</span></div>
      <div class="summary-line"><span>Shipping <em id="shipNote" style="display:block;font-style:italic;font-size:11px"></em></span><span id="sumShip">0.00</span></div>
      <div class="summary-line"><span>Assembly</span><span id="sumAssembly">&mdash;</span></div>
      <div class="summary-line"><span>Tax (HST 13%)</span><span id="sumTax">&mdash;</span></div>
      <div class="summary-total"><span>Order total</span><strong id="sumTotal">&mdash;</strong></div>
      <p class="price-note" id="quoteNote">CAD &middot; dealer pricing</p>

      <div class="field" style="margin-top:16px">
        <label for="orderComment">Comment <span class="field-hint">optional</span></label>
        <textarea id="orderComment" placeholder="Delivery instructions, site contact, anything the order desk should know"></textarea>
      </div>

      <div class="po-field" id="poField">
        <label for="poNumber"><span>PO Number <span class="req">*</span></span><span class="status submitted" style="font-size:10px">Required</span></label>
        <input id="poNumber" type="text" maxlength="30" placeholder="Your purchase order number" autocomplete="off">
      </div>

      <button class="discount-toggle" id="discountToggle" aria-expanded="false"><span>Have a discount code?</span><svg class="icon" width="15" height="15"><use href="#i-down"/></svg></button>
      <div class="discount-panel" id="discountPanel">
        <div class="input-group"><input id="discountCode" type="text" placeholder="Enter discount code"><button class="secondary-button" id="applyDiscount">Apply</button></div>
        <div class="discount-message" id="discountMessage" aria-live="polite"></div>
      </div>

      <div class="summary-actions">
        <button class="primary-button" id="placeOrder">Place order</button>
        <button class="secondary-button" id="saveDraft">Draft order</button>
        <button class="quiet-button" id="printOrder" style="justify-self:center"><svg class="icon"><use href="#i-printer"/></svg>Print</button>
      </div>
    </section>
    <section class="order-card draft-explainer">
      <strong>What is a draft order?</strong>
      <p>It saves your items, address and shipping choices so you can return later. PO number and ready date are only required when you place the order.</p>
    </section>
  </aside>
</div>

<div class="confirm-layer" id="confirmLayer" aria-hidden="true">
  <div class="confirm-dialog" role="alertdialog" aria-modal="true" aria-labelledby="confirmTitle" aria-describedby="confirmDescription">
    <div class="confirm-mark"><svg class="icon" width="22" height="22"><use href="#i-check"/></svg></div>
    <h2 id="confirmTitle">Ready to place this order?</h2>
    <p id="confirmDescription">After submission, the order moves from Draft to Submitted and the PO number is locked. You can still track it from Orders.</p>
    <div class="confirm-details">
      <div><span>PO number</span><strong id="confirmPo"></strong></div>
      <div><span>Series</span><strong id="confirmSeries"></strong></div>
      <div><span>Customer tag</span><strong id="confirmTag"></strong></div>
      <div><span>Assembly required</span><strong id="confirmAssembly"></strong></div>
      <div><span>Ready date</span><strong id="confirmDate"></strong></div>
      <div><span>Shipping</span><strong id="confirmShip"></strong></div>
      <div><span>Order total</span><strong id="confirmTotal"></strong></div>
    </div>
    <div class="confirm-actions"><button class="secondary-button" id="cancelSubmit">Go back</button><button class="primary-button" id="confirmSubmit">Place order</button></div>
  </div>
</div>
"""

SCRIPT = r"""<script>
(() => {
  const { $, $$, ORDERS, money, longDate, toast } = Portal;
  const C = Catalog;
  const TAX = 0.13;
  const SHIP_LABEL = { dealer: 'Pick up by dealer – Free', 'cbc-truck': 'CBC truck stand delivery', dc: 'Pick up by DC', 'third-party': 'Pick up by third party' };
  const params = new URLSearchParams(location.search);
  const quoteId = params.get('quote');
  const quote = quoteId ? ORDERS.find(o => o.id === quoteId) : null;
  let selectedDate = '';

  if (quote) {
    if (quote.items) { C.writeCart({ items: quote.items.map(i => ({ ...i })), quote: quote.id, po: quote.po, comment: quote.comment, ship: quote.ship, load: quote.load }); }
    else C.loadDraft(quote.id);
    $('h1').textContent = `Edit quote ${quote.id}`;
    $('.lede').textContent = `${quote.name} · saved draft · prices shown in CAD`;
    $('#itemsTitle').textContent = 'Items in this quote';
  }
  const meta = C.readCart();
  const backToSummary = () => { const first = C.readCart().items[0]; const s = first && C.seriesById(first.series); return (s ? C.pageFor(s) : 'new-order-products.html?series=') + '&summary=1'; };
  function renderAssembly() {
    const cart = C.readCart();
    const a = cart.assembly;
    $('#assemblyView').textContent = a === 'yes' ? 'Yes' : a === 'no' ? 'No' : 'Not chosen';
    $('#assemblyHint').textContent = a === 'yes' ? 'Cabinets are delivered fully assembled' : a === 'no' ? 'Ships flat-packed' : 'Open the order summary on the product page to choose';
    $('#assemblyBar').classList.toggle('invalid', cart.items.length > 0 && !a);
    $('#customerTagView').innerHTML = `<a href="${backToSummary()}">Edit items, tags or assembly in the order summary</a>`;
  }
  renderAssembly();
  if (meta.po) $('#poNumber').value = meta.po;
  if (meta.comment) $('#orderComment').value = meta.comment;
  if (meta.ship) { const r = $(`input[name=ship][value="${meta.ship}"]`); if (r) r.checked = true; }
  if (meta.load) $('#loadMethod').value = meta.load;

  const THUMB = OrderSummary.THUMB;

  // Vanity-top lines remember their colour so "Edit quantities" reopens the same colour
  const i0color = (i) => { if (i.colorCode) return `&color=${i.colorCode}`; const s = C.seriesById(i.series); const c = s && s.colors && s.colors.find(x => x.name === i.color); return c ? `&color=${c.code}` : ''; };
  function renderItems() {
    const cart = C.readCart();
    const body = $('#lineItems');
    const list = C.units(cart);
    if (!list.length) {
      body.innerHTML = '<div class="empty-state visible" style="padding:34px 10px"><strong>Your cart is empty</strong>Choose a series and add products to build this order.</div><div class="inline-action-row" style="justify-content:center"><a class="table-action primary" href="new-order.html">Choose a series</a></div>';
    } else {
      const groups = [...new Set(list.map(i => i.seriesName))];
      body.innerHTML = groups.map(g => {
        const items = list.filter(i => i.seriesName === g);
        const s = C.seriesById(items[0].series);
        return `<p class="series-group">${g} · ${C.LINE_LABEL[s.line]} <a class="text-link" style="margin-left:8px;text-transform:none;letter-spacing:0" href="${C.pageFor(s)}${i0color(items[0])}">Edit quantities</a></p>` + items.map(i => `<div class="line-item" data-key="${i.key}">
          <div class="product-visual" style="width:56px;height:56px"><svg class="icon" style="width:28px;height:28px;stroke-width:1.4;color:#6d6862"><use href="#${THUMB[i.img] || 'i-box'}"/></svg></div>
          <div><div class="item-name">${i.sku}${i.qty > 1 ? ` <span class="type-chip">${i.unit + 1} of ${i.qty}</span>` : ''}</div><div class="item-meta">${i.desc}${i.box ? ` · Box ${i.box}` : ''}</div>${OrderSummary.optionText(i) ? `<div class="item-meta svc-text">${OrderSummary.optionText(i)}</div>` : ''}${i.assembly != null && cart.assembly === 'yes' ? `<div class="item-meta">Assembly +${money(i.assembly)}</div>` : ''}<div class="line-tag"><span>Customer tag</span><strong>${i.tag || '—'}</strong></div></div>
          <div class="item-price">${i.dealer == null ? '<span class="price-cell quote">On request</span>' : money(i.dealer)}<span>${i.dealer == null ? '' : 'per piece'}</span></div>
        </div>`).join('');
      }).join('');
      const last = cart.items[cart.items.length - 1];
      $('#addMore').href = C.pageFor(C.seriesById(last.series)) + i0color(last);
    }
    renderTotals(); renderAssembly();
  }

  function renderTotals() {
    const cart = C.readCart();
    const n = C.cartCount(cart);
    const sub = C.cartTotal(cart);
    const msrp = cart.items.reduce((s, i) => s + (i.msrp || 0) * i.qty, 0);
    const checked = $('input[name=ship]:checked');
    const ship = checked ? Number(checked.dataset.fee || 0) : 0;
    const asmAmount = cart.assembly === 'yes' ? C.cartAssemblyTotal(cart) : 0;
    const tax = (sub + ship + asmAmount) * TAX;
    $('#sumCount').textContent = n ? `· ${n} item${n === 1 ? '' : 's'}` : '';
    $('#sumMerch').textContent = n ? money(sub) : '—';
    $('#sumMsrp').textContent = n ? money(msrp) : '—';
    $('#sumShip').textContent = money(ship);
    const asm = cart.assembly;
    $('#sumAssembly').textContent = asm === 'yes' ? (asmAmount ? money(asmAmount) : 'Delivered assembled') : asm === 'no' ? 'Not required' : '—';
    $('#shipNote').textContent = checked ? SHIP_LABEL[checked.value] : '';
    $('#sumTax').textContent = n ? money(tax) : '—';
    $('#sumTotal').textContent = n ? money(sub + ship + asmAmount + tax) : '—';
    $('#quoteNote').textContent = C.cartHasQuoteItems(cart) ? 'CAD · dealer pricing · some items priced on request' : 'CAD · dealer pricing';
  }

  /* Dates */
  (function buildDates() {
    const strip = $('#dateStrip');
    const start = new Date();
    let added = 0, offset = 3;
    while (added < 5) {
      const date = new Date(start);
      date.setDate(start.getDate() + offset++);
      if (date.getDay() === 0 || date.getDay() === 6) continue;
      const iso = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
      const button = document.createElement('button');
      button.type = 'button'; button.className = 'date-option'; button.dataset.date = iso;
      button.innerHTML = `<span>${date.toLocaleDateString('en-CA', { weekday: 'short' })}</span><strong>${date.getDate()}</strong><small>${date.toLocaleDateString('en-CA', { month: 'short' })}</small>`;
      button.addEventListener('click', () => { $$('.date-option').forEach(i => i.classList.toggle('selected', i === button)); selectedDate = iso; $('#customDate').value = iso; });
      strip.append(button); added++;
    }
    $('#customDate').min = strip.firstElementChild.dataset.date;
  })();
  $('#customDate').addEventListener('change', e => { selectedDate = e.target.value; $$('.date-option').forEach(i => i.classList.toggle('selected', i.dataset.date === selectedDate)); });

  /* Persist choices into the cart so a draft keeps them */
  $$('input[name=ship]').forEach(r => r.addEventListener('change', () => { C.setCartMeta({ ship: r.value }); renderTotals(); }));
  $('#loadMethod').addEventListener('change', e => C.setCartMeta({ load: e.target.value }));
  $('#poNumber').addEventListener('input', e => { $('#poField').classList.remove('invalid'); C.setCartMeta({ po: e.target.value.trim() }); });
  $('#orderComment').addEventListener('change', e => C.setCartMeta({ comment: e.target.value.trim() }));
  $('#changeAddress').addEventListener('click', () => toast('Shipping address', 'Additional ship-to addresses are managed by your account team.'));

  $('#discountToggle').addEventListener('click', () => { const open = $('#discountPanel').classList.toggle('open'); $('#discountToggle').setAttribute('aria-expanded', String(open)); if (open) $('#discountCode').focus(); });
  $('#applyDiscount').addEventListener('click', () => { const v = $('#discountCode').value.trim(); $('#discountMessage').textContent = v ? 'Code not recognized for this dealer account.' : 'Enter the code shown on your dealer offer.'; });
  /* Build an order record from the cart + the choices on this page */
  const { getOrder, saveOrder, nextId } = Portal;
  function buildOrder(status, id) {
    const cart = C.readCart();
    const units = C.units(cart);
    const tags = [...new Set(units.map(u => u.tag).filter(Boolean))];
    const lines = [...new Set(cart.items.map(i => i.line))];
    const type = lines.length > 1 ? 'mixed' : (lines[0] || 'vanity');
    const subtotal = C.cartTotal(cart), asm = cart.assembly === 'yes' ? C.cartAssemblyTotal(cart) : 0;
    const checked = $('input[name=ship]:checked'); const shipFee = checked ? Number(checked.dataset.fee || 0) : 0;
    const tax = (subtotal + asm + shipFee) * TAX;
    const names = [...new Set(cart.items.map(i => i.seriesName.split(' · ')[0]))];
    return {
      id, name: names.join(' / '), tag: tags.join(', '), type, status,
      date: status === 'draft' ? null : selectedDate, note: status === 'draft' ? 'Until order is placed' : (SHIP_LABEL[checked ? checked.value : 'dealer']),
      po: $('#poNumber').value.trim(), ship: checked ? checked.value : 'dealer', load: $('#loadMethod').value, assembly: cart.assembly || 'no', comment: $('#orderComment').value.trim(),
      items: cart.items.map(i => ({ ...i })), subtotal: +subtotal.toFixed(2), assemblyTotal: +asm.toFixed(2), shipFee, tax: +tax.toFixed(2), total: +(subtotal + asm + shipFee + tax).toFixed(2),
      placedAt: new Date().toISOString().slice(0, 10), isNew: true
    };
  }
  $('#saveDraft').addEventListener('click', () => {
    if (!C.cartCount()) return toast('Nothing to save', 'Add at least one product before saving a draft.', 'error');
    const id = quote && quote.status === 'draft' ? quote.id : nextId('Q-');
    saveOrder(buildOrder('draft', id));
    location.href = `orders.html?status=draft&highlight=${id}`;
  });
  $('#printOrder').addEventListener('click', () => window.print());

  const confirmLayer = $('#confirmLayer');
  const closeConfirm = () => { confirmLayer.classList.remove('open'); confirmLayer.setAttribute('aria-hidden', 'true'); };
  $('#placeOrder').addEventListener('click', () => {
    const cart = C.readCart();
    if (!cart.items.length) return toast('Cart is empty', 'Add products before placing an order.', 'error');
    const po = $('#poNumber').value.trim();
    if (!cart.assembly) { $('#assemblyBar').classList.add('invalid'); $('#assemblyBar').scrollIntoView({ behavior: 'smooth', block: 'center' }); toast('Assembly required?', 'Choose Yes or No in the order summary first.', 'error'); window.setTimeout(() => location.href = backToSummary(), 1600); return; }
    if (!po) { $('#poField').classList.add('invalid'); $('#poNumber').focus(); return toast('PO number required', 'Enter your purchase order number before placing the order.', 'error'); }
    if (!selectedDate) { toast('Choose a shipping ready date', 'Select one of the available dates before placing the order.', 'error'); $('#dateStrip').scrollIntoView({ behavior: 'smooth', block: 'center' }); return; }
    if (!$('#loadMethod').value) { $('#loadMethod').focus(); return toast('Load truck method required', 'Choose skids or hand carry.', 'error'); }
    $('#confirmPo').textContent = po;
    $('#confirmSeries').textContent = [...new Set(cart.items.map(i => i.seriesName))].join(', ');
    const tags = [...new Set(cart.items.flatMap(i => i.tags || []).filter(Boolean))];
    $('#confirmTag').textContent = tags.length ? tags.join(', ') : 'No tags';
    $('#confirmAssembly').textContent = cart.assembly === 'yes' ? 'Yes' : 'No';
    $('#confirmDate').textContent = longDate(selectedDate);
    $('#confirmShip').textContent = `${SHIP_LABEL[$('input[name=ship]:checked').value]} · ${$('#loadMethod').selectedOptions[0].textContent}`;
    $('#confirmTotal').textContent = $('#sumTotal').textContent + ' CAD';
    confirmLayer.classList.add('open'); confirmLayer.setAttribute('aria-hidden', 'false');
    $('#cancelSubmit').focus();
  });
  $('#cancelSubmit').addEventListener('click', () => { closeConfirm(); $('#placeOrder').focus(); });
  $('#confirmSubmit').addEventListener('click', () => {
    const button = $('#confirmSubmit');
    button.disabled = true; button.textContent = 'Submitting…';
    window.setTimeout(() => {
      const id = nextId('CB-');
      saveOrder(buildOrder('submitted', id));
      if (quote && quote.status === 'draft') { const st = Portal.storedOrders().filter(o => o.id !== quote.id); try { localStorage.setItem('cb-dealer-orders', JSON.stringify(st)); } catch (e) {} }
      closeConfirm(); C.clearCart();
      location.href = `order.html?id=${id}&placed=1`;
    }, 700);
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && confirmLayer.classList.contains('open')) $('#cancelSubmit').click(); });

  renderItems();
})();
</script>"""


def checkout_page(menu):
    content = heading("New order · Step 3 of 3", "Place order", "Confirm the shipping address and method, add your PO number, then place the order or save it as a draft.") + steps(3) + CONTENT
    return content, SCRIPT
