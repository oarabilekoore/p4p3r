import { CheckSquare, Square } from "lucide-react"

export default function DocsRoadmap() {
  const v1 = [
    { text: "Research phase: pre-trained model evaluation", done: true },
    { text: "Architecture decision: custom YOLOv11 Nano", done: true },
    { text: "Proof of concept: figure detection working", done: true },
    { text: "Active learning loop in Label Studio", done: true },
    { text: "rclone backup sync for Label Studio data", done: true },
    { text: "Annotation Batch 1: 50 images", done: false },
    { text: "Annotation Batch 2: 100+ images", done: false },
    { text: "First full training run with stable annotation", done: false },
    { text: "TrOCR & LaTeX-OCR integration", done: false },
    { text: "Excalidraw document reconstruction", done: false },
  ]

  const v2 = [
    { text: "Figure subclassification model (circuit, chart)", done: false },
    { text: "Table cell extraction & Inline styles", done: false },
    { text: "DOCX and Typst export targets", done: false },
  ]

  const renderList = (items: { text: string; done: boolean }[]) => (
    <ul className="space-y-2 mt-3">
      {items.map((item, idx) => (
        <li key={idx} className="flex items-center gap-2.5 text-xs text-coffee-muted">
          {item.done ? (
            <CheckSquare className="size-4 text-coffee-accent shrink-0" />
          ) : (
            <Square className="size-4 text-coffee-muted/40 shrink-0" />
          )}
          <span className={item.done ? "line-through text-coffee-muted/65" : "text-coffee-muted"}>
            {item.text}
          </span>
        </li>
      ))}
    </ul>
  )

  return (
    <section id="roadmap" className="scroll-mt-24 space-y-6">
      <h2 className="text-2xl font-bold font-serif text-coffee-text">Roadmap</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-coffee-surface p-4 rounded-lg border border-coffee-muted/10">
          <span className="font-serif font-semibold text-coffee-text text-sm block border-b border-coffee-muted/10 pb-2">v1 — Core Pipeline</span>
          {renderList(v1)}
        </div>
        <div className="bg-coffee-surface p-4 rounded-lg border border-coffee-muted/10">
          <span className="font-serif font-semibold text-coffee-text text-sm block border-b border-coffee-muted/10 pb-2">v2 — Extended Content</span>
          {renderList(v2)}
        </div>
        <div className="bg-coffee-surface p-4 rounded-lg border border-coffee-muted/10">
          <span className="font-serif font-semibold text-coffee-text text-sm block border-b border-coffee-muted/10 pb-2">v3 — Generalisation</span>
          {renderList([
            { text: "Multi-language handwriting support", done: false },
            { text: "Scan input support", done: false },
            { text: "Public dataset release", done: false },
          ])}
        </div>
      </div>
    </section>
  )
}
