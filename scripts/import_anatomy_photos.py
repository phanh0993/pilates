#!/usr/bin/env python3
"""Đọc ảnh trang sách giải phẫu → draft JSON (OCR khái niệm + nhãn số trên sơ đồ)."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pytesseract
from PIL import Image, ImageOps

LABEL_RE = re.compile(r"^(\d{1,2})[\.\):\-]\s*(.+)$", re.MULTILINE)
TERM_DEF_RE = re.compile(
    r"^([A-Z][A-Za-z\s\-/]+?)\s*[:\-–—]\s*(.+)$",
    re.MULTILINE,
)
VI_TERM_RE = re.compile(r"\(([^)]+)\)")


def ocr_image(path: Path) -> str:
    with Image.open(path) as image:
        rgb = ImageOps.exif_transpose(image.convert("RGB"))
        max_side = max(rgb.size)
        if max_side > 1800:
            scale = 1800 / max_side
            rgb = rgb.resize(
                (int(rgb.width * scale), int(rgb.height * scale)),
                Image.Resampling.LANCZOS,
            )
        return pytesseract.image_to_string(rgb, lang="eng")


def classify_page(text: str) -> str:
    labels = LABEL_RE.findall(text)
    terms = TERM_DEF_RE.findall(text)
    if len(labels) >= 2 and len(terms) >= 1:
        return "mixed"
    if len(labels) >= 2:
        return "diagram"
    if len(terms) >= 1:
        return "text"
    return "unknown"


def extract_labels(text: str) -> list[dict]:
    labels: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        match = LABEL_RE.match(line)
        if match:
            labels.append({"number": int(match.group(1)), "text": match.group(2).strip()})
    return labels


def extract_terms(text: str) -> list[str]:
    terms: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or len(line) < 4:
            continue
        match = TERM_DEF_RE.match(line)
        if match:
            terms.append(match.group(1).strip())
    return terms


def main() -> None:
    parser = argparse.ArgumentParser(description="Import anatomy book photos")
    parser.add_argument("--input", required=True, help="Folder chứa ảnh JPG/PNG")
    parser.add_argument(
        "--output",
        default="public/data/anatomy/import-draft.json",
        help="File JSON output",
    )
    args = parser.parse_args()

    input_dir = Path(args.input)
    if not input_dir.is_dir():
        raise SystemExit(f"Folder không tồn tại: {input_dir}")

    extensions = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
    files = sorted(
        p for p in input_dir.iterdir() if p.suffix.lower() in extensions
    )

    if not files:
        raise SystemExit(f"Không có ảnh trong {input_dir}")

    drafts = []
    all_terms: set[str] = set()

    for index, file_path in enumerate(files, start=1):
        text = ocr_image(file_path)
        page_type = classify_page(text)
        labels = extract_labels(text)
        terms = extract_terms(text)
        all_terms.update(terms)

        drafts.append(
            {
                "sourceFile": file_path.name,
                "pageIndex": index,
                "pageType": page_type,
                "rawText": text[:2000],
                "detectedTerms": terms,
                "detectedLabels": labels,
            }
        )
        print(f"[{index}/{len(files)}] {file_path.name} → {page_type} "
              f"({len(terms)} terms, {len(labels)} labels)")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            {
                "pages": drafts,
                "summary": {
                    "totalPages": len(files),
                    "uniqueTerms": sorted(all_terms),
                },
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"\nĐã ghi {output_path}")
    print("Tiếp theo: chỉnh concepts.json + dùng /admin/anatomy để gán vị trí sơ đồ.")


if __name__ == "__main__":
    main()
