"""Page bodies for the dealer portal. Each function returns (content_html, script_html)."""
import html as H
from docs import DOCS, doc_card

TODAY_KICKER = "Sunday · September 13"


def heading(kicker, title, lede=None, actions=""):
    lede_html = f'<p class="lede">{lede}</p>' if lede else ""
    return f'''
<section class="page-heading">
  <div>
    <p class="kicker">{kicker}</p>
    <h1>{title}</h1>
    {lede_html}
  </div>
  <div class="heading-actions">{actions}</div>
</section>'''


ORDER_TABLE_HEAD = '<thead><tr><th>Order # / PO #</th><th>Status</th><th>Ready date</th><th>Total</th><th><span class="sr-only">Actions</span></th></tr></thead>'


# ---------------------------------------------------------------- Overview
def overview(menu):
    content = heading(TODAY_KICKER, "Good afternoon, Humphrey.", actions=menu) + '''
<section class="metrics" aria-label="Order summary" id="metrics">
  <button class="metric selectable attention" data-filter="draft" aria-pressed="false">
    <div class="metric-label"><svg class="icon" width="15" height="15"><use href="#i-edit"/></svg>Drafts to finish</div>
    <div class="metric-value" data-metric="draft">–</div>
    <div class="metric-note">Oldest saved 5 days ago</div>
  </button>
  <button class="metric selectable" data-filter="production" aria-pressed="false">
    <div class="metric-label"><svg class="icon" width="15" height="15"><use href="#i-box"/></svg>In production</div>
    <div class="metric-value" data-metric="production">–</div>
    <div class="metric-note">2 updated today</div>
  </button>
  <button class="metric selectable ready" data-filter="ready" aria-pressed="false">
    <div class="metric-label"><svg class="icon" width="15" height="15"><use href="#i-check"/></svg>Ready for pickup</div>
    <div class="metric-value" data-metric="ready">–</div>
    <div class="metric-note">Pickup details confirmed</div>
  </button>
  <button class="metric selectable" data-filter="upcoming" aria-pressed="false">
    <div class="metric-label"><svg class="icon" width="15" height="15"><use href="#i-calendar"/></svg>Next ready date</div>
    <div class="metric-value small" data-metric="next-date">–</div>
    <div class="metric-note" data-metric="next-name"></div>
  </button>
</section>

<div class="workspace-grid">
  <section class="panel orders-panel" aria-labelledby="orders-heading">
    <div class="panel-head">
      <h2 id="orders-heading">Recent orders &amp; quotes</h2>
      <a class="text-link" href="orders.html">View all orders<svg class="icon" width="14" height="14"><use href="#i-chevron"/></svg></a>
    </div>
    <div class="table-scroll">
      <table class="data-table orders">''' + ORDER_TABLE_HEAD + '''
        <tbody id="recentOrders"></tbody>
      </table>
    </div>
    <div class="panel-foot"><span id="recentNote">Showing the 5 most recent of <strong data-count="orders">12</strong> orders</span><a class="text-link" id="recentLink" href="orders.html">Open Orders</a></div>
  </section>

  <aside class="side-stack">
    <section class="panel quick-start" aria-labelledby="quick-heading">
      <h2 id="quick-heading">Start an order</h2>
      <p>Choose the product line to begin.</p>
      <a class="start-option" href="new-order.html?line=kitchen">
        <span class="start-icon"><svg class="icon"><use href="#i-kitchen"/></svg></span>
        <span><strong>Kitchen</strong><small>Choose a series, then add cabinets</small></span>
        <svg class="icon"><use href="#i-chevron"/></svg>
      </a>
      <a class="start-option" href="new-order.html?line=vanity">
        <span class="start-icon"><svg class="icon"><use href="#i-vanity"/></svg></span>
        <span><strong>Vanity</strong><small>Choose a series, then add vanities</small></span>
        <svg class="icon"><use href="#i-chevron"/></svg>
      </a>
      <a class="start-option" href="new-order-vanity-top.html?series=vanity-top">
        <span class="start-icon"><svg class="icon"><use href="#i-counter"/></svg></span>
        <span><strong>Vanity top</strong><small>Quartz &amp; sintered stone tops · pick the top, then the size</small></span>
        <svg class="icon"><use href="#i-chevron"/></svg>
      </a>
      <a class="start-option" href="new-order-products.html?series=hardware">
        <span class="start-icon"><svg class="icon"><use href="#i-hardware"/></svg></span>
        <span><strong>Hardware</strong><small>Handles, knobs, LED and parts · standard and premium</small></span>
        <svg class="icon"><use href="#i-chevron"/></svg>
      </a>
    </section>
    <section class="panel quick-start" aria-labelledby="docs-heading">
      <h2 id="docs-heading">Documents</h2>
      <p>Current dealer resources, ready to download.</p>
      <a class="start-option" href="price-book.html">
        <span class="start-icon"><svg class="icon"><use href="#i-book"/></svg></span>
        <span><strong>Price book</strong><small>August 2026 edition now current</small></span>
        <svg class="icon"><use href="#i-chevron"/></svg>
      </a>
      <a class="start-option" href="catalog.html">
        <span class="start-icon"><svg class="icon"><use href="#i-catalog"/></svg></span>
        <span><strong>Catalog</strong><small>Kitchen and bathroom collections</small></span>
        <svg class="icon"><use href="#i-chevron"/></svg>
      </a>
      <a class="start-option" href="design-library.html">
        <span class="start-icon"><svg class="icon"><use href="#i-palette"/></svg></span>
        <span><strong>Design library</strong><small>Door styles, finishes, specs</small></span>
        <svg class="icon"><use href="#i-chevron"/></svg>
      </a>
    </section>
    <section class="panel help-card">
      <span class="mini-label">Dealer support</span>
      <h3>Need an order checked?</h3>
      <p>Send the quote number to your account team before placing the order.</p>
      <a href="support.html">Contact dealer support</a>
    </section>
  </aside>
</div>'''
    script = '''<script>
(() => {
  const { $, $$, ORDERS, renderOrders, counts, shortDate } = Portal;
  const c = counts();
  $('[data-metric="draft"]').textContent = c.draft || 0;
  $('[data-metric="production"]').textContent = c.production || 0;
  $('[data-metric="ready"]').textContent = c.ready || 0;
  const upcoming = ORDERS.filter(o => o.date && o.date !== 'ready').sort((a, b) => a.date.localeCompare(b.date));
  if (upcoming[0]) { $('[data-metric="next-date"]').textContent = shortDate(upcoming[0].date); $('[data-metric="next-name"]').textContent = upcoming[0].name; }

  /* Clicking a metric selects it (coloured bar) and filters the list below; click again to clear */
  const TITLE = { draft: 'Drafts to finish', production: 'In production', ready: 'Ready for pickup', upcoming: 'Upcoming ready dates' };
  const LINK = { draft: 'orders.html?status=draft', production: 'orders.html?status=production', ready: 'orders.html?status=ready', upcoming: 'orders.html' };
  let selected = null;
  function render() {
    $$('#metrics .metric').forEach(m => { const on = m.dataset.filter === selected; m.classList.toggle('selected', on); m.setAttribute('aria-pressed', String(on)); });
    const list = !selected ? ORDERS.slice(0, 5) : selected === 'upcoming' ? upcoming : ORDERS.filter(o => o.status === selected);
    renderOrders($('#recentOrders'), list);
    $('#orders-heading').textContent = selected ? TITLE[selected] : 'Recent orders & quotes';
    $('#recentNote').innerHTML = selected ? `Showing ${list.length} order${list.length === 1 ? '' : 's'} · ${TITLE[selected]}${selected === 'upcoming' ? ', soonest first' : ''} · <a class="text-link" href="#" id="clearFilter">Show recent</a>` : 'Showing the 5 most recent of <strong>' + ORDERS.length + '</strong> orders';
    $('#recentLink').href = selected ? LINK[selected] : 'orders.html';
    const clear = $('#clearFilter'); if (clear) clear.addEventListener('click', e => { e.preventDefault(); selected = null; render(); });
  }
  $$('#metrics .metric').forEach(m => m.addEventListener('click', () => { selected = selected === m.dataset.filter ? null : m.dataset.filter; render(); }));
  render();
})();
</script>'''
    return content, script


