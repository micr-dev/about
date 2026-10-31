# Web font maintenance and measurements

## Rendering contract

Keep the current appearance, `font-display: block`, `"DecimaMono", monospace` fallback stack, font-ready gate, and browser-synthesized bold/italic behavior. Do not add build-time processing, generated fallback faces, stylesheet embedding, or idle precaching.

The site has one page, `/`. There are no article routes, code components, or italic components. `index.html`, all of `style.css`, all of `script.js`, and decoded `data.json` were audited, including inline styles, canvas text measurement, image labels, hover text, and load-error text. The renderer's `fonts` section displays font names as text; it does not load those fonts.

Only DecimaMono is referenced. It is a static regular face. Actual text uses weights 400 and synthesized 700; sizes are 7, 8, 10, 12, and 14px. The initial h1 also uses the browser's heading size and bold. No inline style changes font family, weight, axes, style, or OpenType features. The hover cursor inherits the family and uses 14px. No variable-axis ranges need instancing. There are no explicit feature settings, italic text, or `hyphens: auto` in the shipped page. Keep default `liga`; remove opt-in `dnom`, `frac`, `numr`, `sinf`, `sups`, and `zero`. The source has no positioning lookups and no hint programs.

Content's non-ASCII characters are U+00E9, U+00ED, U+2013, U+2019, U+304D, U+3053, U+3055, U+3086, U+3093, U+30C9, U+30DF, and U+30EA. Preserve ASCII, existing Latin-1 and Latin Extended-A coverage, and all used characters supported by the source. CJK already uses system fallback and must continue doing so. The source lacks U+00A0, U+017F, and U+2010. Do not invent their coverage. U+2010 from automatic hyphenation therefore remains a fallback glyph if hyphenation is introduced. The fixture exercises both automatic hyphenation and explicit U+2010.

The core contains U+0020-007E, U+2013-2014, U+2018-2019, U+201C-201D, and U+2026. Only the core is preloaded. The extended CSS range is U+00A1-017E. Both CSS ranges contain only characters in their corresponding serialized cmap. No intermediate fallback face exists.

### Necessary rasterization exception

The extended file also retains 29 reference cmap entries outside its CSS range: the unique ASCII characters in `THEZOCQSHEZLOCUSfijkdbhxzroescpqgjy`, plus U+2070. These are not additional CSS coverage. The Linux Chromium rasterizer changes accented glyph pixels when these references are removed, even though glyph outlines and advances remain identical.

With the final metadata settings, removing these entries reduces the extended file from 9,528 to 8,752 bytes, saving 776 bytes. That optimization is rejected because it changes rendering. An earlier strict split changed 104 pixels on each actual-page screenshot and 7,124 pixels in the comprehensive fixture. Keeping ASCII alone still left a four-pixel accent difference; retaining U+2070 removed that difference. The shipped reference set produces exact equality at both tested device-pixel ratios. No residual differences are classified as harmless rounding.

DecimaMono is not OFL-licensed in its embedded metadata and has no Reserved Font Name notice. Its copyright and trademark names remain in the outputs. The untouched Terminus file mentions OFL 1.1, but it is not served or modified. Embedded notices are not a substitute for the owner's font license. A replacement source with an RFN notice makes the script stop until its internal names have been renamed and audited.

## Before and after

All sizes are exact file bytes, not HTTP headers. Source inventory and browser measurements are in [font-audit.json](font-audit.json).

| Font | Original bytes | Original glyphs | Served after | Source asset after |
| --- | ---: | ---: | ---: | --- |
| DecimaMono.ttf | 94,392 | 644 | 5,700 core + 9,528 extended | Unchanged manual input |
| Acumin-Variable-Concept.ttf | 1,029,036 | 348 | 0 | Unchanged |
| AlteHaasGroteskBold.ttf | 144,556 | 268 | 0 | Unchanged |
| BONNES.ttf | 28,552 | 169 | 0 | Unchanged |
| DecimaPro.ttf | 147,144 | 565 | 0 | Unchanged |
| Dutch 801 Bold BT.ttf | 48,268 | 260 | 0 | Unchanged |
| Roboto-Regular.ttf | 158,604 | 1,037 | 0 | Unchanged |
| TerminusTTF-4.49.3.ttf | 500,668 | 1,359 | 0 | Unchanged |
| monbaiti.ttf | 356,576 | 1,824 | 0 | Unchanged |

The generated core has 105 glyphs and 102 cmap entries. The extended has 253 glyphs and 251 cmap entries, of which 222 are in its CSS range. Both retain only `liga`, have no axes, and have no hint tables or glyph hint programs. Serialized outlines and horizontal metrics match the source for all 353 cmap entries across the two files.

Acumin is the only variable source asset: `wght` 100..900, default 194.28570556640625; `wdth` 50..115, default 100; `slnt` 0..12, default 0. All other source fonts are static. None of these axes is used by the site.

| Source font | GSUB features | GPOS features | Hinting |
| --- | --- | --- | --- |
| DecimaMono | dnom, frac, liga, numr, sinf, sups, zero | None | None |
| Acumin | case, dnom, frac, liga, numr, ordn, pnum, rvrn, salt, sinf, ss01, subs, sups, tnum, xxxx, zero | kern | No CFF2 hint operators |
| AlteHaasGroteskBold | ccmp, liga | kern | 216 hinted glyphs; fpgm, prep, cvt, hdmx, VDMX, LTSH |
| BONNES | liga | kern | None |
| DecimaPro | dnom, frac, liga, numr, pnum, salt, sinf, sups, tnum, zero | kern | 561 hinted glyphs; fpgm, prep, cvt |
| Dutch 801 Bold BT | None | None | 189 hinted glyphs; fpgm, prep, cvt |
| Roboto-Regular | liga, smcp | kern | 892 hinted glyphs; fpgm, prep, cvt |
| Terminus | None | None | 1 hinted glyph; cvt |
| monbaiti | calt, ccmp, fina, init, isol, medi, rlig, vert | mark | 980 hinted glyphs; fpgm, prep, cvt, hdmx, VDMX, LTSH |

