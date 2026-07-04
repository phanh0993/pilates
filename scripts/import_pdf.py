#!/usr/bin/env python3
"""Import scanned Pilates PDF into app data: grid crop + TTS audio."""

from __future__ import annotations

import asyncio
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import edge_tts
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
DATA_DIR = PUBLIC / "data"
IMG_DIR = PUBLIC / "images"
AUDIO_DIR = PUBLIC / "audio"

PDF_PATH = Path(
    "/Users/prom1/Downloads/thư mục không có tiêu đề 16/Tài liệu được quét.pdf"
)

RENDER_SCALE = 2.0


@dataclass
class PageLayout:
    page: int
    steps: list[int]
    layout: str
    captions: list[str]


@dataclass
class ExerciseSeed:
    id: str
    name_en: str
    name_vi: str
    category: str
    pack_id: str
    prep: str
    steps: str
    reps: str
    pages: list[PageLayout]


EXERCISES: list[ExerciseSeed] = [
    ExerciseSeed(
        id="roll-down",
        name_en="ROLL-DOWN",
        name_vi="Cuộn xuống",
        category="ROLL-DOWN BAR (Thanh cuộn xuống)",
        pack_id="roll-down-bar",
        prep="Ngồi hướng mặt về phía thanh roll-down, lưng-hông trung tính. Hai chân duỗi thẳng, úp lòng bàn chân vào hai bên cột. Nắm hai tay vào thanh, cánh tay thẳng. Bả vai ổn định.",
        steps="Hít vào: chuẩn bị. Thở ra: duy trì bả vai ổn định, bắt đầu đổ hông về sau, cuộn lần lượt từng đốt sống xuống đệm. Hít vào: ổn định bả vai trên đệm, đưa cột sống về trung tính. Thở ra: gập khuỷu tay, kéo gậy về phía ngực. Hít vào: ổn định bả vai, duỗi khuỷu tay từ từ. Thở ra: nâng đầu khỏi đệm và cuộn lên vị trí ngồi. Hít vào: cuộn từ hông lên vị trí ban đầu.",
        reps="10 lần",
        pages=[
            PageLayout(1, [1, 2], "2col", ["Tư thế chuẩn bị", "Cuộn lưng về sau"]),
            PageLayout(2, [3, 4, 5, 6, 7], "3+2", [
                "Nằm xuống giường",
                "Gập khuỷu tay",
                "Bắt đầu cuộn lên",
                "Úp người về phía trước",
                "Cuộn thẳng lưng",
            ]),
        ],
    ),
    ExerciseSeed(
        id="roll-down-with-back-extension",
        name_en="ROLL-DOWN WITH BACK EXTENSION",
        name_vi="Cuộn xuống kèm duỗi lưng",
        category="ROLL-DOWN BAR (Thanh cuộn xuống)",
        pack_id="roll-down-bar",
        prep="Ngồi hướng mặt về phía thanh roll-down, lưng-hông trung tính. Hai chân duỗi thẳng, úp lòng bàn chân vào hai bên cột. Nắm hai tay vào thanh, cánh tay thẳng.",
        steps="Thực hiện roll-down, sau đó gập khuỷu tay kéo gậy về ngực đồng thời duỗi cột sống nâng lưng khỏi thảm. Duỗi khuỷu tay và hạ lưng xuống đệm. Cuộn lên trở lại vị trí ngồi.",
        reps="10 lần",
        pages=[PageLayout(3, [1], "1", ["Gập khuỷu tay và duỗi cột sống"])],
    ),
    ExerciseSeed(
        id="side-bend",
        name_en="SIDE BEND",
        name_vi="Gập người sang bên",
        category="ROLL-DOWN BAR (Thanh cuộn xuống)",
        pack_id="roll-down-bar",
        prep="Nằm nghiêng trên giường, cột sống trung tính. Tay trên duỗi thẳng nắm vào tâm gậy, tay dưới làm gối đầu. Hai chân thẳng.",
        steps="Hít vào: ổn định lưng-hông, vươn dài người và bắt đầu gập người lên. Thở ra: gập khuỷu tay phía trên. Hít vào: duỗi khuỷu tay hạ người xuống. Thở ra: hạ người và tay xuống giường.",
        reps="10 lần",
        pages=[
            PageLayout(4, [1], "1", ["Tư thế chuẩn bị"]),
            PageLayout(5, [2, 3], "2col", ["Nâng thân trên lên", "Gập khuỷu tay, gập eo"]),
        ],
    ),
    ExerciseSeed(
        id="lat-press",
        name_en="LAT PRESS",
        name_vi="Ấn cơ lưng rộng",
        category="ROLL-DOWN BAR (Thanh cuộn xuống)",
        pack_id="roll-down-bar",
        prep="Chống hai gối trên giường, quay mặt về phía thanh, cột sống trung tính. Hai tay đặt lên gậy, cánh tay rộng bằng vai, duỗi thẳng.",
        steps="Hít vào: chuẩn bị. Thở ra: nhấn gậy xuống, giữ cánh tay thẳng. Hít vào: đưa thanh trở lại, kiểm soát lò xo.",
        reps="10 lần",
        pages=[PageLayout(6, [1, 2], "2col", ["Tư thế chuẩn bị", "Hạ cánh tay"])],
    ),
    ExerciseSeed(
        id="press-down-with-triceps",
        name_en="PRESS DOWN WITH TRICEPS",
        name_vi="Đẩy xuống với cơ tay sau",
        category="ROLL-DOWN BAR (Thanh cuộn xuống)",
        pack_id="roll-down-bar",
        prep="Chống hai gối trên giường, quay mặt về phía thanh, cột sống trung tính. Hai tay nắm vào gậy, cánh tay rộng bằng vai.",
        steps="Hít vào: gập khuỷu tay về phía thân. Thở ra: duỗi khuỷu tay để kéo đẩy xuống. Hít vào: gập khuỷu tay lên. Thở ra: đưa thanh trở lại.",
        reps="10 lần",
        pages=[
            PageLayout(7, [1], "1", ["Tư thế chuẩn bị"]),
            PageLayout(8, [2, 3], "2col", ["Gập khuỷu tay", "Duỗi khuỷu tay"]),
        ],
    ),
    ExerciseSeed(
        id="thigh-stretch",
        name_en="THIGH STRETCH",
        name_vi="Duỗi cơ đùi",
        category="ROLL-DOWN BAR (Thanh cuộn xuống)",
        pack_id="roll-down-bar",
        prep="Chống hai gối trên giường, quay mặt về phía thanh, cột sống trung tính. Hai tay nắm vào gậy, cánh tay rộng bằng vai.",
        steps="Hít vào: chuẩn bị. Thở ra: gập khối ra sau cho phép lò xo kéo giãn. Hít vào: tiếp tục hạ tay. Thở ra: nâng tay lên. Hít vào: nâng người về vị trí ban đầu.",
        reps="10 lần",
        pages=[
            PageLayout(9, [1], "1", ["Tư thế chuẩn bị"]),
            PageLayout(10, [2, 3], "2col", ["Gập gối ra sau", "Hạ tay kéo lò xo"]),
        ],
    ),
    ExerciseSeed(
        id="ballet-stretch-kneeling",
        name_en="BALLET STRETCH KNEELING",
        name_vi="Duỗi Ballet Quỳ",
        category="PUSH-THRU BAR: LÒ XO Ở TRÊN",
        pack_id="push-thru-bar",
        prep="Chống gối trên giường, hướng mặt sang bên, cột sống trung tính. Một chân làm trụ, chân còn lại duỗi thẳng đặt lên push-thru.",
        steps="Hít vào: chuẩn bị. Thở ra: duy trì lưng-hông trung tính, trượt người và thanh sang bên. Hít vào: trượt người và thanh về.",
        reps="10 lần sau đó quay người đổi bên",
        pages=[PageLayout(11, [1, 2], "2col", ["Tư thế chuẩn bị", "Trượt người sang bên"])],
    ),
    ExerciseSeed(
        id="scapular-isolation",
        name_en="SCAPULAR ISOLATION",
        name_vi="Cô lập và vận động xương bả vai",
        category="PUSH-THRU BAR: LÒ XO Ở TRÊN",
        pack_id="push-thru-bar",
        prep="Nằm ngửa dọc theo giường, đầu hướng về push-thru, lưng-hông trung tính. Tay nắm thanh, cánh tay rộng bằng vai. Gập gối, úp lòng bàn chân trên giường.",
        steps="Hít vào: nâng hai bả vai khỏi giường, kéo dài cánh tay lên. Thở ra: khép hai vai vào nhau, thanh đi xuống. Hít vào: tách hai bả vai. Thở ra: đưa vai về vị trí ban đầu.",
        reps="10 lần",
        pages=[PageLayout(12, [1, 2, 3], "3col", ["Tư thế chuẩn bị", "Tách bả vai", "Khép bả vai"])],
    ),
    ExerciseSeed(
        id="push-thru-on-back",
        name_en="PUSH-THRU ON BACK",
        name_vi="Đẩy thanh khi nằm ngửa",
        category="PUSH-THRU BAR: LÒ XO Ở TRÊN",
        pack_id="push-thru-bar",
        prep="Nằm ngửa trên giường, đầu hướng về push-thru, cột sống trung tính. Gập gối, úp lòng bàn chân. Hai tay nắm thanh vươn qua đầu.",
        steps="Hít vào: gập khuỷu tay sang hai bên đưa thanh về trước mặt. Thở ra: duỗi thẳng hai tay nâng thanh lên trần nhà. Hít vào: gập khuỷu tay đưa thanh về trước mặt. Thở ra: duỗi khuỷu tay đưa thanh qua đầu.",
        reps="10 lần",
        pages=[
            PageLayout(13, [1], "1", ["Tư thế chuẩn bị"]),
            PageLayout(14, [2, 3], "2col", ["Gập khuỷu tay sang bên", "Duỗi khuỷu tay"]),
        ],
    ),
    ExerciseSeed(
        id="push-thru-on-back-with-roll-up",
        name_en="PUSH-THRU ON BACK WITH ROLL-UP",
        name_vi="Đẩy qua lưng có cuộn lên",
        category="PUSH-THRU BAR: LÒ XO Ở TRÊN",
        pack_id="push-thru-bar",
        prep="Nằm ngửa trên giường, đầu hướng về push-thru, cột sống trung tính. Gập gối, úp lòng bàn chân. Hai tay nắm thanh vươn qua đầu.",
        steps="Gập khuỷu tay đưa thanh về trước mặt, cuộn từng đốt sống lên vị trí ngồi thẳng lưng, rồi cuộn xuống trở lại.",
        reps="10 lần",
        pages=[PageLayout(15, [1, 2, 3, 4], "2x2", [
            "Tư thế chuẩn bị",
            "Gập khuỷu tay sang bên",
            "Cuộn người lên",
            "Ngồi thẳng lưng",
        ])],
    ),
    ExerciseSeed(
        id="teaser-prep",
        name_en="TEASER PREP",
        name_vi="Khởi động",
        category="PUSH-THRU BAR: LÒ XO Ở TRÊN",
        pack_id="push-thru-bar",
        prep="Nằm ngửa trên giường, đầu hướng về push-thru, cột sống trung tính. Hai chân khép sát và duỗi thẳng. Hai tay nắm thanh vươn qua đầu.",
        steps="Gập gối và khuỷu tay đưa thanh về trước mặt, cuộn lên vị trí chữ V với chân duỗi chéo, rồi cuộn xuống trở lại vị trí ban đầu.",
        reps="10 lần",
        pages=[PageLayout(16, [1, 2, 3, 4], "2x2", [
            "Tư thế chuẩn bị",
            "Gập gối, gập khuỷu tay",
            "Nâng chân cuộn lưng lên",
            "Thẳng lưng, thẳng chân tạo chữ V",
        ])],
    ),
]