# ---------------------------------------------------------------- Orders
def orders(menu):
    content = heading("Workspace", "Orders &amp; quotes", "Every draft quote, submitted order and delivery on your dealer account.", actions=menu) + '''
<section class="panel orders-panel" aria-labelledby="orders-heading">
  <div class="panel-head">
    <h2 id="orders-heading">All orders</h2>
    <div class="head-tools">
      <label class="search-box">
        <svg class="icon" width="16" height="16"><use href="#i-search"/></svg>
        <span class="sr-only">Search orders</span>
        <input id="orderSearch" type="search" placeholder="Order, customer or tag">
      </label>
      <select id="typeFilter" class="secondary-button" aria-label="Filter by product line" style="padding-right:12px">
        <option value="all">All lines</option>
        <option value="kitchen">Kitchen</option>
        <option value="vanity">Vanity</option>
      </select>
    </div>
  </div>
  <div class="tabs" role="tablist" aria-label="Filter orders" id="statusTabs">
    <button class="tab active" role="tab" aria-selected="true" data-filter="all">All orders · <span data-tab-count="all"></span></button>
    <button class="tab" role="tab" aria-selected="false" data-filter="draft">Drafts · <span data-tab-count="draft"></span></button>
    <button class="tab" role="tab" aria-selected="false" data-filter="submitted">Submitted · <span data-tab-count="submitted"></span></button>
    <button class="tab" role="tab" aria-selected="false" data-filter="production">In production · <span data-tab-count="production"></span></button>
    <button class="tab" role="tab" aria-selected="false" data-filter="ready">Ready · <span data-tab-count="ready"></span></button>
  </div>
  <div class="table-scroll">
    <table class="data-table orders">''' + ORDER_TABLE_HEAD + '''
      <tbody id="ordersBody"></tbody>
    </table>
  </div>
  <div class="empty-state" id="emptyState"><strong>No matching orders</strong>Try an order number, customer name, or customer tag.</div>
  <div class="panel-foot"><span id="visibleCount"></span><span>Prices shown in CAD · dealer pricing</span></div>
</section>'''
    script = '''<script>
(() => {
  const { $, $$, ORDERS, renderOrders, counts } = Portal;
  const c = counts();
  $$('[data-tab-count]').forEach(el => el.textContent = c[el.dataset.tabCount] || 0);
  renderOrders($('#ordersBody'), ORDERS);

  function filterOrders() {
    const active = $('.tab.active').dataset.filter;
    const type = $('#typeFilter').value;
    const query = $('#orderSearch').value.trim().toLowerCase();
    let visible = 0;
    $$('#ordersBody tr').forEach(row => {
      const ok = (active === 'all' || row.dataset.status === active) && (type === 'all' || row.dataset.type === type) && (!query || row.dataset.search.includes(query));
      row.hidden = !ok;
      if (ok) visible++;
    });
    $('#emptyState').classList.toggle('visible', visible === 0);
    $('.table-scroll').style.display = visible === 0 ? 'none' : '';
    $('#visibleCount').textContent = `Showing ${visible} of ${ORDERS.length} orders`;
  }
  $$('.tab').forEach(tab => tab.addEventListener('click', () => {
    $$('.tab').forEach(item => { item.classList.toggle('active', item === tab); item.setAttribute('aria-selected', String(item === tab)); });
    filterOrders();
  }));
  $('#orderSearch').addEventListener('input', filterOrders);
  $('#typeFilter').addEventListener('change', filterOrders);
  const params = new URLSearchParams(location.search);
  if (params.get('status')) { const tab = $(`.tab[data-filter="${params.get('status')}"]`); tab && tab.click(); }
  if (params.get('highlight')) { const row = $$('#ordersBody tr').find(r => r.dataset.search.startsWith(params.get('highlight').toLowerCase())); if (row) { row.classList.add('highlight'); row.scrollIntoView({ block: 'center' }); } }
  filterOrders();
})();
</script>'''
    return content, script


