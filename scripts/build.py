from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
import sys

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

FEATURES = r'''
languagesystem DFLT dflt;
feature ccmp {
    sub emdash emdash emdash by uni2E3B;
    sub emdash emdash by uni2E3A;
} ccmp;
'''


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
        3: f'1.001;SilentPerson;{psname}',
        4: full,
        5: 'Version 1.001',
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
        ns = s.replace('CJK Punct Bridge ?!', family).replace('CJKPunctBridgeInterrobang', psfamily)
        if ns != s:
            rec.string = ns.encode(rec.getEncoding(), errors='replace')


def subset_font(src, dst):
    font = TTFont(src)
    opts = subset.Options()
    opts.layout_features = ['ccmp']
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
    # Only U+2014 is public. U+2E3A/U+2E3B survive solely as internal
    # ligature-output glyphs required by the ccmp closure.
    sub.populate(unicodes=[0x2014])
    sub.subset(font)

    # Replace the inherited multilingual GSUB matrix with one universal
    # DFLT ccmp rule. No locl, no language/region-specific behavior.
    if 'GSUB' in font:
        del font['GSUB']
    if 'GPOS' in font:
        del font['GPOS']
    addOpenTypeFeaturesFromString(font, FEATURES)

    rename_font(font, src.name)
    font.flavor = None
    font.save(dst)

    web = TTFont(dst)
    web.flavor = 'woff2'
    web.save(dst.with_suffix('.woff2'))


for src in sorted(SRC.glob('*.ttf')):
    outname = src.name.replace('CJKPunctBridgeInterrobang', 'EmDashBridge')
    subset_font(src, OUT / outname)
