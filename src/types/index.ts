export type ExerciseImage = {
  step: number;
  caption: string;
  url: string;
};

export type Exercise = {
  id: string;
  nameEn: string;
  nameVi: string;
  category: string;
  packId: string;
  prep: string;
  steps: string;
  reps: string;
  images: ExerciseImage[];
  audioUrl: string;
};

export type Pack = {
  id: string;
  name: string;
  description: string;
  exerciseIds: string[];
};

export type QuizMode = "listen-pick-image" | "peek-pick-name" | "type-name";

export type QuestionStatus = "unanswered" | "correct" | "wrong";

export type QuizAnswer = {
  value: string;
  isCorrect: boolean;
  submittedAt: number;
};
