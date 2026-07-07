import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { QuestionNav } from "../components/QuestionNav";
import {
  buildConceptOptions,
  getPackConcepts,
  maskDefinition,
} from "../lib/anatomy";
import { shuffle } from "../lib/shuffle";
import type { AnatomyConcept } from "../types/anatomy";
import type { QuestionStatus, QuizAnswer } from "../types";

type AnatomyMcqPageProps = {
  concepts: AnatomyConcept[];
};

type OptionCache = Record<number, AnatomyConcept[]>;

export const AnatomyMcqPage = ({ concepts }: AnatomyMcqPageProps) => {
  const { packId = "" } = useParams<{ packId: string }>();

  const conceptIds = useMemo(
    () => concepts.filter((c) => c.packId === packId).map((c) => c.id),
    [concepts, packId],
  );

  const [packConcepts, setPackConcepts] = useState<AnatomyConcept[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, QuizAnswer>>({});
  const [optionCache, setOptionCache] = useState<OptionCache>({});

  useEffect(() => {
    setPackConcepts(shuffle(getPackConcepts(conceptIds, concepts)));
    setCurrentIndex(0);
    setAnswers({});
    setOptionCache({});
  }, [conceptIds, concepts, packId]);

  const currentConcept = packConcepts[currentIndex];
  const currentAnswer = answers[currentIndex];
  const isSubmitted = Boolean(currentAnswer);

  useEffect(() => {
    if (packConcepts.length === 0) return;

    const next: OptionCache = {};
    packConcepts.forEach((concept, index) => {
      next[index] = buildConceptOptions(concept, packConcepts);
    });
    setOptionCache(next);
  }, [packConcepts]);

  const statuses: QuestionStatus[] = packConcepts.map((_, index) => {
    const answer = answers[index];
    if (!answer) return "unanswered";
    return answer.isCorrect ? "correct" : "wrong";
  });

  const handleSubmit = (conceptId: string, isCorrect: boolean) => {
    if (isSubmitted) return;
    setAnswers((prev) => ({
      ...prev,
      [currentIndex]: { value: conceptId, isCorrect, submittedAt: Date.now() },
    }));
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

  const options = optionCache[currentIndex] ?? [];

  return (
    <div className="mx-auto flex min-h-screen max-w-3xl flex-col">
      <header className="border-b border-slate-200 bg-white px-4 py-4">
        <Link to="/anatomy" className="text-sm text-teal-600 hover:underline">
          ← Giải phẫu
        </Link>
        <p className="mt-2 text-xs font-semibold uppercase tracking-wide text-teal-600">
          Trắc nghiệm 4 đáp án
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
            Chọn thuật ngữ điền vào chỗ trống:
          </p>
        </div>

        <div className="grid gap-3 sm:grid-cols-2">
          {options.map((option) => {
            const isCorrect = option.id === currentConcept.id;
            const isSelected = currentAnswer?.value === option.id;
            let cls =
              "rounded-xl border px-4 py-3 text-left text-sm font-semibold transition ";

            if (!isSubmitted) {
              cls += "border-slate-200 bg-white hover:border-teal-300 hover:bg-teal-50";
            } else if (isCorrect) {
              cls += "border-emerald-400 bg-emerald-100 text-emerald-900";
            } else if (isSelected) {
              cls += "border-rose-400 bg-rose-100 text-rose-900";
            } else {
              cls += "border-slate-200 bg-slate-50 text-slate-500";
            }

            return (
              <button
                key={option.id}
                type="button"
                disabled={isSubmitted}
                aria-label={`Chọn ${option.term}`}
                tabIndex={0}
                onClick={() => handleSubmit(option.id, isCorrect)}
                className={cls}
              >
                <span className="block">{option.term}</span>
                <span className="mt-0.5 block text-xs font-normal text-slate-500">
                  {option.termVi}
                </span>
              </button>
            );
          })}
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
              Đáp án: <span className="font-semibold">{currentConcept.term}</span> —{" "}
              {currentConcept.termVi}
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
