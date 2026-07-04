import { Link } from "react-router-dom";
import type { Pack, QuizMode } from "../types";
import { getModeLabel } from "../lib/quiz";

type HomePageProps = {
  packs: Pack[];
};

const MODES: QuizMode[] = ["peek-pick-name", "listen-pick-image", "type-name"];

export const HomePage = ({ packs }: HomePageProps) => (
  <div className="mx-auto max-w-3xl px-4 py-8">
    <div className="rounded-3xl bg-gradient-to-br from-violet-600 to-indigo-700 p-8 text-white shadow-lg">
      <h1 className="text-3xl font-black tracking-tight">Trắc nghiệm cho Vợ Ánh</h1>
      <p className="mt-2 max-w-xl text-violet-100">
        Học và ghi nhớ tên động tác Pilates qua trắc nghiệm. Hiện có 11 động tác mẫu
        từ sách Emma Pilates Academy.
      </p>
    </div>

    <div className="mt-8 space-y-6">
      {packs.map((pack) => (
        <section
          key={pack.id}
          className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
        >
          <div className="mb-4">
            <h2 className="text-xl font-bold text-slate-900">{pack.name}</h2>
            <p className="text-sm text-slate-500">
              {pack.description} · {pack.exerciseIds.length} động tác
            </p>
          </div>

          <div className="grid gap-3 sm:grid-cols-3">
            {MODES.map((mode) => (
              <Link
                key={mode}
                to={`/quiz/${pack.id}/${mode}`}
                className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-4 text-left transition hover:border-violet-300 hover:bg-violet-50"
              >
                <p className="font-semibold text-slate-900">{getModeLabel(mode)}</p>
                <p className="mt-1 text-xs text-slate-500">Bắt đầu làm bài</p>
              </Link>
            ))}
          </div>
        </section>
      ))}
    </div>
  </div>
);
