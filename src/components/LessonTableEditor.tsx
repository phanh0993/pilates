import type { LessonTable } from "../types/lessonPlan";
import {
  addTableCol,
  addTableRow,
  removeTableCol,
  removeTableRow,
  updateCell,
} from "../lib/lessonPlan";

type LessonTableEditorProps = {
  table: LessonTable;
  onChange: (table: LessonTable) => void;
  readOnly?: boolean;
};

const colLabel = (index: number, cols: number) => {
  if (cols === 2) return index === 0 ? "Trái / Setup" : "Phải / Chuyển động";
  return `Cột ${index + 1}`;
};

export const LessonTableEditor = ({
  table,
  onChange,
  readOnly = false,
}: LessonTableEditorProps) => {
  const handleCellChange = (row: number, col: number, value: string) => {
    onChange(updateCell(table, row, col, value));
  };

  return (
    <div className="space-y-3">
      {/* Mobile: xếp từng ô dọc — dễ gõ bằng ngón tay */}
      <div className="space-y-3 md:hidden print:hidden">
        {table.rows.map((row, ri) => (
          <div
            key={ri}
            className="rounded-2xl border border-slate-200 bg-slate-50 p-3"
          >
            <div className="mb-2 flex items-center justify-between gap-2">
              <p className="text-xs font-bold uppercase tracking-wide text-slate-500">
                Hàng {ri + 1}
              </p>
              {!readOnly && (
                <button
                  type="button"
                  onClick={() => onChange(removeTableRow(table, ri))}
                  disabled={table.rows.length <= 1}
                  aria-label={`Xóa hàng ${ri + 1}`}
                  className="min-h-10 rounded-xl border border-rose-200 bg-white px-3 text-sm font-medium text-rose-600 disabled:opacity-30"
                >
                  Xóa hàng
                </button>
              )}
            </div>
            <div className="space-y-2">
              {row.map((cell, ci) => (
                <label key={ci} className="block">
                  <span className="mb-1 block text-xs font-semibold text-emerald-800">
                    {colLabel(ci, table.cols)}
                  </span>
                  {readOnly ? (
                    <div className="min-h-20 whitespace-pre-wrap rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-base text-slate-800">
                      {cell || "\u00A0"}
                    </div>
                  ) : (
                    <textarea
                      value={cell}
                      onChange={(e) => handleCellChange(ri, ci, e.target.value)}
                      rows={4}
                      aria-label={`${colLabel(ci, table.cols)}, hàng ${ri + 1}`}
                      className="min-h-24 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-base leading-relaxed text-slate-800 outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
                    />
                  )}
                </label>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Desktop + in: bảng lưới */}
      <div className="hidden overflow-x-auto rounded-xl border border-slate-300 bg-white md:block print:block">
        <table className="lesson-table w-full border-collapse text-sm">
          <tbody>
            {table.rows.map((row, ri) => (
              <tr key={ri}>
                {row.map((cell, ci) => (
                  <td
                    key={ci}
                    className="border border-slate-300 p-0 align-top"
                    style={{ width: `${100 / Math.max(table.cols, 1)}%` }}
                  >
                    {readOnly ? (
                      <div className="min-h-16 whitespace-pre-wrap px-2 py-2 text-slate-800">
                        {cell || "\u00A0"}
                      </div>
                    ) : (
                      <textarea
                        value={cell}
                        onChange={(e) => handleCellChange(ri, ci, e.target.value)}
                        rows={3}
                        aria-label={`Ô hàng ${ri + 1} cột ${ci + 1}`}
                        className="min-h-16 w-full resize-y border-0 bg-transparent px-2 py-2 text-sm text-slate-800 outline-none focus:bg-amber-50"
                      />
                    )}
                  </td>
                ))}
                {!readOnly && (
                  <td className="w-12 border border-slate-200 bg-slate-50 p-1 text-center print:hidden">
                    <button
                      type="button"
                      onClick={() => onChange(removeTableRow(table, ri))}
                      disabled={table.rows.length <= 1}
                      aria-label={`Xóa hàng ${ri + 1}`}
                      className="rounded-lg px-2 py-2 text-sm text-rose-600 hover:bg-rose-50 disabled:opacity-30"
                    >
                      −
                    </button>
                  </td>
                )}
              </tr>
            ))}
            {!readOnly && (
              <tr className="print:hidden">
                {Array.from({ length: table.cols }, (_, ci) => (
                  <td
                    key={ci}
                    className="border border-dashed border-slate-200 bg-slate-50 p-1 text-center"
                  >
                    <button
                      type="button"
                      onClick={() => onChange(removeTableCol(table, ci))}
                      disabled={table.cols <= 1}
                      aria-label={`Xóa cột ${ci + 1}`}
                      className="rounded-lg px-2 py-2 text-xs text-rose-600 hover:bg-rose-50 disabled:opacity-30"
                    >
                      Xóa cột
                    </button>
                  </td>
                ))}
                <td className="border border-slate-200 bg-slate-50" />
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {!readOnly && (
        <div className="grid grid-cols-2 gap-2 print:hidden md:flex md:flex-wrap">
          <button
            type="button"
            onClick={() => onChange(addTableRow(table))}
            className="min-h-11 rounded-xl border border-slate-200 bg-white px-3 text-sm font-semibold text-slate-700 active:bg-slate-100"
          >
            + Thêm hàng
          </button>
          <button
            type="button"
            onClick={() => onChange(addTableCol(table))}
            className="min-h-11 rounded-xl border border-slate-200 bg-white px-3 text-sm font-semibold text-slate-700 active:bg-slate-100"
          >
            + Thêm cột
          </button>
          {table.cols > 1 && (
            <button
              type="button"
              onClick={() => onChange(removeTableCol(table, table.cols - 1))}
              className="col-span-2 min-h-11 rounded-xl border border-rose-100 bg-rose-50 px-3 text-sm font-medium text-rose-700 active:bg-rose-100 md:col-span-1"
            >
              − Bớt cột cuối
            </button>
          )}
        </div>
      )}
    </div>
  );
};