# ---------------------------------------------------------------- Invoices
def invoices(menu):
    content = heading("Workspace", "My invoices", "Invoices issued against your dealer account. Contact your CSR for copies or payment questions.", actions='<a class="secondary-button" href="support.html"><svg class="icon"><use href="#i-help"/></svg>Billing question</a>') + '''
<section class="metrics" aria-label="Invoice summary">
  <article class="metric attention">
    <div class="metric-label"><svg class="icon" width="15" height="15"><use href="#i-invoice"/></svg>Outstanding balance</div>
    <div class="metric-value small" id="mOutstanding">–</div>
    <div class="metric-note" id="mOutstandingNote"></div>
  </article>
  <article class="metric danger">
    <div class="metric-label"><svg class="icon" width="15" height="15"><use href="#i-bell"/></svg>Overdue</div>
    <div class="metric-value small" id="mOverdue">–</div>
    <div class="metric-note" id="mOverdueNote"></div>
  </article>
  <article class="metric">
    <div class="metric-label"><svg class="icon" width="15" height="15"><use href="#i-calendar"/></svg>Due within 7 days</div>
    <div class="metric-value small" id="mSoon">–</div>
    <div class="metric-note" id="mSoonNote"></div>
  </article>
  <article class="metric ready">
    <div class="metric-label"><svg class="icon" width="15" height="15"><use href="#i-check"/></svg>Paid · last 90 days</div>
    <div class="metric-value small" id="mPaid">–</div>
    <div class="metric-note" id="mPaidNote"></div>
  </article>
</section>

<section class="panel orders-panel" style="margin-top:24px" aria-labelledby="inv-heading">
  <div class="panel-head">
    <h2 id="inv-heading">Invoices</h2>
    <label class="search-box">
      <svg class="icon" width="16" height="16"><use href="#i-search"/></svg>
      <span class="sr-only">Search invoices</span>
      <input id="invoiceSearch" type="search" placeholder="Invoice, order or tag">
    </label>
  </div>
  <div class="tabs" role="tablist" aria-label="Filter invoices">
    <button class="tab active" role="tab" aria-selected="true" data-filter="all">All</button>
    <button class="tab" role="tab" aria-selected="false" data-filter="unpaid">Unpaid</button>
    <button class="tab" role="tab" aria-selected="false" data-filter="overdue">Overdue</button>
    <button class="tab" role="tab" aria-selected="false" data-filter="paid">Paid</button>
  </div>
  <div class="table-scroll">
    <table class="data-table">
      <thead><tr><th>Invoice / order</th><th>Issued</th><th>Due</th><th>Status</th><th class="num">Amount</th></tr></thead>
      <tbody id="invoiceBody"></tbody>
    </table>
  </div>
  <div class="empty-state" id="emptyState"><strong>No matching invoices</strong>Try an invoice number, order number or customer tag.</div>
  <div class="panel-foot"><span>Amounts include tax · CAD</span></div>
</section>'''
    script = r'''<script>
(() => {
  const { $, $$, money, longDate, toast } = Portal;
  const TODAY = '2026-09-13';
  const INVOICES = [
    { id: 'INV-30412', order: '300010806', name: 'Kingsway guest bath',   tag: 'KING-GUEST', issued: '2026-09-08', due: '2026-10-08', amount: 3945.96,  paid: null },
    { id: 'INV-30398', order: '300010812', name: 'Lakeside condo vanity', tag: 'LAKE-V60',   issued: '2026-09-04', due: '2026-10-04', amount: 3344.80,  paid: null },
    { id: 'INV-30371', order: '300010788', name: 'Parkview ensuite',      tag: 'PARK-ENS',   issued: '2026-08-21', due: '2026-09-20', amount: 5867.20,  paid: null },
    { id: 'INV-30355', order: '300010771', name: 'Ridgeway kitchen',      tag: 'RIDGE-K',    issued: '2026-08-10', due: '2026-09-09', amount: 19214.00, paid: null },
    { id: 'INV-30340', order: '300010763', name: 'Aspen loft vanity',     tag: 'ASPEN-36',   issued: '2026-07-30', due: '2026-08-29', amount: 2610.40,  paid: '2026-08-27' },
    { id: 'INV-30322', order: '300010749', name: 'Hillcrest kitchen',     tag: 'HILL-K2',    issued: '2026-07-18', due: '2026-08-17', amount: 22905.50, paid: '2026-08-15' },
    { id: 'INV-30301', order: '300010731', name: 'Bayview powder room',   tag: 'BAY-PWDR',   issued: '2026-07-03', due: '2026-08-02', amount: 1984.00,  paid: '2026-07-30' },
    { id: 'INV-30288', order: '300010720', name: 'Greenfield kitchen',    tag: 'GREEN-K',    issued: '2026-06-20', due: '2026-07-20', amount: 17350.00, paid: '2026-07-19' }
  ];
  const daysUntil = (iso) => Math.round((new Date(iso + 'T12:00:00Z') - new Date(TODAY + 'T12:00:00Z')) / 86400000);
  const statusOf = (inv) => inv.paid ? 'paid' : daysUntil(inv.due) < 0 ? 'overdue' : 'due';
  const LABEL = { paid: 'Paid', overdue: 'Overdue', due: 'Due' };

  const unpaid = INVOICES.filter(i => !i.paid);
  const overdue = unpaid.filter(i => statusOf(i) === 'overdue');
  const soon = unpaid.filter(i => { const d = daysUntil(i.due); return d >= 0 && d <= 7; });
  const paid = INVOICES.filter(i => i.paid && daysUntil(i.paid) >= -90);
  const sum = (list) => list.reduce((s, i) => s + i.amount, 0);
  $('#mOutstanding').textContent = money(sum(unpaid)); $('#mOutstandingNote').textContent = `${unpaid.length} open invoice${unpaid.length === 1 ? '' : 's'}`;
  $('#mOverdue').textContent = money(sum(overdue)); $('#mOverdueNote').textContent = overdue.length ? `${overdue[0].id} · ${-daysUntil(overdue[0].due)} days past due` : 'Nothing overdue';
  $('#mSoon').textContent = money(sum(soon)); $('#mSoonNote').textContent = soon.length ? `${soon[0].id} due ${longDate(soon[0].due)}` : 'Nothing due this week';
  $('#mPaid').textContent = money(sum(paid)); $('#mPaidNote').textContent = `${paid.length} invoices settled`;

  const body = $('#invoiceBody');
  body.innerHTML = INVOICES.map(inv => {
    const s = statusOf(inv);
    const dueCell = inv.paid ? `${longDate(inv.due)}<span>Paid ${longDate(inv.paid)}</span>` : s === 'overdue' ? `${longDate(inv.due)}<span>${-daysUntil(inv.due)} days past due</span>` : `${longDate(inv.due)}<span>in ${daysUntil(inv.due)} days</span>`;
    return `<tr data-status="${s}" data-search="${(inv.id + ' ' + inv.order + ' ' + inv.name + ' ' + inv.tag + ' ' + s).toLowerCase()}">
      <td><div class="order-id">${inv.id}</div><div class="order-tag">${inv.order} · ${inv.name} · ${inv.tag}</div></td>
      <td class="date-cell">${longDate(inv.issued)}</td>
      <td class="date-cell">${dueCell}</td>
      <td><span class="status ${s}">${LABEL[s]}</span></td>
      <td class="price-cell num">${money(inv.amount)}</td>
    </tr>`;
  }).join('');

  function filter() {
    const active = $('.tab.active').dataset.filter;
    const q = $('#invoiceSearch').value.trim().toLowerCase();
    let visible = 0;
    $$('#invoiceBody tr').forEach(row => {
      const s = row.dataset.status;
      const statusOk = active === 'all' || (active === 'unpaid' ? s !== 'paid' : s === active);
      const ok = statusOk && (!q || row.dataset.search.includes(q));
      row.hidden = !ok; if (ok) visible++;
    });
    $('#emptyState').classList.toggle('visible', visible === 0);
    $('.table-scroll').style.display = visible === 0 ? 'none' : '';
  }
  $$('.tab').forEach(tab => tab.addEventListener('click', () => { $$('.tab').forEach(t => { t.classList.toggle('active', t === tab); t.setAttribute('aria-selected', String(t === tab)); }); filter(); }));
  $('#invoiceSearch').addEventListener('input', filter);
})();
</script>'''
    return content, script


