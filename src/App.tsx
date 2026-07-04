import { BrowserRouter, Route, Routes } from "react-router-dom";
import { useExerciseData } from "./hooks/useExerciseData";
import { HomePage } from "./pages/HomePage";
import { QuizPage } from "./pages/QuizPage";

const App = () => {
  const { exercises, packs, loading, error } = useExerciseData();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-slate-600">
        Đang tải dữ liệu...
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center px-4 text-center text-rose-600">
        {error}
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage packs={packs} />} />
        <Route path="/quiz/:packId/:mode" element={<QuizPage exercises={exercises} />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
