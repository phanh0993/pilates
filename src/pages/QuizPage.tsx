import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { AnswerFeedback } from "../components/AnswerFeedback";
import { ImageGallery } from "../components/ImageGallery";
import { ListenImageOption } from "../components/ListenImageOption";
import { QuestionNav } from "../components/QuestionNav";
import {
  buildImageOptions,
  buildNameOptions,
  getModeLabel,
  getPackExercises,
  isAnswerCorrect,
} from "../lib/quiz";
import type { Exercise, QuestionStatus, QuizAnswer, QuizMode } from "../types";

type QuizPageProps = {
  exercises: Exercise[];
};

type OptionCache = {
  names: string[];
  images: Exercise[];
};

export const QuizPage = ({ exercises }: QuizPageProps) => {
  const { packId = "", mode = "peek-pick-name" } = useParams<{
    packId: string;
    mode: QuizMode;
  }>();

  const quizMode = mode as QuizMode;
  const packExercises = useMemo(
    () =>
      getPackExercises(
        {
          id: packId,
          name: "",
          description: "",
          exerciseIds: exercises.filter((e) => e.packId === packId).map((e) => e.id),
        },
        exercises,
      ),
    [exercises, packId],
  );

  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, QuizAnswer>>({});
  const [typedValue, setTypedValue] = useState("");
  const [optionCache, setOptionCache] = useState<Record<number, OptionCache>>({});
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const currentExercise = packExercises[currentIndex];
  const currentAnswer = answers[currentIndex];
  const isSubmitted = Boolean(currentAnswer);

  useEffect(() => {
    setOptionCache((prev) => {
      const next = { ...prev };
      packExercises.forEach((exercise, index) => {
        if (!next[index]) {
          next[index] = {
            names: buildNameOptions(exercise, exercises),
            images: buildImageOptions(exercise, exercises),
          };
        }
      });
      return next;
    });
  }, [exercises, packExercises]);

  useEffect(() => {
    setTypedValue("");
  }, [currentIndex]);

  useEffect(() => {
    if (quizMode !== "listen-pick-image" || !currentExercise || isSubmitted) {
      return;
    }

    const audio = new Audio(currentExercise.audioUrl);
    audioRef.current = audio;
    void audio.play().catch(() => undefined);

    return () => {
      audio.pause();
      audioRef.current = null;
    };
  }, [currentExercise, currentIndex, isSubmitted, quizMode]);

  const statuses: QuestionStatus[] = packExercises.map((_, index) => {
    const answer = answers[index];
    if (!answer) return "unanswered";
    return answer.isCorrect ? "correct" : "wrong";
  });

  const handleSubmitChoice = (value: string, isCorrect: boolean) => {
    if (isSubmitted) return;
    setAnswers((prev) => ({
      ...prev,
      [currentIndex]: {
        value,
        isCorrect,
        submittedAt: Date.now(),
      },
    }));
  };

  const handleSubmitTyped = () => {
    if (!currentExercise || isSubmitted || !typedValue.trim()) return;
    handleSubmitChoice(typedValue, isAnswerCorrect(typedValue, currentExercise));
  };

  const handleReplayAudio = () => {
    if (!currentExercise) return;
    const audio = new Audio(currentExercise.audioUrl);
    void audio.play().catch(() => undefined);
  };

  const handleKeyDownSubmit = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleSubmitTyped();
    }
  };

  if (!currentExercise) {
    return (
      <div className="px-4 py-10 text-center">
        <p className="text-slate-600">Không tìm thấy gói đề.</p>
        <Link to="/" className="mt-4 inline-block text-violet-600 underline">
          Về trang chủ
        </Link>
      </div>
    );
  }

  const options = optionCache[currentIndex];

  return (
    <div className="mx-auto flex min-h-screen max-w-4xl flex-col">
      <header className="border-b border-slate-200 bg-white px-4 py-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-violet-600">
              {getModeLabel(quizMode)}
            </p>
            <h1 className="text-lg font-bold text-slate-900">
              Câu {currentIndex + 1}/{packExercises.length}
            </h1>
          </div>
          <Link
            to="/"
            className="rounded-xl border border-slate-200 px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50"
          >
            Trang chủ
          </Link>
        </div>
      </header>

      <main className="flex-1 space-y-5 px-4 py-5">
        {quizMode === "listen-pick-image" && (
          <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
            <p className="mb-3 text-sm text-slate-600">Nghe tên động tác và chọn hình đúng:</p>
            <button
              type="button"
              aria-label="Phát lại tên động tác"
              tabIndex={0}
              onClick={handleReplayAudio}
              className="rounded-xl bg-violet-600 px-4 py-2 text-sm font-semibold text-white hover:bg-violet-700"
            >
              🔊 Phát lại
            </button>
          </div>
        )}

        {quizMode !== "listen-pick-image" && (
          <ImageGallery exercise={currentExercise} />
        )}

        {quizMode === "peek-pick-name" && options && (
          <div className="grid gap-3 sm:grid-cols-2">
            {options.names.map((name) => {
              const isCorrect = name === currentExercise.nameEn;
              const isSelected = currentAnswer?.value === name;
              let buttonClass =
                "rounded-xl border px-4 py-3 text-left text-sm font-semibold transition ";

              if (!isSubmitted) {
                buttonClass += "border-slate-200 bg-white hover:border-violet-300 hover:bg-violet-50";
              } else if (isCorrect) {
                buttonClass += "border-emerald-400 bg-emerald-100 text-emerald-900";
              } else if (isSelected) {
                buttonClass += "border-rose-400 bg-rose-100 text-rose-900";
              } else {
                buttonClass += "border-slate-200 bg-slate-50 text-slate-500";
              }

              return (
                <button
                  key={name}
                  type="button"
                  aria-label={`Chọn ${name}`}
                  tabIndex={0}
                  disabled={isSubmitted}
                  onClick={() => handleSubmitChoice(name, isCorrect)}
                  className={buttonClass}
                >
                  {name}
                </button>
              );
            })}
          </div>
        )}

        {quizMode === "listen-pick-image" && options && (
          <div className="grid gap-3 sm:grid-cols-2">
            {options.images.map((option) => (
              <ListenImageOption
                key={option.id}
                exercise={option}
                isSubmitted={isSubmitted}
                isCorrect={option.id === currentExercise.id}
                isSelected={currentAnswer?.value === option.id}
                onSelect={() =>
                  handleSubmitChoice(option.id, option.id === currentExercise.id)
                }
              />
            ))}
          </div>
        )}

        {quizMode === "type-name" && (
          <div className="space-y-3">
            <label htmlFor="answer-input" className="text-sm font-medium text-slate-700">
              Nhập tên tiếng Anh của động tác
            </label>
            <div className="flex gap-2">
              <input
                id="answer-input"
                type="text"
                value={typedValue}
                disabled={isSubmitted}
                onChange={(event) => setTypedValue(event.target.value)}
                onKeyDown={handleKeyDownSubmit}
                placeholder="Ví dụ: Roll Down"
                className="flex-1 rounded-xl border border-slate-300 px-4 py-3 text-base outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-200"
              />
              <button
                type="button"
                aria-label="Nộp câu trả lời"
                tabIndex={0}
                disabled={isSubmitted || !typedValue.trim()}
                onClick={handleSubmitTyped}
                className="rounded-xl bg-violet-600 px-5 py-3 text-sm font-semibold text-white hover:bg-violet-700 disabled:cursor-not-allowed disabled:bg-slate-300"
              >
                Kiểm tra
              </button>
            </div>
          </div>
        )}

        {isSubmitted && currentAnswer && (
          <AnswerFeedback
            exercise={currentExercise}
            isCorrect={currentAnswer.isCorrect}
            showAnswer={quizMode === "type-name"}
          />
        )}

        {isSubmitted && (
          <details className="rounded-2xl border border-slate-200 bg-white p-4">
            <summary className="cursor-pointer text-sm font-semibold text-slate-700">
              Xem hướng dẫn tập
            </summary>
            <div className="mt-3 space-y-2 text-sm text-slate-600">
              <p>
                <span className="font-semibold text-slate-800">Chuẩn bị:</span>{" "}
                {currentExercise.prep}
              </p>
              <p>
                <span className="font-semibold text-slate-800">Cách thực hiện:</span>{" "}
                {currentExercise.steps}
              </p>
              <p>
                <span className="font-semibold text-slate-800">Lặp:</span>{" "}
                {currentExercise.reps}
              </p>
            </div>
          </details>
        )}
      </main>

      <QuestionNav
        total={packExercises.length}
        currentIndex={currentIndex}
        statuses={statuses}
        onSelect={setCurrentIndex}
      />
    </div>
  );
};
