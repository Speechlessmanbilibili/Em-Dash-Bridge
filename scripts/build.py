from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
import sys

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)


def find_ligature_outputs(font, first_glyph):
    outputs = {}
    if 'GSUB' not in font:
        return outputs
    for lookup in font['GSUB'].table.LookupList.Lookup:
        if lookup.LookupType != 4:
            continue
        for subtable in lookup.SubTable:
            ligatures = getattr(subtable, 'ligatures', {})
            for lig in ligatures.get(first_glyph, []):
                length = 1 + len(lig.Component)
                if length in (2, 3) and all(component == first_glyph for component in lig.Component):
                    outputs[length] = lig.LigGlyph
    return outputs


def rename_font(font, src_name):
    stem = src_name[:-4]
    suffix = stem[len('CJKPunctBridgeInterrobang-'):]
    if suffix == 'Variable':
        style = 'Regular'
        psname = 'EmDashBridge'
    elif suffix == 'Italic-Variable':
        style = 'Italic'
        psname = 'EmDashBridge-Italic'
    else:
        style = suffix.replace('Italic', ' Italic').strip()
        psname = f'EmDashBridge-{suffix}'

    family = 'Em Dash Bridge'
    psfamily = 'EmDashBridge'
    full = family if style == 'Regular' else f'{family} {style}'
    replacements = {
        1: family,
        2: style,
        3: f'1.002;SilentPerson;{psname}',
        4: full,
        5: 'Version 1.002',
        6: psname,
        16: family,
        17: style,
        25: psfamily,
    }

    name = font['name']
    for nid, val in replacements.items():
        for rec in [n for n in name.names if n.nameID == nid]:
            rec.string = val.encode(rec.getEncoding(), errors='replace')

    for rec in name.names:
        try:
            s = rec.toUnicode()
        except Exception:
            continue
        ns = s.replace('CJK Punct Bridge ?!', family).replace(
            'CJKPunctBridgeInterrobang', psfamily
        )
        if ns != s:
            rec.string = ns.encode(rec.getEncoding(), errors='replace')


def subset_font(src, dst):
    font = TTFont(src)
    cmap = font.getBestCmap()

    emdash = cmap[0x2014]
    horizontal_bar = cmap[0x2015]
    two_em = cmap[0x2E3A]
    three_em = cmap[0x2E3B]

    horizontal_bar_ligs = find_ligature_outputs(font, horizontal_bar)
    if set(horizontal_bar_ligs) != {2, 3}:
        raise RuntimeError(
            f'{src.name}: expected two- and three-character U+2015 ligatures, '
            f'found {horizontal_bar_ligs}'
        )
    hb_two = horizontal_bar_ligs[2]
    hb_three = horizontal_bar_ligs[3]

    opts = subset.Options()
    opts.layout_features = []
    opts.name_IDs = ['*']
    opts.name_legacy = True
    opts.name_languages = ['*']
    opts.notdef_glyph = True
    opts.notdef_outline = True
    opts.recalc_bounds = True
    opts.recalc_timestamp = False
    opts.canonical_order = True
    opts.glyph_names = True

    sub = subset.Subsetter(options=opts)
    sub.populate(
        unicodes=[0x2014, 0x2015, 0x2E3A, 0x2E3B],
        glyphs=[hb_two, hb_three],
    )
    sub.subset(font)

    if 'GSUB' in font:
        del font['GSUB']
    if 'GPOS' in font:
        del font['GPOS']

    features = f'''
languagesystem DFLT dflt;
feature ccmp {{
    sub {emdash} {emdash} {emdash} by {three_em};
    sub {emdash} {emdash} by {two_em};
    sub {horizontal_bar} {horizontal_bar} {horizontal_bar} by {hb_three};
    sub {horizontal_bar} {horizontal_bar} by {hb_two};
}} ccmp;
'''
    addOpenTypeFeaturesFromString(font, features)

    rename_font(font, src.name)
    font.flavor = None
    font.save(dst)

    web = TTFont(dst)
    web.flavor = 'woff2'
    web.save(dst.with_suffix('.woff2'))


for src in sorted(SRC.glob('*.ttf')):
    outname = src.name.replace('CJKPunctBridgeInterrobang', 'EmDashBridge')
    subset_font(src, OUT / outname)
