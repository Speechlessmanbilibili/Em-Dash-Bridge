# Em Dash Bridge

A minimal fallback/bridge font for continuous em-dash shaping, derived from **CJK Punct Bridge ?! v1.3.5**.

## What it does

Em Dash Bridge exposes only the four Unicode characters needed for its dash shaping:

- `U+2014` — EM DASH
- `U+2015` ― HORIZONTAL BAR
- `U+2E3A` ⸺ TWO-EM DASH
- `U+2E3B` ⸻ THREE-EM DASH

Its OpenType shaping logic is deliberately universal and language-neutral:

- `——` → the same continuous two-em dash glyph used by `⸺`
- `———` → the same continuous three-em dash glyph used by `⸻`
- `――` → the retained continuous two-character HORIZONTAL BAR ligature
- `―――` → the retained continuous three-character HORIZONTAL BAR ligature

The substitutions are implemented in `ccmp` under the OpenType `DFLT` script. There is no `locl` matrix and no Chinese/Japanese/Korean/Western language distinction: the same rules apply everywhere.

The direct `U+2E3A` and `U+2E3B` mappings reuse the exact glyphs that serve as the two- and three-character `U+2014` ligature outputs, so they add no extra outlines.

## Deliberately removed

- All punctuation other than `U+2014`, `U+2015`, `U+2E3A`, and `U+2E3B`
- Other dash- and hyphen-like characters outside those four code points
- `locl` and all language/region-specific shaping branches
- Unrelated GSUB/GPOS behavior

Each built font contains only seven glyphs including `.notdef`: the four directly mapped characters plus the two retained `U+2015` ligature outputs, with `U+2E3A`/`U+2E3B` also serving as the `U+2014` ligature outputs.

## Builds

The build produces upright and italic variable fonts plus nine static weights for each style, in both TTF and WOFF2.

To rebuild from an extracted `CJKPunctBridgeInterrobang-v1.3.5.zip` directory:

```bash
pip install -r requirements.txt
python scripts/build.py /path/to/extracted/source dist
```

The source package used for this build was `CJKPunctBridgeInterrobang-v1.3.5.zip`, SHA-256:

`5554f37832a6cff1ecf4c0815216be73c40176a6c781b9b3df87b0083129afce`

## License

Em Dash Bridge is a modified font distributed under the **SIL Open Font License 1.1**. See `OFL.txt` and `THIRD_PARTY_NOTICES.md`.
