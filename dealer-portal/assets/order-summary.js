/* Classic Brand dealer portal — order summary drawer, "Selected" side panel and cart bar.
   Shared by the product list page and the vanity-top page. Expects the markup ids used in order_pages.py
   (#summaryDrawer, #summaryBody, #assemblyBar, #summaryCheckout, #sideList, #cartBar …). */
window.OrderSummary = (() => {
  const THUMB = { wall: 'i-cab-wall', base: 'i-cab-base', drawer: 'i-cab-drawer', tall: 'i-cab-tall', vanity: 'i-cab-vanity', legs: 'i-cab-legs', mirror: 'i-mirror', counter: 'i-counter', panel: 'i-panel', door: 'i-door', glass: 'i-glass', hardware: 'i-hardware' };
  const serviceText = (i) => i.services && i.services.length ? `Top service · ${i.services.join(', ')}` : '';
  /* Door style / colour recorded on a vanity line, top services on a vanity-top line */
  const optionText = (i) => [i.variant, i.hardwareText, serviceText(i)].filter(Boolean).join(' · ');

  function init({ onClear, onChange } = {}) {
    const { $, $$, money, toast } = Portal;
    const C = Catalog;
    const drawer = $('#summaryDrawer');
    const params = new URLSearchParams(location.search);

    /* Assembly Required starts blank on every visit — it is never pre-selected from a previous session or draft. */
    C.setCartMeta({ assembly: null });
    $$('input[name=assembly]').forEach(r => { r.checked = false; });

    function renderSummary() {
      const cart = C.readCart();
      const body = $('#summaryBody');
      const list = C.units(cart);
      if (!list.length) {
        body.innerHTML = '<div class="empty-state visible"><strong>Nothing selected yet</strong>Add a product and it will appear here.</div>';
      } else {
        const groups = [...new Set(list.map(i => i.seriesName))];
        body.innerHTML = '<p class="summary-note">One line per piece — give each its own customer tag. Quantities are changed in the product list.</p>' + groups.map(g => `<p class="series-group">${g}</p>` + list.filter(i => i.seriesName === g).map(i => `<div class="summary-row" data-key="${i.key}" data-unit="${i.unit}">
          <span class="product-thumb" style="width:40px;height:40px"><svg class="icon" style="width:22px;height:22px"><use href="#${THUMB[i.img] || 'i-box'}"/></svg></span>
          <div><strong>${i.sku}${i.qty > 1 ? ` <span class="type-chip">${i.unit + 1} of ${i.qty}</span>` : ''}</strong><small>${i.desc}${i.box ? ' · Box ' + i.box : ''}</small>${optionText(i) ? `<small class="svc-text">${optionText(i)}</small>` : ''}${i.assembly != null ? `<small>Assembly +${money(i.assembly)} if assembled</small>` : ''}</div>
          <input class="row-tag${i.tag ? ' has-tag' : ''}" type="text" maxlength="12" value="${i.tag}" placeholder="Customer tag" aria-label="Customer tag for ${i.sku} piece ${i.unit + 1}">
          <strong class="summary-price">${i.dealer == null ? 'On request' : money(i.dealer)}</strong>
        </div>`).join('')).join('');
        $$('.summary-row', body).forEach(row => {
          $('.row-tag', row).addEventListener('change', e => { C.setUnitTag(row.dataset.key, Number(row.dataset.unit), e.target.value); e.target.classList.toggle('has-tag', !!e.target.value.trim()); renderSide(); });
        });
      }
      gateCheckout();
      const asm = cart.assembly === 'yes' ? C.cartAssemblyTotal(cart) : 0;
      $('#summaryTotal').textContent = money(C.cartTotal(cart) + asm) + (C.cartHasQuoteItems(cart) ? ' +' : '');
      $('#summaryTotal').title = asm ? `Includes ${money(asm)} assembly` : '';
      $('#summaryTitle').textContent = `Selected products · ${C.cartCount(cart)} piece${C.cartCount(cart) === 1 ? '' : 's'}`;
    }

    function gateCheckout() {
      const cart = C.readCart();
      const ok = cart.items.length > 0 && !!cart.assembly;
      const btn = $('#summaryCheckout');
      btn.classList.toggle('disabled', !ok); btn.setAttribute('aria-disabled', String(!ok));
      const asmTotal = C.cartAssemblyTotal(cart);
      $('#assemblyHint').textContent = !cart.items.length ? 'Add at least one product' : cart.assembly ? (cart.assembly === 'yes' ? `Cabinets are delivered fully assembled${asmTotal ? ' · +' + money(asmTotal) : ''}` : 'Ships flat-packed') : 'Choose one to continue to checkout';
    }
    $$('input[name=assembly]').forEach(r => r.addEventListener('change', () => { C.setCartMeta({ assembly: r.value }); $('#assemblyBar').classList.remove('invalid'); renderSummary(); }));
    $('#summaryCheckout').addEventListener('click', e => {
      const cart = C.readCart();
      if (!cart.items.length) { e.preventDefault(); return toast('Nothing selected', 'Add at least one product first.', 'error'); }
      if (!cart.assembly) { e.preventDefault(); $('#assemblyBar').classList.add('invalid'); return toast('Assembly required?', 'Choose Yes or No before checkout.', 'error'); }
      C.setCartMeta({ summaryViewed: true });
    });

    const isOpen = () => drawer.classList.contains('open');
    const open = () => { renderSummary(); drawer.classList.add('open'); drawer.setAttribute('aria-hidden', 'false'); document.body.style.overflow = 'hidden'; };
    const close = () => { drawer.classList.remove('open'); drawer.setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; };
    $('#viewSummary').addEventListener('click', open);
    $$('[data-cart-link]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); open(); }));
    $('#sideOpen').addEventListener('click', open);
    $('#closeSummary').addEventListener('click', close);
    $('#summaryContinue').addEventListener('click', close);
    drawer.addEventListener('click', e => { if (e.target === drawer) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && isOpen()) close(); });

    function renderSide() {
      const cart = C.readCart();
      $('#sideCount').textContent = C.cartCount(cart) || '';
      $('#sideTotal').textContent = money(C.cartTotal(cart));
      $('#sideList').innerHTML = cart.items.length ? cart.items.slice(-12).reverse().map(i => { const tagged = (i.tags || []).filter(Boolean).length; return `<div class="side-item"><span class="side-sku">${i.sku}${optionText(i) ? `<b>${optionText(i)}</b>` : ''}<em>${tagged ? `${tagged}/${i.qty} tagged` : 'no tag yet'}</em></span><span class="side-qty">× ${i.qty}</span><span class="side-price">${i.dealer == null ? '—' : money(i.dealer * i.qty)}</span></div>`; }).join('') + (cart.items.length > 12 ? `<div class="side-more">+ ${cart.items.length - 12} more in summary</div>` : '') : '<div class="side-empty">Nothing selected yet</div>';
      $('#sideOpen').disabled = !cart.items.length;
    }
    function refresh() {
      renderSide();
      const cart = C.readCart();
      $('#cartCount').textContent = C.cartCount(cart);
      $('#cartTotal').textContent = money(C.cartTotal(cart)) + (C.cartHasQuoteItems(cart) ? ' + items on request' : '');
      const names = [...new Set(cart.items.map(i => i.seriesName))];
      $('#cartSeries').textContent = names.length ? `Series: ${names.join(' · ')}` : 'Cart is empty';
      if (isOpen()) renderSummary();
      if (onChange) onChange(cart);
    }
    $('#clearCart').addEventListener('click', () => { C.clearCart(); if (onClear) onClear(); refresh(); });

    refresh();
    if (params.get('summary') === '1') open();
    return { open, close, refresh, renderSummary, isOpen };
  }

  return { init, THUMB, serviceText, optionText };
})();