# ---------------------------------------------------------------- Documents
DOC_TABS = [("price-book.html", "i-book", "Price book"), ("catalog.html", "i-catalog", "Catalog"), ("design-library.html", "i-palette", "Design library")]


def doc_tabs(active):
    return '<nav class="doc-tabs" aria-label="Document libraries">' + "".join(
        f'<a class="doc-tab{" active" if href == active else ""}" href="{href}"><svg class="icon"><use href="#{icon}"/></svg>{text}</a>' for href, icon, text in DOC_TABS
    ) + '</nav>'


def doc_page(file, kicker, title, lede, sections):
    body = doc_tabs(file)
    for sec in sections:
        cards = "".join(doc_card(d) for d in sec["docs"])
        body += f'''
<section class="doc-section">
  <div class="doc-section-head"><h2>{sec["title"]}</h2><p>{sec["note"]}</p></div>
  <div class="doc-grid">{cards}</div>
</section>'''
    content = heading(kicker, title, lede) + body
    return content, ""


def price_book(menu):
    return doc_page("price-book.html", "Documents", "Price book", "Current dealer price books and price lists. Always quote from the edition marked current — superseded editions are kept for reference only.", DOCS["price-book"])


def catalog(menu):
    return doc_page("catalog.html", "Documents", "Catalog", "Customer-facing product catalogs for the kitchen and bathroom collections. Share these with homeowners and designers.", DOCS["catalog"])


