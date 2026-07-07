import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { QuestionNav } from "../components/QuestionNav";
import { getPackConcepts, isTermCorrect, maskDefinition } from "../lib/anatomy";
import { shuffle } from "../lib/shuffle";
import type { AnatomyConcept } from "../types/anatomy";
import type { QuestionStatus, QuizAnswer } from "../types";

type AnatomyTypePageProps = {
  concepts: AnatomyConcept[];
};

export const AnatomyTypePage = ({ concepts }: AnatomyTypePageProps) => {
  const { packId = "" } = useParams<{ packId: string }>();

  const conceptIds = useMemo(
    () => concepts.filter((c) => c.packId === packId).map((c) => c.id),
    [concepts, packId],
  );

  const [packConcepts, setPackConcepts] = useState<AnatomyConcept[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, QuizAnswer>>({});
  const [typedValue, setTypedValue] = useState("");

  useEffect(() => {
    setPackConcepts(shuffle(getPackConcepts(conceptIds, concepts)));
    setCurrentIndex(0);
    setAnswers({});
  }, [conceptIds, concepts, packId]);

  const currentConcept = packConcepts[currentIndex];
  const currentAnswer = answers[currentIndex];
  const isSubmitted = Boolean(currentAnswer);

  useEffect(() => {
    setTypedValue("");
  }, [currentIndex]);

  const statuses: QuestionStatus[] = packConcepts.map((_, index) => {
    const answer = answers[index];
    if (!answer) return "unanswered";
    return answer.isCorrect ? "correct" : "wrong";
  });

  const handleSubmit = () => {
    if (!currentConcept || isSubmitted || !typedValue.trim()) return;
    const ok = isTermCorrect(typedValue, currentConcept);
    setAnswers((prev) => ({
      ...prev,
      [currentIndex]: { value: typedValue, isCorrect: ok, submittedAt: Date.now() },
    }));
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleSubmit();
    }
  };

  if (!currentConcept) {
    return (
      <div className="px-4 py-10 text-center">
        <p className="text-slate-600">Không tìm thấy gói đề.</p>
        <Link to="/anatomy" className="mt-4 inline-block text-teal-600 underline">
          Về Giải phẫu
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto flex min-h-screen max-w-3xl flex-col">
      <header className="border-b border-slate-200 bg-white px-4 py-4">
        <Link to="/anatomy" className="text-sm text-teal-600 hover:underline">
          ← Giải phẫu
        </Link>
        <p className="mt-2 text-xs font-semibold uppercase tracking-wide text-teal-600">
          Điền thuật ngữ
        </p>
        <h1 className="text-lg font-bold text-slate-900">
          Câu {currentIndex + 1}/{packConcepts.length}
        </h1>
      </header>

      <main className="flex-1 space-y-5 px-4 py-5">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-xs font-semibold uppercase text-slate-500">
            {currentConcept.section ?? currentConcept.category}
          </p>
          <p className="mt-2 text-base leading-relaxed text-slate-800">
            {maskDefinition(currentConcept)}
          </p>
          <p className="mt-3 text-sm font-medium text-slate-600">
            Gõ tên khái niệm điền vào chỗ trống (tiếng Việt hoặc tiếng Anh):
          </p>
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={typedValue}
            disabled={isSubmitted}
            aria-label="Nhập thuật ngữ"
            placeholder="Ví dụ: Khớp trượt"
            onChange={(e) => setTypedValue(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-1 rounded-xl border border-slate-300 px-4 py-3 text-base outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-200"
          />
          <button
            type="button"
            disabled={isSubmitted || !typedValue.trim()}
            onClick={handleSubmit}
            className="rounded-xl bg-teal-600 px-5 py-3 text-sm font-semibold text-white hover:bg-teal-500 disabled:bg-slate-300"
          >
            Kiểm tra
          </button>
        </div>

        {isSubmitted && currentAnswer && (
          <div
            className={`rounded-2xl border px-4 py-3 ${
              currentAnswer.isCorrect
                ? "border-emerald-200 bg-emerald-50 text-emerald-900"
                : "border-rose-200 bg-rose-50 text-rose-900"
            }`}
          >
            <p className="font-bold">{currentAnswer.isCorrect ? "Đúng!" : "Chưa đúng"}</p>
            <p className="mt-1 text-sm">
              {currentConcept.termVi} — <span className="font-semibold">{currentConcept.term}</span>
            </p>
          </div>
        )}
      </main>

      <QuestionNav
        total={packConcepts.length}
        currentIndex={currentIndex}
        statuses={statuses}
        onSelect={setCurrentIndex}
      />
    </div>
  );
};
