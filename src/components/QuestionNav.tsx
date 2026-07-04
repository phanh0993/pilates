import type { QuestionStatus } from "../types";

type QuestionNavProps = {
  total: number;
  currentIndex: number;
  statuses: QuestionStatus[];
  onSelect: (index: number) => void;
};

const statusClass: Record<QuestionStatus, string> = {
  unanswered: "bg-white text-slate-700 border-slate-200 hover:border-violet-300",
  correct: "bg-emerald-100 text-emerald-800 border-emerald-300",
  wrong: "bg-rose-100 text-rose-800 border-rose-300",
};

export const QuestionNav = ({
  total,
  currentIndex,
  statuses,
  onSelect,
}: QuestionNavProps) => {
  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLButtonElement>,
    index: number,
  ) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onSelect(index);
    }
  };

  return (
    <div className="sticky bottom-0 border-t border-slate-200 bg-white/95 px-4 py-3 backdrop-blur">
      <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
        Danh sách câu hỏi
      </p>
      <div className="flex gap-2 overflow-x-auto pb-1">
        {Array.from({ length: total }).map((_, index) => (
          <button
            key={index}
            type="button"
            aria-label={`Câu ${index + 1}`}
            tabIndex={0}
            onClick={() => onSelect(index)}
            onKeyDown={(event) => handleKeyDown(event, index)}
            className={`min-w-10 rounded-xl border px-3 py-2 text-sm font-bold transition ${
              statusClass[statuses[index] ?? "unanswered"]
            } ${index === currentIndex ? "ring-2 ring-violet-500 ring-offset-1" : ""}`}
          >
            {index + 1}
          </button>
        ))}
      </div>
    </div>
  );
};
