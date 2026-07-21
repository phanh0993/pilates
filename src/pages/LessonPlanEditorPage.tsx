import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { LessonTableEditor } from "../components/LessonTableEditor";
import {
  createExerciseBlock,
  createSection,
  createTableBlock,
  createTextBlock,
  getPlan,
  upsertPlan,
} from "../lib/lessonPlan";
import type {
  LessonBlock,
  LessonPlan,
  LessonSection,
  LessonTable,
} from "../types/lessonPlan";

const moveItem = <T,>(list: T[], from: number, to: number): T[] => {
  if (to < 0 || to >= list.length) return list;
  const next = [...list];
  const [item] = next.splice(from, 1);
  next.splice(to, 0, item);
  return next;
};

const iconBtn =
  "flex min-h-11 min-w-11 items-center justify-center rounded-xl border border-slate-200 bg-white text-base font-semibold text-slate-700 active:bg-slate-100 disabled:opacity-30";

export const LessonPlanEditorPage = () => {
  const { planId = "" } = useParams<{ planId: string }>();
  const navigate = useNavigate();
  const [plan, setPlan] = useState<LessonPlan | null>(null);
  const [savedAt, setSavedAt] = useState<string | null>(null);

  useEffect(() => {
    const found = getPlan(planId);
    if (!found) {
      navigate("/lesson-plans", { replace: true });
      return;
    }
    setPlan(found);
  }, [planId, navigate]);

  const blockCount = useMemo(
    () => plan?.sections.reduce((n, s) => n + s.blocks.length, 0) ?? 0,
    [plan],
  );

  if (!plan) {
    return (
      <div className="flex min-h-screen items-center justify-center text-slate-500">
        Đang tải giáo án...
      </div>
    );
  }

  const patchPlan = (updater: (prev: LessonPlan) => LessonPlan) => {
    setPlan((prev) => (prev ? updater(prev) : prev));
  };

  const handleSave = () => {
    const saved = upsertPlan(plan);
    setPlan(saved);
    setSavedAt(new Date().toLocaleTimeString("vi-VN"));
  };

  const handleExportPdf = () => {
    upsertPlan(plan);
    window.print();
  };

  const updateSection = (sectionId: string, updater: (s: LessonSection) => LessonSection) => {
    patchPlan((prev) => ({
      ...prev,
      sections: prev.sections.map((s) => (s.id === sectionId ? updater(s) : s)),
    }));
  };

  const updateBlock = (
    sectionId: string,
    blockId: string,
    updater: (b: LessonBlock) => LessonBlock,
  ) => {
    updateSection(sectionId, (section) => ({
      ...section,
      blocks: section.blocks.map((b) => (b.id === blockId ? updater(b) : b)),
    }));
  };

  const updateBlockTable = (sectionId: string, blockId: string, table: LessonTable) => {
    updateBlock(sectionId, blockId, (block) => {
      if (block.type === "text") return block;
      return { ...block, table };
    });
  };

  return (
    <div className="lesson-plan-app mx-auto min-h-screen max-w-4xl px-3 pb-28 pt-4 sm:px-4 sm:py-6 sm:pb-8">
      <div className="print:hidden">
        <Link
          to="/lesson-plans"
          className="inline-flex min-h-10 items-center text-sm font-medium text-emerald-700"
        >
          ← Danh sách
        </Link>

        <div className="mt-3">
          <h1 className="text-xl font-black text-slate-900 sm:text-2xl">Soạn giáo án</h1>
          <p className="mt-0.5 text-xs text-slate-500 sm:text-sm">
            {plan.sections.length} phần · {blockCount} khối
            {savedAt ? ` · đã lưu ${savedAt}` : ""}
          </p>
        </div>

        {/* Desktop toolbar — mobile dùng thanh đáy */}
        <div className="mt-3 hidden gap-2 sm:flex">
          <button
            type="button"
            onClick={handleSave}
            className="min-h-11 rounded-xl border border-slate-200 bg-white px-4 text-sm font-semibold text-slate-800 hover:bg-slate-50"
          >
            Lưu
          </button>
          <button
            type="button"
            onClick={handleExportPdf}
            className="min-h-11 rounded-xl bg-emerald-700 px-4 text-sm font-semibold text-white hover:bg-emerald-800"
          >
            Xuất PDF (A4 dọc)
          </button>
        </div>
      </div>

      <article className="lesson-print-sheet mt-4 rounded-2xl border border-slate-200 bg-white p-3 shadow-sm sm:mt-6 sm:p-5 print:mt-0 print:rounded-none print:border-0 print:p-0 print:shadow-none">
        <header className="border-b border-slate-200 pb-3 print:border-slate-400 print:pb-3">
          <input
            value={plan.title}
            onChange={(e) => patchPlan((p) => ({ ...p, title: e.target.value }))}
            aria-label="Tiêu đề giáo án"
            placeholder="Tiêu đề giáo án"
            className="w-full border-0 bg-transparent text-2xl font-black leading-tight text-slate-900 outline-none placeholder:text-slate-300 sm:text-3xl print:text-2xl"
          />
          <input
            value={plan.subtitle}
            onChange={(e) => patchPlan((p) => ({ ...p, subtitle: e.target.value }))}
            aria-label="Phụ đề"
            placeholder="Phụ đề / lớp / thiết bị"
            className="mt-1 w-full border-0 bg-transparent text-base text-slate-500 outline-none placeholder:text-slate-300 sm:text-sm"
          />
        </header>

        <div className="mt-4 space-y-6 sm:mt-5 sm:space-y-8">
          {plan.sections.map((section, sectionIndex) => (
            <section key={section.id} className="lesson-section">
              <div className="mb-3 space-y-2">
                <input
                  value={section.title}
                  onChange={(e) =>
                    updateSection(section.id, (s) => ({ ...s, title: e.target.value }))
                  }
                  aria-label="Tiêu đề phần"
                  className="w-full rounded-xl border-0 bg-emerald-50 px-3 py-3 text-base font-bold uppercase tracking-wide text-emerald-900 outline-none print:bg-transparent print:px-0 print:py-0 print:text-sm"
                />
                <div className="flex gap-2 print:hidden">
                  <button
                    type="button"
                    onClick={() =>
                      patchPlan((p) => ({
                        ...p,
                        sections: moveItem(p.sections, sectionIndex, sectionIndex - 1),
                      }))
                    }
                    disabled={sectionIndex === 0}
                    className={iconBtn}
                    aria-label="Đưa phần lên"
                  >
                    ↑
                  </button>
                  <button
                    type="button"
                    onClick={() =>
                      patchPlan((p) => ({
                        ...p,
                        sections: moveItem(p.sections, sectionIndex, sectionIndex + 1),
                      }))
                    }
                    disabled={sectionIndex === plan.sections.length - 1}
                    className={iconBtn}
                    aria-label="Đưa phần xuống"
                  >
                    ↓
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      if (!window.confirm("Xóa phần này?")) return;
                      patchPlan((p) => ({
                        ...p,
                        sections: p.sections.filter((s) => s.id !== section.id),
                      }));
                    }}
                    className="flex min-h-11 flex-1 items-center justify-center rounded-xl border border-rose-200 bg-white text-sm font-medium text-rose-600 active:bg-rose-50"
                  >
                    Xóa phần
                  </button>
                </div>
              </div>

              <div className="space-y-4 sm:space-y-5">
                {section.blocks.map((block, blockIndex) => (
                  <div
                    key={block.id}
                    className="lesson-block rounded-2xl border border-slate-200 bg-white p-3 shadow-sm print:rounded-none print:border-0 print:p-0 print:shadow-none"
                  >
                    <div className="mb-3 flex items-center justify-between gap-2 print:hidden">
                      <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-bold uppercase text-slate-500">
                        {block.type === "exercise"
                          ? "Động tác"
                          : block.type === "table"
                            ? "Bảng"
                            : "Văn bản"}
                      </span>
                      <div className="flex gap-1.5">
                        <button
                          type="button"
                          onClick={() =>
                            updateSection(section.id, (s) => ({
                              ...s,
                              blocks: moveItem(s.blocks, blockIndex, blockIndex - 1),
                            }))
                          }
                          disabled={blockIndex === 0}
                          className={iconBtn}
                          aria-label="Đưa khối lên"
                        >
                          ↑
                        </button>
                        <button
                          type="button"
                          onClick={() =>
                            updateSection(section.id, (s) => ({
                              ...s,
                              blocks: moveItem(s.blocks, blockIndex, blockIndex + 1),
                            }))
                          }
                          disabled={blockIndex === section.blocks.length - 1}
                          className={iconBtn}
                          aria-label="Đưa khối xuống"
                        >
                          ↓
                        </button>
                        <button
                          type="button"
                          onClick={() =>
                            updateSection(section.id, (s) => ({
                              ...s,
                              blocks: s.blocks.filter((b) => b.id !== block.id),
                            }))
                          }
                          className="flex min-h-11 min-w-11 items-center justify-center rounded-xl border border-rose-200 bg-white text-sm font-medium text-rose-600 active:bg-rose-50"
                          aria-label="Xóa khối"
                        >
                          ×
                        </button>
                      </div>
                    </div>

                    {block.type === "text" && (
                      <textarea
                        value={block.content}
                        onChange={(e) =>
                          updateBlock(section.id, block.id, (b) =>
                            b.type === "text" ? { ...b, content: e.target.value } : b,
                          )
                        }
                        rows={4}
                        aria-label="Nội dung văn bản"
                        placeholder="Ghi chú / hướng dẫn chung..."
                        className="w-full rounded-xl border border-slate-200 px-3 py-3 text-base leading-relaxed text-slate-800 outline-none focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100 print:border-0 print:px-0"
                      />
                    )}

                    {block.type === "exercise" && (
                      <div className="space-y-3">
                        <input
                          value={block.name}
                          onChange={(e) =>
                            updateBlock(section.id, block.id, (b) =>
                              b.type === "exercise" ? { ...b, name: e.target.value } : b,
                            )
                          }
                          aria-label="Tên động tác"
                          placeholder="Tên động tác (EN / VI)"
                          className="w-full rounded-xl border border-slate-200 px-3 py-3 text-base font-bold text-slate-900 outline-none focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100 print:border-0 print:px-0 print:text-base"
                        />
                        <input
                          value={block.note}
                          onChange={(e) =>
                            updateBlock(section.id, block.id, (b) =>
                              b.type === "exercise" ? { ...b, note: e.target.value } : b,
                            )
                          }
                          aria-label="Ghi chú động tác"
                          placeholder="Setup / set lò xo (tuỳ chọn)"
                          className="w-full rounded-xl border border-slate-200 px-3 py-3 text-base text-slate-600 outline-none focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100 print:border-0 print:px-0 print:text-sm"
                        />
                        <LessonTableEditor
                          table={block.table}
                          onChange={(table) =>
                            updateBlockTable(section.id, block.id, table)
                          }
                        />
                      </div>
                    )}

                    {block.type === "table" && (
                      <div className="space-y-3">
                        <input
                          value={block.caption}
                          onChange={(e) =>
                            updateBlock(section.id, block.id, (b) =>
                              b.type === "table" ? { ...b, caption: e.target.value } : b,
                            )
                          }
                          aria-label="Chú thích bảng"
                          placeholder="Chú thích bảng (tuỳ chọn)"
                          className="w-full rounded-xl border border-slate-200 px-3 py-3 text-base font-semibold text-slate-700 outline-none focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100 print:border-0 print:px-0 print:text-sm"
                        />
                        <LessonTableEditor
                          table={block.table}
                          onChange={(table) =>
                            updateBlockTable(section.id, block.id, table)
                          }
                        />
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <div className="mt-3 grid grid-cols-1 gap-2 print:hidden sm:grid-cols-3">
                <button
                  type="button"
                  onClick={() =>
                    updateSection(section.id, (s) => ({
                      ...s,
                      blocks: [...s.blocks, createExerciseBlock()],
                    }))
                  }
                  className="min-h-12 rounded-2xl bg-emerald-700 px-3 text-sm font-semibold text-white active:bg-emerald-800"
                >
                  + Động tác (+ bảng)
                </button>
                <button
                  type="button"
                  onClick={() =>
                    updateSection(section.id, (s) => ({
                      ...s,
                      blocks: [...s.blocks, createTableBlock()],
                    }))
                  }
                  className="min-h-12 rounded-2xl border border-emerald-300 bg-emerald-50 px-3 text-sm font-semibold text-emerald-900 active:bg-emerald-100"
                >
                  + Thêm bảng
                </button>
                <button
                  type="button"
                  onClick={() =>
                    updateSection(section.id, (s) => ({
                      ...s,
                      blocks: [...s.blocks, createTextBlock()],
                    }))
                  }
                  className="min-h-12 rounded-2xl border border-slate-200 bg-white px-3 text-sm font-semibold text-slate-700 active:bg-slate-50"
                >
                  + Văn bản
                </button>
              </div>
            </section>
          ))}
        </div>

        <div className="mt-5 print:hidden sm:mt-6">
          <button
            type="button"
            onClick={() =>
              patchPlan((p) => ({
                ...p,
                sections: [...p.sections, createSection(`Phần ${p.sections.length + 1}`)],
              }))
            }
            className="min-h-12 w-full rounded-2xl border border-dashed border-emerald-400 text-sm font-semibold text-emerald-800 active:bg-emerald-50"
          >
            + Thêm phần
          </button>
        </div>
      </article>

      {/* Thanh cố định dưới cùng — tiện bấm một tay trên điện thoại */}
      <div className="fixed inset-x-0 bottom-0 z-40 border-t border-slate-200 bg-white/95 px-3 pb-[max(0.75rem,env(safe-area-inset-bottom))] pt-2 backdrop-blur print:hidden sm:hidden">
        <div className="mx-auto grid max-w-4xl grid-cols-2 gap-2">
          <button
            type="button"
            onClick={handleSave}
            className="min-h-12 rounded-2xl border border-slate-200 bg-white text-base font-semibold text-slate-800 active:bg-slate-100"
          >
            Lưu
          </button>
          <button
            type="button"
            onClick={handleExportPdf}
            className="min-h-12 rounded-2xl bg-emerald-700 text-base font-semibold text-white active:bg-emerald-800"
          >
            Xuất PDF
          </button>
        </div>
      </div>
    </div>
  );
};
