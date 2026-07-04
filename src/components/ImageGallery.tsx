import { useState } from "react";
import type { Exercise } from "../types";

type ImageGalleryProps = {
  exercise: Exercise;
};

export const ImageGallery = ({ exercise }: ImageGalleryProps) => {
  const [activeStep, setActiveStep] = useState(0);
  const [showExtras, setShowExtras] = useState(false);
  const activeImage = exercise.images[activeStep] ?? exercise.images[0];
  const extraCount = Math.max(exercise.images.length - 1, 0);

  const handleSelectStep = (index: number) => {
    setActiveStep(index);
    setShowExtras(true);
  };

  const handleToggleExtras = () => {
    setShowExtras((prev) => !prev);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLButtonElement>, index: number) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      handleSelectStep(index);
    }
  };

  if (!activeImage) {
    return null;
  }

  return (
    <div className="space-y-3">
      <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <img
          src={activeImage.url}
          alt={`${exercise.nameEn} - bước ${activeImage.step}`}
          className="mx-auto max-h-[360px] w-full object-contain bg-slate-50"
        />
        <div className="flex items-center justify-between border-t border-slate-100 px-4 py-2 text-sm text-slate-600">
          <span>
            {activeImage.step}. {activeImage.caption}
          </span>
          {extraCount > 0 && (
            <button
              type="button"
              aria-label={`Xem thêm ${extraCount} ảnh`}
              tabIndex={0}
              onClick={handleToggleExtras}
              className="rounded-full bg-violet-100 px-3 py-1 text-xs font-bold text-violet-700 hover:bg-violet-200"
            >
              +{extraCount}
            </button>
          )}
        </div>
      </div>

      {showExtras && extraCount > 0 && (
        <div className="grid grid-cols-3 gap-2 sm:grid-cols-4">
          {exercise.images.map((image, index) => (
            <button
              key={image.url}
              type="button"
              aria-label={`Xem ảnh bước ${image.step}`}
              tabIndex={0}
              onClick={() => handleSelectStep(index)}
              onKeyDown={(event) => handleKeyDown(event, index)}
              className={`overflow-hidden rounded-xl border-2 transition ${
                index === activeStep
                  ? "border-violet-500"
                  : "border-transparent hover:border-violet-300"
              }`}
            >
              <img
                src={image.url}
                alt={`Bước ${image.step}`}
                className="h-20 w-full object-cover bg-slate-100"
              />
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
