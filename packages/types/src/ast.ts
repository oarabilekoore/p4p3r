export type BBox = {
  x: number;
  y: number;
  width: number;
  height: number;
};

export type Style =
  | { type: "highlight"; color: string }
  | { type: "underline" }
  | { type: "bold" }
  | { type: "strikethrough" };

export type Span = { text: string; styles: Style[] };
export type Line = { spans: Span[] };

export type TextBlock = {
  type: "TextBlock";
  id: string;
  bbox: BBox;
  lines: Line[];
};

export enum MathLang {
  Latex,
  Typst,
}

export type Formula = {
  type: "Formula";
  id: string;
  bbox: BBox;
  value: string;
  mathlang: MathLang;
};
export type Figure = {
  type: "Figure";
  id: string;
  bbox: BBox;
  figure_type: "graph" | "chart" | "circuit" | "sketch" | "doodle" | "unknown";
  recognised_as?: string;
};

export type Table = {
  type: "Table";
  id: string;
  bbox: BBox;
  cells: Cell[];
};
export type Cell = {
  row: number;
  col: number;
  bbox: BBox;
  content: Element[];
};
export type Callout = {
  type: "Callout";
  id: string;
  bbox: BBox;
  shape: "circle" | "rectangle" | "cloud" | "other";
  content: TextBlock;
};
export type Link = {
  type: "Link";
  id: string;
  from_id: string;
  to_id: string;
  direction: "unidirectional" | "bidirectional" | "connector";
  path_type: "straight" | "curved" | "elbow";
  points: [number, number][];
};

export type Element = TextBlock | Formula | Figure | Table | Callout | Link;

export type Page = {
  type: "Page";
  page_number: number;
  dimensions: { width: number; height: number };
  elements: Element[];
};