def design_library(menu):
    return doc_page("design-library.html", "Documents", "Design library", "Door styles, finishes, materials and specification sheets for planning and presenting Classic Brand projects.", DOCS["design-library"])


# ---------------------------------------------------------------- Account
def profile(menu):
    content = heading("Account", "Profile", "Your dealer account details as held by Classic Brand Cabinetry. Contact dealer support to change anything shown here.") + '''
<div class="checkout-grid">
  <div class="checkout-main">
    <section class="order-card">
      <div class="order-card-head"><div><span class="step-label">Dealer</span><h3>Account details</h3></div><span class="status ready">Active</span></div>
      <div class="order-card-body">
        <div class="confirm-details" style="margin:0;font-size:12px">
          <div><span>Dealer name</span><strong>Humphrey</strong></div>
          <div><span>Dealer ID</span><strong>CB-20418</strong></div>
          <div><span>Account email</span><strong>humzch21@gmail.com</strong></div>
          <div><span>Pricing tier</span><strong>Contract pricing · Tier 2</strong></div>
          <div><span>Payment terms</span><strong>Net 30</strong></div>
          <div><span>Default delivery</span><strong>Standard delivery to dealer address</strong></div>
        </div>
      </div>
    </section>
    <section class="order-card">
      <div class="order-card-head"><div><span class="step-label">Notifications</span><h3>Email preferences</h3></div></div>
      <div class="order-card-body">
        <div class="delivery-options">
          <label class="choice"><input type="checkbox" checked><span><strong>Order status changes</strong><small>Submitted, in production, ready for pickup</small></span></label>
          <label class="choice"><input type="checkbox" checked><span><strong>New invoices and payment reminders</strong><small>Sent to the account email</small></span></label>
          <label class="choice"><input type="checkbox"><span><strong>Document updates</strong><small>New price book, catalog and design library releases</small></span></label>
        </div>
      </div>
    </section>
  </div>
  <aside class="checkout-side">
    <section class="order-card draft-explainer">
      <strong>Need to update your details?</strong>
      <p>Address, pricing tier and payment term changes are made by your account team. Use Dealer support and quote your Dealer ID.</p>
    </section>
  </aside>
</div>'''
    return content, ""


