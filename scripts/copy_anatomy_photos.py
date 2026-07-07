#!/usr/bin/env python3
"""Copy & resize ảnh sách giải phẫu vào public/images/anatomy/book/."""

from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageOps

DEFAULT_INPUT = Path(
    "/Users/prom1/Downloads/thư mục không có tiêu đề 15/thư mục không có tiêu đề 16"
)
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "public/images/anatomy/book"
MANIFEST = Path(__file__).resolve().parent.parent / "public/data/anatomy/pages-manifest.json"


def slugify(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-") or "page"


def main() -> None:
    if not DEFAULT_INPUT.is_dir():
        raise SystemExit(f"Không tìm thấy folder: {DEFAULT_INPUT}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    extensions = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".tif", ".tiff"}
    files = sorted(
        p for p in DEFAULT_INPUT.iterdir() if p.suffix.lower() in extensions
    )

    manifest = []
    for index, file_path in enumerate(files, start=1):
        page_id = f"page-{index:03d}"
        out_path = OUTPUT_DIR / f"{page_id}.jpg"

        with Image.open(file_path) as image:
            rgb = ImageOps.exif_transpose(image.convert("RGB"))
            max_side = max(rgb.size)
            if max_side > 1600:
                scale = 1600 / max_side
                rgb = rgb.resize(
                    (int(rgb.width * scale), int(rgb.height * scale)),
                    Image.Resampling.LANCZOS,
                )
            rgb.save(out_path, quality=85, optimize=True)

        manifest.append(
            {
                "id": page_id,
                "sourceFile": file_path.name,
                "imageUrl": f"/images/anatomy/book/{page_id}.jpg",
                "order": index,
            }
        )
        print(f"[{index}/{len(files)}] {file_path.name} → {page_id}.jpg")

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nĐã copy {len(files)} ảnh → {OUTPUT_DIR}")
    print(f"Manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
