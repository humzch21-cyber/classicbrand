/* Classic Brand dealer portal — series, product catalog and cart
   Vanity SKUs and MSRP come from the Quick Reference Bathroom Price Book (August 2026).
   Kitchen SKUs follow the classicbrand.ca pattern (e.g. SSW-W0930); kitchen prices are illustrative. */
window.Catalog = (() => {
  const DEALER_MULTIPLIER = 0.6; // contract pricing tier applied to MSRP (illustrative)

  /* ------------------------------------------------------------------ series */
  const SERIES = [
    // Kitchen — series names as used by Classic Brand; photos from the kitchen gallery.
    { id: 'kitchen-fundamentals', line: 'kitchen', family: 'Fundamentals',   name: '', code: 'FUN', door: 'shaker', color: '#f3f1ec', frame: '#d9d5cc', image: 'assets/covers/kitchen-fundamentals.jpg',   box: ['WBOX', 'FGBOX', 'BHBOX', 'CMBOX', 'SCGBOX'], multiplier: 1.00, badge: 'Best seller', blurb: 'Painted shaker · white and light neutrals',
      colors: [
        { code: 'BW',  name: 'Bermuda White',       swatch: '#f4f2ee', frame: '#d9d5cc', door: 'raised', multiplier: 1.00 },
        { code: 'SSW', name: 'Step Shaker White',   swatch: '#f7f6f3', frame: '#dcd8d1', door: 'shaker', multiplier: 1.00 },
        { code: 'FG',  name: 'Fog Grey',            swatch: '#b8bcbf', frame: '#9fa3a6', door: 'shaker', multiplier: 1.04 },
        { code: 'SCG', name: 'Step Charcoal Grey',  swatch: '#4a4b4d', frame: '#3b3c3e', door: 'shaker', multiplier: 1.06 },
        { code: 'NWS', name: 'Narrow White Shaker', swatch: '#f5f4f1', frame: '#dad6cf', door: 'narrow', multiplier: 1.03 },
        { code: 'NBS', name: 'Narrow Black Shaker', swatch: '#232323', frame: '#151515', door: 'narrow', multiplier: 1.08 }
      ] },
    { id: 'trends-limited',       line: 'kitchen', family: 'Trends Limited', name: '', code: 'TRL', door: 'shaker', color: '#3b3a37', frame: '#2c2b28', image: 'assets/covers/kitchen-trends-limited.jpg', box: ['SCGBOX', 'BHBOX'],        multiplier: 1.12, blurb: 'Two-tone charcoal and driftwood textures',
      colors: [{ code: 'TLC', name: 'Charcoal', swatch: '#3b3a37', frame: '#2c2b28', door: 'shaker', multiplier: 1.0 }, { code: 'TLD', name: 'Driftwood', swatch: '#b9a58a', frame: '#a08c72', door: 'slab', multiplier: 1.0 }] },
    { id: 'trends-select',        line: 'kitchen', family: 'Trends Select',  name: '', code: 'TRS', door: 'shaker', color: '#d3b98f', frame: '#bda27a', image: 'assets/covers/kitchen-trends-select.jpg',  box: ['BHBOX', 'WBOX'],         multiplier: 1.06, blurb: 'Light oak shaker · natural wood grain',
      colors: [{ code: 'TSO', name: 'Natural Oak', swatch: '#d3b98f', frame: '#bda27a', door: 'shaker', multiplier: 1.0 }, { code: 'TSW', name: 'Warm White', swatch: '#f1ede6', frame: '#d6d0c6', door: 'shaker', multiplier: 0.97 }] },
    { id: 'econoline',            line: 'kitchen', family: 'Econoline',      name: '', code: 'ECO', door: 'shaker', color: '#33465f', frame: '#28384c', image: 'assets/covers/kitchen-econoline.jpg',      box: ['WBOX', 'FGBOX'],         multiplier: 0.90, badge: 'Value', blurb: 'Painted shaker · stocked colours, fast lead time',
      colors: [{ code: 'ENV', name: 'Navy', swatch: '#33465f', frame: '#28384c', door: 'shaker', multiplier: 1.0 }, { code: 'EWH', name: 'White', swatch: '#f6f5f2', frame: '#dcd8d1', door: 'shaker', multiplier: 0.96 }, { code: 'EGR', name: 'Grey', swatch: '#a9adb0', frame: '#8f9396', door: 'shaker', multiplier: 1.0 }] },
    { id: 'euroline',             line: 'kitchen', family: 'Euroline',       name: '', code: 'EUR', door: 'slab',   color: '#cfae82', frame: '#b8976c', image: 'assets/covers/kitchen-euroline.jpg',       box: ['BHBOX', 'WBOX'],         multiplier: 1.15, badge: 'New', blurb: 'Frameless slab · European oak and matte white',
      colors: [{ code: 'EUO', name: 'European Oak', swatch: '#cfae82', frame: '#b8976c', door: 'slab', multiplier: 1.0 }, { code: 'EUW', name: 'Matte White', swatch: '#f3f2ef', frame: '#d9d6d0', door: 'slab', multiplier: 0.98 }] },
    // Vanity — five series with gallery photos. Evolution I/II/III and Crush SKUs, MSRP and assembly prices come from
    // their price books (assets/vanity-book.js); door styles and colours are chosen on the product page and recorded on the line.
    { id: 'evolution-iii', line: 'vanity', family: 'Evolution III', name: '', code: 'EV3', door: 'fluted', color: '#2e2f31', frame: '#1f2022', image: 'assets/covers/vanity-evolution-iii.jpg', book: 'evolution-iii', badge: 'New', blurb: 'Fluted thermo-laminate fronts · 20 colours · with legs or full panel',
      doors: [{ id: 'huron', name: 'Huron', style: 'Fluted' }, { id: 'ontario', name: 'Ontario', style: 'Fluted' }, { id: 'michigan', name: 'Michigan', style: 'Fluted' }, { id: 'erie', name: 'Erie', style: 'Fluted' }],
      colors: 'THERMO', caseColor: 'Fog Grey' },
    { id: 'evolution-ii',  line: 'vanity', family: 'Evolution II',  name: '', code: 'EV2', door: 'shaker', color: '#7d93b8', frame: '#66799a', image: 'assets/covers/vanity-evolution-ii.jpg',  book: 'evolution-ii', blurb: 'Six door styles · thermo laminate and ultra slab · with legs or full panel',
      doors: [{ id: 'hamilton', name: 'Hamilton', style: 'Slab', slab: true }, { id: 'woodstock', name: 'Woodstock', style: '¾″ Narrow Shaker' }, { id: 'oakville', name: 'Oakville', style: '1½″ Narrow Shaker' }, { id: 'venice', name: 'Venice', style: '2½″ Bevelled Shaker' }, { id: 'rome', name: 'Rome', style: '2½″ Step Shaker' }, { id: 'london', name: 'London', style: '2¼″ Shaker' }],
      colors: 'THERMO+SLAB', caseColor: 'Fog Grey' },
    { id: 'evolution-i',   line: 'vanity', family: 'Evolution I',   name: '', code: 'EV1', door: 'shaker', color: '#f2f0ec', frame: '#d8d4cc', image: 'assets/covers/vanity-evolution-i.jpg',   book: 'evolution-i', blurb: '1½″ narrow shaker · white or natural oak · with legs',
      doors: [{ id: 'narrow-shaker', name: '1½″ Narrow Shaker', style: 'HDF painted / oak veneer' }],
      colors: [{ code: 'NWS', name: 'Narrow White Shaker', swatch: '#f4f3f0', frame: '#d9d5cc', priceIdx: 0, note: 'White wood legs' }, { code: 'NNO', name: 'Narrow Natural Oak', swatch: '#c9a67a', frame: '#a8865c', priceIdx: 1, note: 'Oak wood legs' }] },
    { id: 'crush',         line: 'vanity', family: 'Crush',         name: '', code: 'CRU', door: 'shaker', color: '#2b2622', frame: '#1c1815', image: 'assets/covers/vanity-crush.jpg',          book: 'crush', badge: 'Value', blurb: '1½″ shaker · white, black or grey · full panel',
      doors: [{ id: 'shaker', name: '1½″ Shaker', style: 'HDF painted' }],
      colors: [{ code: 'NWS', name: 'Narrow White Shaker', swatch: '#f5f4f1', frame: '#d9d5cc' }, { code: 'NBS', name: 'Narrow Black Shaker', swatch: '#1a1a1a', frame: '#0d0d0d' }, { code: 'NGS', name: 'Narrow Grey Shaker', swatch: '#8f9193', frame: '#6f7173' }] },
    { id: 'fundamentals',  line: 'vanity', family: 'Fundamentals',  name: '', code: 'FUN', door: 'raised', color: '#f5f4f0', frame: '#dad7d0', image: 'assets/covers/vanity-fundamentals.jpg',   priceKey: 'fund', badge: 'Best seller', blurb: 'Step shaker and bevelled shaker · white and midnight blue',
      doors: [{ id: 'step-shaker', name: 'Step Shaker', style: 'SSW' }, { id: 'bevelled-shaker', name: 'Bevelled Shaker', style: 'BW · MB' }],
      colors: [{ code: 'SSW', name: 'Step Shaker White', swatch: '#f7f6f3', frame: '#dcd8d1', doors: ['step-shaker'] }, { code: 'BW', name: 'Bermuda White', swatch: '#f4f2ee', frame: '#d9d5cc', doors: ['bevelled-shaker'] }, { code: 'MB', name: 'Midnight Blue', swatch: '#1f2a44', frame: '#141c30', doors: ['bevelled-shaker'] }] },
    // Vanity top — one line, one page: material / thickness / colour → size → top service (as on the original portal).
    // `prefix` is the SKU prefix (AGR31-bundle, AG-MT24-bundle); `idx` is the MSRP column in COUNTERTOPS.
    { id: 'vanity-top', line: 'vanity-top', family: 'Vanity tops', name: '', code: 'VT', door: 'stone', color: '#ecebe7', frame: '#cbc7be', flow: 'vanity-top', blurb: 'Quartz and sintered stone tops · pick the top, then the size · drilling and cuts per top',
      colors: [
        { code: 'PWR', prefix: 'PWR', name: 'Pure White',     group: '2 cm Premium Quartz', short: '2 cm Premium Quartz', idx: 4, mt: true, image: 'assets/covers/top-pure-white.jpg' },
        { code: 'AGR', prefix: 'AGR', name: 'Arctic Glacier', group: '2 cm Premium Quartz', short: '2 cm Premium Quartz', idx: 4, mt: true, image: 'assets/covers/top-arctic-glacier.jpg' },
        { code: 'MLR', prefix: 'MLR', name: 'Moonlight',      group: '2 cm Premium Quartz', short: '2 cm Premium Quartz', idx: 4, mt: true, image: 'assets/covers/top-moonlight.jpg' },
        { code: 'MTR', prefix: 'MTR', name: 'Mist',           group: '2 cm Premium Quartz', short: '2 cm Premium Quartz', idx: 4, mt: true, image: 'assets/covers/top-mist.jpg' },
        { code: 'WHR', prefix: 'WHR', name: 'Whisper',        group: '2 cm Premium Quartz', short: '2 cm Premium Quartz', idx: 4, mt: true, image: 'assets/covers/top-whisper.jpg' },
        { code: 'FUR', prefix: 'FUR', name: 'Fusion',         group: '2 cm Premium Quartz', short: '2 cm Premium Quartz', idx: 4, mt: true, image: 'assets/covers/top-fusion.jpg' },
        { code: 'SLR', prefix: 'SLR', name: 'Starlight',      group: '2 cm Regular Quartz', short: '2 cm Regular Quartz', idx: 3, mt: true, image: 'assets/covers/top-starlight.jpg' },
        { code: 'LGR',     prefix: 'LGR', name: 'Lava Grey', group: '3 cm Premium Quartz', short: '3 cm Premium Quartz', idx: 5, suffix: '-3CM', image: 'assets/covers/top-lava-grey.jpg' },
        { code: 'MLR-3CM', prefix: 'MLR', name: 'Moonlight', group: '3 cm Premium Quartz', short: '3 cm Premium Quartz', idx: 5, suffix: '-3CM', image: 'assets/covers/top-moonlight-3cm.jpg' },
        { code: 'CAG', prefix: 'CAG', name: 'Carrara Gold',  group: 'Sintered Stone', short: 'Sintered stone', idx: 1, note: 'Crush only', image: 'assets/covers/top-carrara-gold.jpg' },
        { code: 'BIR', prefix: 'BIR', name: 'Bianco Rumeno', group: 'Sintered Stone', short: 'Sintered stone', idx: 2, image: 'assets/covers/top-bianco-rumeno.jpg' }
      ],
      services: [
        { code: 'Drill-4',   name: '4″ centerset faucet holes' },
        { code: 'Drill-8',   name: '8″ widespread faucet holes' },
        { code: 'CUT-LEFT',  name: 'Cut to size · left' },
        { code: 'CUT-RIGHT', name: 'Cut to size · right' }
      ] }
  ];
  // Evolution II / III thermo-laminate colours (MDF ¾″ matte) and Evolution II ultra-slab colours (Hamilton slab door only).
  const THERMO = [
    ['Light Grey', '#cfd1d4'], ['Cool Grey', '#d6cdbd'], ['Mint Green', '#9aa996'], ['Reed Green', '#8f9f93'], ['Verde', '#5c6b4f'], ['Alby Blue', '#5a6378'], ['Marine Blue', '#1c2238'], ['Celestine', '#c6d6dc'],
    ['Porcelain', '#f6f6f1'], ['White Cloud', '#f9f9f9'], ['Concrete', '#b9b9b7'], ['Charcoal', '#4b4d52'], ['Black', '#0e0e0e'], ['Grey Vicenza Oak', '#8a7d6b'], ['Casual Chestnut', '#d8b58e'], ['Endless Elm', '#d9ccb5'],
    ['Sheer Beauty', '#d6b27a'], ['Dalia Walnut', '#9d7b63'], ['Wright Walnut', '#5e3b27'], ['Fashionista', '#a57c52']
  ].map(([name, swatch]) => ({ code: name.toLowerCase().replace(/[^a-z]+/g, '-'), name, swatch, group: 'Thermo laminate · matte' }));
  const ULTRA_SLAB = [
    ...[['Arctic Grey', '#e9e8e4'], ['Black Soft Touch', '#0f0f0f'], ['White', '#ffffff'], ['Antique White', '#fbf5e4'], ['Natural Touch Oak', '#c99d65']].map(([name, swatch]) => ({ code: 'st-' + name.toLowerCase().replace(/[^a-z]+/g, '-'), name, swatch, group: 'AGT PET ultra slab · soft touch', slabOnly: true })),
    ...[['Arctic Grey', '#e9e8e4'], ['Black High Gloss', '#0f0f0f'], ['White', '#ffffff'], ['Antique White', '#fbf5e4'], ['Metallic Elm', '#4a3f39'], ['Milano Walnut', '#7b5a3a']].map(([name, swatch]) => ({ code: 'hg-' + name.toLowerCase().replace(/[^a-z]+/g, '-'), name, swatch, group: 'AGT PET ultra slab · high gloss', slabOnly: true })),
    ...[['Carbon Frozen Wood', '#3b3734'], ['Light Tennessee Walnut', '#8e5b3b'], ['Natural Corini Walnut', '#8d6a4f'], ['Natural Tossini Elm', '#d6bb94'], ['White Cape Elm', '#e5ded0'], ['Sand Lyon Textured', '#e2cfae'], ['Stone Grey Frozen Wood', '#9a948b'], ['Sand Gladstone Oak', '#cfae7e'], ['Oiled Kendal Oak', '#c69a63'], ['Natural Halifax Oak', '#d7b98f'], ['Bleached Carini Walnut', '#a8927b'], ['Perona Walnut', '#b57a5c']].map(([name, swatch]) => ({ code: 'eg-' + name.toLowerCase().replace(/[^a-z]+/g, '-'), name, swatch, group: 'Egger ultra slab · wood grain', slabOnly: true }))
  ];
  SERIES.forEach(s => { if (s.colors === 'THERMO') s.colors = THERMO.map(c => ({ ...c })); else if (s.colors === 'THERMO+SLAB') s.colors = [...THERMO, ...ULTRA_SLAB].map(c => ({ ...c })); });

  const LINE_LABEL = { kitchen: 'Kitchen', vanity: 'Vanity', 'vanity-top': 'Vanity top' };

  const seriesById = (id) => SERIES.find(s => s.id === id);
  const seriesTitle = (s) => s.name ? `${s.family} – ${s.name}` : s.family;

  const BOX_COLORS = [
    { code: 'WBOX',   name: 'White',           color: '#f4f4f2' },
    { code: 'FGBOX',  name: 'Fog Grey',        color: '#b9bcbf' },
    { code: 'BHBOX',  name: 'Birch',           color: '#d7b98c' },
    { code: 'CMBOX',  name: 'Cinnamon Maple',  color: '#8a5a3a' },
    { code: 'SCGBOX', name: 'Charcoal',        color: '#3a3b3d' }
  ];

  /* ------------------------------------------------------------------ categories */
  const CATEGORIES = {
    kitchen: [
      { id: 'all', name: 'All product' },
      { id: 'wall', name: 'Wall cabinet', children: [{ id: 'wall-30', name: '30″ high' }, { id: 'wall-36', name: '36″ high' }, { id: 'wall-42', name: '42″ high' }] },
      { id: 'base', name: 'Base cabinet', children: [{ id: 'base-std', name: 'Standard base' }, { id: 'base-sink', name: 'Sink base' }, { id: 'base-drawer', name: 'Drawer base' }] },
      { id: 'pantry', name: 'Pantry cabinet' },
      { id: 'accessories', name: 'Accessories', children: [{ id: 'acc-filler', name: 'Fillers & panels' }, { id: 'acc-moulding', name: 'Mouldings' }] },
      { id: 'doors', name: 'Doors', children: [{ id: 'doors-sample', name: 'Sample doors' }, { id: 'doors-replacement', name: 'Replacement doors' }] },
      { id: 'hardware', name: 'Hardware', children: [{ id: 'hw-hinge', name: 'Hinges & slides' }, { id: 'hw-pull', name: 'Pulls & knobs' }] },
      { id: 'glass', name: 'Specialty glass', children: [{ id: 'glass-door', name: 'Glass doors' }] }
    ],
    vanity: [
      { id: 'all', name: 'All product' },
      { id: 'van-legs', name: 'Vanities with legs', children: ['24', '30', '36', '42', '48', '54', '60', '72'].map(w => ({ id: `van-legs-${w}`, name: `${w}″ wide` })) },
      { id: 'van-panel', name: 'Vanities full panel', children: ['24', '30', '36', '42', '48', '54', '60', '72'].map(w => ({ id: `van-panel-${w}`, name: `${w}″ wide` })) },
      { id: 'linen', name: 'Linen cabinets' },
      { id: 'vbase', name: 'Base & drawer cabinets' },
      { id: 'vwall', name: 'Wall & medicine cabinets' },
      { id: 'mirror', name: 'Mirrors' },
      { id: 'accessory', name: 'Accessories' },
      { id: 'hardware', name: 'Handles & knobs' },
      // Vanity tops are ordered through their own colour → size flow (link rendered in the category tree)
      { id: 'vanity-top-link', name: 'Vanity tops', link: 'new-order-vanity-top.html?series=vanity-top' }
    ],
    'vanity-top': [
      { id: 'all', name: 'All product' },
      { id: 'vt-product', name: 'Vanity Top Product', children: [{ id: 'vt-vanity', name: 'Vanity tops' }, { id: 'vt-makeup', name: 'Makeup table tops' }] },
      { id: 'vt-accessories', name: 'Vanity Top Accessories' }
    ]
  };

  /* ------------------------------------------------------------------ kitchen catalog (generated) */
  const pad = (n) => String(n).padStart(2, '0');
  const r = (n) => Math.round(n);

  // Dealer prices for 30" wall cabinets as listed on classicbrand.ca (Bermuda White); other sizes are scaled from these.
  const WALL30 = { 9: 242, 12: 264, 15: 328, 18: 354, 21: 396, 24: 435, 27: 472, 30: 508, 33: 546, 36: 582 };
  const HEIGHT_FACTOR = { 30: 1, 36: 1.12, 42: 1.25 };

  function kitchenProducts(series, color) {
    const m = (series.multiplier || 1) * (color ? color.multiplier || 1 : 1);
    const P = color ? color.code : series.code;
    const out = [];
    // Prices are stored as dealer price; MSRP is derived (dealer = MSRP × DEALER_MULTIPLIER).
    // generic items (hardware) carry no door-colour prefix and no colour multiplier
    const add = (cat, sub, sku, desc, dealerPrice, img, opts = {}) => out.push({ cat, sub, sku: opts.generic ? sku : `${P}-${sku}`, base: sku, desc, msrp: r(dealerPrice * (opts.generic ? (series.multiplier || 1) : m) / DEALER_MULTIPLIER), img, ...opts });

    [30, 36, 42].forEach(h => [9, 12, 15, 18, 21, 24, 27, 30, 33, 36].forEach(w => {
      if (h === 42 && w < 12) return;
      add('wall', `wall-${h}`, `W${pad(w)}${h}`, `Wall cabinet W${pad(w)} H${h} D12`, WALL30[w] * HEIGHT_FACTOR[h], 'wall');
    }));
    [9, 12, 15, 18, 21, 24, 27, 30, 33, 36].forEach(w => add('base', 'base-std', `B${pad(w)}`, `Base cabinet B${pad(w)} H34.5 D24`, WALL30[w] * 1.35, 'base'));
    [30, 36].forEach(w => add('base', 'base-sink', `SB${w}`, `Sink base SB${w} H34.5 D24 · false front`, WALL30[w] * 1.25, 'base'));
    [18, 24, 30].forEach(w => add('base', 'base-drawer', `DB${w}`, `Drawer base DB${w} · 3 drawers`, WALL30[w] * 1.75, 'drawer'));
    [[18, 84], [24, 84], [18, 90], [24, 90]].forEach(([w, h]) => add('pantry', null, `T${w}${h}`, `Pantry cabinet T${w} H${h} D24 · 2 doors`, WALL30[w] * (h === 84 ? 3.1 : 3.3), 'tall'));
    add('accessories', 'acc-filler', 'F330', 'Filler 3″ × 30″', 38, 'panel');
    add('accessories', 'acc-filler', 'F396', 'Filler 3″ × 96″', 72, 'panel');
    add('accessories', 'acc-filler', 'BEP2434', 'Base end panel 24″ × 34.5″', 96, 'panel');
    add('accessories', 'acc-filler', 'TEP2496', 'Tall end panel 24″ × 96″', 168, 'panel');
    add('accessories', 'acc-filler', 'TK96', 'Toe kick 4.5″ × 96″', 34, 'panel');
    add('accessories', 'acc-moulding', 'CM96', 'Crown moulding 96″', 88, 'panel');
    add('accessories', 'acc-moulding', 'LR96', 'Light rail moulding 96″', 46, 'panel');
    add('accessories', 'acc-moulding', 'SM96', 'Scribe moulding 96″', 22, 'panel');
    add('doors', 'doors-sample', 'SD1215', 'Sample door 12″ × 15″', 45, 'door');
    add('doors', 'doors-replacement', 'RD1530', 'Replacement door 15″ × 30″', 98, 'door');
    add('doors', 'doors-replacement', 'RD1842', 'Replacement door 18″ × 42″', 142, 'door');
    add('doors', 'doors-replacement', 'RDF1806', 'Replacement drawer front 18″ × 6″', 44, 'door');
    add('hardware', 'hw-hinge', 'HNG-SC', 'Soft-close hinge · pair', 9, 'hardware', { generic: true });
    add('hardware', 'hw-hinge', 'SLD-21SC', '21″ soft-close undermount slide · pair', 28, 'hardware', { generic: true });
    add('hardware', 'hw-pull', 'PL-128BN', 'Bar pull 128 mm · brushed nickel', 6, 'hardware', { generic: true });
    add('hardware', 'hw-pull', 'PL-128MB', 'Bar pull 128 mm · matte black', 6, 'hardware', { generic: true });
    add('hardware', 'hw-pull', 'KN-32BN', 'Knob 32 mm · brushed nickel', 4, 'hardware', { generic: true });
    [[12, 30], [15, 30], [18, 36], [15, 42]].forEach(([w, h]) => add('glass', 'glass-door', `W${pad(w)}${h}GD`, `Wall cabinet W${pad(w)} H${h} · glass door frame`, 4.2 * w + 3.1 * h + 130, 'glass'));

    // Box colour variants: the first box colour is the series default and carries the plain SKU.
    const boxed = [];
    out.forEach(p => {
      if (p.generic) { boxed.push({ ...p, box: null }); return; }
      series.box.forEach((box, i) => boxed.push({ ...p, box, sku: i === 0 ? p.sku : `${p.sku}-${box}`, msrp: i === 0 ? p.msrp : r(p.msrp * 1.03) }));
    });
    return boxed;
  }

  /* ------------------------------------------------------------------ vanity catalog (price book) */
  // MSRP by series key; null = N/A in the price book.
  const VANITY_ITEMS = [
    // Vanities — full panel
    { cat: 'van-panel', sku: 'VSD24',  cru: 'CRU24',    desc: '24″ vanity · full panel · 2 doors',            img: 'vanity',  msrp: { contempo: 1278, crush: 400,  fund: 680,  e1nws: 674,  e1nno: 809,  e2: 1147, e3: 1370 } },
    { cat: 'van-panel', sku: 'VSD30L', cru: 'CRU30L',   desc: '30″ vanity · full panel · drawers left',       img: 'vanity',  msrp: { contempo: 1647, crush: 489,  fund: 735,  e1nws: 915,  e1nno: 1098, e2: 1501, e3: 1781 } },
    { cat: 'van-panel', sku: 'VSD30R', cru: 'CRU30R',   desc: '30″ vanity · full panel · drawers right',      img: 'vanity',  msrp: { contempo: 1647, crush: 489,  fund: 735,  e1nws: 915,  e1nno: 1098, e2: 1501, e3: 1781 } },
    { cat: 'van-panel', sku: 'VSD36L', cru: 'CRU36L',   desc: '36″ vanity · full panel · drawers left',       img: 'vanity',  msrp: { contempo: 1770, crush: 530,  fund: 819,  e1nws: 967,  e1nno: 1161, e2: 1605, e3: 1787 } },
    { cat: 'van-panel', sku: 'VSD36R', cru: 'CRU36R',   desc: '36″ vanity · full panel · drawers right',      img: 'vanity',  msrp: { contempo: 1770, crush: 530,  fund: 819,  e1nws: 967,  e1nno: 1161, e2: 1605, e3: 1787 } },
    { cat: 'van-panel', sku: 'VSD42L', cru: 'CRU42L',   desc: '42″ vanity · full panel · drawers left',       img: 'vanity',  msrp: { contempo: 1851, crush: 624,  fund: 966,  e1nws: 1040, e1nno: 1248, e2: 1668, e3: 2060 } },
    { cat: 'van-panel', sku: 'VSD42R', cru: 'CRU42R',   desc: '42″ vanity · full panel · drawers right',      img: 'vanity',  msrp: { contempo: 1851, crush: 624,  fund: 966,  e1nws: 1040, e1nno: 1248, e2: 1668, e3: 2060 } },
    { cat: 'van-panel', sku: 'VSD48',  cru: 'CRU48',    desc: '48″ vanity · full panel · drawers both sides', img: 'vanity',  msrp: { contempo: 2595, crush: 988,  fund: 1260, e1nws: 1560, e1nno: 1872, e2: 2381, e3: 2874 } },
    { cat: 'van-panel', sku: 'VSD54',  cru: null,       desc: '54″ vanity · full panel · drawers both sides', img: 'vanity',  msrp: { contempo: 2750, crush: null, fund: 1418, e1nws: 1664, e1nno: 1997, e2: 2525, e3: 3062 } },
    { cat: 'van-panel', sku: 'VSD60',  cru: 'CRU60-S',  desc: '60″ single sink vanity · full panel',          img: 'vanity',  msrp: { contempo: 2798, crush: 1123, fund: 1680, e1nws: 1726, e1nno: 2072, e2: 2639, e3: 3167 } },
    { cat: 'van-panel', sku: 'VCD60',  cru: 'CRU60D',   desc: '60″ double sink vanity · full panel',          img: 'vanity',  msrp: { contempo: 2506, crush: null, fund: 1575, e1nws: 1560, e1nno: 1872, e2: 2254, e3: 2881 } },
    { cat: 'van-panel', sku: 'VCD72',  cru: 'CRU72D',   desc: '72″ double sink vanity · full panel',          img: 'vanity',  msrp: { contempo: 2674, crush: null, fund: 1785, e1nws: 1768, e1nno: 2122, e2: 2388, e3: 3253 } },
    // Vanities — with legs (not offered in Crush / Fundamentals)
    { cat: 'van-legs', sku: 'VSD24-LG',  desc: '24″ vanity · with legs · 2 doors',       img: 'legs', msrp: { contempo: 1215, fund: null, crush: null, e1nws: 674,  e1nno: 809,  e2: 1107, e3: 1330 } },
    { cat: 'van-legs', sku: 'VSD30L-LG', desc: '30″ vanity · with legs · drawers left',  img: 'legs', msrp: { contempo: 1584, fund: null, crush: null, e1nws: 915,  e1nno: 1098, e2: 1461, e3: 1741 } },
    { cat: 'van-legs', sku: 'VSD30R-LG', desc: '30″ vanity · with legs · drawers right', img: 'legs', msrp: { contempo: 1584, fund: null, crush: null, e1nws: 915,  e1nno: 1098, e2: 1461, e3: 1741 } },
    { cat: 'van-legs', sku: 'VSD36L-LG', desc: '36″ vanity · with legs · drawers left',  img: 'legs', msrp: { contempo: 1707, fund: null, crush: null, e1nws: 967,  e1nno: 1161, e2: 1565, e3: 1901 } },
    { cat: 'van-legs', sku: 'VSD36R-LG', desc: '36″ vanity · with legs · drawers right', img: 'legs', msrp: { contempo: 1707, fund: null, crush: null, e1nws: 967,  e1nno: 1161, e2: 1565, e3: 1901 } },
    { cat: 'van-legs', sku: 'VSD42L-LG', desc: '42″ vanity · with legs · drawers left',  img: 'legs', msrp: { contempo: 1778, fund: null, crush: null, e1nws: 1040, e1nno: 1248, e2: 1621, e3: 1973 } },
    { cat: 'van-legs', sku: 'VSD48-LG',  desc: '48″ vanity · with legs',                 img: 'legs', msrp: { contempo: 2528, fund: null, crush: null, e1nws: 1560, e1nno: 1872, e2: 2295, e3: 2836 } },
    { cat: 'van-legs', sku: 'VSD60-LG',  desc: '60″ single sink vanity · with legs',     img: 'legs', msrp: { contempo: 2782, fund: null, crush: null, e1nws: 1726, e1nno: 2072, e2: 2533, e3: 3095 } },
    { cat: 'van-legs', sku: 'VCD60-LG',  desc: '60″ double sink vanity · with legs',     img: 'legs', msrp: { contempo: 2420, fund: null, crush: null, e1nws: 1560, e1nno: 1872, e2: 2203, e3: 2834 } },
    { cat: 'van-legs', sku: 'VCD72-LG',  desc: '72″ double sink vanity · with legs',     img: 'legs', msrp: { contempo: 2588, fund: null, crush: null, e1nws: 1768, e1nno: 2122, e2: 2347, e3: 3206 } },
    // Linen
    { cat: 'linen', sku: 'LC158421L', cru: 'CRULC18842L', desc: 'Linen cabinet 15″ × 84″ · hinge left',  img: 'tall', msrp: { contempo: 3448, crush: 936, fund: 1155, e1nws: null, e1nno: null, e2: 3063, e3: 3510 } },
    { cat: 'linen', sku: 'LC158421R', cru: 'CRULC18842R', desc: 'Linen cabinet 15″ × 84″ · hinge right', img: 'tall', msrp: { contempo: 3448, crush: 936, fund: 1155, e1nws: null, e1nno: null, e2: 3063, e3: 3510 } },
    { cat: 'linen', sku: 'LC158421-LG', desc: 'Linen cabinet with legs 15″ × 84″',               img: 'tall', msrp: { contempo: 3453, crush: null, fund: null, e1nws: 1758, e1nno: 1872, e2: 3190, e3: 3648 } },
    // Base & drawer
    { cat: 'vbase', sku: 'VDB15',      desc: 'Vanity drawer base 15″ · 3 drawers',          img: 'drawer', msrp: { fund: 730 } },
    { cat: 'vbase', sku: 'VDB18',      desc: 'Vanity drawer base 18″ · 3 drawers',          img: 'drawer', msrp: { fund: 756 } },
    { cat: 'vbase', sku: 'SLC-B153924', desc: 'Slim linen base 15″ × 39″ · drawers',        img: 'drawer', msrp: { fund: 867 } },
    { cat: 'vbase', sku: 'MTD24',      desc: 'Make-up table drawers 24″',                   img: 'panel',  msrp: { fund: 368 } },
    { cat: 'vbase', sku: 'MTD30',      desc: 'Make-up table drawers 30″',                   img: 'panel',  msrp: { fund: 399 } },
    // Wall & medicine
    { cat: 'vwall', sku: 'CUB1548L', desc: 'Wall cabinet 15″ × 48″ · door left · drawer',  img: 'wall', msrp: { fund: 735 } },
    { cat: 'vwall', sku: 'CUB1548R', desc: 'Wall cabinet 15″ × 48″ · door right · drawer', img: 'wall', msrp: { fund: 735 } },
    { cat: 'vwall', sku: 'CUD1548L', desc: 'Wall cabinet 15″ × 48″ · door left · drawer',  img: 'wall', msrp: { fund: 735 } },
    { cat: 'vwall', sku: 'CUD1548R', desc: 'Wall cabinet 15″ × 48″ · door right · drawer', img: 'wall', msrp: { fund: 735 } },
    { cat: 'vwall', sku: 'WC1236',   desc: 'Wall cabinet 12″ × 36″',                        img: 'wall', msrp: { e1nws: 499, e1nno: 599, e2: 721, e3: 920 } },
    { cat: 'vwall', sku: 'MC2432',   desc: 'Medicine cabinet 24″ × 32″ · 2 doors',          img: 'wall', msrp: { fund: 420 } },
    // Mirrors (not priced in the quick reference — illustrative)
    { cat: 'mirror', sku: 'M20X32', desc: 'Framed mirror 20″ × 32″', img: 'mirror', msrp: { any: 189 } },
    { cat: 'mirror', sku: 'M28X36', desc: 'Framed mirror 28″ × 36″', img: 'mirror', msrp: { any: 249 } },
    { cat: 'mirror', sku: 'M42X36', desc: 'Framed mirror 42″ × 36″', img: 'mirror', msrp: { any: 329 } }
  ];

  const COUNTERTOPS = [
    // size, budget sintered, regular sintered, quartz 2cm, premium quartz 2cm, premium quartz 3cm
    ['25', 354, 640, 572, 640, 728], ['31', 395, 728, 624, 728, 936], ['37', 437, 811, 697, 811, 988], ['43', 489, 915, 780, 915, 1040],
    ['49', 572, 1019, 832, 1019, 1144], ['55', 624, 1144, 988, 1144, 1352], ['61S', 676, 1248, 1040, 1248, 1456], ['61D', 780, 1404, 1248, 1404, 1612], ['73D', 832, 1508, 1352, 1508, 1820]
  ];

  /* Price-book series (Evolution I/II/III, Crush): rows from assets/vanity-book.js */
  const BOOK_IMG = { 'van-legs': 'legs', 'van-panel': 'vanity', linen: 'tall', vwall: 'wall', accessory: 'panel', hardware: 'hardware', mirror: 'mirror' };
  const titleToDesc = (t) => t.replace(/[”"]/g, '″').split(/\s+-\s*|\s*-\s+/).map(x => x.trim()).filter(Boolean).map((x, i) => {
    const w = x.match(/^(VANITY|LINEN TOWER|LINEN CABINET|WALL CABINET|ACCESSORY)\s*(.*)$/i);
    if (i === 0 && w) return (w[2] ? w[2].replace(/([LR])$/, ' $1').trim() + ' ' : '') + w[1].toLowerCase();
    return x.toLowerCase();
  }).join(' · ');
  function bookProducts(series, color) {
    const book = window.VanityBook || { series: {}, generic: [] };
    const rows = (book.series[series.book] || []).concat(book.generic.filter(g => g.cat === 'hardware' || g.sku === 'TK18VANITY' || g.sku === 'WF3VANITY' || (g.sku.startsWith('G-EVO') && series.book.startsWith('evolution'))));
    const pick = (v) => Array.isArray(v) ? v[color && color.priceIdx ? color.priceIdx : 0] : v;
    return rows.map(r => {
      const width = (r.dims && r.dims[0]) ? Number(String(r.dims[0]).split(' ')[0]) : null;
      const sub = (r.cat === 'van-legs' || r.cat === 'van-panel') && width ? `${r.cat}-${[24, 30, 36, 42, 48, 54, 60, 72].reduce((a, b) => Math.abs(b - width) < Math.abs(a - width) ? b : a)}` : null;
      const config = (r.features || []).find(f => /\+/.test(f)) || '';
      const desc = r.cat === 'hardware' ? `${r.desc.replace(/\s+/g, ' ').replace(/^(KNOB|HANDLE)\s+/i, (m) => m.trim().toLowerCase() + ' · ')}` : `${titleToDesc(r.title)}${r.dims && r.dims.length === 3 ? ` · ${r.dims[0]}″ W × ${r.dims[1]}″ D × ${r.dims[2]}″ H` : ''}${config ? ' · ' + config.toLowerCase() : ''}`;
      return { cat: r.cat, sub, sku: r.sku, base: r.sku, desc: desc.charAt(0).toUpperCase() + desc.slice(1), msrp: pick(r.msrp), assemblyMsrp: r.assembly != null ? pick(r.assembly) : null, img: BOOK_IMG[r.cat] || 'box', box: null, generic: r.cat === 'hardware' || r.cat === 'accessory', features: r.features || [] };
    });
  }

  function vanityProducts(series, color) {
    if (series.book) return bookProducts(series, color);
    const key = series.priceKey;
    const out = [];
    VANITY_ITEMS.forEach(item => {
      const msrp = series.quoteOnly ? null : (item.msrp[key] !== undefined ? item.msrp[key] : (item.msrp.any !== undefined ? item.msrp.any : undefined));
      if (!series.quoteOnly && msrp === null) return;           // N/A in the price book for this series
      if (!series.quoteOnly && msrp === undefined) return;      // item not offered in this series
      const base = series.id === 'crush' && item.cru ? item.cru : item.sku;
      const sku = series.id === 'crush' && item.cru ? item.cru : `${series.code}-${item.sku}`;
      out.push({ cat: item.cat, sub: null, sku, base, desc: item.desc, msrp: msrp ?? null, img: item.img, box: null });
    });
    return out;
  }

  /* ------------------------------------------------------------------ vanity tops (top → size → top service) */
  // MSRP = COUNTERTOPS column `idx` of the chosen top (AGR31-bundle $728 as on the original portal). Bundle = top + undermount sink.
  const MAKEUP_TOPS = [['24', 468], ['30', 520], ['36', 572]];   // illustrative — not in the quick reference
  function vanityTopProducts(series, top) {
    if (!top) return [];
    const P = top.prefix, S = top.suffix || '';
    const out = [];
    const add = (cat, sub, sku, desc, msrp, img, opts = {}) => out.push({ cat, sub, sku, base: sku, desc, msrp, img, box: null, ...opts });
    COUNTERTOPS.forEach(row => {
      const code = row[0], bowl = code.endsWith('D') ? 'double bowl' : 'single bowl', w = code.replace(/[SD]$/, '');
      add('vt-product', 'vt-vanity', `${P}${code}-bundle${S}`, `${w}″ vanity top · ${bowl} · ${top.short.toLowerCase()} · rectangular undermount sink included`, row[top.idx], 'counter', { width: Number(w) });
    });
    if (top.mt) MAKEUP_TOPS.forEach(([w, msrp]) => add('vt-product', 'vt-makeup', `${P.slice(0, 2)}-MT${w}-bundle`, `${w}″ makeup table top · ${top.short.toLowerCase()} · no sink cut-out`, msrp, 'counter', { width: Number(w) }));
    add('vt-accessories', null, `${P}-BS4${S}`, `4″ backsplash · matches ${top.name} · per linear ft`, top.idx === 1 ? 24 : 37, 'panel');
    add('vt-accessories', null, `${P}-SS422${S}`, `Side splash 4″ × 22″ · matches ${top.name}`, top.idx === 1 ? 39 : 58, 'panel');
    add('vt-accessories', null, 'SINK-RU1813', 'Rectangular undermount sink 18″ × 13″ · white vitreous china', 149, 'counter', { generic: true });
    return out;
  }

  // Kitchen series fall back to their first colour; the vanity-top flow has no default (the dealer must pick a colour first).
  /* ------------------------------------------------------------------ vanity hardware configuration (as on the original product page) */
  const PREMIUM_KNOBS = ['K-2644-1MDB-P', 'K-2640-1BPN-P', 'K-2641-1055-P', 'K-2646-1055-P', 'K-2649-1MDB-P', 'K-2645-1BPN-P', 'K-9903-1MDB-P', 'K-4122-1BPN-P', 'K-4126-1055-P', 'K-4124-1026-P', 'K-5036-4055-P', 'K-5048-4MDB-P', 'K-5024-4BPN-P', 'K-5030-4026-P', 'K-1238-1014-P', 'K-1240-1MDB-P', 'K-1236-1BPN-P', 'K-1239-1055-P', 'K-2324-1BPN-P', 'K-2325-1026-P', 'K-2368-1MDB-P', 'K-2394-1055-P'];
  const HARDWARE_LOCATIONS = [['For-drawer', 'For drawer'], ['For-door', 'For door'], ['For-door-drawer', 'For door & drawer']];
  const HARDWARE_INSTRUCTIONS = [['Install-Hardware', 'Install hardware'], ['Install-Back', 'Install on the back'], ['Loose-Hardware', 'Ship hardware loose'], ['Loose-Drillholes', 'Ship loose · drill holes only']];
  function hardwareOptions(series, product) {
    const book = window.VanityBook || { generic: [] };
    const hw = book.generic.filter(g => g.cat === 'hardware');
    const free = (prefix) => hw.filter(g => g.sku.startsWith(prefix)).map(g => ({ code: g.sku + '-free', name: `${g.sku} · ${g.desc.replace(/^(KNOB|HANDLE)\s+/i, '').replace(/\s+/g, ' ')}`, group: 'Included with the vanity' }));
    // Evolution I / II / III vanities with legs: wood legs are standard, metal legs optional (BL / SV / GD-METALLEG)
    const legs = product && product.cat === 'van-legs' && /^evolution/.test(series.book || '');
    return {
      legs: legs ? [{ code: 'WOODLEG', name: `Wood legs · standard${product.color ? ' · ' + (/oak/i.test(product.color) ? 'oak' : 'white') : ''}` }, { code: 'BL-METALLEG', name: 'Metal legs · black (BL-METALLEG)' }, { code: 'SV-METALLEG', name: 'Metal legs · silver (SV-METALLEG)' }, { code: 'GD-METALLEG', name: 'Metal legs · gold (GD-METALLEG)' }] : null,
      knobs: [...free('K'), ...PREMIUM_KNOBS.map(k => ({ code: k, name: k, group: 'Premium knobs' }))],
      handles: free('H'),
      locations: HARDWARE_LOCATIONS.map(([code, name]) => ({ code, name })),
      instructions: HARDWARE_INSTRUCTIONS.map(([code, name]) => ({ code, name }))
    };
  }
  /* Short text for a hardware configuration, shown on cart lines */
  const hardwareText = (h) => h ? [h.legs ? (h.legs === 'WOODLEG' ? 'Wood legs' : h.legs) : null, h.knob ? `${h.knob.replace(/-free$/, '')}${h.knobLoc ? ' ' + h.knobLoc.replace(/^For-/, 'for ').replace('door-drawer', 'door & drawer') : ''}` : null, h.handle ? `${h.handle.replace(/-free$/, '')}${h.handleLoc ? ' ' + h.handleLoc.replace(/^For-/, 'for ').replace('door-drawer', 'door & drawer') : ''}` : null, h.instruction || null].filter(Boolean).join(' · ') : '';

  const colorOf = (series, code) => series.colors ? (series.colors.find(c => c.code === code) || (series.flow === 'vanity-top' ? null : series.colors[0])) : null;
  const doorOf = (series, id) => series.doors ? (series.doors.find(d => d.id === id) || series.doors[0]) : null;
  /* Colours that can be ordered with a given door (ultra slab only on the Hamilton slab door; Fundamentals colours are door-specific) */
  const colorsFor = (series, door) => (series.colors || []).filter(c => (!c.slabOnly || (door && door.slab)) && (!c.doors || !door || c.doors.includes(door.id)));
  /* Page that lists a series' products (the vanity-top flow has its own page) */
  const pageFor = (series) => `${series.flow === 'vanity-top' ? 'new-order-vanity-top.html' : 'new-order-products.html'}?series=${series.id}`;

  function products(series, colorCode, doorId) {
    const door = doorOf(series, doorId);
    let color = colorOf(series, colorCode);
    if (color && door && !colorsFor(series, door).includes(color)) color = colorsFor(series, door)[0] || null;
    const list = series.flow === 'vanity-top' ? vanityTopProducts(series, color) : series.line === 'kitchen' ? kitchenProducts(series, color) : vanityProducts(series, color);
    const colorName = color ? (color.short ? `${color.name} · ${color.short}` : color.name) : null;
    // Vanity series keep the price-book SKU and record door style + colour on the line instead of a SKU prefix
    const variant = series.line === 'vanity' && color ? [door && series.doors.length > 1 && !color.doors ? door.name : null, color.name].filter(Boolean).join(' · ') : null;
    return list.map((p, i) => ({ ...p, color: color && !p.generic ? colorName : null, colorCode: color && !p.generic ? color.code : null, door: door && !p.generic ? door.id : null, variant: p.generic ? null : variant, dealer: p.msrp == null ? null : Math.round(p.msrp * DEALER_MULTIPLIER * 100) / 100, assembly: p.assemblyMsrp == null ? null : Math.round(p.assemblyMsrp * DEALER_MULTIPLIER * 100) / 100, stock: stockFor(p.sku, i) }));
  }

  function stockFor(sku, i) {
    let h = 0; for (const ch of sku) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
    const v = (h + i) % 10;
    return v < 6 ? 99 : v < 9 ? 1 + (h % 9) : 0;
  }

  /* ------------------------------------------------------------------ cart */
  const KEY = 'cb-dealer-cart';
  function readCart() {
    try { return JSON.parse(localStorage.getItem(KEY)) || { items: [] }; } catch (e) { return { items: [] }; }
  }
  function writeCart(cart) {
    try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) { /* storage unavailable — cart lives in memory for this page only */ }
    document.dispatchEvent(new CustomEvent('cart:change', { detail: cart }));
  }
  /* A cart line is identified by its key: the SKU, plus the chosen top services for vanity tops
     (AGR31-bundle with Drill-4 and AGR31-bundle with Drill-8 are two lines). */
  const lineKey = (sku, services, variant, hw) => sku + (variant ? `|${variant}` : '') + (services && services.length ? `|${services.join('+')}` : '') + (hw ? `|${hw}` : '');
  const keyOf = (item) => item.key || item.sku;
  const fit = (it) => { it.tags = (it.tags || []).slice(0, it.qty); while (it.tags.length < it.qty) it.tags.push(''); };
  const newLine = (product, series, qty, services, hardware) => ({ key: lineKey(product.sku, services, product.variant, hardwareText(hardware)), hardware: hardware || null, hardwareText: hardwareText(hardware) || null, tags: Array.from({ length: qty }, () => ''), sku: product.sku, desc: product.desc, dealer: product.dealer, msrp: product.msrp, assembly: product.assembly == null ? null : product.assembly, assemblyMsrp: product.assemblyMsrp == null ? null : product.assemblyMsrp, box: product.box, img: product.img, qty, services: services && services.length ? services.slice() : null, variant: product.variant || null, series: series.id, seriesName: seriesTitle(series) + (series.line !== 'vanity' && product.color ? ' · ' + product.color : ''), color: product.color || null, colorCode: product.colorCode || null, door: product.door || null, line: series.line });
  function setQty(product, series, qty, services) {
    const cart = readCart();
    const key = lineKey(product.sku, services, product.variant);
    const idx = cart.items.findIndex(i => keyOf(i) === key);
    if (qty <= 0) { if (idx > -1) cart.items.splice(idx, 1); }
    else if (idx > -1) { cart.items[idx].qty = qty; fit(cart.items[idx]); }
    else cart.items.push(newLine(product, series, qty, services));
    writeCart(cart);
    return cart;
  }
  /* Add n more pieces of a line (vanity-top "Add to cart"), each pre-filled with the same customer tag */
  function addUnits(product, series, n, services, tag, hardware) {
    const cart = readCart();
    const key = lineKey(product.sku, services, product.variant, hardwareText(hardware));
    let it = cart.items.find(i => keyOf(i) === key);
    if (!it) { it = newLine(product, series, 0, services, hardware); it.tags = []; cart.items.push(it); }
    it.qty += n; fit(it);
    for (let k = it.qty - n; k < it.qty; k++) it.tags[k] = (tag || '').trim().slice(0, 12);
    writeCart(cart);
    return it;
  }
  const qtyOf = (key) => { const it = readCart().items.find(i => keyOf(i) === key); return it ? it.qty : 0; };
  const qtyOfSku = (sku) => readCart().items.filter(i => i.sku === sku).reduce((s, i) => s + i.qty, 0);
  /* Remove every line of a SKU (the product list's "Remove" action) */
  function removeSku(sku) { const cart = readCart(); cart.items = cart.items.filter(i => i.sku !== sku); writeCart(cart); return cart; }
  /* One customer tag per unit: item.tags[k] belongs to the k-th piece of that line */
  function setUnitTag(key, k, tag) { const cart = readCart(); const it = cart.items.find(i => keyOf(i) === key); if (it) { fit(it); it.tags[k] = (tag || '').trim().slice(0, 12); writeCart(cart); } return cart; }
  /* Flatten the cart into one line per unit (used by the summary drawer and checkout) */
  const units = (cart = readCart()) => cart.items.flatMap(i => Array.from({ length: i.qty }, (_, k) => ({ ...i, key: keyOf(i), unit: k, tag: (i.tags || [])[k] || '' })));
  const cartCount = (cart = readCart()) => cart.items.reduce((s, i) => s + i.qty, 0);
  const cartTotal = (cart = readCart()) => cart.items.reduce((s, i) => s + (i.dealer || 0) * i.qty, 0);
  /* Assembly charges (dealer price) if the order is assembled — price-book items carry their own assembly price */
  const cartAssemblyTotal = (cart = readCart()) => cart.items.reduce((s, i) => s + (i.assembly || 0) * i.qty, 0);
  const cartHasQuoteItems = (cart = readCart()) => cart.items.some(i => i.dealer == null);
  function clearCart() { writeCart({ items: [] }); }
  function setCartMeta(patch) { const cart = readCart(); Object.assign(cart, patch); writeCart(cart); return cart; }
  function loadDraft(quoteId) {
    // Sample drafts so "Edit order" opens a populated checkout.
    const drafts = {
      'Q-1847': { series: 'evolution-iii', skus: [['E3-EVO48', 1], ['E3-EVOLC18L', 1]] },
      'Q-1835': { series: 'fundamentals', skus: [['FUN-VSD36L', 1], ['FUN-MC2432', 1]] },
      'Q-1852': { series: 'crush', skus: [['CRU48', 1], ['CRULC188421L', 1]] }
    };
    const d = drafts[quoteId];
    if (!d) return false;
    const series = seriesById(d.series);
    const list = products(series);
    const cart = { items: [], quote: quoteId };
    const tag = { 'Q-1847': 'LIN-WASHROOM', 'Q-1835': 'OAK-36', 'Q-1852': 'SUNSET-48' }[quoteId];
    d.skus.forEach(([sku, qty]) => { const p = list.find(x => x.sku === sku); if (p) { const it = newLine(p, series, qty, null); it.tags = it.tags.map(() => tag); cart.items.push(it); } });
    // Assembly Required is never pre-selected — the dealer chooses it in the order summary every time.
    writeCart(cart);
    return true;
  }

  /* Cart badge in the topbar */
  document.addEventListener('DOMContentLoaded', () => {
    const update = () => {
      const cart = readCart(), n = cartCount(cart);
      document.querySelectorAll('[data-cart-count]').forEach(el => el.textContent = n);
      // The topbar cart opens the order summary: on a product page the drawer opens in place (order-summary.js),
      // elsewhere it goes to the product page of the last line with the summary open.
      const last = cart.items[cart.items.length - 1], s = last && seriesById(last.series);
      document.querySelectorAll('[data-cart-link]').forEach(a => { a.href = s ? `${pageFor(s)}${last.colorCode ? '&color=' + last.colorCode : ''}&summary=1` : 'new-order.html'; });
    };
    update();
    document.addEventListener('cart:change', update);
    window.addEventListener('storage', update);
  });

  return { SERIES, LINE_LABEL, BOX_COLORS, CATEGORIES, DEALER_MULTIPLIER, seriesById, seriesTitle, colorOf, doorOf, colorsFor, pageFor, products, hardwareOptions, hardwareText, readCart, writeCart, lineKey, keyOf, setQty, addUnits, removeSku, qtyOf, qtyOfSku, setUnitTag, units, cartCount, cartTotal, cartAssemblyTotal, cartHasQuoteItems, clearCart, setCartMeta, loadDraft };
})();