The original font directory totals 2,507,796 bytes. Original assets remain as requested scope preservation and generation inputs, so repository storage grows by 15,228 font bytes. Unused assets never contributed to page transfer; deleting them would save repository/deployment storage, not page font bytes.

### Cold page requests

Browser cache was disabled. Values below are observed decoded resource bytes; the static server sent the font files without additional HTTP compression.

| Page or isolated verification case | Before | After | Extended requested? |
| --- | ---: | ---: | --- |
| `/`, desktop and mobile | 94,392 | 15,228 | Yes, content contains é and í |
| `/`, accented image-label hover | 94,392 | 15,228 | Yes |
| Comprehensive fixture, code/italic/Latin/component overrides/CJK | 94,392 | 15,228 | Yes |
| ASCII fixture | 94,392 | 5,700 | No |
| Accented fixture | 94,392 | 15,228 | Yes |
| CJK fixture, including ASCII spaces | 94,392 | 5,700 | No |

The page preload changes from `fonts/DecimaMono.ttf` to `fonts/decima-mono-core.woff2`. The comprehensive fixture has that same preload. The small coverage fixtures intentionally have no preload, to prove demand loading. The real page saves 79,164 bytes, or 83.87%. Preloaded font bytes decrease by 93.96%.

## Pixel proof

The baseline is a filesystem snapshot of revision `f5ae9223` taken before changes, not the live website. Both variants use identical `data.json`, JavaScript, images, viewport, browser, and system fonts. This static site has no build step. The optimized snapshot differs only in the font-face block, preload, and font outputs.

Chromium 156.0.8078.47 on Linux arm64, FontTools 4.62.1, Brotli 1.2.0. Each capture disables browser cache, waits for network idle, `document.fonts.ready`, and image decoding, then captures the full page. Exact RGB comparison uses no tolerance or ignored regions. Every pair also has identical rendered body text.

| Comparison | Screenshot pixels | Changed pixels | Maximum channel delta |
| --- | ---: | ---: | ---: |
| Desktop, 1440x1000 viewport, DPR 1 | 5,161,350 | 0 | 0 |
| Mobile, 390x844 viewport, DPR 1 | 1,612,125 | 0 | 0 |
| Comprehensive fixture, DPR 1 | 1,440,000 | 0 | 0 |
| ASCII fixture | 1,440,000 | 0 | 0 |
| Accented fixture | 1,440,000 | 0 | 0 |
| CJK fixture | 1,440,000 | 0 | 0 |
| Desktop, DPR 2 | 20,645,400 | 0 | 0 |
| Comprehensive fixture, DPR 2 | 5,760,000 | 0 | 0 |
| Actual accented hover label, DPR 1 | 5,161,350 | 0 | 0 |

Total: 44,100,225 compared pixels, zero changed pixels. The fixture tests browser-default code styling with the inherited font family, synthesized italics, bold inside italics, a 19px bold-italic component override, all printable Latin-1 and Latin Extended-A characters, punctuation, CJK, soft hyphen, and explicit/automatic hyphenation. Fixture-only content is not added to the site.

[font-proof.tar.xz](font-proof.tar.xz) contains the before/after PNGs, exact difference PNGs, fixture HTML for both variants, request records, and pixel counts. Screenshot SHA-256 values and unchanged source hashes are in `font-audit.json`. Extract it with `tar -xJf docs/font-proof.tar.xz -C <empty-directory>`.

For a new comparison, take a fresh baseline snapshot before changing content or fonts. Serve baseline and optimized snapshots on the same machine. Use the fixture HTML from the archive at each snapshot's root so relative URLs resolve. Repeat the viewports above with cache disabled; wait for fonts and images, capture full-page PNGs, and compare RGB arrays without tolerance. Do not compare today's content with an older screenshot. Preserve every difference as a failure until explained and fixed or explicitly approved.

This proves the measured Chromium/Linux configurations, not every browser or operating system. Safari, Firefox, and native Windows/macOS rasterizers were not exercised. Source-outline and advance equality provide an additional cross-platform invariant, not a substitute for those browser checks.

## Regenerate by hand

There is no package manager, build command, or configured lint/typecheck/test suite in this repository. Font processing is deliberately outside deployment. Set up a disposable Python environment once:

```sh
python3 -m venv /tmp/about-font-tools
/tmp/about-font-tools/bin/python -m pip install 'fonttools[woff]==4.62.1' 'brotli==1.2.0'
```

Run from any directory:

```sh
/tmp/about-font-tools/bin/python /path/to/about/scripts/subset-fonts.py
```

The script reads the original `fonts/DecimaMono.ttf`, HTML, decoded JSON content, JavaScript, and CSS. It overwrites the two WOFF2 files and only the marked generated font-face section of `style.css`. It checks the saved cmaps, layout features, and absence of hinting. Two consecutive runs produced identical SHA-256 values for both fonts and CSS.

Rerun after changing content, labels, generated/error strings, CSS text, or the source font. A change to family, weight, style, variable axes, feature settings, hyphenation, or source license also requires a fresh usage audit and pixel proof; the script does not infer CSS cascade semantics or arbitrary JavaScript Unicode escapes. Review new character coverage and fallback boundaries. Commit both WOFF2 files and generated CSS with the source/content change. Never run this script automatically from a build or deploy hook.
