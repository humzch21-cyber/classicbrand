"""Build assets/vanity-book.js from the vanity price-book PDFs (pdftotext -layout output).

    python3 vanity_book.py <evolution.txt> <crush.txt>

Parses every "SKU  $MSRP [$MSRP]  description  W D H" row with its "$xx ASSEMBLY PRICE" line and the
door/drawer configuration that follows, and writes window.VanityBook = {...} for assets/catalog.js.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SKU_RE = re.compile(r'(?<![\w-])([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)\s+\$([\d,]+)(?:\s+\$([\d,]+))?')
DIM_RE = re.compile(r'(\d+(?: \d+/\d+)?|\d+/\d+)\s*[”"]')
TITLE_RE = re.compile(r'^\s*(VANITY|WALL CABINET|LINEN CABINET|LINEN TOWER|ACCESSORY|TALL|MIRROR|MEDICINE|HANDLES & KNOBS|2cm Sintered Stone)\b(.*)$')
ASSEMBLY_RE = re.compile(r'\$(\d+)(?:\s+\$(\d+))?\s+ASSEMBLY PRICE')
LEAD_JUNK = re.compile(r'^(?:\s*(?:\d+(?: \d+/\d+)?|\d+/\d+)\s*[”"]\s*)+')
FEATURE_RE = re.compile(r'((?:\d+\s+)?(?:FAKE|DOORS?|DRAWERS?|LEGS)\b.*|INCLUDE HANDLES.*|Includes .*|SLAB & SHAKER.*|FULL PANELS?.*|\d+ Adjustable.*|CUT TO SIZE.*)')


def num(s):
    return int(s.replace(',', ''))


def clean(line):
    """Strip the drawing dimensions pdftotext leaves at the start of a line."""
    s = LEAD_JUNK.sub('', line).strip()
    return s


def series_of(sku, book):
    if book == 'crush':
        return 'crush' if sku.startswith('CRU') else 'generic'
    if sku.startswith('E2FP-') or sku.startswith('E2-'):
        return 'evolution-ii'
    if sku.startswith('E3FP-') or sku.startswith('E3-'):
        return 'evolution-iii'
    if sku.startswith('EVO'):
        return 'evolution-i'
    return 'generic'


def category(title, sku, series):
    t = title.upper()
    if t.startswith('HANDLES'):
        return 'hardware'
    if t.startswith('2CM'):
        return 'top'
    if t.startswith('LINEN'):
        return 'linen'
    if t.startswith('WALL') or t.startswith('MEDICINE'):
        return 'vwall'
    if t.startswith('MIRROR'):
        return 'mirror'
    if t.startswith('ACCESSORY') or sku.startswith(('G-', 'TK', 'WF')):
        return 'accessory'
    if t.startswith('VANITY'):
        if 'FP-' in sku or series == 'crush':
            return 'van-panel'
        return 'van-legs'
    return 'other'


def parse(text, book):
    lines = text.split('\n')
    items, title, cur = [], '', None
    for raw in lines:
        line = raw.rstrip()
        m = TITLE_RE.match(line)
        if m and '$' not in line:
            title = ' '.join(line.split())
            cur = None
            continue
        c = clean(line)
        m = SKU_RE.search(c)
        if m and 'ASSEMBLY' not in c and not re.match(r'^\d', m.group(1)):
            sku, p1, p2 = m.group(1), num(m.group(2)), (num(m.group(3)) if m.group(3) else None)
            rest = c[m.end():].strip()
            dims = [d for d in DIM_RE.findall(rest)]
            desc = DIM_RE.sub('', rest).strip(' -')
            cur = {'sku': sku, 'msrp': [p1, p2] if p2 is not None else p1, 'desc': desc, 'dims': dims[:3], 'title': title,
                   'series': series_of(sku, book), 'assembly': None, 'features': []}
            cur['cat'] = category(title, sku, cur['series'])
            items.append(cur)
            continue
        if cur is None:
            continue
        a = ASSEMBLY_RE.search(c)
        if a:
            cur['assembly'] = [int(a.group(1)), int(a.group(2))] if a.group(2) else int(a.group(1))
            continue
        if 'ASSEMBLY PRICE' in c and cur['assembly'] is None:
            cur['assembly'] = 'pending'
        elif cur['assembly'] == 'pending':
            m2 = re.search(r'\$(\d+)', c)
            if m2:
                cur['assembly'] = int(m2.group(1))
        f = FEATURE_RE.search(c)
        if f:
            cur['features'].append(' '.join(f.group(1).split()))
    return items


def main():
    evo = Path(sys.argv[1]).read_text(errors='ignore')
    crush = Path(sys.argv[2]).read_text(errors='ignore')
    items = parse(evo, 'evolution') + parse(crush, 'crush')
    # Left/right twins share one block: "EVO30L $915 $1,098 RTA - FLAT …" then "EVO30R $915 $1,098" then the assembly line.
    for i, it in enumerate(items):
        twin = items[i + 1] if i + 1 < len(items) and items[i + 1]['title'] == it['title'] and items[i + 1]['series'] == it['series'] else None
        prev = items[i - 1] if i and items[i - 1]['title'] == it['title'] and items[i - 1]['series'] == it['series'] else None
        for other in (twin, prev):
            if not other:
                continue
            if it['assembly'] is None and other['assembly'] is not None:
                it['assembly'] = other['assembly']
            if not it['dims'] and other['dims']:
                it['dims'] = other['dims']
            if not it['features'] and other['features']:
                it['features'] = other['features']
    # Hardware / generic accessories repeat in every section — keep one copy per SKU.
    out, seen = {'series': {}, 'generic': []}, set()
    for it in items:
        if it['cat'] == 'top':
            continue  # sintered tops live on the vanity-top page
        key = (it['series'], it['sku'])
        if key in seen:
            continue
        seen.add(key)
        if it['series'] == 'generic':
            out['generic'].append(it)
        else:
            out['series'].setdefault(it['series'], []).append(it)
    js = 'window.VanityBook = ' + json.dumps(out, ensure_ascii=False, indent=None, separators=(',', ':')) + ';\n'
    (ROOT / 'assets/vanity-book.js').write_text('/* Generated by vanity_book.py from the Evolution I/II/III (June 2026) and Crush (March 2026) price books. */\n' + js, encoding='utf-8')
    for k, v in out['series'].items():
        print(k, len(v), 'items;', sum(1 for i in v if i['assembly'] is None), 'without assembly')
    print('generic', len(out['generic']))


if __name__ == '__main__':
    main()
