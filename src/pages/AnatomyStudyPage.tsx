import { useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import type { AnatomyPage } from "../hooks/useAnatomyData";
import type { AnatomyPack } from "../types/anatomy";

type AnatomyStudyPageProps = {
  pages: AnatomyPage[];
  packs: AnatomyPack[];
};

export const AnatomyStudyPage = ({ pages, packs }: AnatomyStudyPageProps) => {
  const { packId = "" } = useParams<{ packId: string }>();
  const [pageIndex, setPageIndex] = useState(0);

  const pack = packs.find((p) => p.id === packId);

  const chapterPages = useMemo(() => {
    const range = pack?.pageRange;
    if (!range) return pages;
    return pages.filter((p) => p.order >= range[0] && p.order <= range[1]);
  }, [pack?.pageRange, pages]);

  const current = chapterPages[pageIndex];

  if (!current) {
    return (
      <div className="px-4 py-10 text-center">
        <Link to="/anatomy" className="text-teal-600 underline">
          ← Giải phẫu
        </Link>
        <p className="mt-4 text-slate-600">Chưa có trang sách cho chương này.</p>
      </div>
    );
  }

  return (
    <div className="mx-auto min-h-screen max-w-3xl px-4 py-6">
      <Link to="/anatomy" className="text-sm text-teal-600 hover:underline">
        ← Giải phẫu
      </Link>
      <h1 className="mt-3 text-xl font-bold text-slate-900">
        {pack?.name ?? "Đọc sách"}
      </h1>
      <p className="text-sm text-slate-500">
        Trang sách {current.order} · {pageIndex + 1}/{chapterPages.length}
      </p>

      <img
        src={current.imageUrl}
        alt={`Trang ${current.order}`}
        className="mt-4 w-full rounded-2xl border border-slate-200 shadow-sm"
      />

      <div className="mt-4 flex gap-2">
        <button
          type="button"
          disabled={pageIndex === 0}
          onClick={() => setPageIndex((i) => i - 1)}
          className="flex-1 rounded-xl border border-slate-200 py-3 font-semibold disabled:opacity-40"
        >
          ← Trang trước
        </button>
        <button
          type="button"
          disabled={pageIndex >= chapterPages.length - 1}
          onClick={() => setPageIndex((i) => i + 1)}
          className="flex-1 rounded-xl bg-teal-600 py-3 font-semibold text-white disabled:opacity-40"
        >
          Trang sau →
        </button>
      </div>
    </div>
  );
};
