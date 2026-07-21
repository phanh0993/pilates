export type LessonTable = {
  cols: number;
  rows: string[][];
};

export type LessonBlock =
  | {
      id: string;
      type: "text";
      content: string;
    }
  | {
      id: string;
      type: "exercise";
      name: string;
      note: string;
      table: LessonTable;
    }
  | {
      id: string;
      type: "table";
      caption: string;
      table: LessonTable;
    };

export type LessonSection = {
  id: string;
  title: string;
  blocks: LessonBlock[];
};

export type LessonPlan = {
  id: string;
  title: string;
  subtitle: string;
  createdAt: string;
  updatedAt: string;
  sections: LessonSection[];
};
