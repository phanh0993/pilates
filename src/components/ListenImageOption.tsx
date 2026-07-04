import { useState } from "react";
import type { Exercise } from "../types";
import { getPrimaryImage } from "../lib/quiz";
import { ExerciseStepsModal } from "./ExerciseStepsModal";

type ListenImageOptionProps = {
  exercise: Exercise;
  isSubmitted: boolean;
  isCorrect: boolean;
  isSelected: boolean;
  onSelect: () => void;
};

export const ListenImageOption = ({
  exercise,
  isSubmitted,
  isCorrect,
  isSelected,
  onSelect,
}: ListenImageOptionProps) => {
  const [showSteps, setShowSteps] = useState(false);
  const extraCount = Math.max(exercise.images.length - 1, 0);

  let cardClass = "relative overflow-hidden rounded-2xl border bg-white transition ";

  if (!isSubmitted) {
    cardClass += "border-slate-200 active:border-violet-300";
  } else if (isCorrect) {
    cardClass += "border-emerald-400 ring-2 ring-emerald-300";
  } else if (isSelected) {
    cardClass += "border-rose-400 ring-2 ring-rose-300";
  } else {
    cardClass += "border-slate-200 opacity-70";
  }

  const handleOpenSteps = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.stopPropagation();
    setShowSteps(true);
  };

  const handleKeyDownSteps = (event: React.KeyboardEvent<HTMLButtonElement>) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      setShowSteps(true);
    }
  };

  return (
    <>
      <div className={cardClass}>
        <button
          type="button"
          aria-label={`Chọn hình ${exercise.nameEn}`}
          tabIndex={0}
          disabled={isSubmitted}
          onClick={onSelect}
          className="block w-full disabled:cursor-not-allowed"
        >
          <img
            src={getPrimaryImage(exercise)}
            alt={exercise.nameEn}
            className="h-40 w-full object-contain bg-slate-50 sm:h-44"
          />
        </button>

        {extraCount > 0 && !isSubmitted && (
          <>
            <button
              type="button"
              aria-label={`Xem ${exercise.images.length} bước`}
              tabIndex={0}
              onClick={handleOpenSteps}
              onKeyDown={handleKeyDownSteps}
              className="absolute right-2 top-2 z-10 rounded-full bg-violet-600 px-2.5 py-1 text-xs font-bold text-white shadow-md hover:bg-violet-700"
            >
              +{extraCount}
            </button>
            <button
              type="button"
              aria-label={`Xem các bước của ${exercise.nameEn}`}
              tabIndex={0}
              onClick={handleOpenSteps}
              className="w-full border-t border-slate-100 bg-violet-50 py-2 text-xs font-semibold text-violet-700 sm:hidden"
            >
              Xem {exercise.images.length} bước
            </button>
          </>
        )}
      </div>

      <ExerciseStepsModal
        exercise={exercise}
        isOpen={showSteps}
        onClose={() => setShowSteps(false)}
      />
    </>
  );
};
