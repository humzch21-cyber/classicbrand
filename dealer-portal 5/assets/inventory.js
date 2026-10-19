/* Classic Brand dealer portal — Inventory checking index.
   Mirrors the dealer stock index (classicbrand.ca/cb/stock): every button is a colour / finish code that opens the
   live stock page for that code. Full names and series follow the August 2026 Quick Reference Cabinetry Price Book.
   An empty `name` means the full name is not in the price book — the code is shown on its own until it is confirmed.

   Links: each family has a URL pattern; `{code}` is replaced by the item code (Kitchen SSW → KITCHEN-SSW.html, which
   is the pattern confirmed so far). Give an item its own `href` to override the pattern. */
window.Inventory = (() => {
  const BASE = 'http://20.151.216.184:39002/';

  const FAMILIES = [
    { id: 'kitchen', name: 'Kitchen', icon: 'i-kitchen', pattern: 'KITCHEN-{code}.html', groups: [
      { name: 'Fundamentals', items: [
        { code: 'SSW', name: 'Step Shaker White' },
        { code: 'BW',  name: 'Bermuda White' },
        { code: 'FG',  name: 'Fog Grey' },
        { code: 'SCG', name: 'Step Charcoal Grey' },
        { code: 'NWS', name: 'Narrow White Shaker' },
        { code: 'NBS', name: 'Narrow Black Shaker' },
        { code: 'NNO', name: 'Narrow Natural Oak' },
        { code: 'NSP', name: 'Narrow Sea Pearl' },
        { code: 'WS',  name: 'White Shaker' }
      ] },
      { name: 'Trends Limited', items: [
        { code: 'JV', name: 'Java' },
        { code: 'OW', name: 'Off White' }
      ] },
      { name: 'Trends Select', items: [
        { code: 'MB', name: 'Midnight Blue' }
      ] },
      { name: 'Econoline', items: [
        { code: 'ESSW', name: 'Step Shaker White' },
        { code: 'EBW',  name: 'Bermuda White' },
        { code: 'ENWS', name: 'Narrow White Shaker' },
        { code: 'ENBS', name: 'Narrow Black Shaker' },
        { code: 'EFTW', name: 'Slab White' },
        { code: 'EFTO', name: 'Slab Light Oak' }
      ] },
      { name: 'Cabinet boxes', items: [
        { code: 'WBOX',  name: 'White' },
        { code: 'BHBOX', name: 'Birch' },
        { code: 'CMBOX', name: 'Cinnamon Maple' },
        { code: 'FGBOX', name: 'Fog Grey' },
        { code: 'CGBOX', name: 'Charcoal Grey' },
        { code: 'PBBOX', name: 'Particleboard White' }
      ] }
    ] },
    { id: 'vanity', name: 'Vanity', icon: 'i-vanity', pattern: 'VANITY-{code}.html', groups: [
      { name: 'Fundamentals', items: [
        { code: 'SSW', name: 'Step Shaker White' },
        { code: 'BW',  name: 'Bermuda White' },
        { code: 'MB',  name: 'Midnight Blue' }
      ] },
      { name: 'Crush', items: [
        { code: 'NWS-C', name: 'Narrow White Shaker' },
        { code: 'NBS-C', name: 'Narrow Black Shaker' },
        { code: 'NGS-C', name: 'Narrow Grey Shaker' }
      ] },
      { name: 'Evolution', items: [
        { code: 'NWS-E', name: 'Narrow White Shaker' },
        { code: 'NNO-E', name: 'Narrow Natural Oak' }
      ] },
      { name: 'Other finishes', items: [
        { code: 'SG', name: 'Step Grey' },
        { code: 'LF', name: 'London Fog' },
        { code: 'RS', name: 'Riverstone' },
        { code: 'SS', name: 'Sandstone' }
      ] }
    ] },
    { id: 'vanity-top', name: 'Vanity top', icon: 'i-counter', pattern: 'VANITYTOP-{code}.html', groups: [
      { name: '2 cm Premium Quartz', items: [
        { code: 'PWR', name: 'Pure White' },
        { code: 'AGR', name: 'Arctic Glacier' },
        { code: 'MLR', name: 'Moonlight' },
        { code: 'MTR', name: 'Mist' },
        { code: 'WHR', name: 'Whisper' },
        { code: 'FUR', name: 'Fusion' }
      ] },
      { name: '2 cm Regular Quartz', items: [
        { code: 'SLR', name: 'Starlight' }
      ] },
      { name: '3 cm Premium Quartz', items: [
        { code: 'LGR', name: 'Lava Grey' },
        { code: 'MLR', name: 'Moonlight', suffix: '3CM' }
      ] },
      { name: 'Other', items: [
        { code: 'CWR', name: 'Cloud White' }
      ] },
      { name: 'Discontinued', items: [
        { code: 'SWR', name: '', discontinued: true },
        { code: 'SBR', name: '', discontinued: true },
        { code: 'MIR', name: '', discontinued: true },
        { code: 'CBR', name: '', discontinued: true },
        { code: 'SGR', name: '', discontinued: true },
        { code: 'PLR', name: '', discontinued: true }
      ] }
    ] },
    { id: 'sintered', name: 'Sintered stone', icon: 'i-swatch', pattern: 'VANITYTOP-{code}.html', groups: [
      { name: 'Sintered stone', items: [
        { code: 'CAG', name: 'Carrara Gold', note: 'Crush only' },
        { code: 'BIR', name: 'Bianco Rumeno' }
      ] }
    ] },
    { id: 'hardware', name: 'Hardware', icon: 'i-hardware', pattern: 'HARDWARE.html', groups: [
      { name: 'Hardware', items: [
        { code: 'HARDWARE', name: 'Handles & knobs, LED light, kitchen parts', hideCode: true }
      ] }
    ] }
  ];

  const codeOf = (item) => item.code + (item.suffix ? `-${item.suffix}` : '');
  const hrefOf = (fam, item) => item.href || BASE + fam.pattern.replace('{code}', codeOf(item));
  const labelOf = (item) => item.name ? `${item.name} (${codeOf(item)})` : codeOf(item);

  return { BASE, FAMILIES, codeOf, hrefOf, labelOf };
})();
