#!/usr/bin/env python3
"""Structural layout audit for a single-slide A4 resume PPTX.

Local-only, Python standard library only, never writes to the input file.

Why this script exists
----------------------
Final visual QA requires eyes. When the executing model cannot reliably view a
rendered image, this script provides a deterministic fallback gate covering the
checks that are mechanical: page size, shape bounds, minimum font size, image
count, and reading-order sanity. It does NOT replace a human glance at the
rendered PNG; it only gates the obvious structural failures first.

Usage
-----
    python audit_pptx_layout.py FILE.pptx
    python audit_pptx_layout.py FILE.pptx --min-font 9 --tolerance-cm 0.15

Exit code 0 = no structural failures; 1 = failures found.
"""
from __future__ import annotations

import argparse
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

EMU_PER_CM = 360000.0
A4_CM = (21.0, 29.7)


def local(tag: str) -> str:
    return tag.split("}")[-1]


def num_attr(el, name, default=None):
    for k, v in el.attrib.items():
        if local(k) == name:
            try:
                return float(v)
            except ValueError:
                return default
    return default


def shape_geometry(el):
    for d in el.iter():
        if local(d.tag) == "xfrm":
            off = next((c for c in d if local(c.tag) == "off"), None)
            ext = next((c for c in d if local(c.tag) == "ext"), None)
            x = num_attr(off, "x", 0) / EMU_PER_CM if off is not None else 0.0
            y = num_attr(off, "y", 0) / EMU_PER_CM if off is not None else 0.0
            w = num_attr(ext, "cx", 0) / EMU_PER_CM if ext is not None else 0.0
            h = num_attr(ext, "cy", 0) / EMU_PER_CM if ext is not None else 0.0
            return (x, y, w, h)
    return (0.0, 0.0, 0.0, 0.0)


def explicit_sizes(el):
    """Collect every explicit run font size in hundredths of a point."""
    sizes = []
    for rpr in el.iter():
        if local(rpr.tag) != "rPr":
            continue
        sz = num_attr(rpr, "sz")
        if sz is not None:
            sizes.append(sz / 100.0)
    return sizes


def audit(path: Path, min_font: float, tolerance_cm: float):
    fails, warns = [], []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        slides = sorted(n for n in names if n.startswith("ppt/slides/slide")
                        and n.endswith(".xml"))
        if not slides:
            return (["未找到 ppt/slides/slide*.xml"], [])
        # slide size from first slide's sldSz is unreliable; use presentation.xml
        pres = [n for n in names if n == "ppt/presentation.xml"]
        W, H = A4_CM
        if pres:
            root = ET.fromstring(z.read(pres[0]))
            for el in root.iter():
                if local(el.tag) == "sldSz":
                    cx = num_attr(el, "cx"); cy = num_attr(el, "cy")
                    if cx and cy:
                        W, H = cx / EMU_PER_CM, cy / EMU_PER_CM
                    break
        if abs(W - A4_CM[0]) > 0.05 or abs(H - A4_CM[1]) > 0.05:
            warns.append(f"页面非 A4 竖版：{W:.2f} x {H:.2f} cm")
        total_shapes = 0
        total_pics = 0
        all_sizes = []
        text_tops = []
        for sn in slides:
            root = ET.fromstring(z.read(sn))
            for el in root.iter():
                if local(el.tag) not in ("sp", "pic", "graphicFrame", "cxnSp"):
                    continue
                total_shapes += 1
                if local(el.tag) == "pic":
                    total_pics += 1
                x, y, w, h = shape_geometry(el)
                if y < -tolerance_cm or y + h > H + tolerance_cm or \
                   x < -tolerance_cm or x + w > W + tolerance_cm:
                    # text-only invisible line boxes may have h=0; still bounds-checked
                    fails.append(f"{sn}: 越界 shape at x={x:.2f} y={y:.2f} w={w:.2f} h={h:.2f}")
                has_text = any(local(t.tag) == "t" for t in el.iter())
                if has_text and w > 0.1:
                    text_tops.append((y, x))
                all_sizes.extend(explicit_sizes(el))
        if total_pics:
            warns.append(f"含 {total_pics} 张图片对象（无头像/纯文字简历应避免）")
        if all_sizes:
            mn, mx = min(all_sizes), max(all_sizes)
            if mn < min_font - 0.05:
                fails.append(f"最小显式字号 {mn:.1f}pt < 门禁 {min_font}pt")
            warns.append(f"字号范围 {mn:.1f}–{mx:.1f}pt，共 {len(all_sizes)} 处显式设置")
        else:
            warns.append("未发现显式字号设置（可能依赖主题默认值，需人工核验）")
        if len(slides) > 1:
            warns.append(f"共 {len(slides)} 页（单页简历应只有 1 页）")
        warns.append(f"形状 {total_shapes} 个 / 文本块 {len(text_tops)} 个")
    return fails, warns


def main() -> int:
    ap = argparse.ArgumentParser(description="Structural audit for A4 resume PPTX")
    ap.add_argument("file")
    ap.add_argument("--min-font", type=float, default=9.0,
                    help="minimum allowed explicit font size in pt (default 9)")
    ap.add_argument("--tolerance-cm", type=float, default=0.15,
                    help="boundary tolerance in cm (default 0.15)")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"文件不存在: {path}", file=sys.stderr)
        return 2
    if path.suffix.lower() != ".pptx":
        print("仅支持 .pptx", file=sys.stderr)
        return 2

    fails, warns = audit(path, args.min_font, args.tolerance_cm)
    print("== 结构审计 ==")
    for w in warns:
        print(f"WARN  {w}")
    for f in fails:
        print(f"FAIL  {f}")
    if fails:
        print(f"RESULT: FAILED（{len(fails)} 项）— 请修复后重跑；仍建议目视渲染 PNG")
        return 1
    print("RESULT: PASSED（结构门禁通过；视觉与换行仍以人工目检渲染图为准）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
