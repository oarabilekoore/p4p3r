import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function DocsPipeline() {
  const processors = [
    { label: "Plain_Text", desc: "TrOCR (microsoft/trocr-base-handwritten) + style detectors" },
    { label: "Formula", desc: "LaTeX-OCR (Pix2Tex)" },
    { label: "Figure", desc: "Preserved image crop in v1, subclassified in v2" },
    { label: "Table", desc: "Cell segmentation → TrOCR per cell in v2" },
    { label: "Link", desc: "Stroke skeleton analysis → arrowhead directionality" },
    { label: "Callout", desc: "Contour classification (shape) + inner TrOCR" },
    { label: "Abandon", desc: "Discarded" },
  ]

  return (
    <div className="space-y-12 text-coffee-muted text-sm leading-relaxed">
      <section id="intro" className="scroll-mt-24 space-y-4">
        <h2 className="text-2xl font-bold font-serif text-coffee-text">What PaperMd Does</h2>
        <p>
          PaperMd is an offline pipeline converting handwritten note photos into editable documents. A picture of a notebook page goes in, and a structured Excalidraw document comes out, preserving the original page layout.
        </p>
      </section>

      <section id="problems" className="scroll-mt-24 space-y-4">
        <h2 className="text-2xl font-bold font-serif text-coffee-text">The Problem with Existing Tools</h2>
        <p>
          Generic layout detection fails on handwriting. LayoutParser (EfficientDet) was trained on digital PDFs, misclassifying handwriting as huge tables. OpenCV thresholding is highly brittle under uneven notebook lighting. Tesseract lacks block awareness, fragmenting single paragraphs.
        </p>
      </section>

      <section id="pipeline" className="scroll-mt-24 space-y-4">
        <h2 className="text-2xl font-bold font-serif text-coffee-text">How the Pipeline Works</h2>
        <div className="space-y-6">
          <div>
            <h3 className="font-bold text-coffee-text mb-1">Stage 1: YOLOv11 Nano Layout Detection</h3>
            <p>
              A custom YOLOv11 Nano model segments the page into 7 classes (Abandon, Plain_Text, Formula, Figure, Table, Link, Callout). YOLO Nano is selected for local edge-computing, running on an Intel Celeron without a GPU.
            </p>
          </div>
          <div>
            <h3 className="font-bold text-coffee-text mb-2">Stage 2: Ink Runtime Content Extraction</h3>
            <p className="mb-4">
              Detected regions are cropped and routed to specialist interpreters:
            </p>
            <div className="border border-coffee-muted/10 rounded-lg overflow-hidden bg-coffee-surface">
              {processors.map((p) => (
                <div key={p.label} className="grid grid-cols-3 border-b border-coffee-muted/10 p-3 text-xs last:border-none">
                  <span className="font-mono text-coffee-accent font-semibold">{p.label}</span>
                  <span className="col-span-2 text-coffee-muted">{p.desc}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
