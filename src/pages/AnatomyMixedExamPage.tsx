import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { QuestionNav } from "../components/QuestionNav";
import { AnatomyQuestionPrompt } from "../components/AnatomyQuestionPrompt";
import {
  buildConceptOptions,
  buildMixedExam,
  countExamScore,
  isTermCorrect,
  type MixedExamQuestion,
} from "../lib/anatomy";
import type { AnatomyConcept, AnatomyPack } from "../types/anatomy";
import type { QuestionStatus, QuizAnswer } from "../types";

const EXAM_ALL_SIZE = 40;

type AnatomyMixedExamPageProps = {
  concepts: AnatomyConcept[];
  packs: AnatomyPack[];
  pageIllustrations: Record<string, string>;
};

type OptionCache = Record<number, AnatomyConcept[]>;

export const AnatomyMixedExamPage = ({
  concepts,
  packs,
  pageIllustrations,
}: AnatomyMixedExamPageProps) => {
  const { packId = "all" } = useParams<{ packId: string }>();

  const pack = packs.find((p) => p.id === packId);
  const isAll = packId === "all";

  const poolConcepts = useMemo(() => {
    if (isAll) return concepts;
    return concepts.filter((c) => c.packId === packId);
  }, [concepts, isAll, packId]);

  const [examQuestions, setExamQuestions] = useState<MixedExamQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, QuizAnswer>>({});
  const [optionCache, setOptionCache] = useState<OptionCache>({});
  const [typedValue, setTypedValue] = useState("");

  useEffect(() => {
    setExamQuestions(buildMixedExam(poolConcepts, isAll ? EXAM_ALL_SIZE : undefined));
    setCurrentIndex(0);
    setAnswers({});
    setOptionCache({});
  }, [isAll, packId, poolConcepts]);

  const current = examQuestions[currentIndex];
  const currentAnswer = answers[currentIndex];
  const isSubmitted = Boolean(currentAnswer);
  const score = countExamScore(answers, examQuestions.length);

  useEffect(() => {
    setTypedValue("");
  }, [currentIndex]);

  useEffect(() => {
    if (examQuestions.length === 0) return;

    const next: OptionCache = {};
    examQuestions.forEach((q, index) => {
      if (q.mode === "mcq") {
        next[index] = buildConceptOptions(q.concept, poolConcepts);
      }
    });
    setOptionCache(next);
  }, [examQuestions, poolConcepts]);

  const statuses: QuestionStatus[] = examQuestions.map((_, index) => {
    const answer = answers[index];
    if (!answer) return "unanswered";
    return answer.isCorrect ? "correct" : "wrong";
  });

  const handleMcqSubmit = (conceptId: string, isCorrect: boolean) => {
    if (isSubmitted) return;
    setAnswers((prev) => ({
      ...prev,
      [currentIndex]: { value: conceptId, isCorrect, submittedAt: Date.now() },
    }));
  };

  const handleTypeSubmit = () => {
    if (!current || isSubmitted || !typedValue.trim()) return;
    const ok = isTermCorrect(typedValue, current.concept);
    setAnswers((prev) => ({
      ...prev,
      [currentIndex]: { value: typedValue, isCorrect: ok, submittedAt: Date.now() },
    }));
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleTypeSubmit();
    }
  };

  if (!current || examQuestions.length === 0) {
    return (
      <div className="px-4 py-10 text-center">
        <p className="text-slate-600">Không có câu hỏi cho bài thi này.</p>
        <Link to="/anatomy" className="mt-4 inline-block text-teal-600 underline">
          Về Giải phẫu
        </Link>
      </div>
    );
  }

  const title = isAll ? "Bài thi tổng hợp" : pack?.name ?? "Bài thi mix";
  const options = optionCache[currentIndex] ?? [];

  return (
    <div className="mx-auto flex min-h-screen max-w-3xl flex-col">
      <header className="border-b border-slate-200 bg-white px-4 py-4">
        <Link to="/anatomy" className="text-sm text-teal-600 hover:underline">
          ← Giải phẫu
        </Link>
        <p className="mt-2 text-xs font-semibold uppercase tracking-wide text-teal-600">
          Kiểm tra mix · {current.mode === "mcq" ? "Trắc nghiệm" : "Điền thuật ngữ"}
        </p>
        <div className="mt-2 flex flex-wrap items-end justify-between gap-2">
          <h1 className="text-lg font-bold text-slate-900">
            Câu {currentIndex + 1}/{examQuestions.length}
          </h1>
          <div
            className="rounded-xl bg-teal-50 px-3 py-1.5 text-sm font-semibold text-teal-800"
            aria-live="polite"
          >
            Đúng {score.correct}/{score.answered}
            {score.answered > 0 && (
              <span className="font-normal text-teal-600"> · {score.percent}%</span>
            )}
          </div>
        </div>
        <p className="mt-1 truncate text-xs text-slate-500">{title}</p>
      </header>

      <main className="flex-1 space-y-5 px-4 py-5">
        <AnatomyQuestionPrompt
          concept={current.concept}
          pageIllustrations={pageIllustrations}
          prompt={
            current.mode === "mcq"
              ? "Chọn thuật ngữ điền vào chỗ trống:"
              : "Gõ tên khái niệm điền vào chỗ trống (tiếng Việt hoặc tiếng Anh):"
          }
        />

        {current.mode === "mcq" ? (
          <div className="grid gap-3 sm:grid-cols-2">
            {options.map((option) => {
              const isCorrect = option.id === current.concept.id;
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
                  onClick={() => handleMcqSubmit(option.id, isCorrect)}
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
        ) : (
          <div className="flex gap-2">
            <input
              type="text"
              value={typedValue}
              disabled={isSubmitted}
              aria-label="Nhập thuật ngữ"
              placeholder="Gõ đáp án..."
              onChange={(e) => setTypedValue(e.target.value)}
              onKeyDown={handleKeyDown}
              className="flex-1 rounded-xl border border-slate-300 px-4 py-3 text-base outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-200"
            />
            <button
              type="button"
              disabled={isSubmitted || !typedValue.trim()}
              onClick={handleTypeSubmit}
              className="rounded-xl bg-teal-600 px-5 py-3 text-sm font-semibold text-white hover:bg-teal-500 disabled:bg-slate-300"
            >
              Kiểm tra
            </button>
          </div>
        )}

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
              {current.concept.termVi} —{" "}
              <span className="font-semibold">{current.concept.term}</span>
            </p>
          </div>
        )}

        {score.finished && (
          <div className="rounded-2xl border-2 border-teal-300 bg-gradient-to-br from-teal-50 to-emerald-50 p-6 text-center shadow-sm">
            <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">
              Kết quả bài thi
            </p>
            <p className="mt-2 text-4xl font-black text-teal-900">
              {score.correct}/{score.total}
            </p>
            <p className="mt-1 text-lg font-semibold text-teal-800">
              {score.percent}% đúng
            </p>
            <p className="mt-3 text-sm text-slate-600">
              {score.percent >= 80
                ? "Xuất sắc! Bạn đã thuộc khá tốt."
                : score.percent >= 60
                  ? "Khá ổn — ôn thêm các câu sai nhé."
                  : "Cần ôn lại thêm — thử đọc sách và làm lại từng chương."}
            </p>
            <Link
              to="/anatomy"
              className="mt-4 inline-block rounded-xl bg-teal-600 px-6 py-2.5 text-sm font-semibold text-white hover:bg-teal-500"
            >
              Về Giải phẫu
            </Link>
          </div>
        )}
      </main>

      <QuestionNav
        total={examQuestions.length}
        currentIndex={currentIndex}
        statuses={statuses}
        onSelect={setCurrentIndex}
      />
    </div>
  );
};
