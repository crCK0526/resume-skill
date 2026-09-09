#!/usr/bin/env python3
"""Extract text from PPTX/DOCX and reconstruct a plausible reading order.

Local-only, Python standard library only, never writes to the input file.

Why this script exists
----------------------
PPTX stores text in XML/zip order that often differs from visual order. In
past resume runs, a company name that was visibly present was "missed" because
the raw XML stream order misled the reader. This script reconstructs reading
order from shape geometry (top, then left) so field ownership can be judged
correctly, and offers a keyword-neighborhood mode to decide which entry a field
belongs to.

Usage
-----
    python extract_office_text.py FILE.pptx
    python extract_office_text.py FILE.docx
    python extract_office_text.py FILE.pptx --find "公司,实习" --context 1
    python extract_office_text.py FILE.pptx --json > out.json

Notes
-----
- PDFs are not handled here: they need a PDF library or a text layer tool.
  Re-extract PDF text with an available local tool before relying on it.
- Output lines print only text with geometry; no candidate-specific data is
  written back into the source file.
"""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

EMU_PER_CM = 360000.0


def local(tag: str) -> str:
    return tag.split("}")[-1]


def attr(el, name):
    for k, v in el.attrib.items():
        if local(k) == name:
            return v
    return None


def num_attr(el, name, default=0.0):
    try:
        return float(attr(el, name) or default)
    except ValueError:
        return default


def block_geometry(shape_el):
    """Return (top_cm, left_cm, width_cm, height_cm) for a shape element."""
    xfrm = None
    for d in shape_el.iter():
        if local(d.tag) == "xfrm":
            xfrm = d
            break
    if xfrm is None:
        return (0.0, 0.0, 0.0, 0.0)
    off = next((c for c in xfrm if local(c.tag) == "off"), None)
    ext = next((c for c in xfrm if local(c.tag) == "ext"), None)
    x = num_attr(off, "x") / EMU_PER_CM if off is not None else 0.0
    y = num_attr(off, "y") / EMU_PER_CM if off is not None else 0.0
    w = num_attr(ext, "cx") / EMU_PER_CM if ext is not None else 0.0
    h = num_attr(ext, "cy") / EMU_PER_CM if ext is not None else 0.0
    return (round(y, 2), round(x, 2), round(w, 2), round(h, 2))


def paragraphs_of(shape_el):
    """Return list of paragraphs (each = joined run text) inside a shape."""
    paras = []
    for tx in shape_el.iter():
        if local(tx.tag) != "txBody":
            continue
        for p in tx:
            if local(p.tag) != "p":
                continue
            runs = []
            for node in p.iter():
                if local(node.tag) == "t" and node.text:
                    runs.append(node.text)
            paras.append("".join(runs))
    return [p for p in paras if p.strip()]


def text_blocks(path: Path):
    """Yield list of blocks across all slides of a pptx."""
    slides = sorted(
        n for n in zipfile.ZipFile(path).namelist()
        if n.startswith("ppt/slides/slide") and n.endswith(".xml")
    )
    out = []
    for slide_name in slides:
        root = ET.fromstring(zipfile.ZipFile(path).read(slide_name))
        for el in root.iter():
            if local(el.tag) not in ("sp", "pic", "graphicFrame"):
                continue
            paras = paragraphs_of(el)
            if not paras:
                continue
            y, x, w, h = block_geometry(el)
            for para in paras:
                out.append({"slide": slide_name, "y": y, "x": x,
                            "w": w, "h": h, "text": para})
    out.sort(key=lambda b: (b["y"], b["x"]))
    return out


def docx_blocks(path: Path):
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    body = next((c for c in root if local(c.tag) == "body"), root)
    out = []
    for el in body.iter():
        if local(el.tag) != "p":
            continue
        text = "".join(t.text or "" for t in el.iter() if local(t.tag) == "t")
        if text.strip():
            out.append({"slide": "document", "y": 0.0, "x": 0.0,
                        "w": 0.0, "h": 0.0, "text": text})
    return out


def render(blocks, show_slide=False):
    lines = []
    for b in blocks:
        prefix = b["slide"].split("/")[-1] if show_slide else ""
        label = f"[{prefix} y{b['y']:.2f} x{b['x']:.2f}]" if show_slide else \
            f"[y{b['y']:.2f} x{b['x']:.2f}]"
        lines.append(f"{label} {b['text']}")
    return "\n".join(lines)


def find_matches(blocks, keywords, context):
    kws = [k.strip().lower() for k in keywords if k.strip()]
    hits = []
    for i, b in enumerate(blocks):
        if any(k in b["text"].lower() for k in kws):
            hits.append(i)
    if not hits:
        return "未命中任何关键字（按阅读顺序全文输出见无 --find 模式）\n"
    lines = []
    shown = set()
    for i in hits:
        lo = max(0, i - context)
        hi = min(len(blocks), i + context + 1)
        for j in range(lo, hi):
            if j in shown:
                continue
            shown.add(j)
            mark = ">>" if j == i else "  "
            lines.append(f"{mark} [y{blocks[j]['y']:.2f} x{blocks[j]['x']:.2f}] {blocks[j]['text']}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract reading-order text from PPTX/DOCX")
    ap.add_argument("file", help="path to .pptx or .docx")
    ap.add_argument("--find", default="", help="comma-separated keywords to locate with context")
    ap.add_argument("--context", type=int, default=1, help="context lines around a hit")
    ap.add_argument("--json", action="store_true", help="output JSON instead of text")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"文件不存在: {path}", file=sys.stderr)
        return 2
    suffix = path.suffix.lower()
    if suffix == ".pptx":
        blocks = text_blocks(path)
    elif suffix == ".docx":
        blocks = docx_blocks(path)
    else:
        print("仅支持 .pptx / .docx；PDF 请使用本机可用工具提取文本层", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(blocks, ensure_ascii=False, indent=2))
        return 0
    if args.find:
        print(find_matches(blocks, args.find.split(","), args.context))
        return 0
    print(render(blocks, show_slide=suffix == ".pptx"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
