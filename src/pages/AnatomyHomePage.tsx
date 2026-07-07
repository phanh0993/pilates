import { Link } from "react-router-dom";
import type { AnatomyConcept, AnatomyPack } from "../types/anatomy";

type AnatomyHomePageProps = {
  packs: AnatomyPack[];
  concepts: AnatomyConcept[];
};

export const AnatomyHomePage = ({ packs, concepts }: AnatomyHomePageProps) => (
  <div className="mx-auto max-w-3xl px-4 py-8">
    <Link to="/" className="text-sm text-teal-600 hover:underline">
      ← Tất cả môn học
    </Link>

    <div className="mt-4 rounded-3xl bg-gradient-to-br from-teal-600 to-emerald-700 p-8 text-white shadow-lg">
      <h1 className="text-3xl font-black tracking-tight">Giải phẫu cơ thể</h1>
      <p className="mt-2 text-teal-100">
        Thuộc khái niệm theo chương — trắc nghiệm, điền thuật ngữ & bài thi mix.
      </p>
    </div>

    <section className="mt-6 rounded-2xl border-2 border-amber-200 bg-amber-50 p-5 shadow-sm">
      <h2 className="text-lg font-bold text-amber-900">Bài kiểm tra tổng hợp</h2>
      <p className="mt-1 text-sm text-amber-800">
        40 câu ngẫu nhiên (trắc nghiệm + điền thuật ngữ) từ toàn bộ {concepts.length}{" "}
        khái niệm · có chấm điểm.
      </p>
      <Link
        to="/anatomy/exam/all"
        className="mt-4 inline-flex rounded-xl bg-amber-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-amber-500"
      >
        Bắt đầu bài thi
      </Link>
    </section>

    <div className="mt-8 space-y-6">
      {packs.map((pack) => {
        const packConcepts = concepts.filter((c) => c.packId === pack.id);
        const sections = [...new Set(packConcepts.map((c) => c.section ?? c.category))];

        return (
          <section
            key={pack.id}
            className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
          >
            <div className="mb-4">
              <h2 className="text-xl font-bold text-slate-900">{pack.name}</h2>
              <p className="text-sm text-slate-500">
                {pack.description} · {packConcepts.length} khái niệm
              </p>
              {sections.length > 0 && (
                <ul className="mt-2 space-y-1 text-xs text-slate-600">
                  {sections.map((section) => (
                    <li key={section}>• {section}</li>
                  ))}
                </ul>
              )}
            </div>

            <div className="grid gap-3 sm:grid-cols-2">
              <Link
                to={`/anatomy/mcq/${pack.id}`}
                className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-4 transition hover:border-teal-300 hover:bg-teal-50"
              >
                <p className="font-semibold text-slate-900">Trắc nghiệm 4 đáp án</p>
                <p className="mt-1 text-xs text-slate-500">Chọn thuật ngữ theo định nghĩa</p>
              </Link>

              <Link
                to={`/anatomy/type/${pack.id}`}
                className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-4 transition hover:border-teal-300 hover:bg-teal-50"
              >
                <p className="font-semibold text-slate-900">Điền thuật ngữ</p>
                <p className="mt-1 text-xs text-slate-500">Gõ tên khái niệm từ mô tả</p>
              </Link>

              <Link
                to={`/anatomy/exam/${pack.id}`}
                className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-4 transition hover:border-amber-300 hover:bg-amber-100"
              >
                <p className="font-semibold text-amber-900">Kiểm tra mix</p>
                <p className="mt-1 text-xs text-amber-700">
                  Trộn trắc nghiệm & điền · {packConcepts.length} câu · chấm điểm
                </p>
              </Link>

              <Link
                to={`/anatomy/study/${pack.id}`}
                className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-4 transition hover:border-teal-300 hover:bg-teal-50"
              >
                <p className="font-semibold text-slate-900">Đọc sách</p>
                <p className="mt-1 text-xs text-slate-500">Xem ảnh trang theo chương</p>
              </Link>
            </div>
          </section>
        );
      })}
    </div>
  </div>
);
