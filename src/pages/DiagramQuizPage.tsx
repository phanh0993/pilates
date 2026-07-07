import { useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getConceptById, isTermCorrect } from "../lib/anatomy";
import type { AnatomyConcept, AnatomyDiagram } from "../types/anatomy";

type DiagramQuizPageProps = {
  concepts: AnatomyConcept[];
  diagrams: AnatomyDiagram[];
};

export const DiagramQuizPage = ({ concepts, diagrams }: DiagramQuizPageProps) => {
  const { diagramId = "" } = useParams<{ diagramId: string }>();
  const diagram = diagrams.find((item) => item.id === diagramId);

  const [inputs, setInputs] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);

  const results = useMemo(() => {
    if (!diagram || !submitted) return {};
    const map: Record<string, boolean> = {};
    diagram.hotspots.forEach((hotspot) => {
      const concept = getConceptById(concepts, hotspot.conceptId);
      if (!concept) {
        map[hotspot.id] = false;
        return;
      }
      map[hotspot.id] = isTermCorrect(inputs[hotspot.id] ?? "", concept);
    });
    return map;
  }, [concepts, diagram, inputs, submitted]);

  if (!diagram) {
    return (
      <div className="px-4 py-10 text-center">
        <p className="text-slate-600">Không tìm thấy sơ đồ.</p>
        <Link to="/anatomy" className="mt-4 inline-block text-teal-600 underline">
          Về Giải phẫu
        </Link>
      </div>
    );
  }

  const handleInputChange = (hotspotId: string, value: string) => {
    if (submitted) return;
    setInputs((prev) => ({ ...prev, [hotspotId]: value }));
  };

  const handleSubmit = () => {
    setSubmitted(true);
  };

  const handleReset = () => {
    setInputs({});
    setSubmitted(false);
  };

  const correctCount = Object.values(results).filter(Boolean).length;
  const total = diagram.hotspots.length;

  return (
    <div className="mx-auto min-h-screen max-w-3xl px-4 py-6">
      <Link to="/anatomy" className="text-sm text-teal-600 hover:underline">
        ← Giải phẫu
      </Link>

      <h1 className="mt-3 text-xl font-bold text-slate-900">{diagram.name}</h1>
      <p className="mt-1 text-sm text-slate-500">
        Điền tên bộ phận / thuật ngữ đúng cho từng số trên sơ đồ.
      </p>

      <div className="relative mt-5 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <img
          src={diagram.imageUrl}
          alt={diagram.name}
          className="w-full object-contain"
        />
        {diagram.hotspots.map((hotspot) => {
          const isCorrect = results[hotspot.id];
          let badgeClass = "bg-teal-600 text-white";

          if (submitted && isCorrect === true) badgeClass = "bg-emerald-600 text-white";
          if (submitted && isCorrect === false) badgeClass = "bg-rose-600 text-white";

          return (
            <div
              key={hotspot.id}
              className="absolute flex -translate-x-1/2 -translate-y-1/2 flex-col items-center gap-1"
              style={{ left: `${hotspot.x}%`, top: `${hotspot.y}%` }}
            >
              <span
                className={`flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold shadow ${badgeClass}`}
              >
                {hotspot.number}
              </span>
            </div>
          );
        })}
      </div>

      <div className="mt-5 space-y-3">
        {diagram.hotspots
          .slice()
          .sort((a, b) => a.number - b.number)
          .map((hotspot) => {
            const concept = getConceptById(concepts, hotspot.conceptId);
            const isCorrect = results[hotspot.id];

            return (
              <div key={hotspot.id} className="flex items-center gap-3">
                <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-teal-100 text-sm font-bold text-teal-800">
                  {hotspot.number}
                </span>
                <input
                  type="text"
                  value={inputs[hotspot.id] ?? ""}
                  disabled={submitted}
                  aria-label={`Điền tên cho vị trí ${hotspot.number}`}
                  placeholder="Nhập thuật ngữ..."
                  onChange={(e) => handleInputChange(hotspot.id, e.target.value)}
                  className={`flex-1 rounded-xl border px-3 py-2.5 text-base outline-none focus:ring-2 ${
                    submitted && isCorrect === true
                      ? "border-emerald-400 bg-emerald-50 ring-emerald-200"
                      : submitted && isCorrect === false
                        ? "border-rose-400 bg-rose-50 ring-rose-200"
                        : "border-slate-300 focus:border-teal-500 focus:ring-teal-200"
                  }`}
                />
                {submitted && concept && (
                  <span className="hidden shrink-0 text-xs text-slate-500 sm:block">
                    {isCorrect ? "✓" : concept.term}
                  </span>
                )}
              </div>
            );
          })}
      </div>

      <div className="mt-6 flex gap-3">
        {!submitted ? (
          <button
            type="button"
            aria-label="Kiểm tra đáp án"
            tabIndex={0}
            onClick={handleSubmit}
            className="flex-1 rounded-2xl bg-teal-600 py-3.5 font-bold text-white hover:bg-teal-500"
          >
            Kiểm tra
          </button>
        ) : (
          <>
            <div className="flex-1 rounded-2xl border border-slate-200 bg-white px-4 py-3 text-center">
              <p className="text-lg font-bold text-slate-900">
                {correctCount}/{total} đúng
              </p>
            </div>
            <button
              type="button"
              aria-label="Làm lại"
              tabIndex={0}
              onClick={handleReset}
              className="rounded-2xl border border-slate-200 px-5 py-3 font-semibold text-slate-700 hover:bg-slate-50"
            >
              Làm lại
            </button>
          </>
        )}
      </div>
    </div>
  );
};
