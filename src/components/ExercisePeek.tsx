import { useState } from "react";
import type { Exercise } from "../types";
import { ExerciseStepsModal } from "./ExerciseStepsModal";

type ExercisePeekProps = {
  exercise: Exercise;
  fixed?: boolean;
};

export const ExercisePeek = ({ exercise, fixed = true }: ExercisePeekProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const primaryImage = exercise.images[0];
  const extraCount = Math.max(exercise.images.length - 1, 0);

  const handleOpen = () => {
    setIsOpen(true);
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLButtonElement>) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      handleOpen();
    }
  };

  if (!primaryImage) {
    return null;
  }

  const positionClass = fixed
    ? "fixed right-3 top-[4.75rem] z-40 sm:right-4"
    : "relative";

  return (
    <>
      <button
        type="button"
        aria-label={`Xem ${exercise.images.length} bước động tác`}
        tabIndex={0}
        onClick={handleOpen}
        onKeyDown={handleKeyDown}
        className={`${positionClass} w-[5.5rem] overflow-hidden rounded-2xl border-2 border-violet-400 bg-white shadow-lg shadow-violet-200/60 transition active:scale-95 sm:w-24`}
      >
        <div className="relative">
          <img
            src={primaryImage.url}
            alt="Peek động tác"
            className="aspect-square w-full object-cover bg-slate-100"
          />
          {extraCount > 0 && (
            <span className="absolute bottom-1 right-1 rounded-full bg-violet-600 px-1.5 py-0.5 text-[10px] font-bold text-white">
              +{extraCount}
            </span>
          )}
        </div>
        <div className="bg-violet-600 px-1 py-1.5 text-center text-[10px] font-bold uppercase tracking-wide text-white sm:text-[11px]">
          Peek
        </div>
      </button>

      <ExerciseStepsModal exercise={exercise} isOpen={isOpen} onClose={handleClose} />
    </>
  );
};
