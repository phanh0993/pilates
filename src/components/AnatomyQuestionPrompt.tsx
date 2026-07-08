import { AnatomyQuestionIllustration } from "./AnatomyQuestionIllustration";
import { getConceptIllustrationUrl, maskDefinition } from "../lib/anatomy";
import type { AnatomyConcept } from "../types/anatomy";

type AnatomyQuestionPromptProps = {
  concept: AnatomyConcept;
  pageIllustrations: Record<string, string>;
  prompt: string;
};

export const AnatomyQuestionPrompt = ({
  concept,
  pageIllustrations,
  prompt,
}: AnatomyQuestionPromptProps) => {
  const illustrationUrl = getConceptIllustrationUrl(concept, pageIllustrations);

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-xs font-semibold uppercase text-slate-500">
        {concept.section ?? concept.category}
      </p>
      {illustrationUrl && (
        <div className="mt-3">
          <AnatomyQuestionIllustration
            imageUrl={illustrationUrl}
            section={concept.section ?? concept.category}
          />
        </div>
      )}
      <p className="mt-3 text-base leading-relaxed text-slate-800">
        {maskDefinition(concept)}
      </p>
      <p className="mt-3 text-sm font-medium text-slate-600">{prompt}</p>
    </div>
  );
};
