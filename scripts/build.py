from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset
import sys

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)


def rename_font(font, src_name):
    suffix = src_name[:-4][len('CJKPunctBridgeInterrobang-'):]
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
    full = family if style == 'Regular' else f'{family} {style}'
    replacements = {
        1: family, 2: style, 4: full, 6: psname, 16: family, 17: style,
        25: 'EmDashBridge', 5: 'Version 1.000',
        3: f'1.000;SilentPerson;{psname}',
    }
    for nid, val in replacements.items():
        for n in font['name'].names:
            if n.nameID == nid:
                n.string = val.encode(n.getEncoding(), errors='replace')
    for n in font['name'].names:
        try:
            s = n.toUnicode()
        except Exception:
            continue
        s2 = s.replace('CJK Punct Bridge ?!', family).replace('CJKPunctBridgeInterrobang', 'EmDashBridge')
        if s2 != s:
            n.string = s2.encode(n.getEncoding(), errors='replace')


def subset_font(src, dst):
    f = TTFont(src)
    opts = subset.Options()
    opts.layout_features = ['ccmp', 'locl']
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
    sub.populate(unicodes=[0x2014, 0x2015, 0x2E3A, 0x2E3B])
    sub.subset(f)
    rename_font(f, src.name)
    f.flavor = None
    f.save(dst)
    wf = TTFont(dst)
    wf.flavor = 'woff2'
    wf.save(dst.with_suffix('.woff2'))


for src in sorted(SRC.glob('*.ttf')):
    outname = src.name.replace('CJKPunctBridgeInterrobang', 'EmDashBridge')
    subset_font(src, OUT / outname)