# ---------------------------------------------------------------- Inventory checking
def inventory(menu):
    from support_pages import support_tabs
    content = heading("Dealer support", "Inventory checking", "Open the live stock page for any colour or finish code.") + support_tabs("inventory.html") + '''
<div class="stock-board" id="stockBoard"></div>'''
    script = r'''<script src="assets/inventory.js"></script>
<script>
(() => {
  const { $ } = Portal;
  const I = Inventory;
  $('#stockBoard').innerHTML = I.FAMILIES.map(f => `<section class="panel stock-family stock-${f.id}" aria-labelledby="stock-${f.id}">
    <header class="stock-family-head"><span class="stock-family-icon"><svg class="icon"><use href="#${f.icon}"/></svg></span><h2 id="stock-${f.id}">${f.name}</h2></header>
    ${f.groups.map(g => `<div class="stock-group"><div class="stock-group-name">${g.name}</div><div class="stock-chips">${g.items.map(i => `<a class="stock-chip${i.discontinued ? ' discontinued' : ''}" href="${I.hrefOf(f, i)}" target="_blank" rel="noopener" title="Open stock page for ${I.codeOf(i)}">${i.hideCode ? i.name : i.name ? `${i.name} <b>(${I.codeOf(i)})</b>` : `<b class="only">${I.codeOf(i)}</b>`}${i.note ? `<small>${i.note}</small>` : ''}</a>`).join('')}</div></div>`).join('')}
  </section>`).join('');
})();
</script>'''
    return content, script


