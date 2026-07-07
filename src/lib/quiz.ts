import type { Exercise, Pack, QuizMode } from "../types";
import { shuffle } from "./shuffle";

export { shuffle };

export const normalizeAnswer = (value: string): string =>
  value
    .trim()
    .toLowerCase()
    .replace(/-/g, " ")
    .replace(/[^a-z0-9\s]/g, "")
    .replace(/\s+/g, " ");

export const isAnswerCorrect = (input: string, exercise: Exercise): boolean => {
  const normalized = normalizeAnswer(input);
  const expected = normalizeAnswer(exercise.nameEn);
  return normalized === expected;
};

export const pickDistractors = (
  exercise: Exercise,
  pool: Exercise[],
  count: number,
): Exercise[] => {
  const candidates = pool.filter(
    (item) => item.id !== exercise.id && item.packId === exercise.packId,
  );
  return shuffle(candidates).slice(0, count);
};

export const buildNameOptions = (exercise: Exercise, pool: Exercise[]): string[] => {
  const distractors = pickDistractors(exercise, pool, 3);
  return shuffle([exercise.nameEn, ...distractors.map((item) => item.nameEn)]);
};

export const buildImageOptions = (
  exercise: Exercise,
  pool: Exercise[],
): Exercise[] => {
  const distractors = pickDistractors(exercise, pool, 3);
  return shuffle([exercise, ...distractors]);
};

export const getPrimaryImage = (exercise: Exercise): string =>
  exercise.images[0]?.url ?? "";

export const getModeLabel = (mode: QuizMode): string => {
  if (mode === "listen-pick-image") return "Nghe tên → chọn hình";
  if (mode === "peek-pick-name") return "Nhìn hình → chọn tên";
  return "Nhìn hình → điền tên";
};

export const getPackExercises = (
  pack: Pack,
  exercises: Exercise[],
): Exercise[] => pack.exerciseIds
  .map((id) => exercises.find((exercise) => exercise.id === id))
  .filter((exercise): exercise is Exercise => Boolean(exercise));
