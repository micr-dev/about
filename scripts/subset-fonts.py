#!/usr/bin/env python3
"""Run by hand after content/font/style changes. Never part of deployment."""
from pathlib import Path
from html import unescape
import json

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "fonts/DecimaMono.ttf"
# Includes generated/error/hover text and inline component styles, not just HTML.
INPUTS = ("index.html", "data.json", "script.js", "style.css")
CORE = set(range(0x20, 0x7F)) | {0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2026}
FEATURES = ["liga"]  # Browser-default ligatures; no opt-in numeric alternates.
# FreeType's unhinted Latin rasterizer uses reference glyphs even when they are
# not drawn. Removing these from the extended face shifts accent rendering.
# Keep their cmap entries for the rasterizer, but exclude them from its CSS range.
RASTER_REFERENCES = set(map(ord, "THEZOCQSHEZLOCUSfijkdbhxzroescpqgjy")) | {0x2070}
START = "/* Generated font faces: scripts/subset-fonts.py */"
END = "/* End generated font faces */"


def unicode_range(points):
    runs = []
    for point in sorted(points):
        if runs and point == runs[-1][1] + 1:
            runs[-1][1] = point
        else:
            runs.append([point, point])
    return ", ".join(f"U+{a:04X}" + (f"-{b:04X}" if a != b else "") for a, b in runs)


def main():
    source = TTFont(SOURCE)
    # This pipeline is intentionally specific to the site's static, unhinted face.
    # New sources need an axis/style/license audit, not automatic instancing.
    if "fvar" in source:
        raise ValueError("Audit variable axis usage before replacing this static font")
    names = " ".join(n.toUnicode() for n in source["name"].names)
    if "reserved font name" in names.lower():
        raise ValueError("Rename this RFN font internally before generating subsets")
    available = set(source.getBestCmap())
    contents = {name: (ROOT / name).read_text() for name in INPUTS}
    # Decode JSON escapes and HTML entities before collecting characters.
    contents["data.json"] = json.dumps(json.loads(contents["data.json"]), ensure_ascii=False)
    used = {ord(c) for text in contents.values() for c in unescape(text)}
    # Retain only existing coverage. In particular, never introduce Latin or CJK
    # glyphs that previously came from the unchanged system fallback stack.
    keep = (used | set(range(0x00A0, 0x0180)) | CORE | {0x2010}) & available
    groups = {"core": keep & CORE, "extended": keep - CORE}
    faces = [START]
    for label, points in groups.items():
        coverage = points | (RASTER_REFERENCES & available if label == "extended" else set())
        font = TTFont(SOURCE, recalcTimestamp=False, recalcBBoxes=False)
        options = subset.Options()
        options.hinting = False
        options.layout_features = FEATURES
        options.recalc_bounds = False
        options.recalc_timestamp = False
        options.canonical_order = True
        # The source has no positioning lookups; omit its empty GPOS table.
        options.drop_tables += ["FFTM", "GPOS"]
        # Keep legal notices and required names, not vendor/version metadata.
        options.name_IDs = [0, 1, 2, 4, 6, 7, 13, 14]
        subsetter = subset.Subsetter(options=options)
        subsetter.populate(unicodes=coverage)
        subsetter.subset(font)
        font.flavor = "woff2"
        target = ROOT / f"fonts/decima-mono-{label}.woff2"
        font.save(target)
        # Verify the serialized result, not the pre-save representation.
        result = TTFont(target)
        actual = set(result.getBestCmap())
        if actual != coverage:
            raise ValueError(f"{target.name}: cmap changed during serialization")
        if any(t in result for t in ("fpgm", "prep", "cvt ", "hdmx", "VDMX", "LTSH")):
            raise ValueError(f"{target.name}: hint tables remain")
        if any(getattr(result["glyf"][g], "program", None) and result["glyf"][g].program.getBytecode() for g in result.getGlyphOrder()):
            raise ValueError(f"{target.name}: glyph hinting remains")
        for table in ("GSUB", "GPOS"):
            if table in result and result[table].table.FeatureList:
                tags = {r.FeatureTag for r in result[table].table.FeatureList.FeatureRecord}
                if tags - set(FEATURES):
                    raise ValueError(f"{target.name}: unexpected features {tags}")
        faces.append(f'''@font-face {{
  font-family: "DecimaMono";
  src: url("fonts/{target.name}") format("woff2");
  font-display: block;
  unicode-range: {unicode_range(points)};
}}''')
        print(json.dumps({"file": target.name, "bytes": target.stat().st_size,
                          "glyphs": result["maxp"].numGlyphs, "characters": len(actual)}))
    faces.append(END)
    stylesheet = ROOT / "style.css"
    css = stylesheet.read_text()
    if START not in css or END not in css:
        raise ValueError("Missing generated font-face boundaries in style.css")
    before, rest = css.split(START, 1)
    _, after = rest.split(END, 1)
    stylesheet.write_text(before + "\n".join(faces) + after)


if __name__ == "__main__":
    main()