# ---------------------------------------------------------------- Order detail
def order_detail(menu):
    actions = '''<a class="secondary-button" href="orders.html"><svg class="icon back"><use href="#i-chevron"/></svg>All orders</a><button class="secondary-button" id="reorder"><svg class="icon"><use href="#i-cart"/></svg>Reorder</button><a class="quiet-button" id="reportIssue" href="support-replacement.html"><svg class="icon"><use href="#i-swap"/></svg>Report an issue</a><button class="quiet-button" id="printOrder"><svg class="icon"><use href="#i-printer"/></svg>Print</button>'''
    content = heading("Order", "Order", actions=actions) + '''
<div class="placed-banner" id="placedBanner" hidden><svg class="icon"><use href="#i-check"/></svg><div><strong>Order placed</strong><span>It now shows under Orders as Submitted. The order desk confirms the ready date by email.</span></div></div>

<section class="order-facts" id="orderFacts"></section>

<div class="checkout-grid">
  <div class="checkout-main">
    <section class="order-card">
      <div class="order-card-head"><div><span class="step-label">Order contents</span><h3 id="itemsTitle">Items</h3></div><span class="status" id="assemblyChip"></span></div>
      <div class="order-card-body checkout-items" id="lineItems"></div>
    </section>
    <section class="order-card">
      <div class="order-card-head"><div><span class="step-label">Delivery</span><h3>Shipping &amp; pickup</h3></div></div>
      <div class="order-card-body" id="shipBody"></div>
    </section>
  </div>
  <aside class="checkout-side">
    <section class="order-card summary-card">
      <h3>Order summary</h3>
      <div class="summary-line"><span>Cart subtotal <span id="sumCount"></span></span><span id="sumMerch">&mdash;</span></div>
      <div class="summary-line"><span>MSRP value</span><span id="sumMsrp">&mdash;</span></div>
      <div class="summary-line"><span>Shipping</span><span id="sumShip">&mdash;</span></div>
      <div class="summary-line"><span>Assembly</span><span id="sumAssembly">&mdash;</span></div>
      <div class="summary-line"><span>Tax (HST 13%)</span><span id="sumTax">&mdash;</span></div>
      <div class="summary-total"><span>Order total</span><strong id="sumTotal">&mdash;</strong></div>
      <p class="price-note">CAD &middot; dealer pricing</p>
    </section>
    <section class="order-card">
      <div class="order-card-head"><div><span class="step-label">Status</span><h3>Progress</h3></div></div>
      <div class="order-card-body"><ol class="timeline" id="timeline"></ol></div>
    </section>
  </aside>
</div>
<div class="empty-state" id="notFound"><strong>Order not found</strong>This order number is not on file in this browser. <a class="text-link" href="orders.html">Back to orders</a></div>'''
    script = r'''<script>
(() => {
  const { $, $$, money, longDate, getOrder, STATUS_LABEL } = Portal;
  const C = Catalog;
  const params = new URLSearchParams(location.search);
  const order = getOrder(params.get('id'));
  const SHIP_LABEL = { dealer: 'Pick up by dealer – Free', 'cbc-truck': 'CBC truck stand delivery', dc: 'Pick up by DC', 'third-party': 'Pick up by third party' };
  const LOAD_LABEL = { skids: 'Load product with skids', hand: 'Hand carry product with truck' };
  if (!order) { $('.checkout-grid').hidden = true; $('#orderFacts').hidden = true; $('#notFound').classList.add('visible'); $('h1').textContent = 'Order not found'; return; }
  document.title = `${order.id} — Classic Brand Cabinetry`;
  $('h1').innerHTML = `${order.status === 'draft' ? '' : '<span class="h1-label">Order #</span>'}${order.id} <span class="status ${order.status}" style="vertical-align:middle;margin-left:10px">${STATUS_LABEL[order.status]}</span>`;
  $('.kicker').textContent = order.status === 'draft' ? 'Draft quote · gets an order number when placed' : 'Order · this number is also the SAP sales order (SO) number';
  $('#placedBanner').hidden = params.get('placed') !== '1';
  if (order.status === 'draft') { const a = document.createElement('a'); a.className = 'primary-button'; a.href = `new-order-checkout.html?quote=${order.id}`; a.innerHTML = '<svg class="icon"><use href="#i-edit"/></svg>Continue this quote'; $('.heading-actions').prepend(a); }

  const units = C.units({ items: order.items || [] });
  const tags = [...new Set(units.map(u => u.tag).filter(Boolean))];
  const facts = [
    ['Order # · SAP SO', order.status === 'draft' ? 'Assigned when placed' : order.id], ['PO # (yours)', order.po || '—'], ['Customer tag', tags.length ? tags.join(', ') : '—'],
    [order.status === 'draft' ? 'Saved' : 'Placed', order.placedAt ? longDate(order.placedAt) : '—'],
    ['Ready date', order.status === 'draft' ? 'Set when placed' : order.date === 'ready' ? 'Ready now' : order.date ? longDate(order.date) : 'To be confirmed'],
    ['Shipping', SHIP_LABEL[order.ship] || order.note || '—']
  ];
  $('#orderFacts').innerHTML = facts.map(([l, v]) => `<div><span>${l}</span><strong>${v}</strong></div>`).join('');

  const THUMB = OrderSummary.THUMB;
  const groups = [...new Set(units.map(i => i.seriesName))];
  $('#itemsTitle').textContent = `${units.length} piece${units.length === 1 ? '' : 's'} · ${order.items.length} line${order.items.length === 1 ? '' : 's'}`;
  $('#lineItems').innerHTML = units.length ? groups.map(g => `<p class="series-group">${g}</p>` + units.filter(i => i.seriesName === g).map(i => `<div class="line-item">
      <div class="product-visual" style="width:56px;height:56px"><svg class="icon" style="width:28px;height:28px;stroke-width:1.4;color:#6d6862"><use href="#${THUMB[i.img] || 'i-box'}"/></svg></div>
      <div><div class="item-name">${i.sku}${i.qty > 1 ? ` <span class="type-chip">${i.unit + 1} of ${i.qty}</span>` : ''}</div><div class="item-meta">${i.desc}${i.box ? ` · Box ${i.box}` : ''}</div>${OrderSummary.optionText(i) ? `<div class="item-meta svc-text">${OrderSummary.optionText(i)}</div>` : ''}${i.assembly != null && order.assembly === 'yes' ? `<div class="item-meta">Assembly +${money(i.assembly)}</div>` : ''}<div class="line-tag"><span>Customer tag</span><strong>${i.tag || '—'}</strong></div></div>
      <div class="item-price">${i.dealer == null ? '<span class="price-cell quote">On request</span>' : money(i.dealer)}<span>per piece</span></div>
    </div>`).join('')).join('') : '<div class="empty-state visible">No line items on file for this order.</div>';
  const asmChip = $('#assemblyChip'); asmChip.classList.add(order.assembly === 'yes' ? 'ready' : 'submitted'); asmChip.textContent = order.assembly === 'yes' ? 'Delivered assembled' : 'Ships flat-packed';

  $('#shipBody').innerHTML = `<div class="address-card"><span class="addr-check"><svg class="icon" width="14" height="14"><use href="#i-check"/></svg></span><strong>Humphrey · Dealer CB-20418</strong>3095 Universal Drive<br>Mississauga, Ontario<br>Canada<div class="addr-phone">905 232 4660</div></div>
    <div class="ship-facts"><div><span>Shipping method</span><strong>${SHIP_LABEL[order.ship] || '—'}</strong></div><div><span>Load truck method</span><strong>${LOAD_LABEL[order.load] || '—'}</strong></div><div><span>Ready date</span><strong>${order.date === 'ready' ? 'Ready now · ' + (order.note || '') : order.date ? longDate(order.date) : 'To be confirmed'}</strong></div>${order.comment ? `<div><span>Comment</span><strong>${order.comment}</strong></div>` : ''}</div>`;

  const msrp = (order.items || []).reduce((s, i) => s + (i.msrp || 0) * i.qty, 0);
  $('#sumCount').textContent = `· ${units.length} item${units.length === 1 ? '' : 's'}`;
  $('#sumMerch').textContent = money(order.subtotal || 0); $('#sumMsrp').textContent = money(msrp);
  $('#sumShip').textContent = money(order.shipFee || 0);
  $('#sumAssembly').textContent = order.assembly === 'yes' ? money(order.assemblyTotal || 0) : 'Not required';
  $('#sumTax').textContent = money(order.tax || 0); $('#sumTotal').textContent = money(order.total || 0);

  const steps = order.status === 'draft' ? [['Draft saved', true], ['Order placed', false], ['In production', false], ['Ready for pickup', false]] : [['Order placed', true], ['Submitted · confirmed by order desk', true], ['In production', order.status === 'production' || order.status === 'ready'], ['Ready for pickup', order.status === 'ready']];
  const currentIdx = steps.map(s => s[1]).lastIndexOf(true);
  $('#timeline').innerHTML = steps.map(([label, done], i) => `<li class="${done ? 'done' : ''}${i === currentIdx ? ' current' : ''}"><i></i><span>${label}</span>${i === 0 && order.placedAt ? `<small>${longDate(order.placedAt)}</small>` : i === 3 && order.date && order.date !== 'ready' ? `<small>Est. ${longDate(order.date)}</small>` : ''}</li>`).join('');

  $('#printOrder').addEventListener('click', () => window.print());
  $('#reportIssue').href = `support-replacement.html?order=${order.id}`; $('#reportIssue').hidden = order.status === 'draft';
  $('#reorder').addEventListener('click', () => { C.writeCart({ items: (order.items || []).map(i => ({ ...i, tags: Array.from({ length: i.qty }, () => '') })) }); const first = order.items[0]; const s = first && C.seriesById(first.series); location.href = s ? `${C.pageFor(s)}${first.colorCode ? '&color=' + first.colorCode : ''}&summary=1` : 'new-order.html'; });
})();
</script>'''
    return content, script


