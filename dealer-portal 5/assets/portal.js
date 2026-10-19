/* Classic Brand dealer portal — shared data and behaviour */
window.Portal = (() => {
  const $ = (selector, parent = document) => parent.querySelector(selector);
  const $$ = (selector, parent = document) => [...parent.querySelectorAll(selector)];

  /* Orders = orders placed or drafted in this browser (localStorage) followed by the sample orders in assets/sample-orders.js */
  const ORDERS_KEY = 'cb-dealer-orders';
  const storedOrders = () => { try { return JSON.parse(localStorage.getItem(ORDERS_KEY)) || []; } catch (e) { return []; } };
  const SAMPLE = window.SampleOrders || [];
  const ORDERS = [...storedOrders(), ...SAMPLE];
  const getOrder = (id) => ORDERS.find(o => o.id === id) || null;
  /* Next order / quote number after the highest one on file */
  /* Web order numbers start with 3 (Magento increment ID, synced to SAP as the sales order number); quotes use Q- */
  const nextId = (prefix) => {
    if (prefix === 'Q-') { const n = Math.max(1852, ...ORDERS.filter(o => o.id.startsWith('Q-')).map(o => Number(o.id.slice(2)) || 0)); return `Q-${n + 1}`; }
    const n = Math.max(300010860, ...ORDERS.filter(o => /^3\d{8}$/.test(o.id)).map(o => Number(o.id)));
    return String(n + 1);
  };
  function saveOrder(order) {
    const list = storedOrders().filter(o => o.id !== order.id);
    list.unshift(order);
    try { localStorage.setItem(ORDERS_KEY, JSON.stringify(list)); } catch (e) { /* storage unavailable */ }
    const i = ORDERS.findIndex(o => o.id === order.id); if (i > -1) ORDERS.splice(i, 1); ORDERS.unshift(order);
    return order;
  }

  const STATUS_LABEL = { draft: 'Draft quote', submitted: 'Submitted', production: 'In production', ready: 'Ready for pickup' };

  const money = (value) => '$' + value.toLocaleString('en-CA', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  const longDate = (iso) => {
    if (!iso) return 'Select a date';
    return new Intl.DateTimeFormat('en-CA', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' }).format(new Date(iso + 'T12:00:00Z'));
  };
  const shortDate = (iso) => new Intl.DateTimeFormat('en-CA', { month: 'short', day: 'numeric', timeZone: 'UTC' }).format(new Date(iso + 'T12:00:00Z'));

  function toast(title, message, type = '') {
    let region = $('#toastRegion');
    if (!region) {
      region = document.createElement('div');
      region.id = 'toastRegion';
      region.className = 'toast-region';
      region.setAttribute('aria-live', 'polite');
      document.body.append(region);
    }
    const node = document.createElement('div');
    node.className = `toast ${type}`.trim();
    node.innerHTML = `<span class="toast-icon"><svg class="icon"><use href="#i-${type === 'error' ? 'close' : 'check'}"/></svg></span><span><strong>${title}</strong><span>${message}</span></span><button aria-label="Dismiss"><svg class="icon" width="15" height="15"><use href="#i-close"/></svg></button>`;
    region.append(node);
    $('button', node).addEventListener('click', () => node.remove());
    window.setTimeout(() => node.remove(), 5200);
  }

  function orderRow(order) {
    const dateCell = order.status === 'draft'
      ? `Not required<span>${order.note}</span>`
      : order.status === 'ready'
        ? `Ready now<span>${order.note}</span>`
        : `${longDate(order.date)}<span>${order.note}</span>`;
    const action = order.status === 'draft'
      ? `<a class="table-action primary" href="new-order-checkout.html?quote=${order.id}"><svg class="icon" width="14" height="14"><use href="#i-edit"/></svg>Edit order</a>`
      : `<a class="table-action view-order" href="order.html?id=${order.id}">${order.status === 'ready' ? 'View pickup' : 'View details'}</a>`;
    return `<tr data-status="${order.status}" data-type="${order.type}" data-search="${(order.id + ' ' + order.name + ' ' + order.tag + ' ' + order.status + ' ' + order.type).toLowerCase()}">
      <td><div class="order-id">${order.id}<span class="type-chip">${order.type === 'kitchen' ? 'Kitchen' : order.type === 'vanity-top' ? 'Vanity top' : order.type === 'mixed' ? 'Mixed' : 'Vanity'}</span>${order.isNew ? '<span class="type-chip in-cart">New</span>' : ''}</div><div class="order-tag">${order.po ? `<span class="po-chip">PO ${order.po}</span>` : ''}${order.name}${order.tag ? ' · ' + order.tag : ''}</div></td>
      <td><span class="status ${order.status}">${STATUS_LABEL[order.status]}</span></td>
      <td class="date-cell">${dateCell}</td>
      <td class="price-cell">${money(order.total)}</td>
      <td><div class="row-actions">${action}</div></td>
    </tr>`;
  }

  function renderOrders(tbody, orders) {
    tbody.innerHTML = orders.map(orderRow).join('');
  }

  const counts = () => ORDERS.reduce((acc, o) => { acc[o.status] = (acc[o.status] || 0) + 1; acc.all++; return acc; }, { all: 0 });

  /* Shell behaviour shared by every page */
  function initShell() {
    const c = counts();
    $$('[data-count="orders"]').forEach(el => el.textContent = c.all);

    const menuButton = $('#newOrderButton');
    const menu = $('#orderMenu');
    if (menuButton && menu) {
      menuButton.addEventListener('click', () => {
        const isOpen = menu.classList.toggle('open');
        menuButton.setAttribute('aria-expanded', String(isOpen));
      });
      document.addEventListener('click', event => {
        if (!event.target.closest('.new-order-wrap')) { menu.classList.remove('open'); menuButton.setAttribute('aria-expanded', 'false'); }
      });
      document.addEventListener('keydown', event => { if (event.key === 'Escape') { menu.classList.remove('open'); menuButton.setAttribute('aria-expanded', 'false'); } });
    }

    const sidebar = $('.sidebar');
    const backdrop = $('.sidebar-backdrop');
    const mobileMenu = $('.mobile-menu');
    if (sidebar && mobileMenu) {
      const setOpen = (open) => { sidebar.classList.toggle('open', open); backdrop && backdrop.classList.toggle('open', open); mobileMenu.setAttribute('aria-expanded', String(open)); };
      mobileMenu.addEventListener('click', () => setOpen(!sidebar.classList.contains('open')));
      backdrop && backdrop.addEventListener('click', () => setOpen(false));
    }

    const signOut = $('#signOut');
    signOut && signOut.addEventListener('click', () => toast('Signed out', 'You would be returned to the dealer login in production.'));

    $$('[data-download-note]').forEach(link => link.addEventListener('click', () => toast('Download started', link.dataset.downloadNote, 'success')));
  }

  document.addEventListener('DOMContentLoaded', initShell);

  return { $, $$, ORDERS, STATUS_LABEL, money, longDate, shortDate, toast, renderOrders, counts, getOrder, saveOrder, nextId, storedOrders };
})();
