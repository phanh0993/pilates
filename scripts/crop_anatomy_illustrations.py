#!/usr/bin/env python3
"""Chuẩn bị ảnh trang sách giải phẫu cho quiz: xoay đúng chiều, full trang, làm mờ văn bản."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parent.parent
BOOK_DIR = ROOT / "public/images/anatomy/book"
OUT_DIR = ROOT / "public/images/anatomy/illustrations"
MANIFEST = ROOT / "public/data/anatomy/page-illustrations.json"
MAX_WIDTH = 900
STRIP_H = 28


def estimate_bg(gray: Image.Image) -> int:
    hist = Counter(
        gray.getpixel((x, y))
        for y in range(0, gray.height, 8)
        for x in range(0, gray.width, 8)
    )
    return hist.most_common(1)[0][0]


def peak_score(gray: Image.Image, dark_t: int) -> float:
    w, h = gray.size
    px = gray.load()
    peaks = 0
    for x in range(4, w - 4, 4):
        col = sum(px[x, y] < dark_t for y in range(h))
        left = sum(px[x - 4, y] < dark_t for y in range(h))
        right = sum(px[x + 4, y] < dark_t for y in range(h))
        if col > left and col > right and col > h * 0.08:
            peaks += 1
    return peaks / (w / 4)


def is_paragraph_strip(fg: float, peaks: float, mean: float, bg: int) -> bool:
    """Dải văn bản giải thích (không phải sơ đồ dày hay tiêu đề tối)."""
    if mean < bg - 35 or fg > 0.48:
        return False
    return 0.17 <= fg <= 0.32 and peaks >= 0.068 and mean > 95


def header_edge_scores(image: Image.Image) -> dict[str, float]:
    """Tìm cạnh có dải tiêu đề tối (thanh Emma)."""
    gray = image.convert("L")
    w, h = gray.size
    px = gray.load()

    def dark_ratio(x0: int, y0: int, x1: int, y1: int) -> float:
        total = dark = 0
        for y in range(y0, y1, 4):
            for x in range(x0, x1, 4):
                if px[x, y] < 95:
                    dark += 1
                total += 1
        return dark / total if total else 0.0

    return {
        "top": dark_ratio(0, 0, w, h // 5),
        "bottom": dark_ratio(0, 4 * h // 5, w, h),
        "left": dark_ratio(0, 0, w // 5, h),
        "right": dark_ratio(4 * w // 5, 0, w, h),
    }


def auto_rotate_to_reading_orientation(image: Image.Image) -> Image.Image:
    """Xoay ảnh sao cho thanh tiêu đề nằm phía trên."""
    scores = header_edge_scores(image)
    edge = max(scores, key=scores.get)
    rotations = {
        "top": None,
        "right": Image.ROTATE_90,
        "bottom": Image.ROTATE_180,
        "left": Image.ROTATE_270,
    }
    rotate = rotations[edge]
    return image if rotate is None else image.transpose(rotate)


def trim_scan_margins(image: Image.Image, pad: int = 8) -> Image.Image:
    """Bỏ viền tối của ảnh chụp, giữ nguyên nội dung trang."""
    gray = image.convert("L")
    px = gray.load()
    w, h = gray.size
    minx, miny, maxx, maxy = w, h, 0, 0
    for y in range(h):
        for x in range(w):
            if px[x, y] > 55:
                minx = min(minx, x)
                maxx = max(maxx, x)
                miny = min(miny, y)
                maxy = max(maxy, y)
    if maxx <= minx or maxy <= miny:
        return image
    return image.crop(
        (
            max(0, minx - pad),
            max(0, miny - pad),
            min(w, maxx + pad),
            min(h, maxy + pad),
        )
    )


def blur_paragraph_text(image: Image.Image) -> Image.Image:
    """Làm mờ các dải văn bản giải thích; giữ sơ đồ/ảnh rõ."""
    gray = image.convert("L")
    bg = estimate_bg(gray)
    dark_t = bg - 18
    w, h = image.size
    blurred = image.filter(ImageFilter.GaussianBlur(radius=7))
    result = image.copy()

    for y in range(0, h, STRIP_H):
        y2 = min(h, y + STRIP_H)
        strip = gray.crop((0, y, w, y2))
        px = strip.load()
        sw, sh = strip.size
        fg = sum(px[x, yy] < dark_t for yy in range(sh) for x in range(sw)) / (sw * sh)
        peaks = peak_score(strip, dark_t)
        mean = ImageStat.Stat(strip).mean[0]
        if not is_paragraph_strip(fg, peaks, mean, bg):
            continue
        result.paste(blurred.crop((0, y, w, y2)), (0, y))

    return result


def prepare_page(path: Path) -> Image.Image:
    with Image.open(path) as raw:
        image = ImageOps.exif_transpose(raw.convert("RGB"))

    image = auto_rotate_to_reading_orientation(image)
    image = trim_scan_margins(image)
    image = blur_paragraph_text(image)

    if image.width > MAX_WIDTH:
        ratio = MAX_WIDTH / image.width
        image = image.resize(
            (MAX_WIDTH, int(image.height * ratio)),
            Image.Resampling.LANCZOS,
        )
    return image


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, str] = {}

    for page_path in sorted(BOOK_DIR.glob("page-*.jpg")):
        page_num = int(page_path.stem.split("-")[1])
        prepared = prepare_page(page_path)
        out_name = f"page-{page_num:03d}.jpg"
        prepared.save(OUT_DIR / out_name, quality=88, optimize=True)
        manifest[str(page_num)] = f"/images/anatomy/illustrations/{out_name}"

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Prepared {len(manifest)} quiz pages → {OUT_DIR}")
    print(f"Manifest → {MANIFEST}")


if __name__ == "__main__":
    main()