PAGES = [
    ("index.html",          "Dealer Order Desk", "Overview",       overview),
    ("orders.html",         "Orders & quotes",   "Orders",         orders),
    ("order.html",          "Order details",     "Orders",         order_detail),
    ("new-order.html",          "New order · Choose a series", "New order", "series_page"),
    ("new-order-products.html", "New order · Add products",    "New order", "products_page"),
    ("new-order-vanity-top.html", "New order · Vanity tops",   "New order", "vanity_top_page"),
    ("new-order-checkout.html", "New order · Checkout",        "New order", "checkout_page"),
    ("invoices.html",       "My invoices",       "My invoices",    invoices),
    ("inventory.html",      "Inventory checking", "Inventory checking", inventory),
    ("price-book.html",     "Price book",        "Price book",     price_book),
    ("catalog.html",        "Catalog",           "Catalog",        catalog),
    ("design-library.html", "Design library",    "Design library", design_library),
    ("profile.html",        "Profile",           "Profile",        profile),
    ("support.html",             "Customer support",    "Customer support",    "customer_support"),
    ("support-delivery.html",    "Delivery service",    "Delivery service",    "delivery"),
    ("support-assembly.html",    "Assembly service",    "Assembly service",    "assembly"),
    ("support-videos.html",      "Assembly videos",     "Assembly videos",     "videos"),
    ("support-replacement.html", "Product replacement", "Product replacement", "replacement"),
]


def build(shell, menu):
    import order_pages, support_pages
    out = {}
    for file, title, crumb, fn in PAGES:
        if isinstance(fn, str):
            fn = getattr(order_pages, fn, None) or getattr(support_pages, fn)
        content, script = fn(menu)
        out[file] = shell(file=file, title=title, crumb=crumb, content=content, script=script)
    return out
