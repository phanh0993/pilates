import { useState } from "react";
import type { Exercise } from "../types";
import { getPrimaryImage } from "../lib/quiz";

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
  const [showExtras, setShowExtras] = useState(false);
  const extraCount = Math.max(exercise.images.length - 1, 0);

  let cardClass = "group relative overflow-hidden rounded-2xl border bg-white transition ";

  if (!isSubmitted) {
    cardClass += "border-slate-200 hover:border-violet-300 hover:shadow-md";
  } else if (isCorrect) {
    cardClass += "border-emerald-400 ring-2 ring-emerald-300";
  } else if (isSelected) {
    cardClass += "border-rose-400 ring-2 ring-rose-300";
  } else {
    cardClass += "border-slate-200 opacity-70";
  }

  const handleToggleExtras = () => {
    setShowExtras((prev) => !prev);
  };

  const handleKeyDownExtras = (event: React.KeyboardEvent<HTMLButtonElement>) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      handleToggleExtras();
    }
  };

  return (
    <div className={cardClass}>
      <div className="relative">
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
            className="h-44 w-full object-contain bg-slate-50"
          />
        </button>

        {extraCount > 0 && !isSubmitted && (
          <button
            type="button"
            aria-label={`Xem thêm ${extraCount} ảnh của động tác`}
            aria-expanded={showExtras}
            tabIndex={0}
            onClick={handleToggleExtras}
            onKeyDown={handleKeyDownExtras}
            className="absolute right-2 top-2 z-10 rounded-full bg-violet-600 px-2.5 py-1 text-xs font-bold text-white opacity-0 shadow-md transition hover:bg-violet-700 group-hover:opacity-100 group-focus-within:opacity-100 focus:opacity-100"
          >
            +{extraCount}
          </button>
        )}
      </div>

      {showExtras && extraCount > 0 && (
        <div className="border-t border-slate-100 bg-slate-50 p-2">
          <p className="mb-2 px-1 text-xs font-medium text-slate-500">
            Các bước của động tác
          </p>
          <div className="grid grid-cols-3 gap-2">
            {exercise.images.map((image) => (
              <div
                key={image.url}
                className="overflow-hidden rounded-lg border border-slate-200 bg-white"
              >
                <img
                  src={image.url}
                  alt={`Bước ${image.step}`}
                  className="h-16 w-full object-cover"
                />
                <p className="truncate px-1 py-0.5 text-[10px] text-slate-600">
                  {image.step}. {image.caption}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
