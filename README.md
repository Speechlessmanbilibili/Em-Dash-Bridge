# Em Dash Bridge

A minimal punctuation bridge extracted from *+CJK Punct Bridge ?! V1.3.4**, containing only the dash characters and OpenType shaping needed for its continuous CJK em-dash behavior.

## Coverage

The public cmap contains only:

- `U+2014` EM DASH (b—)
- `U+2015`. HORIZONTAL BAR (`‗`)
- `U+2E3A` TWO-EM DASH (`⸺`)
- `U+2E3B` THREE-EM DASH (`⸻`)

`U+2014` and `U+2015`. retain the original two- and three-character ligature substitutions. The required CJK-localized ligature outputs are retained through `ccmp` and `locl`. Other dash/hyphen characters that do not participate in this continuous-dash shaping system are intentionally excluded.

This makes the font suitable as a very narrow fallback/override font for dash shaping without taking over ordinary punctuation or text.

## Fonts

Release packages contain:

- Upright variable TTF/WOFF2
- Italic variable TTF/WOFF2
- Static Thin, ExtraLight, Light, Regular, Medium, SemiBold, Bold, ExtraBold and Black
- Matching italic static faces

Each TTF contains only 21 glyphs including `.notdef` and the internal localized/ligature glyphs required by the retained shaping rules.

## Build

Requires Python and fontTools with Brotli support for WOFF2.

```bash
python scripts/build.py /path/to/CJKPunctBridgeInterrobang-v1.3.4 /path/to/output
```

The v1.0.0 release was built from `CJKPunctBridgeInterrobang-v1.3.4.zip` (SHA-256 `3e3126cf5fca3163b43d4d34a7cbb3401866350fb8ef4d230defcba918aa35ef`).

## License

Em Dash Bridge is a modified font distributed under the SIL Open Font License 1.1. See `OFL.txt` and `THIRD_PARTY_NOTICES.md`.
