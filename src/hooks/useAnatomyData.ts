import { useEffect, useState } from "react";
import type {
  AnatomyConcept,
  AnatomyDiagram,
  AnatomyPack,
} from "../types/anatomy";

export type AnatomyPage = {
  id: string;
  sourceFile: string;
  imageUrl: string;
  order: number;
};

type AnatomyDataState = {
  concepts: AnatomyConcept[];
  packs: AnatomyPack[];
  diagrams: AnatomyDiagram[];
  pages: AnatomyPage[];
  pageIllustrations: Record<string, string>;
  loading: boolean;
  error: string | null;
};

export const useAnatomyData = (): AnatomyDataState => {
  const [concepts, setConcepts] = useState<AnatomyConcept[]>([]);
  const [packs, setPacks] = useState<AnatomyPack[]>([]);
  const [diagrams, setDiagrams] = useState<AnatomyDiagram[]>([]);
  const [pages, setPages] = useState<AnatomyPage[]>([]);
  const [pageIllustrations, setPageIllustrations] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [conceptsRes, packsRes, diagramsRes, pagesRes, illustrationsRes] =
          await Promise.all([
          fetch("/data/anatomy/concepts.json"),
          fetch("/data/anatomy/packs.json"),
          fetch("/data/anatomy/diagrams.json"),
          fetch("/data/anatomy/pages-manifest.json"),
          fetch("/data/anatomy/page-illustrations.json"),
        ]);

        if (!conceptsRes.ok || !packsRes.ok || !diagramsRes.ok) {
          throw new Error("Không tải được dữ liệu giải phẫu");
        }

        setConcepts((await conceptsRes.json()) as AnatomyConcept[]);
        setPacks((await packsRes.json()) as AnatomyPack[]);
        setDiagrams((await diagramsRes.json()) as AnatomyDiagram[]);

        if (pagesRes.ok) {
          setPages((await pagesRes.json()) as AnatomyPage[]);
        }
        if (illustrationsRes.ok) {
          setPageIllustrations((await illustrationsRes.json()) as Record<string, string>);
        }
      } catch (loadError) {
        setError(loadError instanceof Error ? loadError.message : "Lỗi không xác định");
      } finally {
        setLoading(false);
      }
    };

    void load();
  }, []);

  return { concepts, packs, diagrams, pages, pageIllustrations, loading, error };
};
