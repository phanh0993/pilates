import type { AnatomyConcept } from "../types/anatomy";
import { shuffle } from "./shuffle";

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

type AnswerKind = "quantity" | "angle" | "term";

const getAnswerKind = (concept: AnatomyConcept): AnswerKind => {
  if (/°/.test(concept.term) || /°/.test(concept.termVi) || /góc/i.test(concept.definition)) {
    return "angle";
  }
  if (
    /^\d/.test(concept.term.trim()) ||
    /^Số |^Tổng cộng có \d+/i.test(concept.definition)
  ) {
    return "quantity";
  }
  return "term";
};

const escapeRegex = (value: string): string =>
  value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/** Che thuật ngữ đáp án trong câu định nghĩa bằng chỗ trống */
export const maskDefinition = (concept: AnatomyConcept): string => {
  const text = concept.definition;
  const kind = getAnswerKind(concept);
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

  if (kind === "quantity" || kind === "angle") {
    return `${text.replace(/\.\s*$/, "")}: ${BLANK}`;
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

const sameKindPool = (concept: AnatomyConcept, pool: AnatomyConcept[]): AnatomyConcept[] => {
  const kind = getAnswerKind(concept);
  return pool.filter((item) => item.id !== concept.id && getAnswerKind(item) === kind);
};

const generateQuantityDistractors = (
  concept: AnatomyConcept,
  count: number,
): AnatomyConcept[] => {
  const termMatch = concept.term.match(/^(\d+)([\s\S]*)$/);
  if (!termMatch || count <= 0) return [];

  const correct = parseInt(termMatch[1], 10);
  const suffix = termMatch[2];
  const viMatch = concept.termVi.match(/^(\d+)([\s\S]*)$/);
  const viSuffix = viMatch?.[2] ?? "";

  const offsets = shuffle([-30, -20, -12, 12, 18, 24, 35, 50, -8, 8]);
  const values: number[] = [];

  for (const offset of offsets) {
    const value = correct + offset;
    if (value > 0 && value !== correct && !values.includes(value)) {
      values.push(value);
    }
    if (values.length >= count) break;
  }

  return values.slice(0, count).map((num) => ({
    ...concept,
    id: `${concept.id}-d-${num}`,
    term: `${num}${suffix}`,
    termVi: viMatch ? `${num}${viSuffix}` : `${num}`,
    aliases: undefined,
  }));
};

export const buildConceptOptions = (
  concept: AnatomyConcept,
  pool: AnatomyConcept[],
): AnatomyConcept[] => {
  const kind = getAnswerKind(concept);

  if (kind === "quantity") {
    const peers = relatedConcepts(concept, sameKindPool(concept, pool));
    const distractors: AnatomyConcept[] = shuffle([...peers]).slice(0, 3);
    if (distractors.length < 3) {
      distractors.push(...generateQuantityDistractors(concept, 3 - distractors.length));
    }
    return shuffle([concept, ...distractors.slice(0, 3)]);
  }

  if (kind === "angle") {
    const withDegree = (items: AnatomyConcept[]) =>
      items.filter((c) => /°/.test(c.term) || /°/.test(c.termVi));
    let anglePool = withDegree(sameKindPool(concept, pool));
    if (anglePool.length < 3) {
      anglePool = withDegree(pool.filter((c) => c.id !== concept.id));
    }
    const candidates = relatedConcepts(concept, anglePool);
    const distractors = shuffle(candidates).slice(0, 3);
    return shuffle([concept, ...distractors]);
  }

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
