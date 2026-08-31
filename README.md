# Em Dash Bridge

A minimal fallback/bridge font for continuous em-dash shaping, derived from **CJK Punct Bridge ?! v1.3.4**.

## What it does

Em Dash Bridge intentionally exposes only one Unicode character:

- `U+2014 — EM DASH`

Its OpenType shaping logic is deliberately universal and language-neutral:

- `——` → one continuous two-em dash glyph
- `———` → one continuous three-em dash glyph

The substitutions are implemented in `ccmp` under the OpenType `DFLT` script. There is no `locl` matrix and no Chinese/Japanese/Korean/Western language distinction: the same rule applies everywhere.

`U+2E3A TWO-EM DASH` and `U+2E3B THREE-EM DASH` are **not** exposed through cmap. Their outlines remain only as internal ligature outputs required to shape repeated `U+2014`.

## Deliberately removed

- All punctuation other than `U+2014`
- Direct cmap mappings for `U+2015`, `U+2E3A`, `U+2E3B`, and other dash-like characters
- `locl` and all language/region-specific shaping branches
- Unrelated GSUB/GPOS behavior

The resulting static fonts contain only four glyphs including `.notdef`.

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
