import type { AnatomyConcept } from "../types/anatomy";

const shuffle = <T,>(items: T[]): T[] => {
  const copy = [...items];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
};

export const normalizeTerm = (value: string): string =>
  value
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9\s]/g, "")
    .replace(/\s+/g, " ");

export const isTermCorrect = (input: string, concept: AnatomyConcept): boolean => {
  const normalized = normalizeTerm(input);
  const candidates = [concept.term, concept.termVi, ...(concept.aliases ?? [])];
  return candidates.some((item) => normalizeTerm(item) === normalized);
};

const BLANK = "_____";

const escapeRegex = (value: string): string =>
  value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/** Che thuật ngữ đáp án trong câu định nghĩa bằng chỗ trống */
export const maskDefinition = (concept: AnatomyConcept): string => {
  const text = concept.definition;
  const terms = [concept.term, concept.termVi, ...(concept.aliases ?? [])]
    .filter((t) => t.trim().length >= 2)
    .sort((a, b) => b.length - a.length);

  for (const term of terms) {
    const pattern = new RegExp(escapeRegex(term).replace(/\s+/g, "\\s+"), "gi");
    if (pattern.test(text)) {
      return text.replace(pattern, BLANK);
    }
  }

  const normalizedDef = normalizeTerm(text);
  for (const term of terms) {
    const normalizedTerm = normalizeTerm(term);
    if (normalizedTerm.length < 2) continue;
    const idx = normalizedDef.indexOf(normalizedTerm);
    if (idx === -1) continue;

    let normPos = 0;
    let start = -1;
    let end = -1;
    for (let i = 0; i < text.length; i += 1) {
      const ch = text[i];
      if (/[\p{L}\p{N}]/u.test(ch)) {
        if (normPos === idx) start = i;
        normPos += 1;
        if (normPos === idx + normalizedTerm.length) {
          end = i + 1;
          break;
        }
      }
    }
    if (start >= 0 && end > start) {
      return text.slice(0, start) + BLANK + text.slice(end);
    }
  }

  return `${text}\n\nThuật ngữ cần điền: ${BLANK}`;
};

const relatedConcepts = (concept: AnatomyConcept, pool: AnatomyConcept[]): AnatomyConcept[] => {
  const section = concept.section ?? concept.category;
  const sameSection = pool.filter(
    (item) => item.id !== concept.id && (item.section ?? item.category) === section,
  );
  if (sameSection.length >= 3) return sameSection;

  const samePack = pool.filter(
    (item) =>
      item.id !== concept.id &&
      item.packId === concept.packId &&
      !sameSection.some((s) => s.id === item.id),
  );
  const merged = [...sameSection, ...samePack];
  if (merged.length >= 3) return merged;

  const rest = pool.filter(
    (item) => item.id !== concept.id && !merged.some((m) => m.id === item.id),
  );
  return [...merged, ...rest];
};

export const buildConceptOptions = (
  concept: AnatomyConcept,
  pool: AnatomyConcept[],
): AnatomyConcept[] => {
  const candidates = relatedConcepts(concept, pool);
  const distractors = shuffle(candidates).slice(0, 3);
  return shuffle([concept, ...distractors]);
};

export const getConceptById = (
  concepts: AnatomyConcept[],
  id: string,
): AnatomyConcept | undefined => concepts.find((c) => c.id === id);

export const getPackConcepts = (
  conceptIds: string[],
  concepts: AnatomyConcept[],
): AnatomyConcept[] =>
  conceptIds
    .map((id) => concepts.find((c) => c.id === id))
    .filter((c): c is AnatomyConcept => Boolean(c));

export type MixedQuestionMode = "mcq" | "type";

export type MixedExamQuestion = {
  concept: AnatomyConcept;
  mode: MixedQuestionMode;
};

export const buildMixedExam = (
  concepts: AnatomyConcept[],
  limit?: number,
): MixedExamQuestion[] => {
  const selected = limit ? shuffle(concepts).slice(0, Math.min(limit, concepts.length)) : shuffle([...concepts]);
  return selected.map((concept) => ({
    concept,
    mode: Math.random() < 0.5 ? "mcq" : "type",
  }));
};

export const countExamScore = (answers: Record<number, { isCorrect: boolean }>, total: number) => {
  const entries = Object.values(answers);
  const answered = entries.length;
  const correct = entries.filter((a) => a.isCorrect).length;
  const percent = answered > 0 ? Math.round((correct / answered) * 100) : 0;
  const finished = answered === total;
  return { answered, correct, total, percent, finished };
};