def render_page(doc: fitz.Document, page_index: int) -> Image.Image:
    page = doc[page_index]
    matrix = fitz.Matrix(RENDER_SCALE, RENDER_SCALE)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def photo_region(image: Image.Image) -> tuple[int, int, int, int]:
    w, h = image.size
    return (int(w * 0.04), int(h * 0.42), int(w * 0.96), int(h * 0.93))


def split_region(region: Image.Image, layout: str) -> list[Image.Image]:
    w, h = region.size
    if layout == "1":
        return [region]
    if layout == "2col":
        mid = w // 2
        return [region.crop((0, 0, mid - 4, h)), region.crop((mid + 4, 0, w, h))]
    if layout == "3col":
        third = w // 3
        return [
            region.crop((0, 0, third - 3, h)),
            region.crop((third + 3, 0, 2 * third - 3, h)),
            region.crop((2 * third + 3, 0, w, h)),
        ]
    if layout == "2x2":
        mid_x, mid_y = w // 2, h // 2
        return [
            region.crop((0, 0, mid_x - 3, mid_y - 3)),
            region.crop((mid_x + 3, 0, w, mid_y - 3)),
            region.crop((0, mid_y + 3, mid_x - 3, h)),
            region.crop((mid_x + 3, mid_y + 3, w, h)),
        ]
    if layout == "3+2":
        top_h = int(h * 0.56)
        bottom_h = h - top_h
        third = w // 3
        top = [
            region.crop((0, 0, third - 3, top_h)),
            region.crop((third + 3, 0, 2 * third - 3, top_h)),
            region.crop((2 * third + 3, 0, w, top_h)),
        ]
        half = w // 2
        bottom = [
            region.crop((int(w * 0.08), top_h + 4, half - 3, h)),
            region.crop((half + 3, top_h + 4, int(w * 0.92), h)),
        ]
        return top + bottom
    raise ValueError(f"Unknown layout: {layout}")


