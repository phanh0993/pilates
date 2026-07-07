import { BrowserRouter, Route, Routes } from "react-router-dom";
import { useAnatomyData } from "./hooks/useAnatomyData";
import { useExerciseData } from "./hooks/useExerciseData";
import { AnatomyAdminPage } from "./pages/AnatomyAdminPage";
import { AnatomyHomePage } from "./pages/AnatomyHomePage";
import { AnatomyMcqPage } from "./pages/AnatomyMcqPage";
import { AnatomyMixedExamPage } from "./pages/AnatomyMixedExamPage";
import { AnatomyStudyPage } from "./pages/AnatomyStudyPage";
import { AnatomyTypePage } from "./pages/AnatomyTypePage";
import { LegacyQuizRedirect } from "./pages/LegacyQuizRedirect";
import { PilatesHomePage } from "./pages/PilatesHomePage";
import { QuizPage } from "./pages/QuizPage";
import { SubjectHomePage } from "./pages/SubjectHomePage";

const LoadingScreen = () => (
  <div className="flex min-h-screen items-center justify-center text-slate-600">
    Đang tải dữ liệu...
  </div>
);

const App = () => {
  const pilates = useExerciseData();
  const anatomy = useAnatomyData();

  if (pilates.loading || anatomy.loading) {
    return <LoadingScreen />;
  }

  if (pilates.error && anatomy.error) {
    return (
      <div className="flex min-h-screen items-center justify-center px-4 text-center text-rose-600">
        {pilates.error || anatomy.error}
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SubjectHomePage />} />

        <Route
          path="/pilates"
          element={<PilatesHomePage packs={pilates.packs} />}
        />
        <Route
          path="/pilates/quiz/:packId/:mode"
          element={<QuizPage exercises={pilates.exercises} />}
        />
        <Route path="/quiz/:packId/:mode" element={<LegacyQuizRedirect />} />

        <Route
          path="/anatomy"
          element={
            <AnatomyHomePage packs={anatomy.packs} concepts={anatomy.concepts} />
          }
        />
        <Route
          path="/anatomy/exam/:packId"
          element={
            <AnatomyMixedExamPage
              concepts={anatomy.concepts}
              packs={anatomy.packs}
            />
          }
        />
        <Route
          path="/anatomy/mcq/:packId"
          element={<AnatomyMcqPage concepts={anatomy.concepts} />}
        />
        <Route
          path="/anatomy/type/:packId"
          element={<AnatomyTypePage concepts={anatomy.concepts} />}
        />
        <Route
          path="/anatomy/study/:packId"
          element={
            <AnatomyStudyPage pages={anatomy.pages} packs={anatomy.packs} />
          }
        />
        <Route
          path="/admin/anatomy"
          element={<AnatomyAdminPage concepts={anatomy.concepts} />}
        />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
