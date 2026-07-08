type AnatomyQuestionIllustrationProps = {
  imageUrl: string;
  section?: string;
};

export const AnatomyQuestionIllustration = ({
  imageUrl,
  section,
}: AnatomyQuestionIllustrationProps) => (
  <div className="overflow-hidden rounded-xl border border-slate-100 bg-slate-50">
    <img
      src={imageUrl}
      alt={section ? `Minh họa: ${section}` : "Minh họa giải phẫu"}
      className="mx-auto max-h-64 w-full object-contain"
    />
  </div>
);