def resize_image(image: Image.Image, max_width: int = 900) -> Image.Image:
    if image.width <= max_width:
        return image
    ratio = max_width / image.width
    return image.resize((max_width, int(image.height * ratio)), Image.Resampling.LANCZOS)


async def generate_audio(text: str, output_path: Path) -> None:
    communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural", rate="-12%")
    await communicate.save(str(output_path))


async def main() -> None:
    if not PDF_PATH.exists():
        raise SystemExit(f"PDF not found: {PDF_PATH}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(PDF_PATH)
    page_cache: dict[int, Image.Image] = {}

    exercises_out: list[dict] = []
    audio_jobs = []

    for seed in EXERCISES:
        ex_dir = IMG_DIR / seed.id
        ex_dir.mkdir(parents=True, exist_ok=True)
        images: list[dict] = []

        for layout in seed.pages:
            if layout.page not in page_cache:
                page_cache[layout.page] = render_page(doc, layout.page - 1)

            page_image = page_cache[layout.page]
            x1, y1, x2, y2 = photo_region(page_image)
            region = page_image.crop((x1, y1, x2, y2))
            crops = split_region(region, layout.layout)

            if len(crops) != len(layout.steps):
                raise SystemExit(
                    f"Layout mismatch on page {layout.page}: "
                    f"expected {len(layout.steps)} crops, got {len(crops)}"
                )

            for step, caption, crop in zip(layout.steps, layout.captions, crops, strict=True):
                filename = f"{step}.jpg"
                resized = resize_image(crop)
                resized.save(ex_dir / filename, quality=88, optimize=True)
                images.append(
                    {
                        "step": step,
                        "caption": caption,
                        "url": f"/images/{seed.id}/{filename}",
                    }
                )

        images.sort(key=lambda item: item["step"])
        audio_path = AUDIO_DIR / f"{seed.id}.mp3"
        audio_jobs.append(generate_audio(seed.name_en, audio_path))

        exercises_out.append(
            {
                "id": seed.id,
                "nameEn": seed.name_en,
                "nameVi": seed.name_vi,
                "category": seed.category,
                "packId": seed.pack_id,
                "prep": seed.prep,
                "steps": seed.steps,
                "reps": seed.reps,
                "images": images,
                "audioUrl": f"/audio/{seed.id}.mp3",
            }
        )

    await asyncio.gather(*audio_jobs)

    packs = [
        {
            "id": "roll-down-bar",
            "name": "Roll-down Bar",
            "description": "6 động tác với thanh roll-down",
            "exerciseIds": [e["id"] for e in exercises_out if e["packId"] == "roll-down-bar"],
        },
        {
            "id": "push-thru-bar",
            "name": "Push-thru Bar",
            "description": "5 động tác với thanh push-thru",
            "exerciseIds": [e["id"] for e in exercises_out if e["packId"] == "push-thru-bar"],
        },
    ]

    (DATA_DIR / "exercises.json").write_text(
        json.dumps(exercises_out, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (DATA_DIR / "packs.json").write_text(
        json.dumps(packs, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Imported {len(exercises_out)} exercises")
    for ex in exercises_out:
        print(f"  - {ex['nameEn']} ({len(ex['images'])} images)")


if __name__ == "__main__":
    asyncio.run(main())
