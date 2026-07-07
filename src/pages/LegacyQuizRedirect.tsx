import { Navigate, useParams } from "react-router-dom";

export const LegacyQuizRedirect = () => {
  const { packId = "", mode = "" } = useParams<{ packId: string; mode: string }>();
  return <Navigate to={`/pilates/quiz/${packId}/${mode}`} replace />;
};
