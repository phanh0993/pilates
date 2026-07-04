import type { Exercise } from "../types";

type AnswerFeedbackProps = {
  exercise: Exercise;
  isCorrect: boolean;
  showAnswer?: boolean;
};

export const AnswerFeedback = ({
  exercise,
  isCorrect,
  showAnswer = false,
}: AnswerFeedbackProps) => (
  <div
    className={`rounded-2xl border px-4 py-3 ${
      isCorrect
        ? "border-emerald-200 bg-emerald-50 text-emerald-900"
        : "border-rose-200 bg-rose-50 text-rose-900"
    }`}
  >
    <p className="text-lg font-bold">{isCorrect ? "Đúng rồi!" : "Chưa đúng"}</p>
    <p className="mt-1 text-sm">
      Tên tiếng Việt: <span className="font-semibold">{exercise.nameVi}</span>
    </p>
    {!isCorrect && showAnswer && (
      <p className="mt-1 text-sm">
        Đáp án đúng: <span className="font-semibold">{exercise.nameEn}</span>
      </p>
    )}
  </div>
);
