# Em Dash Bridge

A minimal fallback/bridge font for continuous em-dash shaping, derived from **CJK Punct Bridge ?! v1.3.4**.

## What it does

Em Dash Bridge exposes only the three Unicode characters needed for em-dash use:

- `U+2014 — EM DASH`
- `U+2E3A ⸺ TWO-EM DASH`
- `U+2E3B ⸻ THREE-EM DASH`

Its OpenType shaping logic is deliberately universal and language-neutral:

- `——` → the same continuous two-em dash glyph used by `⸺`
- `———` → the same continuous three-em dash glyph used by `⸻`

The substitutions are implemented in `ccmp` under the OpenType `DFLT` script. There is no `locl` matrix and no Chinese/Japanese/Korean/Western language distinction: the same rule applies everywhere.

The direct `U+2E3A` and `U+2E3B` mappings reuse the exact glyphs that serve as the two- and three-character `ccmp` ligature outputs, so they add no extra outlines.

## Deliberately removed

- All punctuation other than `U+2014`, `U+2E3A`, and `U+2E3B`
- `U+2015` and other dash-like characters
- `locl` and all language/region-specific shaping branches
- Unrelated GSUB/GPOS behavior

The resulting static fonts still contain only four glyphs including `.notdef`.

## Builds

The build produces upright and italic variable fonts plus nine static weights for each style, in both TTF and WOFF2.

To rebuild from an extracted `CJKPunctBridgeInterrobang-v1.3.4.zip` directory:

```bash
pip install -r requirements.txt
python scripts/build.py /path/to/extracted/source dist
```

The source package used for the initial derivation was `CJKPunctBridgeInterrobang-v1.3.4.zip`, SHA-256:

`3e3126cf5dca3163b43d4d34a7cbb3401866350fb8ef4d230defcba918aa35ef`

## License

Em Dash Bridge is a modified font distributed under the **SIL Open Font License 1.1**. See `OFL.txt` and `THIRD_PARTY_NOTICES.md`.
