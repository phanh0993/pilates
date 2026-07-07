#!/usr/bin/env python3
"""Import scanned Pilates Mat PDFs into app data: grid crop + TTS audio."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from pathlib import Path

import edge_tts
import fitz
from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
DATA_DIR = PUBLIC / "data"
IMG_DIR = PUBLIC / "images"
AUDIO_DIR = PUBLIC / "audio"

PDFS = {
    "mat1": Path("/Users/prom1/Downloads/Tài liệu được quét.pdf"),
    "mat2": Path("/Users/prom1/Downloads/Tài liệu được quét 2.pdf"),
    "mat3": Path("/Users/prom1/Downloads/Tài liệu được quét 3.pdf"),
}

RENDER_SCALE = 2.0
WARMUP = "MAT (Thảm) — Khởi động"
MAIN = "MAT (Thảm) — Bài chính"


@dataclass
class PageLayout:
    pdf: str
    page: int
    steps: list[int]
    layout: str
    captions: list[str]
    region: tuple[float, float, float, float] | None = None
    boxes: list[tuple[float, float, float, float]] | None = None


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


def P(
    pdf: str,
    page: int,
    layout: str,
    captions: list[str],
    start: int = 1,
    region: tuple[float, float, float, float] | None = None,
    boxes: list[tuple[float, float, float, float]] | None = None,
) -> PageLayout:
    steps = list(range(start, start + len(captions)))
    return PageLayout(pdf, page, steps, layout, captions, region, boxes)


def ex(
    id_: str,
    en: str,
    vi: str,
    cat: str,
    pack: str,
    prep: str,
    steps: str,
    reps: str,
    *pages: PageLayout,
) -> ExerciseSeed:
    return ExerciseSeed(id_, en, vi, cat, pack, prep, steps, reps, list(pages))


MAT_EXERCISES: list[ExerciseSeed] = [
    ex(
        "mat-breathing",
        "BREATHING",
        "Hít thở",
        WARMUP,
        "mat-warmup",
        "Ngồi khoanh chân, lưng-hông trung tính. Một tay trên ngực, một tay trên khung sườn.",
        "Hít: mở căng lồng ngực ra bốn phía, cảm nhận khung sườn mở rộng. Thở: đóng lồng ngực, thu khung sườn lại.",
        "5–10 lần",
        P("mat1", 1, "3col", [
            "Hơi thở về phía trước và sang hai bên",
            "Tư thế chuẩn bị cho hình 3",
            "Hơi thở ở phía sau",
        ], region=(0.04, 0.38, 0.96, 0.52)),
    ),
    ex(
        "mat-leg-lift",
        "LEG LIFT",
        "Nâng chân",
        WARMUP,
        "mat-warmup",
        "Nằm ngửa, lưng-hông trung tính.",
        "Thở: siết bụng, nâng một chân lên table-top. Hít: hạ chân. Thở: đổi chân.",
        "5–10 lần",
        P("mat1", 1, "3col", [
            "Vị trí chuẩn bị",
            "Nâng một chân lên",
            "Hạ chân để đổi bên",
        ], region=(0.04, 0.62, 0.96, 0.76)),
    ),
    ex(
        "mat-leg-slide",
        "LEG SLIDE",
        "Trượt chân",
        WARMUP,
        "mat-warmup",
        "Nằm ngửa, lưng-hông trung tính. Hai tay cạnh thân, lòng bàn tay úp. Gập gối, chân mở bằng hông. Siết bụng, bả vai ổn định.",
        "Hít: thả lỏng khớp hông, mở một chân sang bên, duỗi gối trượt má chân ra xa mông. Thở: xoay chân về neutral, gập gối trượt lòng bàn chân về.",
        "3 lần mỗi chân",
        P("mat1", 2, "boxes", [
            "Tư thế chuẩn bị",
            "Bắt đầu nâng 1 chân",
            "Trượt gót chân ra xa xương ngồi",
            "Trượt gót về",
            "Đưa chân về vị trí ban đầu",
        ], boxes=[
            (0.085, 0.273, 0.412, 0.504),
            (0.210, 0.331, 0.501, 0.512),
            (0.503, 0.270, 0.822, 0.503),
            (0.733, 0.325, 0.915, 0.506),
            (0.070, 0.483, 0.433, 0.699),
        ]),
    ),
    ex(
        "mat-spinal-rotation",
        "SPINAL ROTATION",
        "Xoay cột sống",
        WARMUP,
        "mat-warmup",
        "Nằm nghiêng, gối co xếp chồng, tay duỗi phía trước ngực.",
        "Thở: xoay người ra sau, mở ngực hướng trần, tay mở ra sau. Hít: duy trì. Thở: xoay về, khép tay.",
        "6–8 lần mỗi bên",
        P("mat1", 3, "2x2", [
            "Tư thế chuẩn bị",
            "Nâng 1 tay lên",
            "Xoay người mở tay ra sau",
            "Trở về",
        ]),
    ),
    ex(
        "mat-hip-rolls",
        "HIP ROLLS",
        "Cuộn hông",
        WARMUP,
        "mat-warmup",
        "Nằm ngửa, gối co, chân úp sàn.",
        "Hít: mở căng lồng ngực. Thở: cuộn tuần tự từ mông lên ngực qua imprint lên cây cầu. Hít: duy trì, mở khung sườn. Thở: cuộn từ ngực xuống, lưng-hông trung tính.",
        "5–8 lần",
        P("mat1", 4, "2+1L", [
            "Vị trí ban đầu",
            "Cuộn lưng qua imprint lên cây cầu",
            "Cuộn trở về",
        ]),
    ),
    ex(
        "mat-arm-circle",
        "ARM CIRCLE",
        "Xoay vòng cánh tay",
        WARMUP,
        "mat-warmup",
        "Nằm ngửa, lưng-hông trung tính. Hai tay nâng vuông góc lên trần, mở rộng bằng vai.",
        "Hít: đưa tay qua đầu, giữ kết nối cơ bụng, bả vai ổn định trên thảm. Thở: mở tay sang hai bên, vẽ vòng tròn qua hông, nâng lên trần. Vẽ ngược lại.",
        "5–8 lần mỗi bên",
        P("mat1", 5, "2+1", [
            "Vị trí chuẩn bị",
            "Tay qua đầu",
            "Vẽ vòng tròn",
        ]),
    ),
    ex(
        "mat-twist",
        "TWIST",
        "Xoay người",
        WARMUP,
        "mat-warmup",
        "Ngồi khoanh chân, lưng-hông trung tính. Khuỷu tay chéo trước ngực.",
        "Thở: xoay người sang một bên. Hít: xoay về giữa. Thở: xoay bên còn lại.",
        "6–8 lần",
        P("mat1", 6, "2x2", [
            "Vị trí bắt đầu",
            "Xoay một bên",
            "Xoay về giữa",
            "Xoay bên còn lại",
        ]),
    ),
    ex(
        "mat-side-bend-sitting",
        "SIDE BEND SITTING",
        "Ngồi gập bên",
        WARMUP,
        "mat-warmup",
        "Ngồi khoanh chân, lưng-hông trung tính. Hai tay duỗi cạnh thân.",
        "Hít: nâng một tay lên trần. Thở: nghiêng bên đối diện tay nâng. Hít: trở về. Thở: hạ tay. Đổi bên.",
        "6–8 lần",
        P("mat1", 7, "3x2+1", [
            "Vị trí bắt đầu",
            "Nâng một tay lên trần",
            "Nghiêng bên",
            "Trở về",
            "Hạ tay",
            "Nâng đối tay",
            "Nghiêng bên còn lại",
        ]),
    ),
    ex(
        "mat-scapula-isolation",
        "SCAPULA ISOLATION",
        "Cử động cô lập bả vai",
        WARMUP,
        "mat-warmup",
        "Ngồi khoanh chân, hai tay duỗi thẳng phía trước ngực.",
        "Thở: ép bả vai xuống. Hít: đưa bả vai về trung lập. Thở: tách hai bả vai xa nhau.",
        "6–8 lần",
        P("mat1", 8, "2x2", [
            "Vị trí chuẩn bị",
            "Ép bả vai",
            "Đưa bả vai về trung lập",
            "Tách hai bả vai xa nhau",
        ]),
    ),
    ex(
        "mat-half-roll-back",
        "HALF ROLL BACK",
        "Cuộn nửa người về sau",
        WARMUP,
        "mat-warmup",
        "Ngồi khoanh chân, lưng-hông trung tính, tay ôm đầu gối.",
        "Hít: chuẩn bị. Thở: cuộn cong lưng ra sau. Hít: giữ C, mở ngực. Thở: úp về chân. Hít: cuộn dựng lên.",
        "6–8 lần",
        P("mat1", 9, "2x2", [
            "Vị trí chuẩn bị",
            "Cuộn cong lưng ra sau",
            "Cong lưng về trước chân",
            "Cuộn thẳng lưng về vị trí ban đầu",
        ]),
    ),
    ex(
        "mat-cat-stretch",
        "CAT STRETCH",
        "Tư thế con mèo",
        WARMUP,
        "mat-warmup",
        "Tư thế bốn điểm, cột sống trung tính.",
        "Thở: cuộn cong lưng lên trần (cat). Hít: cuộn lưng về neutral. Thở: cuộn duỗi lưng (cow).",
        "5–8 lần",
        P("mat1", 10, "3col2", [
            "Vị trí chuẩn bị",
            "Cuộn cong lưng lên trần",
            "Cuộn lưng về neutral",
            "Tư thế bốn điểm",
            "Cuộn cong lên",
            "Cuộn duỗi lưng (cow)",
        ]),
    ),
    ex(
        "mat-chest-lift",
        "CHEST LIFT",
        "Nâng ngực",
        MAIN,
        "mat-main",
        "Nằm ngửa, tay sau đầu, gối co, chân table-top hoặc úp sàn.",
        "Thở: siết bụng, nâng ngực lên. Hít: hạ xuống.",
        "5–10 lần",
        P("mat1", 11, "2+1", [
            "Vị trí bắt đầu",
            "Nâng ngực lên",
            "Biến thể: chân table-top",
        ]),
    ),
    ex(
        "mat-obliques",
        "OBLIQUES",
        "Cơ chéo bụng",
        MAIN,
        "mat-main",
        "Tư thế chest lift, tay sau đầu.",
        "Thở: xoay người sang một bên. Hít: về giữa. Thở: xoay đối bên.",
        "8–10 lần",
        P("mat1", 12, "2x2", [
            "Vị trí bắt đầu",
            "Xoay bên",
            "Xoay về giữa",
            "Đối bên",
        ]),
    ),
    ex(
        "mat-obliques-variation",
        "OBLIQUES VARIATION",
        "Cơ chéo bụng — Biến thể",
        MAIN,
        "mat-main",
        "Chest lift, chân table-top.",
        "Hít: chân table-top. Thở: xoay trái, duỗi chân phải. Hít: trở về. Thở: xoay phải, duỗi chân trái.",
        "8–10 lần",
        P("mat1", 13, "2x2", [
            "Chân table-top",
            "Xoay trái, duỗi chân phải",
            "Trở về",
            "Xoay phải, duỗi chân trái",
        ]),
    ),
    ex(
        "mat-hundred",
        "THE HUNDRED",
        "Trăm nhịp",
        MAIN,
        "mat-main",
        "Nằm ngửa, gối co table-top, tay dọc thân.",
        "Thở: nâng ngực, duỗi chân đường chéo. Đập tay: hít 5 nhịp, thở 5 nhịp.",
        "10 lần (100 nhịp)",
        P("mat1", 14, "2x2", [
            "Vị trí chuẩn bị",
            "Nâng người, duỗi chân đường chéo",
            "Hít thở kết hợp đập tay",
            "Hít thở kết hợp đập tay",
        ]),
    ),
    ex(
        "mat-hundred-easy",
        "THE HUNDRED — EASY VARIATION",
        "Trăm nhịp — Biến thể dễ",
        MAIN,
        "mat-main",
        "Nằm ngửa, giữ chân table-top.",
        "Giữ chân table-top khi thực hiện hundred.",
        "10 lần",
        P("mat1", 15, "boxes", [
            "Biến thể dễ",
            "Giữ chân table-top",
            "Đập tay",
        ], boxes=[
            (0.04, 0.44, 0.50, 0.58),
            (0.04, 0.44, 0.50, 0.58),
            (0.04, 0.58, 0.50, 0.70),
        ]),
    ),
    ex(
        "mat-roll-up",
        "ROLL UP",
        "Cuộn người lên",
        MAIN,
        "mat-main",
        "Nằm ngửa, chân duỗi, tay qua đầu, lưng-hông trung tính.",
        "Hít: nâng tay lên trần. Thở: cuộn cột sống lên, úp lưng về trước. Hít: chuẩn bị cuộn xuống. Thở: cuộn lưng nằm xuống.",
        "5–8 lần",
        P("mat1", 16, "page_auto", [
            "Vị trí chuẩn bị",
            "Nâng tay lên trần nhà",
            "Cuộn cột sống lên",
            "Úp lưng về trước",
            "Cuộn lưng nằm xuống",
        ]),
    ),
    ex(
        "mat-one-leg-circle",
        "ONE LEG CIRCLE",
        "Vẽ vòng tròn một chân",
        MAIN,
        "mat-main",
        "Nằm ngửa, một chân duỗi sàn, một chân nâng vuông góc.",
        "Thở: hạ chân. Hít: mở chân vẽ vòng tròn. Thở: nâng chân về. Đổi chiều và chân.",
        "5 vòng mỗi chiều mỗi chân",
        P("mat1", 17, "2x2", [
            "Vị trí chuẩn bị",
            "Hạ chân",
            "Mở chân vẽ vòng tròn",
            "Nâng chân về vị trí bắt đầu",
        ]),
    ),
    ex(
        "mat-single-leg-stretch",
        "SINGLE LEG STRETCH",
        "Duỗi một chân",
        MAIN,
        "mat-main",
        "Nằm ngửa, đầu và vai nâng, một chân co table-top, tay nắm ống chân.",
        "Thở: duỗi chân ra, giữ chân còn lại co. Hít: đổi chân.",
        "8–10 lần cả hai chân",
        P("mat1", 18, "2+1", [
            "Vị trí bắt đầu",
            "Một chân co, một chân duỗi",
            "Đổi chân",
        ]),
    ),
    ex(
        "mat-double-leg-stretch",
        "DOUBLE LEG STRETCH",
        "Duỗi hai chân",
        MAIN,
        "mat-main",
        "Chest lift, hai chân co table-top, tay nắm ống chân.",
        "Hít: gập khuỷu tay. Thở: vươn tay qua đầu, duỗi thẳng chân. Hít: mở tay sang hai bên, co gối. Thở: vẽ tay vòng tròn trở về.",
        "5–10 lần",
        P("mat1", 19, "boxes", [
            "Vị trí chuẩn bị",
            "Gập khuỷu tay",
            "Vươn tay qua đầu, duỗi chân",
            "Mở tay sang hai bên, co gối",
            "Vẽ tay vòng tròn trở về",
        ], boxes=[
            (0.535, 0.159, 0.838, 0.375),
            (0.093, 0.379, 0.443, 0.636),
            (0.342, 0.430, 0.493, 0.579),
            (0.506, 0.365, 0.860, 0.636),
            (0.077, 0.609, 0.435, 0.878),
        ]),
    ),
    ex(
        "mat-scissors",
        "SCISSORS",
        "Kéo chân",
        MAIN,
        "mat-main",
        "Nằm ngửa, một chân thẳng sàn, một chân nâng, tay nắm cổ chân, imprint.",
        "Hít: kéo chân nâng về phía người. Thở: đổi chân.",
        "8–10 lần",
        P("mat1", 20, "2col", [
            "Vị trí chuẩn bị",
            "Đổi chân",
        ]),
    ),
    ex(
        "mat-double-leg-straight",
        "DOUBLE LEG STRAIGHT",
        "Duỗi thẳng hai chân",
        MAIN,
        "mat-main",
        "Nằm ngửa, hai chân nâng vuông góc, tay sau đầu.",
        "Hít: gập cổ chân. Thở: nâng chân lên. Hít: duỗi cổ chân. Thở: hạ chân xuống.",
        "8–10 lần",
        P("mat1", 21, "1+2x2", [
            "Vị trí chuẩn bị",
            "Gập cổ chân",
            "Nâng chân lên",
            "Duỗi cổ chân",
            "Hạ chân xuống",
        ]),
    ),
    ex(
        "mat-shoulder-bridge",
        "SHOULDER BRIDGE",
        "Cầu vai",
        MAIN,
        "mat-main",
        "Nằm ngửa, gối co, chân úp sàn, cây cầu.",
        "Nâng một chân table-top, duỗi thẳng lên trần, gập cổ chân hạ xuống. Đổi chân.",
        "3 lần mỗi chân",
        P("mat1", 22, "3col2", [
            "Tư thế chuẩn bị",
            "Nâng một chân table-top",
            "Duỗi thẳng lên trần",
            "Gập cổ chân, hạ chân",
            "Đổi chân lên table-top",
            "Nâng thẳng chân lên trần",
        ]),
    ),
    ex(
        "mat-rolling-like-a-ball",
        "ROLLING LIKE A BALL",
        "Lăn như một quả bóng",
        MAIN,
        "mat-main",
        "Ngồi, ôm gối, cằm hướng xương ức, mắt nhìn rốn.",
        "Hít: lăn về vai. Thở: lăn về cân bằng.",
        "7–10 lần",
        P("mat1", 23, "2col", [
            "Tư thế chuẩn bị",
            "Lăn về vai",
        ]),
    ),
    ex(
        "mat-roll-over",
        "ROLL OVER",
        "Cuộn người qua đầu",
        MAIN,
        "mat-main",
        "Nằm ngửa, chân duỗi thẳng, tay dọc thân.",
        "Thở: nâng chân lên trần, cuộn qua đầu, chân song song sàn, hạ mũi chân, mở chân. Thở: cuộn xuống, khép chân về.",
        "5 lần",
        P("mat1", 24, "page_auto", [
            "Vị trí chuẩn bị",
            "Nâng chân lên trần",
            "Cuộn lên chân song song sàn",
            "Hạ mũi chân",
            "Nâng mở chân",
            "Cuộn xuống",
            "Bắt đầu hạ chân",
            "Khép về ban đầu",
        ]),
    ),
    ex(
        "mat-teaser",
        "TEASER",
        "Ngồi chữ V",
        MAIN,
        "mat-main",
        "Nằm ngửa, tay qua đầu, chân duỗi khép, lưng-hông trung tính.",
        "Hít: nâng tay vuông góc, co gối. Thở: cuộn lên ngồi thăng bằng trên xương ngồi, nâng chân (table-top hoặc duỗi). Hít: tay sát tai. Thở: cuộn xuống.",
        "3–5 lần",
        P("mat2", 1, "page_auto", [
            "Vị trí chuẩn bị",
            "Nâng tay lên",
            "Bắt đầu cuộn lưng lên",
            "Ngồi ở vị trí chữ V",
            "Duỗi gối",
        ]),
    ),
    ex(
        "mat-side-kick",
        "SIDE KICK",
        "Đá chân sang ngang",
        MAIN,
        "mat-main",
        "Nằm nghiêng, đầu trên tay, chân trên nâng ngang hông.",
        "Hít: đá chân về trước 2 lần. Thở: đá chân về sau.",
        "8–10 lần",
        P("mat2", 2, "2+1", [
            "Vị trí chuẩn bị",
            "Đá chân về trước 2 lần",
            "Đá chân về sau",
        ]),
    ),
    ex(
        "mat-side-leg-abduction",
        "TOP LEG ABDUCTION",
        "Dạng chân nằm nghiêng",
        MAIN,
        "mat-main",
        "Nằm nghiêng, chân xếp chồng, tay nâng đầu.",
        "Thở: nâng chân trên lên. Hít: gập cổ chân. Thở: hạ chân. Hít: duỗi cổ chân.",
        "5–10 lần",
        P("mat2", 3, "boxes", [
            "Tư thế nằm nghiêng",
            "Nâng chân lên",
            "Gập cổ chân",
            "Hạ chân xuống",
            "Duỗi cổ chân",
        ], boxes=[
            (0.103, 0.230, 0.583, 0.449),
            (0.523, 0.241, 0.875, 0.451),
            (0.112, 0.548, 0.347, 0.742),
            (0.533, 0.552, 0.765, 0.739),
            (0.102, 0.726, 0.342, 0.910),
        ]),
    ),
    ex(
        "mat-side-leg-circles",
        "TOP LEG CIRCLES",
        "Xoay chân trên",
        MAIN,
        "mat-main",
        "Nằm nghiêng, chân trên nâng ngang hông.",
        "Thở: nâng chân. Hít: vẽ vòng tròn. Thở: hạ chân về.",
        "5 vòng mỗi chiều",
        P("mat2", 4, "2+1", [
            "Nâng chân lên",
            "Vẽ chân vòng tròn",
            "Hạ chân về vị trí ban đầu",
        ]),
    ),
    ex(
        "mat-staggered-legs",
        "STAGGERED LEGS",
        "Chân so le",
        MAIN,
        "mat-main",
        "Nằm nghiêng, chân so le phía trước.",
        "Thở: nâng chân trên. Hít: nâng chân dưới chạm chân trên. Thở: hạ hai chân.",
        "5–10 lần",
        P("mat2", 5, "boxes", [
            "Nâng chân lên",
            "Nâng chân dưới chạm chân trên",
            "Hạ 2 chân xuống",
        ], boxes=[
            (0.117, 0.257, 0.348, 0.454),
            (0.530, 0.262, 0.753, 0.450),
            (0.115, 0.496, 0.340, 0.676),
        ]),
    ),
    ex(
        "mat-both-legs-together",
        "BOTH LEGS TOGETHER",
        "Nâng cả hai chân",
        MAIN,
        "mat-main",
        "Nằm nghiêng, chân xếp chồng.",
        "Thở: nâng hai chân lên. Hít: hạ hai chân xuống.",
        "5–10 lần",
        P("mat2", 6, "2col", [
            "Nâng hai chân lên",
            "Hạ hai chân xuống",
        ]),
    ),
    ex(
        "mat-breast-stroke-prep-shoulders",
        "BREAST STROKE PREP — HANDS BY SHOULDERS",
        "Chuẩn bị bơi ếch — Tay ngang vai",
        MAIN,
        "mat-main",
        "Nằm sấp, khuỷu gập ngang mũi, trán trên tay.",
        "Thở: nâng ngực lên. Hít: hạ xuống.",
        "5–8 lần",
        P("mat2", 7, "2col", [
            "Vị trí chuẩn bị",
            "Nâng ngực lên",
        ]),
    ),
    ex(
        "mat-breast-stroke-prep-flight",
        "BREAST STROKE PREP — FLIGHT",
        "Chuẩn bị bơi ếch — Tư thế bay",
        MAIN,
        "mat-main",
        "Nằm sấp, tay duỗi sang hai bên (tư thế bay).",
        "Thở: nâng ngực lên. Hít: hạ xuống.",
        "5–8 lần",
        P("mat2", 8, "2col", [
            "Vị trí chuẩn bị",
            "Nâng ngực lên",
        ]),
    ),
    ex(
        "mat-breast-stroke",
        "BREAST STROKE",
        "Bơi ếch",
        MAIN,
        "mat-main",
        "Nằm sấp, tay dọc thân.",
        "Thở: nâng ngực, duỗi tay qua đầu. Hít: mở tay về hông. Thở: trở về.",
        "5–8 lần",
        P("mat2", 9, "2x2+1", [
            "Vị trí chuẩn bị",
            "Nâng ngực lên",
            "Duỗi tay qua đầu",
            "Mở tay về hông",
            "Trở về vị trí ban đầu",
        ]),
    ),
    ex(
        "mat-heel-squeeze-prone",
        "HEEL SQUEEZE PRONE",
        "Ép gót chân nằm sấp",
        MAIN,
        "mat-main",
        "Nằm sấp, hai gót chân khép sát.",
        "Thở: nhấn gót vào nhau. Hít: thả lỏng.",
        "8–10 lần",
        P("mat2", 10, "2col", [
            "Vị trí chuẩn bị",
            "Nhấn gót vào nhau",
        ]),
    ),
    ex(
        "mat-heel-beats",
        "HEEL BEATS",
        "Đập gót chân",
        MAIN,
        "mat-main",
        "Nằm sấp, hai chân duỗi, tay gối đầu.",
        "Thở: nâng hai chân. Hít: gõ chân 3 lần. Thở: gập cổ chân, gõ gót 3 lần.",
        "8–10 lần",
        P("mat2", 11, "2x2+1", [
            "Vị trí chuẩn bị",
            "Nâng hai chân",
            "Gõ chân 3 lần",
            "Gập cổ chân",
            "Gõ gót 3 lần",
        ]),
    ),
    ex(
        "mat-one-leg-kick",
        "ONE LEG KICK",
        "Đá một chân",
        MAIN,
        "mat-main",
        "Nằm sấp, khuỷu gập, trán trên tay, một chân co.",
        "Thở: gập gối đá chân 2 lần về mông. Hít: gập cổ chân. Thở: đá 2 lần. Đổi chân.",
        "5–8 lần mỗi chân",
        P("mat2", 12, "2x2+1", [
            "Vị trí chuẩn bị",
            "Gập gối, đá chân 2 lần",
            "Gập cổ chân",
            "Đá chân 2 lần",
            "Trở về và đổi chân",
        ]),
    ),
    ex(
        "mat-shell-stretch",
        "SHELL STRETCH",
        "Nghỉ ngơi tư thế em bé",
        MAIN,
        "mat-main",
        "Quỳ, ngồi lên gót, gập người về phía trước.",
        "Giãn lưng ở tư thế em bé.",
        "Theo nhu cầu",
        P("mat2", 13, "1", ["Giãn lưng ở tư thế em bé"]),
    ),
    ex(
        "mat-leg-extension",
        "SINGLE & DOUBLE LEG EXTENSION",
        "Đuôi một chân / hai chân",
        MAIN,
        "mat-main",
        "Nằm sấp, tay gối đầu, chân duỗi.",
        "Thở: nâng một chân. Hít: hạ. Thở: nâng cả hai chân.",
        "6–8 lần",
        P("mat2", 14, "1col", [
            "Nâng một chân",
            "Nâng cả 2 chân",
        ]),
    ),
    ex(
        "mat-swimming",
        "SWIMMING",
        "Động tác bơi",
        MAIN,
        "mat-main",
        "Nằm sấp, tay duỗi phía trước.",
        "Thở: nâng người, nâng tay và chân. Hít/thở: đổi tay chân đối diện như bơi.",
        "3–5 lần (hít 5/thở 5)",
        P("mat2", 15, "2x2", [
            "Vị trí chuẩn bị",
            "Nâng người, nâng tay và chân",
            "Nâng tay trái chân phải",
            "Đổi tay và chân",
        ]),
    ),
    ex(
        "mat-baby-swan",
        "BABY SWAN",
        "Thiên nga nhỏ",
        MAIN,
        "mat-main",
        "Nằm sấp, khuỷu gập ngang vai.",
        "Thở: nâng người lên, duỗi cột sống.",
        "5–8 lần",
        P("mat2", 16, "1col", [
            "Vị trí chuẩn bị",
            "Nâng người lên",
        ]),
    ),
    ex(
        "mat-swan-dive",
        "SWAN DIVE",
        "Thiên nga bay",
        MAIN,
        "mat-main",
        "Nằm sấp, tay dọc thân.",
        "Thở: nâng lên baby swan. Hít: bập bênh. Thở: trở về.",
        "Lắc 3 lần/bộ, 5 lần",
        P("mat2", 17, "2x2", [
            "Vị trí chuẩn bị",
            "Nâng người lên baby swan",
            "Bập bênh",
            "Trở về tư thế ban đầu",
        ]),
    ),
    ex(
        "mat-leg-pull-front-prep",
        "LEG PULL FRONT PREP",
        "Chuẩn bị nâng chân trước",
        MAIN,
        "mat-main",
        "Tư thế plank, tay thẳng.",
        "Thở: nâng gối. Hít: trở về.",
        "5–8 lần",
        P("mat2", 18, "2+1", [
            "Vị trí chuẩn bị",
            "Nâng gối",
            "Trở về vị trí ban đầu",
        ]),
    ),
    ex(
        "mat-bird-dog",
        "BIRD DOG",
        "Kéo dài tay chân đối diện",
        MAIN,
        "mat-main",
        "Tư thế bốn điểm, cột sống trung tính.",
        "Thở: nâng tay trái chân phải. Hít: hạ về. Thở: nâng tay phải chân trái.",
        "3–5 lần mỗi bên",
        P("mat2", 19, "2x2", [
            "Vị trí chuẩn bị",
            "Nâng tay trái, chân phải",
            "Hạ tay và chân về",
            "Nâng tay phải, chân trái",
        ]),
    ),
    ex(
        "mat-leg-pull-front",
        "LEG PULL FRONT",
        "Nâng chân trước",
        MAIN,
        "mat-main",
        "Tư thế plank.",
        "Thở: nâng một chân. Hít: duỗi mũi chân. Thở: gập cổ chân hạ chân. Đổi bên.",
        "8 lần cả hai chân",
        P("mat2", 20, "2x2+1", [
            "Vị trí chuẩn bị",
            "Nâng một chân lên",
            "Duỗi mũi chân",
            "Gập cổ chân, hạ chân",
            "Về vị trí ban đầu và đổi bên",
        ]),
    ),
    ex(
        "mat-spine-twist",
        "SPINE TWIST",
        "Xoay cột sống",
        MAIN,
        "mat-main",
        "Ngồi thẳng lưng, chân mở rộng hơn vai, tay dang ngang.",
        "Hít: xoay người sang bên. Thở: xoay đối bên. Trở về giữa.",
        "3–5 lần mỗi bên",
        P("mat2", 21, "2x2", [
            "Vị trí chuẩn bị",
            "Xoay người sang bên",
            "Xoay đối bên",
            "Trở về",
        ]),
    ),
    ex(
        "mat-saw",
        "SAW",
        "Động tác cưa",
        MAIN,
        "mat-main",
        "Ngồi thẳng lưng, chân mở V, tay dang ngang, lòng bàn tay đối nhau.",
        "Hít: xoay người sang bên. Thở: gập người trên chân, mắt nhìn tay sau. Hít: nâng lên. Thở: xoay về giữa. Đổi bên.",
        "6–8 lần",
        P("mat2", 22, "2x3", [
            "Vị trí chuẩn bị",
            "Xoay người sang bên",
            "Gập người trên chân",
            "Nâng người lên",
            "Xoay về giữa",
            "Xoay đối bên",
        ], start=1),
        P("mat2", 23, "page_auto", [
            "Gập người trên chân",
            "Nâng người lên",
            "Trở về vị trí ban đầu",
        ], start=7),
    ),
    ex(
        "mat-obliques-roll-back",
        "OBLIQUES ROLL BACK",
        "Cuộn lưng nghiêng",
        MAIN,
        "mat-main",
        "Ngồi khoanh chân, tay trước ngực.",
        "Thở: cuộn ra sau và xoay người. Hít: trở về. Đổi bên.",
        "3–5 lần mỗi bên",
        P("mat2", 24, "2x2", [
            "Vị trí chuẩn bị",
            "Cuộn ra sau và xoay người",
            "Trở về",
            "Đổi bên",
        ]),
    ),
    ex(
        "mat-spine-stretch-forward",
        "SPINE STRETCH FORWARD",
        "Duỗi cột sống về phía trước",
        MAIN,
        "mat-main",
        "Ngồi thẳng lưng, chân duỗi mở rộng hơn vai, cổ chân gập, tay giữa hai chân.",
        "Hít: giữ nguyên. Thở: cuộn từ cổ xuống, siết bụng giữ xương chậu dựng. Hít: giữ, mở khung sườn. Thở: cuộn từ xương cụt dựng lên.",
        "3–5 lần",
        P("mat3", 1, "2x2", [
            "Vị trí chuẩn bị",
            "Cuộn từ đầu",
            "Cong lưng về phía trước",
            "Cuộn về vị trí ban đầu",
        ]),
    ),
    ex(
        "mat-open-leg-rocker",
        "OPEN LEG ROCKER",
        "Lắc người chân mở",
        MAIN,
        "mat-main",
        "Ngồi thăng bằng trên xương ngồi, ôm ống chân, chân mở rộng hơn vai.",
        "Thở: cuộn ra sau. Hít: cuộn lên về cân bằng.",
        "6–8 lần",
        P("mat3", 2, "2+1", [
            "Vị trí chuẩn bị",
            "Cuộn ra sau",
            "Cuộn lên",
        ]),
    ),
    ex(
        "mat-mermaid",
        "MERMAID",
        "Tư thế nghiêng mở hông",
        MAIN,
        "mat-main",
        "Ngồi, chân gập một bên, tay đặt cạnh hông.",
        "Hít: nâng tay. Thở: nghiêng bên. Đổi bên.",
        "6–8 lần",
        P("mat3", 3, "2+1L", [
            "Vị trí chuẩn bị",
            "Nâng tay",
            "Nghiêng bên",
        ]),
    ),
    ex(
        "mat-leg-pull-prep",
        "LEG PULL PREP",
        "Chuẩn bị nâng chân sau",
        MAIN,
        "mat-main",
        "Ngồi chân duỗi, tay đặt sau hông.",
        "Thở: nhấn chân, cuộn từ mông nâng lên push-up ngược. Hít: trở về.",
        "6 lần",
        P("mat3", 4, "2x2", [
            "Vị trí chuẩn bị",
            "Nhấn chân, cuộn từ mông",
            "Nâng thẳng người push-up ngược",
            "Trở về",
        ]),
    ),
    ex(
        "mat-side-bend",
        "SIDE BEND",
        "Gập nghiêng người",
        MAIN,
        "mat-main",
        "Ngồi nghiêng, chân xếp chồng, tay đặt cạnh hông.",
        "Thở: nâng hông lên. Hít: hạ hông xuống. Đổi bên.",
        "6 lần mỗi bên",
        P("mat3", 5, "2+1", [
            "Vị trí chuẩn bị",
            "Nâng hông lên",
            "Hạ hông xuống",
        ]),
    ),
    ex(
        "mat-push-up",
        "PUSH UP",
        "Chuỗi hít đất",
        MAIN,
        "mat-main",
        "Đứng thẳng, chân khép.",
        "Gập gối, kiễng gót, cuộn xuống, bước tay ra plank, chống đẩy 3 lần, thu tay, cuộn lên đứng.",
        "3 chống đẩy/bộ, 3 lần",
        P("mat3", 6, "boxes", [
            "Vị trí chuẩn bị",
            "Gập gối",
            "Kiễng gót",
            "Hạ gót",
            "Cuộn xuống",
            "Hạ lòng bàn tay xuống thảm",
            "Bước bằng tay",
            "Bước tay đến tư thế tấm ván",
        ], start=1, boxes=[
            (0.1566, 0.7064, 0.3581, 0.7691),
            (0.3600, 0.7064, 0.5605, 0.7691),
            (0.5624, 0.7064, 0.7629, 0.7691),
            (0.7452, 0.7064, 0.9669, 0.7691),
            (0.1566, 0.7697, 0.3581, 0.8330),
            (0.3600, 0.7697, 0.5605, 0.8330),
            (0.5624, 0.7697, 0.7629, 0.8330),
            (0.7648, 0.7697, 0.9669, 0.8330),
        ]),
        P("mat3", 7, "boxes", [
            "Chống đẩy",
            "Nâng người",
            "Bắt đầu thu tay về",
            "Cuộn lên",
            "Trở về tư trí ban đầu",
        ], start=9, boxes=[
            (0.12, 0.16, 0.32, 0.30),
            (0.34, 0.16, 0.55, 0.30),
            (0.58, 0.16, 0.73, 0.30),
            (0.78, 0.16, 0.92, 0.30),
            (0.58, 0.28, 0.92, 0.44),
        ]),
    ),
]


def render_page(doc: fitz.Document, page_index: int) -> Image.Image:
    page = doc[page_index]
    matrix = fitz.Matrix(RENDER_SCALE, RENDER_SCALE)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def _find_components(
    region: Image.Image,
    threshold: int = 238,
    min_cnt: int = 35,
) -> tuple[list[list[float | int]], tuple[int, int]]:
    w, h = region.size
    target_w = min(600, w)
    scale = w / target_w
    sh, sw = int(h / scale), target_w
    small = region.resize((sw, sh), Image.Resampling.BILINEAR).convert("L")
    px = small.load()
    mask = [[px[x, y] < threshold for x in range(sw)] for y in range(sh)]
    visited = [[False] * sw for _ in range(sh)]
    comps: list[list[float | int]] = []

    for sy in range(sh):
        for sx in range(sw):
            if not mask[sy][sx] or visited[sy][sx]:
                continue
            stack = [(sx, sy)]
            visited[sy][sx] = True
            minx = maxx = sx
            miny = maxy = sy
            cnt = 0
            while stack:
                x, y = stack.pop()
                cnt += 1
                minx = min(minx, x)
                maxx = max(maxx, x)
                miny = min(miny, y)
                maxy = max(maxy, y)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < sw and 0 <= ny < sh and mask[ny][nx] and not visited[ny][nx]:
                        visited[ny][nx] = True
                        stack.append((nx, ny))
            bw, bh = maxx - minx + 1, maxy - miny + 1
            comps.append([minx, miny, maxx + 1, maxy + 1, bw, bh, cnt, scale])

    return comps, (sw, sh)


def _is_ruled_line(box: list[float | int], sw: int, sh: int) -> bool:
    bw, bh, cnt = int(box[4]), int(box[5]), int(box[6])
    if bh <= max(3, int(sh * 0.028)) and bw >= sw * 0.55:
        return True
    if bh <= max(4, int(sh * 0.035)) and cnt < bw * bh * 0.15:
        return True
    return False


def _merge_boxes(raw_boxes: list[list[float | int]]) -> list[list[int]]:
    boxes = [[int(v) for v in b[:4]] for b in raw_boxes]
    boxes.sort(key=lambda b: (b[1], b[0]))
    merged: list[list[int]] = []

    for box in boxes:
        placed = False
        for i, prev in enumerate(merged):
            ox = max(0, min(prev[2], box[2]) - max(prev[0], box[0]))
            minw = min(prev[2] - prev[0], box[2] - box[0])
            if minw <= 0:
                continue
            vgap = box[1] - prev[3]
            if ox >= minw * 0.22 and -2 <= vgap <= 40:
                merged[i] = [
                    min(prev[0], box[0]),
                    min(prev[1], box[1]),
                    max(prev[2], box[2]),
                    max(prev[3], box[3]),
                ]
                placed = True
                break
        if not placed:
            merged.append(box)

    return merged


def smart_photo_region(
    image: Image.Image,
    region: tuple[float, float, float, float] | None = None,
) -> Image.Image:
    w, h = image.size
    if region:
        x1, y1, x2, y2 = region
        return image.crop((int(w * x1), int(h * y1), int(w * x2), int(h * y2)))

    scan = image.crop((int(w * 0.04), int(h * 0.35), int(w * 0.96), int(h * 0.80)))
    comps, (sw, sh) = _find_components(scan)
    photo_boxes = []
    for box in comps:
        if _is_ruled_line(box, sw, sh):
            continue
        bw, bh, cnt = int(box[4]), int(box[5]), int(box[6])
        if bw >= sw * 0.07 and bh >= sh * 0.06 and cnt >= 50:
            photo_boxes.append(box)

    if not photo_boxes:
        return image.crop((int(w * 0.04), int(h * 0.40), int(w * 0.96), int(h * 0.70)))

    merged = _merge_boxes(photo_boxes)
    scale = float(photo_boxes[0][7])
    pad = int(14 * scale)
    minx = min(int(b[0]) for b in merged)
    miny = min(int(b[1]) for b in merged)
    maxx = max(int(b[2]) for b in merged)
    maxy = max(int(b[3]) for b in merged)
    sx1 = int(w * 0.04)
    sy1 = int(h * 0.35)
    x1 = max(0, sx1 + int(minx * scale) - pad)
    y1 = max(0, sy1 + int(miny * scale) - pad)
    x2 = min(w, sx1 + int(maxx * scale) + pad)
    y2 = min(h, sy1 + int(maxy * scale) + pad + int(18 * scale))
    return image.crop((x1, y1, x2, y2))


def auto_split(region: Image.Image, expected: int) -> list[Image.Image] | None:
    comps, (sw, sh) = _find_components(region, threshold=237, min_cnt=25)
    boxes = []
    for box in comps:
        if _is_ruled_line(box, sw, sh):
            continue
        bw, bh, cnt = int(box[4]), int(box[5]), int(box[6])
        if bw >= sw * 0.05 and bh >= sh * 0.035 and cnt >= 30:
            boxes.append(box)

    merged = _merge_boxes(boxes)
    merged = [b for b in merged if (b[2] - b[0]) >= sw * 0.08 and (b[3] - b[1]) >= sh * 0.06]
    if len(merged) != expected:
        return None

    scale = float(boxes[0][7]) if boxes else 1.0
    merged.sort(key=lambda b: (round((b[1] + b[3]) / 2 / (sh * 0.14)), b[0]))
    rw, rh = region.size
    pad = int(8 * scale)
    crops: list[Image.Image] = []
    for minx, miny, maxx, maxy in merged:
        crops.append(
            region.crop(
                (
                    max(0, int(minx * scale) - pad),
                    max(0, int(miny * scale) - pad),
                    min(rw, int(maxx * scale) + pad),
                    min(rh, int(maxy * scale) + pad + int(12 * scale)),
                )
            )
        )
    return crops


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

    if layout == "2+1L":
        top_h = h * 2 // 3
        mid = w // 2
        return [
            region.crop((0, 0, mid - 3, top_h)),
            region.crop((mid + 3, 0, w, top_h)),
            region.crop((0, top_h + 3, mid - 3, h)),
        ]

    if layout == "4+1BR":
        top_h = int(h * 0.50)
        col_w = w // 4
        top = [
            region.crop((i * col_w + (2 if i else 0), 0, (i + 1) * col_w - (2 if i < 3 else 0), top_h))
            for i in range(4)
        ]
        bottom = region.crop((int(w * 0.62), top_h + 2, int(w * 0.98), h))
        return top + [bottom]

    if layout == "3+2":
        top_h = int(h * 0.56)
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

    if layout == "2+1":
        top_h = int(h * 0.52)
        mid = w // 2
        return [
            region.crop((0, 0, mid - 3, top_h)),
            region.crop((mid + 3, 0, w, top_h)),
            region.crop((0, top_h + 4, mid - 3, h)),
        ]

    if layout == "2x2+1":
        top_h = int(h * 0.66)
        mid_x = w // 2
        mid_y = top_h // 2
        grid = [
            region.crop((0, 0, mid_x - 3, mid_y - 3)),
            region.crop((mid_x + 3, 0, w, mid_y - 3)),
            region.crop((0, mid_y + 3, mid_x - 3, top_h)),
            region.crop((mid_x + 3, mid_y + 3, w, top_h)),
        ]
        bottom = region.crop((int(w * 0.22), top_h + 4, int(w * 0.78), h))
        return grid + [bottom]

    if layout == "3x2+1":
        row_h = h // 3
        third = w // 3
        cells = []
        for row in range(2):
            y1, y2 = row * row_h, (row + 1) * row_h - 3
            for col in range(3):
                x1 = col * third
                x2 = (col + 1) * third - 3 if col < 2 else w
                cells.append(region.crop((x1 + (3 if col else 0), y1, x2, y2)))
        cells.append(region.crop((0, 2 * row_h + 3, third - 3, h)))
        return cells

    if layout == "3col2":
        row_h = h // 2
        third = w // 3
        cells = []
        for row in range(2):
            y1, y2 = row * row_h, (row + 1) * row_h - 3
            for col in range(3):
                x1 = col * third
                x2 = (col + 1) * third - 3 if col < 2 else w
                cells.append(region.crop((x1 + (3 if col else 0), y1, x2, y2)))
        return cells

    if layout == "1+2x2":
        top_h = int(h * 0.38)
        bottom = region.crop((0, top_h, w, h))
        mid_x, mid_y = w // 2, (h - top_h) // 2
        return [
            region.crop((mid_x + 3, 0, w, top_h)),
            bottom.crop((0, 0, mid_x - 3, mid_y - 3)),
            bottom.crop((mid_x + 3, 0, w, mid_y - 3)),
            bottom.crop((0, mid_y + 3, mid_x - 3, h - top_h)),
            bottom.crop((mid_x + 3, mid_y + 3, w, h - top_h)),
        ]

    if layout == "3+3+2":
        row1_h = int(h * 0.34)
        row2_h = int(h * 0.34)
        third = w // 3
        half = w // 2
        rows = []
        for _, rh, yoff in [(0, row1_h, 0), (1, row2_h, row1_h + 3)]:
            for col in range(3):
                x1 = col * third
                x2 = (col + 1) * third - 3 if col < 2 else w
                rows.append(region.crop((x1 + (3 if col else 0), yoff, x2, yoff + rh)))
        y3 = row1_h + row2_h + 6
        rows.append(region.crop((0, y3, half - 3, h)))
        rows.append(region.crop((half + 3, y3, w, h)))
        return rows

    if layout == "2x3":
        col_w = w // 2
        row_h = h // 3
        cells = []
        for row in range(3):
            y1, y2 = row * row_h, (row + 1) * row_h - 3
            cells.append(region.crop((0, y1, col_w - 3, y2)))
            cells.append(region.crop((col_w + 3, y1, w, y2)))
        return cells

    if layout == "1col":
        mid_y = h // 2
        return [
            region.crop((0, 0, w, mid_y - 3)),
            region.crop((0, mid_y + 3, w, h)),
        ]

    if layout == "4x2":
        col_w = w // 4
        row_h = h // 2
        cells = []
        for row in range(2):
            y1, y2 = row * row_h, (row + 1) * row_h - 3
            for col in range(4):
                x1 = col * col_w
                x2 = (col + 1) * col_w - 3 if col < 3 else w
                cells.append(region.crop((x1 + (3 if col else 0), y1, x2, y2)))
        return cells

    raise ValueError(f"Unknown layout: {layout}")


def page_auto_split(page_image: Image.Image, expected: int) -> list[Image.Image]:
    w, h = page_image.size
    target_w = min(600, w)
    scale = w / target_w
    sh, sw = int(h / scale), target_w
    small = page_image.resize((sw, sh), Image.Resampling.BILINEAR).convert("L")
    px = small.load()
    threshold = 232
    mask = [[px[x, y] < threshold for x in range(sw)] for y in range(sh)]
    visited = [[False] * sw for _ in range(sh)]
    raw: list[list[int]] = []

    for sy in range(sh):
        for sx in range(sw):
            if not mask[sy][sx] or visited[sy][sx]:
                continue
            stack = [(sx, sy)]
            visited[sy][sx] = True
            minx = maxx = sx
            miny = maxy = sy
            cnt = 0
            while stack:
                x, y = stack.pop()
                cnt += 1
                minx = min(minx, x)
                maxx = max(maxx, x)
                miny = min(miny, y)
                maxy = max(maxy, y)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < sw and 0 <= ny < sh and mask[ny][nx] and not visited[ny][nx]:
                        visited[ny][nx] = True
                        stack.append((nx, ny))
            bw, bh = maxx - minx + 1, maxy - miny + 1
            if cnt >= 60 and bw >= sw * 0.05 and bh >= sh * 0.02:
                if bh <= max(3, int(sh * 0.028)) and bw >= sw * 0.5:
                    continue
                raw.append([minx, miny, maxx + 1, maxy + 1])

    merged: list[list[int]] = []
    for box in sorted(raw, key=lambda b: (b[1], b[0])):
        if not merged:
            merged.append(box)
            continue
        prev = merged[-1]
        ox = max(0, min(prev[2], box[2]) - max(prev[0], box[0]))
        minw = min(prev[2] - prev[0], box[2] - box[0])
        vgap = box[1] - prev[3]
        prev_h = prev[3] - prev[1]
        box_h = box[3] - box[1]
        if minw > 0 and ox >= minw * 0.25 and 0 <= vgap <= 30 and box_h < prev_h * 0.5:
            merged[-1] = [
                min(prev[0], box[0]),
                min(prev[1], box[1]),
                max(prev[2], box[2]),
                max(prev[3], box[3]),
            ]
        else:
            merged.append(box)

    merged = [b for b in merged if (b[2] - b[0]) >= sw * 0.07 and (b[3] - b[1]) >= sh * 0.035]
    merged.sort(key=lambda b: (round((b[1] + b[3]) / 2 / (sh * 0.10)), b[0]))
    if len(merged) != expected:
        raise ValueError(f"page_auto found {len(merged)} photos, expected {expected}")

    crops: list[Image.Image] = []
    for minx, miny, maxx, maxy in merged:
        pad_x = int(18 * scale)
        pad_y = int(30 * scale)
        if (maxx - minx) > (maxy - miny) * 1.5:
            pad_y = int(50 * scale)
        x1 = max(0, int(minx * scale) - pad_x)
        y1 = max(0, int(miny * scale) - pad_y)
        x2 = min(w, int(maxx * scale) + pad_x)
        y2 = min(h, int(maxy * scale) + pad_y + int(25 * scale))
        crops.append(page_image.crop((x1, y1, x2, y2)))
    return crops


def _crop_std(crop: Image.Image) -> float:
    return ImageStat.Stat(crop.convert("L")).stddev[0]


def _crop_quality(crop: Image.Image) -> bool:
    std = _crop_std(crop)
    if std < 16:
        return False
    w, h = crop.size
    if w < 40 or h < 40:
        return False
    center = crop.crop((w // 4, h // 4, 3 * w // 4, 3 * h // 4))
    return _crop_std(center) >= 12


def trim_photo_crop(crop: Image.Image, threshold: int = 185, pad: int = 6) -> Image.Image:
    """Cắt sát nội dung ảnh, bỏ vùng giấy trắng và dòng kẻ notebook."""
    gray = crop.convert("L")
    w, h = gray.size
    px = gray.load()
    minx, miny, maxx, maxy = w, h, 0, 0
    found = False
    for y in range(h):
        for x in range(w):
            if px[x, y] < threshold:
                found = True
                minx = min(minx, x)
                maxx = max(maxx, x)
                miny = min(miny, y)
                maxy = max(maxy, y)
    if not found:
        return crop
    return crop.crop(
        (
            max(0, minx - pad),
            max(0, miny - pad),
            min(w, maxx + 1 + pad),
            min(h, maxy + 1 + pad),
        )
    )


def _finalize_crop(crop: Image.Image) -> Image.Image:
    if _crop_quality(crop):
        return crop
    trimmed = trim_photo_crop(crop)
    return trimmed if _crop_quality(trimmed) else crop


def _finalize_crops(crops: list[Image.Image]) -> list[Image.Image]:
    return [_finalize_crop(c) for c in crops]


def extract_crops(
    page_image: Image.Image,
    layout: PageLayout,
) -> list[Image.Image]:
    expected = len(layout.captions)

    if layout.boxes:
        w, h = page_image.size
        crops = [
            page_image.crop(
                (
                    int(w * x1),
                    int(h * y1),
                    int(w * x2),
                    int(h * y2),
                )
            )
            for x1, y1, x2, y2 in layout.boxes
        ]
        if len(crops) != expected:
            raise ValueError(f"boxes produced {len(crops)} crops, expected {expected}")
        crops = _finalize_crops(crops)
        if not all(_crop_quality(c) for c in crops):
            raise ValueError(f"boxes quality check failed on {layout.pdf}-p{layout.page}")
        return crops

    if layout.layout == "page_auto":
        crops = _finalize_crops(page_auto_split(page_image, expected))
        if not all(_crop_quality(c) for c in crops):
            raise ValueError(f"page_auto quality check failed on {layout.pdf}-p{layout.page}")
        return crops

    region = smart_photo_region(page_image, layout.region)
    crops = split_region(region, layout.layout)

    if len(crops) != expected:
        alt = auto_split(region, expected)
        if alt is not None:
            crops = alt
        else:
            raise ValueError(f"layout {layout.layout} produced {len(crops)} crops, expected {expected}")

    crops = _finalize_crops(crops)
    if not all(_crop_quality(c) for c in crops):
        alt = auto_split(region, expected)
        if alt is not None:
            alt = _finalize_crops(alt)
            if all(_crop_quality(c) for c in alt):
                return alt

    return crops


def resize_image(image: Image.Image, max_width: int = 900) -> Image.Image:
    if image.width <= max_width:
        return image
    ratio = max_width / image.width
    return image.resize((int(image.width * ratio), int(image.height * ratio)), Image.Resampling.LANCZOS)


async def generate_audio(text: str, output_path: Path) -> None:
    communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural", rate="-12%")
    await communicate.save(str(output_path))


async def main() -> None:
    for key, path in PDFS.items():
        if not path.exists():
            raise SystemExit(f"PDF not found ({key}): {path}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    docs = {key: fitz.open(path) for key, path in PDFS.items()}
    page_cache: dict[tuple[str, int], Image.Image] = {}

    def get_page(pdf: str, page: int) -> Image.Image:
        key = (pdf, page)
        if key not in page_cache:
            page_cache[key] = render_page(docs[pdf], page - 1)
        return page_cache[key]

    exercises_out: list[dict] = []
    audio_jobs = []

    for seed in MAT_EXERCISES:
        ex_dir = IMG_DIR / seed.id
        ex_dir.mkdir(parents=True, exist_ok=True)
        if ex_dir.exists():
            for old in ex_dir.glob("*.jpg"):
                old.unlink()
        images: list[dict] = []

        for layout in seed.pages:
            page_image = get_page(layout.pdf, layout.page)
            crops = extract_crops(page_image, layout)

            if len(crops) != len(layout.steps):
                raise SystemExit(
                    f"{seed.id} page {layout.pdf}-p{layout.page}: "
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

    existing_exercises = json.loads((DATA_DIR / "exercises.json").read_text(encoding="utf-8"))
    existing_packs = json.loads((DATA_DIR / "packs.json").read_text(encoding="utf-8"))
    existing_ids = {e["id"] for e in existing_exercises}

    merged_exercises = existing_exercises + [
        e for e in exercises_out if e["id"] not in existing_ids
    ]

    mat_warmup_ids = [e["id"] for e in exercises_out if e["packId"] == "mat-warmup"]
    mat_main_ids = [e["id"] for e in exercises_out if e["packId"] == "mat-main"]

    new_packs = [
        {
            "id": "mat-warmup",
            "name": "Mat — Khởi động",
            "description": "Bài tập khởi động trên thảm",
            "exerciseIds": mat_warmup_ids,
        },
        {
            "id": "mat-main",
            "name": "Mat — Bài chính",
            "description": "Bài tập chính trên thảm",
            "exerciseIds": mat_main_ids,
        },
    ]

    existing_pack_ids = {p["id"] for p in existing_packs}
    merged_packs = existing_packs + [p for p in new_packs if p["id"] not in existing_pack_ids]

    (DATA_DIR / "exercises.json").write_text(
        json.dumps(merged_exercises, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (DATA_DIR / "packs.json").write_text(
        json.dumps(merged_packs, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    for doc in docs.values():
        doc.close()

    print(f"Imported {len(exercises_out)} mat exercises")
    print(f"Total exercises: {len(merged_exercises)}")
    for ex_item in exercises_out:
        print(f"  - {ex_item['nameEn']} ({len(ex_item['images'])} images)")


if __name__ == "__main__":
    asyncio.run(main())
