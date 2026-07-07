#!/usr/bin/env python3
"""Generate full anatomy concepts + chapter structure from Emma book (66 pages)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "public/data/anatomy"

P1 = "ch01-tong-quan"
P2 = "ch02-xuong"
P3 = "ch03-khop"
P4 = "ch04-van-dong"
P5 = "ch05-mac-co"
P6 = "ch06-dia-dem"
P7 = "ch07-chi-tren"
P8 = "ch08-phan-than"
P9 = "ch09-khung-chau"

CONCEPTS: list[dict] = []


def c(
    id: str,
    term: str,
    term_vi: str,
    definition: str,
    pack_id: str,
    section: str,
    aliases: list[str] | None = None,
    page: int | None = None,
) -> dict:
    item = {
        "id": id,
        "term": term,
        "termVi": term_vi,
        "definition": definition,
        "category": section,
        "packId": pack_id,
        "section": section,
    }
    if aliases:
        item["aliases"] = aliases
    if page:
        item["pageRef"] = page
    return item


def muscle(
    mid: str,
    en: str,
    vi: str,
    origin: str,
    insertion: str,
    action: str,
    pack: str,
    section: str,
    page: int | None = None,
    aliases: list[str] | None = None,
) -> dict:
    al = [vi.lower(), en.lower(), *(aliases or [])]
    return c(
        mid,
        en,
        vi,
        f"Nguyên ủy: {origin}. Bám tận: {insertion}. Hành động: {action}",
        pack,
        section,
        al,
        page,
    )


# ══════════════════════════════════════════════════════════════
# CH I — Tổng quan cấu tạo cơ thể (trang 1–10)
# ══════════════════════════════════════════════════════════════
S1 = "Các cấp độ cơ thể"
CONCEPTS += [
    c("cap-hoa-hoc", "Cấp độ hóa học", "Chemical level", "Cấp thấp nhất: nguyên tử và phân tử.", P1, S1, page=1),
    c("nguyen-tu", "Nguyên tử", "Atom", "Đơn vị nhỏ nhất của nguyên tố hóa học. Cơ thể người gồm 26 nguyên tố (C, H, N, O…).", P1, S1, ["atom"], 1),
    c("phan-tu", "Phân tử", "Molecule", "Kết hợp nhiều nguyên tử, ví dụ H₂O, ADN.", P1, S1, ["molecule", "adn", "dna"], 1),
    c("cap-te-bao", "Cấp độ tế bào", "Cellular level", "Đơn vị cơ bản và nền tảng của mọi thực thể sống.", P1, S1, page=2),
    c("te-bao", "Tế bào", "Cell", "Cơ thể người có hơn 10 nghìn tỷ tế bào.", P1, S1, ["cell"], 2),
    c("te-bao-hong-cau", "Tế bào hồng cầu", "Red blood cell", "Vận chuyển oxy trong máu.", P1, S1, page=2),
    c("te-bao-than-kinh", "Tế bào thần kinh", "Neuron", "Tế bào truyền tín hiệu thần kinh.", P1, S1, ["neuron"], 2),
    c("te-bao-bieu-mo", "Tế bào biểu mô", "Epithelial cell", "Lớp tế bào phủ bề mặt và tuyến.", P1, S1, page=2),
    c("te-bao-co-tron", "Tế bào cơ trơn", "Smooth muscle cell", "Tế bào cơ không ý thức kiểm soát được.", P1, S1, page=2),
    c("cap-mo", "Cấp độ mô", "Tissue level", "Nhiều tế bào cùng loại tạo thành mô.", P1, S1, page=2),
    c("mo-bieu-mo", "Biểu mô", "Epithelium", "Mô phân tách cơ quan và môi trường bên ngoài.", P1, S1, page=2),
    c("mo-lien-ket", "Mô liên kết", "Connective tissue", "Mô nối, bao bọc, hỗ trợ các cấu trúc.", P1, S1, page=2),
    c("mo-co", "Mô cơ", "Muscle tissue", "Mô tạo lực co và vận động.", P1, S1, page=2),
    c("mo-than-kinh", "Mô thần kinh", "Nervous tissue", "Mô truyền và xử lý tín hiệu.", P1, S1, page=2),
    c("co-quan", "Cơ quan", "Organ", "Nhiều mô phối hợp: tim, phổi, gan, não, thực quản…", P1, S1, ["organ"], 3),
    c("he-co-quan", "Hệ cơ quan", "Organ system", "Nhiều cơ quan cùng chức năng: hệ cơ, xương, thần kinh, hô hấp, tiêu hóa…", P1, S1, page=3),
    c("co-the", "Cơ thể", "Organism", "Toàn bộ cơ thể sống hoàn chỉnh.", P1, S1, page=3),
]

S_POS = "Tư thế & hướng giải phẫu"
CONCEPTS += [
    c("tu-the-giai-phau", "Tư thế giải phẫu", "Anatomical position", "Đứng thẳng, hai chân, tay buông xuôi, mắt và lòng bàn tay hướng trước.", P1, S_POS, ["anatomical position"], 5),
    c("phia-tren", "Phía trên", "Superior", "Hướng về phía đầu.", P1, S_POS, ["superior"], 5),
    c("phia-duoi", "Phía dưới", "Inferior", "Hướng về phía bàn chân.", P1, S_POS, ["inferior"], 5),
    c("phia-truoc", "Phía trước", "Anterior", "Mặt trước cơ thể.", P1, S_POS, ["anterior"], 5),
    c("phia-sau", "Phía sau", "Posterior", "Mặt sau cơ thể.", P1, S_POS, ["posterior"], 5),
    c("ben-trai", "Trái", "Left", "Phía trái của cơ thể.", P1, S_POS, ["left"], 5),
    c("ben-phai", "Phải", "Right", "Phía phải của cơ thể.", P1, S_POS, ["right"], 5),
]

S_MP = "Mặt phẳng giải phẫu"
CONCEPTS += [
    c("mp-nam-ngang", "Mặt phẳng nằm ngang", "Transverse plane", "Chia cơ thể thành phần trên và dưới. Hành động: xoay vặn.", P1, S_MP, ["transverse"], 6),
    c("hanh-dong-xoay", "Xoay vặn", "Rotation", "Hành động trên mặt phẳng nằm ngang: xoay tay trong/ngoài, vặn cột sống, giang/khép vai ngang.", P1, S_MP, page=7),
    c("mp-dung-ngang", "Mặt phẳng đứng ngang", "Frontal plane", "Chia cơ thể thành phần trước và sau. Hành động: giang, khép, nghiêng.", P1, S_MP, ["frontal", "coronal"], 6),
    c("hanh-dong-giang", "Giang", "Abduction", "Di chuyển ra xa đường giữa cơ thể (mặt phẳng đứng ngang).", P1, S_MP, ["abduction"], 8),
    c("hanh-dong-khep", "Khép", "Adduction", "Di chuyển về gần đường giữa cơ thể (mặt phẳng đứng ngang).", P1, S_MP, ["adduction"], 8),
    c("hanh-dong-nghieng", "Nghiêng", "Lateral flexion", "Nghiêng cột sống hoặc thân sang một bên.", P1, S_MP, ["lateral flexion"], 8),
    c("mp-dung-doc", "Mặt phẳng đứng dọc", "Sagittal plane", "Chia cơ thể thành trái và phải. Hành động: gập, duỗi.", P1, S_MP, ["sagittal"], 6),
    c("hanh-dong-gap", "Gập", "Flexion", "Giảm góc giữa hai phần cơ thể (mặt phẳng đứng dọc).", P1, S_MP, ["flexion"], 9),
    c("hanh-dong-duoi", "Duỗi", "Extension", "Tăng góc giữa hai phần cơ thể (mặt phẳng đứng dọc).", P1, S_MP, ["extension"], 9),
]

# ══════════════════════════════════════════════════════════════
# CH II — Xương (trang 11–13)
# ══════════════════════════════════════════════════════════════
CONCEPTS += [
    c("206-xuong", "206 xương chính", "206 main bones", "Số xương chính cơ thể người trưởng thành.", P2, "Cấu tạo xương", ["206"], 11),
    c("xuong-truc", "Xương trục", "Axial skeleton", "Xương sọ, cột sống, sườn, ức.", P2, "Cấu tạo xương", ["axial"], 11),
    c("xuong-treo", "Xương treo", "Appendicular skeleton", "Chi trên, chi dưới, xương chậu.", P2, "Cấu tạo xương", ["appendicular"], 11),
    c("xuong-vun", "Xương vụn", "Sesamoid/small bones", "Nhiều xương vụn rải rác, không tính vào 206 xương chính.", P2, "Cấu tạo xương", page=11),
    c("xuong-dai", "Xương dài", "Long bone", "Ví dụ xương đùi (femur).", P2, "Phân loại xương", ["long bone", "femur"], 12),
    c("xuong-ngan", "Xương ngắn", "Short bone", "Ví dụ các xương cổ chân (tarsals).", P2, "Phân loại xương", ["short bone"], 12),
    c("xuong-det", "Xương dẹt", "Flat bone", "Ví dụ xương ức (sternum).", P2, "Phân loại xương", ["flat bone", "sternum"], 12),
    c("xuong-bat-dinh", "Xương bất định hình", "Irregular bone", "Ví dụ đốt sống (vertebra).", P2, "Phân loại xương", ["irregular bone"], 12),
    c("xuong-vung", "Xương vừng", "Sesamoid bone", "Ví dụ bánh chè (patella).", P2, "Phân loại xương", ["sesamoid", "patella"], 12),
    c("xn-nang-do", "Nâng đỡ, bảo vệ", "Support & protection", "Xương bảo vệ tủy sống, não, tim-phổi trong lồng ngực.", P2, "Chức năng xương", page=13),
    c("xn-van-dong", "Vận động (xương)", "Movement", "Xương nối cơ qua gân, hoạt động như đòn bẩy tại khớp; nối nhau bằng dây chằng.", P2, "Chức năng xương", page=13),
    c("xn-san-xuat-mau", "Sản xuất máu", "Blood production", "Tủy đỏ xương sản xuất hồng cầu.", P2, "Chức năng xương", page=13),
    c("xn-du-tru", "Dự trữ khoáng chất", "Mineral storage", "Xương dự trữ canxi, phốt pho và khoáng chất thiết yếu.", P2, "Chức năng xương", page=13),
]

S_XUONG = "Xương chính trên cơ thể"
BONES = [
    ("xuong-so", "Skull", "Xương sọ", "Bảo vệ não bộ.", 13),
    ("xuong-ham-duoi", "Mandible", "Xương hàm dưới", "Xương hàm dưới.", 13),
    ("cot-song", "Spine", "Cột sống", "Trục chính của cơ thể.", 13),
    ("dot-song-co", "Cervical vertebrae", "Đốt sống cổ C1–C7", "7 đốt sống cổ.", 13),
    ("dot-song-nguc", "Thoracic vertebrae", "Đốt sống ngực T1–T12", "12 đốt sống ngực.", 13),
    ("dot-song-lung", "Lumbar vertebrae", "Đốt sống lưng L1–L5", "5 đốt sống thắt lưng.", 13),
    ("xuong-cung", "Sacrum", "Xương cùng", "Nối cột sống với xương chậu.", 13),
    ("xuong-cut", "Coccyx", "Xương cụt", "Đuôi cột sống.", 13),
    ("xuong-do", "Clavicle", "Xương đòn", "Nối vai với thân.", 13),
    ("xuong-uc", "Sternum", "Xương ức", "Xương giữa ngực.", 13),
    ("xuong-suon", "Ribs", "Xương sườn", "Tạo lồng ngực.", 13),
    ("xuong-bai-vai", "Scapula", "Xương bả vai", "Xương vai phía sau.", 13),
    ("xuong-canh-tay", "Humerus", "Xương cánh tay", "Xương cánh tay trên.", 13),
    ("xuong-quay", "Radius", "Xương quay", "Xương cẳng tay bên ngón cái.", 13),
    ("xuong-tru", "Ulna", "Xương trụ", "Xương cẳng tay bên ngón út.", 13),
    ("xuong-chau", "Pelvis", "Xương chậu", "Khung chậu nối cột sống với chi dưới.", 13),
    ("xuong-dui", "Femur", "Xương đùi", "Xương dài nhất cơ thể.", 13),
    ("xuong-banh-che", "Patella", "Xương bánh chè", "Xương vừng bảo vệ khớp gối.", 13),
    ("xuong-chay", "Tibia", "Xương chày", "Xương cẳng chân trong.", 13),
    ("xuong-mac", "Fibula", "Xương mác", "Xương cẳng chân ngoài.", 13),
]
for bid, en, vi, desc, pg in BONES:
    CONCEPTS.append(c(bid, en, vi, desc, P2, S_XUONG, [vi.lower()], pg))

# ══════════════════════════════════════════════════════════════
# CH III — Khớp (trang 14–24)
# ══════════════════════════════════════════════════════════════
CONCEPTS += [
    c("khop-dinh-nghia", "Khớp", "Joint", "Điểm kết nối giữa hai hoặc nhiều xương. Ví dụ: cổ tay, vai, hông, gối.", P3, "Hệ thống khớp", page=14),
    c("khop-dong", "Khớp động", "Synovial joint", "Cử động dễ dàng; hai đầu có sụn trơn, dịch khớp và dây chằng.", P3, "Phân loại theo tầm vận động", ["khớp hoạt dịch"], 15),
    c("khop-ban-dong", "Khớp bán động", "Cartilaginous joint", "Cử động hạn chế; giữa hai đầu xương có đĩa sụn. Ví dụ: đốt sống.", P3, "Phân loại theo tầm vận động", page=15),
    c("khop-bat-dong", "Khớp bất động", "Fibrous joint", "Không cử động; nối xương bằng đường răng cưa sít nhau. Ví dụ: hộp sọ.", P3, "Phân loại theo tầm vận động", page=15),
    c("khop-hoat-dich", "Khớp hoạt dịch", "Synovial joint structure", "Loại khớp phổ biến nhất; có khoang khớp chứa dịch khớp.", P3, "Cấu tạo khớp hoạt dịch", page=16),
    c("sun-khop", "Sụn khớp", "Articular cartilage", "Lớp sụn trơn bao phủ đầu xương.", P3, "Cấu tạo khớp hoạt dịch", page=16),
    c("day-chang", "Dây chằng", "Ligament", "Sợi liên kết bao quanh và ổn định khớp.", P3, "Cấu tạo khớp hoạt dịch", page=16),
    c("mang-hoat-dich", "Màng hoạt dịch", "Synovial membrane", "Lớp màng lót bên trong bao khớp.", P3, "Cấu tạo khớp hoạt dịch", page=16),
    c("khoang-hoat-dich", "Khoang hoạt dịch", "Synovial cavity", "Khoang chứa dịch khớp giữa hai mặt khớp.", P3, "Cấu tạo khớp hoạt dịch", page=16),
    c("dich-khop", "Dịch khớp", "Synovial fluid", "Chất lỏng trong khoang khớp, bôi trơn chuyển động.", P3, "Cấu tạo khớp hoạt dịch", page=16),
    c("khop-truc", "Khớp trục", "Pivot joint", "Xoay quanh một trục. Ví dụ: C1–C2, khớp quay–trụ.", P3, "6 loại khớp hoạt dịch", ["pivot joint"], 17),
    c("khop-ban-le", "Khớp bản lề", "Hinge joint", "Chỉ gập và duỗi. Ví dụ: khuỷu, gối.", P3, "6 loại khớp hoạt dịch", ["hinge joint"], 17),
    c("khop-yen-ngua", "Khớp yên ngựa", "Saddle joint", "Gập-duỗi, dạng-khép, xoay nhẹ. Ví dụ: khớp ngón cái–cổ tay.", P3, "6 loại khớp hoạt dịch", ["saddle joint"], 17),
    c("khop-truot", "Khớp trượt", "Plane/Gliding joint", "Mặt phẳng trượt qua nhau. Ví dụ: đốt chân, mặt lồi đốt sống.", P3, "6 loại khớp hoạt dịch", ["plane joint", "gliding joint"], 17),
    c("khop-loi-cau", "Khớp lồi cầu", "Condyloid joint", "Lên-xuống và sang hai bên, không xoay. Ví dụ: cổ tay.", P3, "6 loại khớp hoạt dịch", ["condyloid joint"], 17),
    c("khop-o-cau", "Khớp ổ-cầu", "Ball-and-socket joint", "Phạm vi chuyển động rộng nhất. Ví dụ: hông, vai.", P3, "6 loại khớp hoạt dịch", ["ball and socket"], 17),
    c("c1-atlas", "Đốt cổ C1 (Atlas)", "Atlas (C1)", "Đốt sống cổ 1; quay quanh C2 để xoay đầu.", P3, "Ví dụ khớp trục", ["atlas"], 18),
    c("c2-axis", "Đốt cổ C2 (Axis)", "Axis (C2)", "Đốt sống cổ 2; trục xoay cho C1.", P3, "Ví dụ khớp trục", ["axis"], 18),
    c("khop-quay-tru", "Khớp quay–trụ", "Radioulnar joint", "Xương quay xoay quanh xương trụ để sấp/ngửa bàn tay.", P3, "Ví dụ khớp trục", page=18),
    c("khop-khuyu", "Khớp khuỷu", "Elbow joint", "Khớp bản lề: chỉ gập và duỗi.", P3, "Ví dụ khớp bản lề", page=19),
    c("khop-goi", "Khớp gối", "Knee joint", "Khớp bản lề lớn nhất cơ thể.", P3, "Ví dụ khớp bản lề", page=19),
    c("khop-ngon-cai", "Khớp ngón cái–cổ tay", "CMC thumb joint", "Khớp yên ngựa: gập-duỗi, dạng-khép, xoay nhẹ (cầm bút).", P3, "Ví dụ khớp yên ngựa", page=20),
    c("facet-joint", "Khớp mặt lồi", "Facet joint", "Giữa mỏm phụ hai đốt sống liền kề; trượt để gập/duỗi cột sống.", P3, "Ví dụ khớp trượt", ["facet"], 21),
    c("khop-co-tay", "Khớp lồi cầu cổ tay", "Wrist condyloid", "Cho phép lên-xuống và sang hai bên, không xoay.", P3, "Ví dụ khớp lồi cầu", page=22),
    c("khop-hong", "Khớp hông", "Hip joint", "Khớp ổ-cầu: xương đùi (quả cầu) + xương chậu (ổ cắm).", P3, "Ví dụ khớp ổ-cầu", page=23),
    c("khop-vai", "Khớp vai", "Shoulder joint", "Khớp ổ chảo–cánh tay (glenohumeral); phạm vi ROM rộng.", P3, "Ví dụ khớp ổ-cầu", page=23),
    c("rom-dinh-nghia", "ROM", "Range of Motion", "Góc độ khớp có thể di chuyển theo các hướng; quan trọng trong Pilates.", P3, "ROM khớp", ["tầm vận động"], 24),
    c("rom-vai-gap", "Gập vai 180°", "Shoulder flexion 180°", "Góc gập vai tối đa trong mặt phẳng đứng dọc.", P3, "ROM khớp", page=24),
    c("rom-vai-duoi", "Duỗi vai 50°", "Shoulder extension 50°", "Góc duỗi vai tối đa phía sau.", P3, "ROM khớp", page=24),
    c("rom-cot-gap", "Gập cột sống 75°", "Spinal flexion 75°", "Góc gập cột sống tối đa (mặt phẳng đứng dọc).", P3, "ROM khớp", page=24),
    c("rom-cot-duoi", "Duỗi cột sống 30°", "Spinal extension 30°", "Góc duỗi cột sống tối đa.", P3, "ROM khớp", page=24),
    c("rom-cot-nghieng", "Nghiêng cột sống 35°", "Lateral flexion 35°", "Góc nghiêng cột sống sang bên tối đa.", P3, "ROM khớp", page=24),
    c("rom-goi-gap", "Gập gối 140°", "Knee flexion 140°", "Góc gập gối tối đa khi nằm ngửa.", P3, "ROM khớp", page=24),
]

# ══════════════════════════════════════════════════════════════
# CH IV — Phạm vi chuyển động (trang 25–31)
# ══════════════════════════════════════════════════════════════
CONCEPTS += [
    c("arom", "AROM", "Active ROM", "Chuyển động chủ động — người tập tự thực hiện, không lực ngoài.", P4, "AROM & PROM", ["phạm vi chuyển động chủ động"], 25),
    c("prom", "PROM", "Passive ROM", "Chuyển động thụ động — do người khác hoặc máy tác động.", P4, "AROM & PROM", ["phạm vi chuyển động thụ động"], 25),
    c("rom-linh-hoat", "Tính linh hoạt", "Flexibility", "ROM liên quan đến độ linh hoạt của khớp và cơ.", P4, "Ứng dụng Pilates", page=24),
    c("rom-on-dinh", "Tính ổn định", "Stability", "Cân bằng giữa linh hoạt và ổn định khi tập Pilates.", P4, "Ứng dụng Pilates", page=24),
]

S_ROM_CS = "ROM cột sống theo đoạn"
ROM_SPINE = [
    ("rom-cs-gap-co", "Gập cột sống cổ 60°", "Cervical flexion 60°", "Góc gập tối đa đoạn cổ.", 26),
    ("rom-cs-gap-nguc", "Gập cột sống ngực 45°", "Thoracic flexion 45°", "Góc gập tối đa đoạn ngực.", 26),
    ("rom-cs-gap-lung", "Gập cột sống thắt lưng 40°", "Lumbar flexion 40°", "Góc gập tối đa đoạn thắt lưng.", 26),
    ("rom-cs-duoi-co", "Duỗi cột sống cổ 75°", "Cervical extension 75°", "Góc duỗi tối đa đoạn cổ.", 26),
    ("rom-cs-duoi-nguc", "Duỗi cột sống ngực 25°", "Thoracic extension 25°", "Góc duỗi tối đa đoạn ngực.", 26),
    ("rom-cs-duoi-lung", "Duỗi cột sống thắt lưng 35°", "Lumbar extension 35°", "Góc duỗi tối đa đoạn thắt lưng.", 26),
    ("rom-cs-nghieng-co", "Nghiêng cột sống cổ 45°", "Cervical lateral flexion 45°", "Góc nghiêng tối đa đoạn cổ.", 26),
    ("rom-cs-nghieng-nguc", "Nghiêng cột sống ngực 20°", "Thoracic lateral flexion 20°", "Góc nghiêng tối đa đoạn ngực.", 26),
    ("rom-cs-nghieng-lung", "Nghiêng cột sống thắt lưng 20°", "Lumbar lateral flexion 20°", "Góc nghiêng tối đa đoạn thắt lưng.", 26),
    ("rom-cs-xoay-co", "Xoay cột sống cổ 50°", "Cervical rotation 50°", "Góc xoay tối đa đoạn cổ.", 26),
    ("rom-cs-xoay-nguc", "Xoay cột sống ngực 35°", "Thoracic rotation 35°", "Góc xoay tối đa đoạn ngực.", 26),
    ("rom-cs-xoay-lung", "Xoay cột sống thắt lưng 5°", "Lumbar rotation 5°", "Góc xoay tối đa đoạn thắt lưng — rất hạn chế.", 26),
]
for rid, en, vi, desc, pg in ROM_SPINE:
    CONCEPTS.append(c(rid, en, vi, desc, P4, S_ROM_CS, [vi.lower()], pg))

# ══════════════════════════════════════════════════════════════
# CH V — Mạc cơ & vai (trang 32–50)
# ══════════════════════════════════════════════════════════════
CONCEPTS += [
    c("mac-co", "Mạc cơ", "Fascia", "Lớp mô liên kết mỏng dai bao quanh, ngăn cách và liên kết các bó cơ với xương, gân, da.", P5, "Mạc cơ", ["fascia"], 32),
    c("mac-nguc-that-lung", "Mạc ngực-thắt lưng", "Thoracolumbar fascia", "Mạc sâu vùng lưng dưới; ổn định cột sống, truyền lực cơ học.", P5, "Mạc cơ", ["thoracolumbar fascia"], 32),
    c("rotator-cuff", "Rotator cuff", "Chóp xoay", "Nhóm 4 cơ vai giữ ổn định khớp vai, tránh trật khớp.", P5, "Chóp xoay", ["chóp xoay"], 40),
    c("co-duoi-vai", "Cơ dưới vai", "Subscapularis", "Chóp xoay — mặt trước xương bả vai, xoay trong.", P5, "Chóp xoay", page=40),
    c("co-tren-gai", "Cơ trên gai", "Supraspinatus", "Chóp xoay — hố trên gai; bắt đầu dạng tay 0–15°.", P5, "Chóp xoay", page=40),
    c("co-duoi-gai", "Cơ dưới gai", "Infraspinatus", "Chóp xoay — hố dưới gai; xoay ngoài.", P5, "Chóp xoay", page=40),
    c("co-tron-be", "Cơ tròn bé", "Teres minor", "Chóp xoay — xoay ngoài, khép tay nhẹ.", P5, "Chóp xoay", page=40),
    c("chop-xoay-y-nghia", "Vai trò chóp xoay", "Rotator cuff function", "Nếu yếu → vai dễ lệch, đau, viêm.", P5, "Chóp xoay", page=40),
]

# ══════════════════════════════════════════════════════════════
# CH VI — Đĩa đệm & Pilates (trang 51–53)
# ══════════════════════════════════════════════════════════════
CONCEPTS += [
    c("dia-dem", "Đĩa đệm", "Intervertebral disc", "Đệm giữa các đốt sống, hấp thụ chấn động.", P6, "Bệnh lý cột sống", page=51),
    c("nhan-nhay", "Nhân nhầy", "Nucleus pulposus", "Phần gel bên trong đĩa đệm.", P6, "Bệnh lý cột sống", page=51),
    c("vong-soi", "Vòng sợi", "Annulus fibrosus", "Bao xơ bao quanh nhân nhầy.", P6, "Bệnh lý cột sống", ["bao xơ"], 51),
    c("thoat-vi-dia-dem", "Thoát vị đĩa đệm", "Herniated disc", "Nhân nhầy lệch/phình ra ngoài vòng sợi, chèn rễ thần kinh hoặc tủy sống.", P6, "Bệnh lý cột sống", ["herniated disc"], 51),
    c("dia-dem-binh-thuong", "Đĩa đệm bình thường", "Normal disc", "Nhân nhầy nằm gọn trong vòng sợi, không chèn ép dây thần kinh.", P6, "Bệnh lý cột sống", page=51),
    c("khoi-thoat-vi", "Khối thoát vị", "Herniated mass", "Phần nhân nhầy tràn ra ngoài vòng sợi.", P6, "Bệnh lý cột sống", page=51),
    c("tranh-gap-sau", "Gập cột sống quá mức", "Excessive flexion", "Tránh Roll Up, Roll Over, Teaser, The Hundred khi thoát vị.", P6, "Pilates & thoát vị", page=53),
    c("tranh-xoay", "Xoay cột sống quá mạnh", "Excessive rotation", "Tránh Spine Twist, Saw, Corkscrew.", P6, "Pilates & thoát vị", page=53),
    c("tranh-gap-xoay", "Gập + xoay đồng thời", "Flexion + rotation", "Tránh Criss-Cross, Obliques classic — nguy hiểm nhất.", P6, "Pilates & thoát vị", page=53),
    c("tranh-nang-2-chan", "Nâng hai chân cùng lúc", "Double leg lifts", "Tránh Double Leg Stretch, Leg Circles 2 chân khi lõi yếu.", P6, "Pilates & thoát vị", page=53),
    c("tranh-uan-qua", "Tư thế ưỡn quá mức", "Hyperextension", "Tránh Swan Dive, Swimming sai kỹ thuật.", P6, "Pilates & thoát vị", page=53),
]

# ══════════════════════════════════════════════════════════════
# CH VII — Cơ chi trên (trang 54–58)
# ══════════════════════════════════════════════════════════════
S_CT = "Bảng cơ chi trên"
UPPER_MUSCLES = [
    ("co-delta", "Deltoid", "Cơ delta", "X. đòn, mỏm cùng vai, gai vai", "Mấu động lớn x. cánh tay", "Dạng, gấp, duỗi, xoay tay", 54),
    ("co-nhi-dau", "Biceps brachii", "Cơ nhị đầu cánh tay", "Đầu dài: ổ chảo; đầu ngắn: mỏm quạ", "Lồi củ x. quay", "Gập khuỷu, ngửa cẳng, hỗ trợ gập vai", 54),
    ("co-tam-dau", "Triceps brachii", "Cơ tam đầu cánh tay", "Đầu dài: x. vai; 2 đầu: x. cánh tay", "Mỏm khuỷu x. trụ", "Duỗi khuỷu, hỗ trợ duỗi vai", 54),
    ("co-canh-tay-truoc", "Brachialis", "Cơ cánh tay trước", "1/2 dưới x. cánh tay", "Mỏm chỏm x. trụ", "Gập khuỷu (mạnh hơn nhị đầu)", 55),
    ("co-ngua", "Supinator", "Cơ ngửa", "Mỏm lồi cầu ngoài và x. trụ", "Mặt ngoài x. quay", "Ngửa cẳng tay", 55),
    ("co-sap-tron", "Pronator teres", "Cơ sấp tròn", "Mỏm trên lồi cầu trong", "Giữa mặt ngoài x. quay", "Sấp cẳng tay, hỗ trợ gập khuỷu", 55),
    ("co-gap-co-quay", "Flexor carpi radialis", "Cơ gấp cổ tay quay", "Mỏm trên lồi cầu trong", "Nền x. bàn tay II", "Gập cổ tay, dạng cổ tay", 56),
    ("co-duoi-co-quay", "Extensor carpi radialis longus", "Cơ duỗi cổ tay quay dài", "Mỏm trên lồi cầu ngoài", "Nền x. bàn tay II", "Duỗi cổ tay, dạng cổ tay", 56),
    ("co-nguc-lon", "Pectoralis major", "Cơ ngực lớn", "X. đòn, x. ức, sụn sườn", "Mào mấu động lớn", "Khép tay, xoay trong, gập vai", 56),
    ("co-lung-rong", "Latissimus dorsi", "Cơ lưng rộng", "Cột sống ngực–thắt lưng, mào chậu", "Rãnh gian củ x. cánh tay", "Duỗi, khép, xoay trong tay", 57),
    ("co-tren-gai-ct", "Supraspinatus", "Cơ trên gai", "Hố trên gai x. bả vai", "Mấu động lớn", "Bắt đầu dạng tay 0–15°", 57),
    ("co-duoi-gai-ct", "Infraspinatus", "Cơ dưới gai", "Hố dưới gai", "Mấu động lớn", "Xoay ngoài tay", 57),
    ("co-tron-be-ct", "Teres minor", "Cơ tròn bé", "Bờ ngoài x. bả vai", "Mấu động lớn", "Xoay ngoài, khép tay nhẹ", 58),
    ("co-duoi-vai-ct", "Subscapularis", "Cơ dưới vai", "Hố dưới vai (mặt trước x. bả vai)", "Mấu động nhỏ", "Xoay trong tay", 58),
    ("co-qua-canh-tay", "Coracobrachialis", "Cơ quạ – cánh tay", "Mỏm quạ", "Giữa thân x. cánh tay", "Gập vai, khép tay", 58),
]
for mid, en, vi, origin, insertion, action, pg in UPPER_MUSCLES:
    CONCEPTS.append(muscle(mid, en, vi, origin, insertion, action, P7, S_CT, pg))

# ══════════════════════════════════════════════════════════════
# CH VIII — Phần thân & core (trang 59–62)
# ══════════════════════════════════════════════════════════════
CONCEPTS += [
    c("phan-than", "Phần thân (Trunk)", "Trunk", "Vùng giữa cổ và chi dưới: cột sống, lồng ngực, ổ bụng–chậu, cơ xung quanh.", P8, "Phần thân", page=59),
    c("long-nguc", "Lồng ngực", "Rib cage", "Xương sườn + xương ức.", P8, "Phần thân", page=59),
    c("o-bung-chau", "Ổ bụng – chậu", "Abdominopelvic cavity", "Khoang bụng và vùng chậu.", P8, "Phần thân", page=59),
    c("trung-tam-tu-the", "Trung tâm tư thế", "Postural center", "Phần thân là trung tâm điều khiển tư thế, thăng bằng, chuyển động toàn thân.", P8, "Vai trò trong Pilates", page=59),
    c("truyen-luc-phan-than", "Truyền lực từ thân", "Force transmission", "Phần thân truyền lực cho tay chân hoạt động trơn tru.", P8, "Vai trò trong Pilates", page=59),
]

S_BUNG = "Nhóm cơ bụng"
ABS = [
    ("co-thang-bung", "Rectus abdominis", "Cơ thẳng bụng", "Chạy dọc giữa bụng (6 múi)", "Gập thân, ổn định khung chậu, ép bụng khi thở mạnh", 60),
    ("co-cheo-ngoai", "External oblique", "Cơ chéo ngoài", "Chéo từ ngoài xuống trong (chữ V ngược)", "Xoay thân ngược bên, nghiêng cùng bên, ép bụng", 60),
    ("co-cheo-trong", "Internal oblique", "Cơ chéo trong", "Chéo từ trong ra ngoài (chữ V)", "Xoay/nghiêng cùng bên, ép bụng, hỗ trợ thở ra", 60),
    ("co-ngang-bung", "Transversus abdominis", "Cơ ngang bụng", "Nằm ngang quanh eo, sâu nhất", "Siết bụng, ổn định cột sống–core, ép bụng mạnh", 60),
]
for aid, en, vi, pos, action, pg in ABS:
    CONCEPTS.append(c(aid, en, vi, f"Vị trí: {pos}. Chức năng: {action}", P8, S_BUNG, [vi.lower()], pg))

S_LUNG = "Nhóm cơ lưng (mặt sau)"
BACK_SUP = [
    ("co-thang", "Trapezius", "Cơ thang", "Nâng, hạ, xoay xương bả vai; giữ cổ–vai ổn định", 61),
    ("co-lung-rong-pt", "Latissimus dorsi", "Cơ lưng rộng", "Duỗi, khép, xoay trong cánh tay; kéo tay về sau", 61),
    ("co-nang-vai", "Levator scapulae", "Cơ nâng vai", "Nâng và xoay xương bả vai", 61),
    ("co-tram", "Rhomboids", "Cơ trám lớn/nhỏ", "Kéo xương bả vai vào trong, ổn định khi xoay tay", 61),
]
for bid, en, vi, action, pg in BACK_SUP:
    CONCEPTS.append(c(bid, en, vi, f"Chức năng: {action}", P8, S_LUNG, [vi.lower()], pg))

S_LUNG_SAU = "Cơ lưng lớp sâu"
BACK_DEEP = [
    ("co-vuong-that-lung", "Quadratus lumborum", "Cơ vuông thắt lưng", "Hai bên cột sống thắt lưng, nối sườn 12 và mào chậu", "Nghiêng thân, giữ thăng bằng thắt lưng–chậu", 62),
    ("co-dung-song", "Erector spinae", "Cơ dựng sống", "Dọc 2 bên cột sống từ cùng đến nền sọ", "Duỗi lưng, giữ thẳng cột sống, nghiêng và xoay nhẹ", 62),
    ("co-da-nhanh", "Multifidus", "Cơ đa nhánh", "Từ mỏm ngang/mỏm gai đốt sống phía trên", "Ổn định từng đốt sống, chống xoay quá mức", 62),
]
for bid, en, vi, pos, action, pg in BACK_DEEP:
    CONCEPTS.append(c(bid, en, vi, f"Vị trí: {pos}. Chức năng: {action}", P8, S_LUNG_SAU, [vi.lower()], pg))

# ══════════════════════════════════════════════════════════════
# CH IX — Khung chậu (trang 63–66)
# ══════════════════════════════════════════════════════════════
S_CHAU = "Cấu trúc khung chậu"
CONCEPTS += [
    c("khung-chau", "Khung chậu", "Pelvic girdle", "Xương chậu nối cột sống với chi dưới.", P9, S_CHAU, page=63),
    c("mao-chau", "Mào chậu", "Iliac crest", "Cạnh cong trên cùng xương chậu.", P9, S_CHAU, page=63),
    c("eo-tren", "Eo trên", "Pelvic inlet", "Lỗ mở phía trên khung chậu.", P9, S_CHAU, page=63),
    c("khop-hong-kc", "Khớp hông", "Hip joint", "Khớp giữa xương đùi và xương chậu.", P9, S_CHAU, page=63),
    c("gai-lu-ngoi", "Gai lụ ngồi", "Ischial spine", "Mỏm xương phía sau khung chậu.", P9, S_CHAU, page=63),
    c("u-ngoi", "Ụ ngồi", "Ischial tuberosity", "Xương ngồi — điểm bám khi ngồi.", P9, S_CHAU, page=63),
    c("xuong-mu", "Xương mu", "Pubis", "Phần trước khung chậu.", P9, S_CHAU, page=63),
    c("khop-mu", "Khớp mu", "Pubic symphysis", "Khớp nối hai nửa xương mu phía trước.", P9, S_CHAU, page=63),
    c("chong-do-trong-luong", "Chống đỡ trọng lượng", "Weight bearing", "Khung chậu truyền tải trọng lượng từ cột sống xuống chi dưới.", P9, "Chức năng khung chậu", page=63),
    c("bao-ve-noi-tang", "Bảo vệ nội tạng chậu", "Organ protection", "Bao bọc bàng quang, tử cung, trực tràng.", P9, "Chức năng khung chậu", page=63),
    c("gam-co-chau", "Gắn kết cơ và dây chằng", "Muscle attachment", "Bám cơ mông, đùi, bụng dưới, sàn chậu.", P9, "Chức năng khung chậu", page=63),
]

S_CO_CHAU = "Cơ khung chậu"
CONCEPTS += [
    c("co-san-chau", "Cơ sàn chậu", "Pelvic floor", "Levator ani & Coccygeus — đáy chậu, nâng đỡ tạng, kiểm soát đại tiểu tiện.", P9, S_CO_CHAU, page=64),
    c("co-that-lung-chau", "Cơ thắt lưng–chậu", "Iliopsoas", "Psoas (cột sống) + Iliacus (cánh chậu) → x. đùi nhỏ; gập hông.", P9, S_CO_CHAU, ["iliopsoas"], 64),
]

S_CD_CHAU = "Chuyển động khung chậu"
CONCEPTS += [
    c("asis", "Gai chậu trước trên (ASIS)", "Anterior superior iliac spine", "Điểm mốc phía trước trên xương chậu.", P9, S_CD_CHAU, ["asis"], 65),
    c("kc-trung-tinh", "Khung chậu trung tính", "Neutral pelvis", "Tư thế cân bằng trên mặt phẳng đứng dọc.", P9, S_CD_CHAU, page=65),
    c("kc-nga-truoc", "Khung chậu ngả trước", "Anterior pelvic tilt", "Xương chậu nghiêng về trước, lưng dưới ưỡn.", P9, S_CD_CHAU, page=65),
    c("kc-nga-sau", "Khung chậu ngả sau", "Posterior pelvic tilt", "Xương chậu nghiêng về sau, mất đường cong sinh lý.", P9, S_CD_CHAU, page=65),
    c("kc-lech-ben", "Khung chậu lệch bên", "Lateral pelvic tilt", "Một bên chậu cao hơn bên kia (mặt phẳng đứng ngang).", P9, S_CD_CHAU, page=65),
    c("kc-xoay-van", "Khung chậu xoay vặn", "Pelvic rotation", "Một bên chậu xoay ra trước/sau (mặt phẳng nằm ngang).", P9, S_CD_CHAU, page=65),
]

S_SAI_LECH = "Sai lệch khung chậu"
CONCEPTS += [
    c("sl-nga-truoc", "Ngả trước — biểu hiện", "APT symptoms", "Tăng ưỡn thắt lưng, bụng trồi, mông vểnh; đau lưng dưới, căng gập hông.", P9, S_SAI_LECH, page=66),
    c("sl-nga-sau", "Ngả sau — biểu hiện", "PPT symptoms", "Cong lưng tròn, co cơ bụng/mông; giảm linh hoạt hông.", P9, S_SAI_LECH, page=66),
    c("sl-lech-ben", "Lệch bên — biểu hiện", "Lateral tilt symptoms", "Mất cân bằng hông–chân, lệch vai; đau gối, vai, cổ.", P9, S_SAI_LECH, page=66),
    c("sl-xoay", "Xoay khung chậu — biểu hiện", "Rotation symptoms", "Xoắn thân, lệch trục cột sống; căng một bên lưng/hông.", P9, S_SAI_LECH, page=66),
]

# ── Bổ sung trang còn thiếu ──
CONCEPTS += [
    # ROM hông (27)
    c("rom-hong-gap", "Gập hông 110–120°", "Hip flexion 110-120°", "Góc gập hông tối đa.", P4, "ROM khớp hông", page=27),
    c("rom-hong-duoi", "Duỗi hông 10–15°", "Hip extension 10-15°", "Góc duỗi hông tối đa.", P4, "ROM khớp hông", page=27),
    c("rom-hong-dang", "Dạng hông 45°", "Hip abduction 45°", "Góc dạng hông tối đa.", P4, "ROM khớp hông", page=27),
    c("rom-hong-khep", "Khép hông 15–25°", "Hip adduction 15-25°", "Góc khép hông tối đa.", P4, "ROM khớp hông", page=27),
    c("rom-hong-xoay-ngoai", "Xoay ngoài hông 40–60°", "Hip external rotation 40-60°", "Góc xoay ngoài hông tối đa.", P4, "ROM khớp hông", page=27),
    c("rom-hong-xoay-trong", "Xoay trong hông 30–45°", "Hip internal rotation 30-45°", "Góc xoay trong hông tối đa.", P4, "ROM khớp hông", page=27),
    # Mô liên kết chuyên biệt (28)
    c("gan", "Gân", "Tendon", "Mô liên kết chuyên biệt — nối cơ với xương.", P1, "Mô liên kết chuyên biệt", page=28),
    c("sun", "Sụn", "Cartilage", "Mô liên kết chuyên biệt — bao phủ mặt khớp.", P1, "Mô liên kết chuyên biệt", page=28),
    c("mo-mo", "Mô mỡ", "Adipose tissue", "Mô liên kết — dự trữ năng lượng, bảo vệ.", P1, "Mô liên kết chuyên biệt", page=28),
    # Phân loại cơ (33)
    c("co-tim", "Cơ tim", "Cardiac muscle", "Cơ có vân, co bất thường, không ý thức kiểm soát.", P5, "Phân loại cơ", page=33),
    c("co-xuong", "Cơ xương", "Skeletal muscle", "Có vân, bám xương qua gân, điều khiển tự ý; chiếm 40–50% khối lượng cơ thể.", P5, "Phân loại cơ", ["cơ vân"], 33),
    c("co-tron", "Cơ trơn", "Smooth muscle", "Không vân, ở ruột, mạch máu; không ý thức kiểm soát.", P5, "Phân loại cơ", page=33),
    # Khớp khuỷu chi tiết (43)
    c("khop-canh-tay-tru", "Khớp cánh tay–trụ", "Humeroulnar joint", "Khớp bản lề — gập/duỗi khuỷu.", P3, "Khớp khuỷu tay", page=43),
    c("khop-canh-tay-quay", "Khớp cánh tay–quay", "Humeroradial joint", "Hỗ trợ gập/duỗi và xoay nhẹ.", P3, "Khớp khuỷu tay", page=43),
    c("khop-quay-tru-gan", "Khớp quay–trụ gần", "Proximal radioulnar joint", "Khớp trục — sấp/ngửa cẳng tay.", P3, "Khớp khuỷu tay", page=43),
    c("tennis-elbow", "Viêm gân khuỷu ngoài", "Tennis elbow", "Đau vùng ngoài khuỷu (lateral epicondylitis).", P3, "Tổn thương khuỷu", page=43),
    c("golfer-elbow", "Viêm gân khuỷu trong", "Golfer's elbow", "Đau vùng trong khuỷu (medial epicondylitis).", P3, "Tổn thương khuỷu", page=43),
    # Cấu tạo đốt sống (48)
    c("than-dot-song", "Thân đốt sống", "Vertebral body", "Phần chịu lực nén của đốt sống.", P2, "Cấu tạo đốt sống", page=48),
    c("cung-dot-song", "Cung đốt sống", "Vertebral arch", "Bao quanh lỗ sống, bảo vệ tủy.", P2, "Cấu tạo đốt sống", page=48),
    c("mom-gai", "Mỏm gai", "Spinous process", "Mỏm nhô ra sau — điểm bám cơ.", P2, "Cấu tạo đốt sống", page=48),
    c("mom-ngang", "Mỏm ngang", "Transverse process", "Mỏm nhô ra hai bên.", P2, "Cấu tạo đốt sống", page=48),
    c("lo-song", "Lỗ sống", "Vertebral foramen", "Lỗ chứa tủy sống.", P2, "Cấu tạo đốt sống", page=48),
    c("chuc-nang-dot-song", "Chức năng đốt sống", "Vertebra function", "Chống đỡ, bảo vệ tủy, trục vận động, bám cơ–dây chằng.", P2, "Cấu tạo đốt sống", page=48),
    # Bệnh lý đĩa đệm khác (52)
    c("thoai-hoa-dia-dem", "Thoái hóa đĩa đệm", "Disc degeneration", "Đĩa đệm mỏng, mất nước, giảm đệm.", P6, "Bệnh lý cột sống", page=52),
    c("loi-dia-dem", "Lồi đĩa đệm", "Bulging disc", "Vòng sợi phình ra nhưng nhân nhầy chưa vỡ.", P6, "Bệnh lý cột sống", page=52),
    c("hep-dia-dem", "Hẹp đĩa đệm", "Disc narrowing", "Khoảng cách giữa đốt sống bị nén.", P6, "Bệnh lý cột sống", page=52),
    c("gai-xuong", "Gai xương", "Bone spur", "Thoái hóa kèm gai xương (osteophyte).", P6, "Bệnh lý cột sống", page=52),
    c("cot-song-quan-trong", "Tầm quan trọng cột sống", "Spine importance", "Trục chống đỡ, bảo vệ tủy sống, duy trì tư thế và chuyển động.", P6, "Bệnh lý cột sống", page=52),
    # Dây chằng (29)
    c("day-chang-dinh-nghia", "Dây chằng", "Ligament", "Mô liên kết collagen nối xương–xương, ổn định khớp, hạn chế ROM quá mức.", P3, "Dây chằng", ["ligament"], 29),
    c("day-chang-vs-gan", "Dây chằng vs Gân", "Ligament vs tendon", "Dây chằng ít đàn hồi hơn gân.", P3, "Dây chằng", page=29),
    c("acl", "Dây chằng chéo trước", "ACL", "Anterior cruciate ligament — ổn định khớp gối.", P3, "Dây chằng", page=29),
    c("lcl", "Dây chằng bên ngoài", "LCL", "Lateral collateral ligament — bên ngoài khớp gối.", P3, "Dây chằng", page=29),
    c("day-chang-mom-ngang", "Dây chằng mỏm ngang", "Intertransverse ligament", "Nối mỏm ngang hai đốt sống liền kề; hạn chế nghiêng bên.", P3, "Dây chằng", page=29),
    # Hình thức co cơ (36)
    c("co-dong-tam", "Co cơ đồng tâm", "Concentric contraction", "Cơ co và rút ngắn.", P5, "Hình thức co cơ", ["concentric"], 36),
    c("co-ly-tam", "Co cơ ly tâm", "Eccentric contraction", "Cơ co nhưng bị kéo dài.", P5, "Hình thức co cơ", ["eccentric"], 36),
    c("co-dang-truong", "Co cơ đẳng trường", "Isometric contraction", "Cơ co nhưng chiều dài không đổi.", P5, "Hình thức co cơ", ["isometric"], 36),
    # Bàn tay (44)
    c("27-xuong-ban-tay", "27 xương bàn tay", "27 hand bones", "Mỗi bàn tay: 8 cổ tay + 5 bàn + 14 đốt ngón.", P2, "Bàn tay & cổ tay", page=44),
    c("xuong-co-tay", "Xương cổ tay", "Carpal bones", "8 xương tạo khớp lồi cầu cổ tay.", P2, "Bàn tay & cổ tay", page=44),
    c("xuong-ban-tay", "Xương bàn tay", "Metacarpals", "5 xương bàn tay.", P2, "Bàn tay & cổ tay", page=44),
    c("xuong-doi-ngon", "Xương đốt ngón", "Phalanges", "14 xương đốt ngón (3 mỗi ngón, 2 ở ngón cái).", P2, "Bàn tay & cổ tay", page=44),
    # Bệnh lý cột sống (49)
    c("gu-lung", "Gù lưng", "Kyphosis", "Vai tròn, lưng cong — do cúi đầu lâu.", P6, "Bệnh lý cột sống", page=49),
    c("cong-veo", "Cong vẹo cột sống", "Scoliosis", "Cột sống cong sang bên; lệch vai, hông.", P6, "Bệnh lý cột sống", ["scoliosis"], 49),
    c("truot-dot-song", "Trượt đốt sống", "Spondylolisthesis", "Đốt sống trượt về phía trước.", P6, "Bệnh lý cột sống", page=49),
    c("piriformis", "Hội chứng cơ hình lê", "Piriformis syndrome", "Đau mông lan chân; dễ nhầm thoát vị.", P6, "Bệnh lý cột sống", page=49),
    c("co-vai-gay", "Hội chứng cổ vai gáy", "Neck-shoulder syndrome", "Đau vai gáy, tê tay — do cúi điện thoại, ngồi sai.", P6, "Bệnh lý cột sống", page=49),
]

# ── Packs ──
PACKS = [
    {
        "id": P1,
        "name": "I. Tổng quan cấu tạo cơ thể",
        "description": "Trang 1–10 · Cấp độ, tế bào, mô, tư thế, mặt phẳng",
        "pageRange": [1, 10],
        "conceptIds": [x["id"] for x in CONCEPTS if x["packId"] == P1],
        "diagramIds": [],
    },
    {
        "id": P2,
        "name": "II. Cấu tạo & chức năng xương",
        "description": "Trang 11–13, 48 · Phân loại, chức năng, xương, đốt sống",
        "pageRange": [11, 13],
        "conceptIds": [x["id"] for x in CONCEPTS if x["packId"] == P2],
        "diagramIds": [],
    },
    {
        "id": P3,
        "name": "III. Hệ thống khớp",
        "description": "Trang 14–24 · Phân loại, 6 loại khớp, ROM",
        "pageRange": [14, 24],
        "conceptIds": [x["id"] for x in CONCEPTS if x["packId"] == P3],
        "diagramIds": [],
    },
    {
        "id": P4,
        "name": "IV. Phạm vi chuyển động",
        "description": "Trang 25–31 · AROM, PROM, ROM cột sống & hông",
        "pageRange": [25, 31],
        "conceptIds": [x["id"] for x in CONCEPTS if x["packId"] == P4],
        "diagramIds": [],
    },
    {
        "id": P5,
        "name": "V. Mạc cơ & chóp xoay",
        "description": "Trang 32–50 · Fascia, rotator cuff",
        "pageRange": [32, 50],
        "conceptIds": [x["id"] for x in CONCEPTS if x["packId"] == P5],
        "diagramIds": [],
    },
    {
        "id": P6,
        "name": "VI. Đĩa đệm & Pilates",
        "description": "Trang 51–53 · Thoát vị, thoái hóa, động tác tránh",
        "pageRange": [51, 53],
        "conceptIds": [x["id"] for x in CONCEPTS if x["packId"] == P6],
        "diagramIds": [],
    },
    {
        "id": P7,
        "name": "VII. Cơ chi trên",
        "description": "Trang 54–58 · 15 cơ — nguyên ủy, bám, hành động",
        "pageRange": [54, 58],
        "conceptIds": [x["id"] for x in CONCEPTS if x["packId"] == P7],
        "diagramIds": [],
    },
    {
        "id": P8,
        "name": "VIII. Phần thân & core",
        "description": "Trang 59–62 · Cơ bụng, cơ lưng",
        "pageRange": [59, 62],
        "conceptIds": [x["id"] for x in CONCEPTS if x["packId"] == P8],
        "diagramIds": [],
    },
    {
        "id": P9,
        "name": "IX. Khung chậu",
        "description": "Trang 63–66 · Cấu trúc, chuyển động, sai lệch",
        "pageRange": [63, 66],
        "conceptIds": [x["id"] for x in CONCEPTS if x["packId"] == P9],
        "diagramIds": [],
    },
]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "concepts.json").write_text(
        json.dumps(CONCEPTS, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (DATA / "packs.json").write_text(
        json.dumps(PACKS, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (DATA / "diagrams.json").write_text("[]\n", encoding="utf-8")

    pages_covered = sorted({x["pageRef"] for x in CONCEPTS if "pageRef" in x})
    print(f"Generated {len(CONCEPTS)} concepts in {len(PACKS)} chapters")
    print(f"Pages with concepts: {len(pages_covered)}/66")
    for p in PACKS:
        n = len(p["conceptIds"])
        print(f"  {p['name']}: {n}")


if __name__ == "__main__":
    main()
