import type {
  LessonBlock,
  LessonPlan,
  LessonSection,
  LessonTable,
} from "../types/lessonPlan";

const STORAGE_KEY = "pilates-lesson-plans-v1";

export const createId = () =>
  `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;

export const emptyTable = (cols = 2, rows = 2): LessonTable => ({
  cols,
  rows: Array.from({ length: rows }, () => Array.from({ length: cols }, () => "")),
});

export const createTextBlock = (content = ""): LessonBlock => ({
  id: createId(),
  type: "text",
  content,
});

export const createExerciseBlock = (
  name = "Động tác mới",
  note = "",
): LessonBlock => ({
  id: createId(),
  type: "exercise",
  name,
  note,
  table: emptyTable(2, 2),
});

export const createTableBlock = (caption = ""): LessonBlock => ({
  id: createId(),
  type: "table",
  caption,
  table: emptyTable(2, 2),
});

export const createSection = (title = "Phần mới"): LessonSection => ({
  id: createId(),
  title,
  blocks: [],
});

export const createEmptyPlan = (title = "Giáo án mới"): LessonPlan => {
  const now = new Date().toISOString();
  return {
    id: createId(),
    title,
    subtitle: "",
    createdAt: now,
    updatedAt: now,
    sections: [
      {
        id: createId(),
        title: "Khởi động",
        blocks: [createExerciseBlock()],
      },
    ],
  };
};

/** Mẫu theo file PDF Khởi động — rút gọn để HLV chỉnh tiếp. */
export const createSampleWarmupPlan = (): LessonPlan => {
  const now = new Date().toISOString();
  return {
    id: createId(),
    title: "Khởi động",
    subtitle: "Reformer — mẫu từ giáo án",
    createdAt: now,
    updatedAt: now,
    sections: [
      {
        id: createId(),
        title: "PHẦN CHÂN & MÔNG",
        blocks: [
          {
            id: createId(),
            type: "exercise",
            name: "Single Leg: Xe đạp",
            note: "",
            table: {
              cols: 2,
              rows: [
                [
                  "Set lò xo: 1 Đỏ + 1 Xanh (lực trung bình–nặng để đỡ chân). Nằm ngửa, đặt 1 đệm bàn chân lên footbar, chân còn lại nâng tabletop duỗi chéo.",
                  "Chuẩn bị — Hít sâu. Thở — Đẩy thẳng chân đỡ đi, đồng thời co chân trở về tabletop. Hít — Co chân đỡ thu giường về, đồng thời duỗi thẳng chân trở chéo góc.",
                ],
                [
                  "Đặt tay phía sau bàn chân để dẫn hướng mũi chân thẳng.",
                  "",
                ],
              ],
            },
          },
          {
            id: createId(),
            type: "exercise",
            name: "Single Thigh Stretch: Kéo giãn đùi đơn",
            note: "",
            table: {
              cols: 2,
              rows: [
                [
                  "1 Đỏ hoặc 1 Đỏ + 1 Xanh, lực vừa phải. Chống 1 gối trên giường sát shoulder rest, 1 chân đặt lên footbar. 2 tay nắm 2 đầu footbar. Hạ thấp mông.",
                  "Hạ hông xuống, chuẩn bị — Hít vào. Thở — Siết mông bụng, đẩy giường đi kéo giãn đùi sau. Hít — Từ từ thu giường về kiểm soát. Nhịp 10 đẩy giường ra xa, GIỮ LẠI: 3.2.1. Chầm chậm thu về.",
                ],
                [
                  "Tưởng tượng như ép đùi trước khi chạy bộ.",
                  "Cảm nhận giãn sâu đùi trước và cơ gập hông chân chống, siết nhẹ mông đùi sau.",
                ],
              ],
            },
          },
          {
            id: createId(),
            type: "exercise",
            name: "Side Split: Dạng chân",
            note: "",
            table: {
              cols: 2,
              rows: [
                [
                  "1 lò xo nhẹ. Đứng ngang trên Reformer, 1 chân trên đệm giường, 1 chân đặt ở platform. 2 tay dang ngang.",
                  "Dựng thẳng lưng, chuẩn bị — Hít sâu. Thở — Siết mông nhỡ, tách chân đẩy giường. Hít — Dùng đùi trong kéo giường về. Nhịp 10 tách rộng giữ thăng bằng, GIỮ: 3.2.1. Hít thu chân về.",
                ],
                [
                  "Giữ khớp hông thăng bằng, tránh xoay khớp hông vào trong.",
                  "Siết mông nhỡ ở đùi ngoài khi đẩy đi, siết đùi trong khi thu về. Lưng–hông luôn giữ thẳng trục đứng.",
                ],
              ],
            },
          },
        ],
      },
      {
        id: createId(),
        title: "PHẦN LƯNG & TAY",
        blocks: [
          {
            id: createId(),
            type: "exercise",
            name: "Airplane: Máy bay",
            note: "Long Box — tư thế cái cày / nằm sấp trên hộp",
            table: {
              cols: 2,
              rows: [
                [
                  "1 lò xo nhẹ. Đặt hộp dọc. Nằm sấp trên hộp, ngực nằm ngoài mép hộp, đầu hướng phía pulley, 2 chân rộng bằng mép hộp, cổ chân duỗi. 2 tay nắm dây rope.",
                  "Ổn định thân người — Hít sâu — Duỗi cột sống, nâng nhẹ người song song sàn. Thở — Siết lưng trên, kéo dây về phía hông, duỗi vai. Hít — Chậm đưa tay trở lại vuông góc sàn, hạ ngực nhẹ.",
                ],
                [
                  "Hướng lên phía gáy để dẫn khách vươn dài cổ và ngực về phía trước.",
                  "Siết bả vai, duỗi vai và cơ lưng trên, kéo dài toàn bộ cột sống từ gót chân đến đỉnh đầu.",
                ],
              ],
            },
          },
          {
            id: createId(),
            type: "exercise",
            name: "Triceps: Cơ tam đầu cánh tay — Bắp tay sau",
            note: "",
            table: {
              cols: 2,
              rows: [
                [
                  "Lò xo nhẹ (1 Vàng) hoặc 1 Xanh. Ngồi thẳng lưng trên Box, 2 tay cầm dây rope sát vai, gập khuỷu tay vuông góc cạnh sườn.",
                  "Khuỷu tay khóa sát sườn — Hít sâu. Thở — Siết bắp tay sau, duỗi thẳng khuỷu tay ra sau. Hít — Chầm chậm gập khuỷu tay về vuông góc.",
                ],
                [
                  "",
                  "Ổn định khớp vai, ghìm chặt bả vai, cô lập siết bắp tay sau.",
                ],
              ],
            },
          },
        ],
      },
    ],
  };
};

export const loadPlans = (): LessonPlan[] => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as LessonPlan[];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
};

export const savePlans = (plans: LessonPlan[]) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(plans));
};

export const upsertPlan = (plan: LessonPlan) => {
  const plans = loadPlans();
  const index = plans.findIndex((p) => p.id === plan.id);
  const next = { ...plan, updatedAt: new Date().toISOString() };
  if (index >= 0) plans[index] = next;
  else plans.unshift(next);
  savePlans(plans);
  return next;
};

export const deletePlan = (id: string) => {
  savePlans(loadPlans().filter((p) => p.id !== id));
};

export const getPlan = (id: string) => loadPlans().find((p) => p.id === id);

export const ensureTableSize = (table: LessonTable): LessonTable => {
  const cols = Math.max(1, table.cols);
  const rows = table.rows.map((row) => {
    const next = [...row];
    while (next.length < cols) next.push("");
    return next.slice(0, cols);
  });
  return { cols, rows: rows.length ? rows : [Array.from({ length: cols }, () => "")] };
};

export const updateCell = (
  table: LessonTable,
  row: number,
  col: number,
  value: string,
): LessonTable => {
  const next = ensureTableSize(table);
  next.rows = next.rows.map((r, ri) =>
    ri === row ? r.map((c, ci) => (ci === col ? value : c)) : r,
  );
  return next;
};

export const addTableRow = (table: LessonTable): LessonTable => {
  const next = ensureTableSize(table);
  return {
    ...next,
    rows: [...next.rows, Array.from({ length: next.cols }, () => "")],
  };
};

export const removeTableRow = (table: LessonTable, rowIndex: number): LessonTable => {
  const next = ensureTableSize(table);
  if (next.rows.length <= 1) return next;
  return { ...next, rows: next.rows.filter((_, i) => i !== rowIndex) };
};

export const addTableCol = (table: LessonTable): LessonTable => {
  const next = ensureTableSize(table);
  return {
    cols: next.cols + 1,
    rows: next.rows.map((row) => [...row, ""]),
  };
};

export const removeTableCol = (table: LessonTable, colIndex: number): LessonTable => {
  const next = ensureTableSize(table);
  if (next.cols <= 1) return next;
  return {
    cols: next.cols - 1,
    rows: next.rows.map((row) => row.filter((_, i) => i !== colIndex)),
  };
};
