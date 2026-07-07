export type AnatomyConcept = {
  id: string;
  term: string;
  termVi: string;
  definition: string;
  category: string;
  packId: string;
  section?: string;
  pageRef?: number;
  aliases?: string[];
};

export type AnatomyPack = {
  id: string;
  name: string;
  description: string;
  pageRange?: [number, number];
  conceptIds: string[];
  diagramIds: string[];
};

export type DiagramHotspot = {
  id: string;
  number: number;
  x: number;
  y: number;
  conceptId: string;
};

/** Sơ đồ điền chữ — che nhãn trên ảnh, ô input đặt đúng vị trí (phase 2) */
export type MaskedLabel = {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  answer: string;
  aliases?: string[];
};

export type AnatomyDiagram = {
  id: string;
  name: string;
  packId: string;
  imageUrl: string;
  /** 0 = không xoay; ảnh đã chỉnh EXIF đúng chiều đọc */
  rotation?: number;
  hotspots: DiagramHotspot[];
  maskedLabels?: MaskedLabel[];
};

export type AnatomyImportDraft = {
  sourceFile: string;
  pageType: "text" | "diagram" | "mixed" | "unknown";
  rawText: string;
  detectedTerms: string[];
  detectedLabels: { number: number; text: string }[];
};
