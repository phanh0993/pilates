#!/usr/bin/env python3
"""Crop vùng minh họa từ trang sách giải phẫu → ảnh hiển thị trong câu hỏi quiz."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parent.parent
BOOK_DIR = ROOT / "public/images/anatomy/book"
OUT_DIR = ROOT / "public/images/anatomy/illustrations"
MANIFEST = ROOT / "public/data/anatomy/page-illustrations.json"
MAX_WIDTH = 900


def crop_illustration(path: Path) -> Image.Image | None:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    y1, y2 = int(h * 0.10), int(h * 0.88)
    region = im.crop((int(w * 0.04), y1, int(w * 0.96), y2))
    rw, rh = region.size
    gray = region.convert("L")
    px = gray.load()
    minx, miny, maxx, maxy = rw, rh, 0, 0
    for y in range(rh):
        for x in range(rw):
            if px[x, y] < 230:
                minx = min(minx, x)
                maxx = max(maxx, x)
                miny = min(miny, y)
                maxy = max(maxy, y)
    if maxx <= minx:
        return None
    pad = 10
    crop = region.crop(
        (
            max(0, minx - pad),
            max(0, miny - pad),
            min(rw, maxx + pad),
            min(rh, maxy + pad),
        )
    )
    cw, ch = crop.size
    center = crop.crop((cw // 4, ch // 4, 3 * cw // 4, 3 * ch // 4)).convert("L")
    if ImageStat.Stat(center).stddev[0] < 20:
        return None
    if crop.width > MAX_WIDTH:
        ratio = MAX_WIDTH / crop.width
        crop = crop.resize(
            (MAX_WIDTH, int(crop.height * ratio)),
            Image.Resampling.LANCZOS,
        )
    return crop


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, str] = {}

    for page_path in sorted(BOOK_DIR.glob("page-*.jpg")):
        page_num = int(page_path.stem.split("-")[1])
        crop = crop_illustration(page_path)
        if crop is None:
            continue
        out_name = f"page-{page_num:03d}.jpg"
        crop.save(OUT_DIR / out_name, quality=88, optimize=True)
        manifest[str(page_num)] = f"/images/anatomy/illustrations/{out_name}"

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Cropped {len(manifest)} illustrations → {OUT_DIR}")
    print(f"Manifest → {MANIFEST}")


if __name__ == "__main__":
    main()
