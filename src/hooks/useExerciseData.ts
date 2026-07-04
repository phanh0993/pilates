import { useEffect, useState } from "react";
import type { Exercise, Pack } from "../types";

type DataState = {
  exercises: Exercise[];
  packs: Pack[];
  loading: boolean;
  error: string | null;
};

export const useExerciseData = (): DataState => {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [packs, setPacks] = useState<Pack[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [exercisesRes, packsRes] = await Promise.all([
          fetch("/data/exercises.json"),
          fetch("/data/packs.json"),
        ]);

        if (!exercisesRes.ok || !packsRes.ok) {
          throw new Error("Không tải được dữ liệu bài tập");
        }

        const exercisesData = (await exercisesRes.json()) as Exercise[];
        const packsData = (await packsRes.json()) as Pack[];
        setExercises(exercisesData);
        setPacks(packsData);
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Lỗi không xác định");
      } finally {
        setLoading(false);
      }
    };

    void load();
  }, []);

  return { exercises, packs, loading, error };
};
