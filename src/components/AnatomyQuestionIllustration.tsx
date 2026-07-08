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
      alt={section ? `Trang sách: ${section}` : "Trang sách giải phẫu"}
      className="mx-auto w-full object-contain"
    />
  </div>
);
