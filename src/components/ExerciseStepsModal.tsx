import { useEffect, useState } from "react";
import type { Exercise } from "../types";

type ExerciseStepsModalProps = {
  exercise: Exercise;
  isOpen: boolean;
  onClose: () => void;
  hideExerciseName?: boolean;
};

export const ExerciseStepsModal = ({
  exercise,
  isOpen,
  onClose,
  hideExerciseName = false,
}: ExerciseStepsModalProps) => {
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    if (isOpen) {
      setActiveIndex(0);
      document.body.style.overflow = "hidden";
      return () => {
        document.body.style.overflow = "";
      };
    }
    return undefined;
  }, [isOpen, exercise.id]);

  if (!isOpen || exercise.images.length === 0) {
    return null;
  }

  const handleBackdropKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    if (event.key === "Escape") {
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex flex-col bg-slate-950/98"
      role="dialog"
      aria-modal="true"
      aria-label={hideExerciseName ? "Các bước động tác" : `Các bước của ${exercise.nameEn}`}
      onKeyDown={handleBackdropKeyDown}
    >
      <div className="flex items-center justify-between border-b border-white/10 px-4 py-3 text-white">
        <div>
          <p className="text-xs uppercase tracking-wide text-violet-300">Các bước động tác</p>
          {!hideExerciseName && (
            <p className="text-sm font-semibold">{exercise.nameEn}</p>
          )}
        </div>
        <button
          type="button"
          aria-label="Đóng"
          tabIndex={0}
          onClick={onClose}
          className="rounded-full bg-white/10 px-3 py-1 text-sm font-medium hover:bg-white/20"
        >
          ✕
        </button>
      </div>

      <div className="flex-1 overflow-y-auto overscroll-contain px-4 py-4">
        <div className="mx-auto max-w-lg space-y-5">
          {exercise.images.map((image, index) => (
            <button
              key={image.url}
              type="button"
              aria-label={`Xem bước ${image.step}`}
              tabIndex={0}
              onClick={() => setActiveIndex(index)}
              className={`w-full overflow-hidden rounded-2xl border-2 text-left transition ${
                index === activeIndex
                  ? "border-violet-400 shadow-lg shadow-violet-900/40"
                  : "border-white/10"
              }`}
            >
              <img
                src={image.url}
                alt={`Bước ${image.step}`}
                className="w-full bg-white object-contain"
              />
              <p className="bg-white px-3 py-2 text-sm font-medium text-slate-800">
                {image.step}. {image.caption}
              </p>
            </button>
          ))}
        </div>
      </div>

      <div className="border-t border-white/10 bg-slate-950 p-4 pb-[max(1rem,env(safe-area-inset-bottom))]">
        <button
          type="button"
          aria-label="Quay lại màn hình câu hỏi"
          tabIndex={0}
          onClick={onClose}
          className="w-full rounded-2xl bg-violet-600 py-3.5 text-base font-bold text-white hover:bg-violet-500"
        >
          ← Quay lại câu hỏi
        </button>
      </div>
    </div>
  );
};
