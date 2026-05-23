# PaperMd

![Status](https://img.shields.io/badge/Status-Active_Development-green)
![Stage](https://img.shields.io/badge/Stage-Dataset_Annotation-blue)
![Architecture](https://img.shields.io/badge/Model-YOLOv11_Nano-orange)
![License: Model](https://img.shields.io/badge/Model_License-GPL--3.0-blue)
![License: App](https://img.shields.io/badge/App_License-BSL--1.1-orange)

PaperMd is a local-first, offline pipeline that converts photographs of handwritten notes into structured digital documents. A photo of a notebook page goes in — a clean, formatted, editable document comes out.

The core thesis is that layout understanding and handwriting recognition are two separate problems that must be solved independently before they can be composed. PaperMd solves them in sequence.



## The Problem

Existing document AI is trained on digital PDFs and typed text. It fails on handwriting because handwriting has no implicit grid — ascenders and descenders from adjacent lines overlap in pixel space, ink color varies, ruled lines interfere, and no two people's spatial conventions are the same. Generic tools like LayoutParser and DocLayout-YOLO misclassify entire handwritten pages as a single figure. Tesseract fragments paragraphs into individual lines. There is no production-grade open tool that handles this correctly.

PaperMd is being built to solve this specifically and locally, with no external API dependencies.



## Current Status

**Phase: Dataset Annotation — Batch 1 (50 images)**

The first training batch is being annotated in Label Studio using the class schema below. A proof-of-concept model trained on 61 images (earlier label schema) already detects figures at 0.88 confidence and equations at 0.41–0.66 confidence. Equation fragmentation is the primary known issue and is being addressed through annotation consistency rules in this batch. An active learning loop is in place — the current model pre-labels new images in Label Studio, which are then reviewed and corrected rather than annotated from scratch.

Target for v1 release: 300+ annotated images across diverse handwriting styles, subjects, and capture conditions.


## Label Schema

The following classes are used for layout annotation in Label Studio:

| ID | Class | Description |
|---|---|---|
| `0` | `Abandon` | Crossed-out or cancelled content |
| `1` | `Plain_Text` | Body paragraph, heading, title, caption, or date header |
| `2` | `Formula` | Mathematical expression or equation |
| `3` | `Figure` | Diagram, graph, sketch, or any visual content |
| `4` | `Table` | Tabular data with visible or implied grid structure |
| `5` | `Link` | Arrow or line connecting two other elements |
| `6` | `Callout` | Text enclosed by a drawn shape (circle, rectangle, cloud) |

### Annotation Rules

**Plain_Text**
- Body paragraphs, headings, titles, captions, and date headers at the top of a page are all `Plain_Text`. Position in the layout conveys their role — no separate label is needed.
- A sentence containing inline math (e.g. "where n is the number of values") is `Plain_Text`. A standalone expression on its own line is `Formula`.
- Highlighted words, underlines, or circled numbers within a paragraph do not change the label — the block remains one `Plain_Text` bounding box. Style details are recovered during content extraction, not annotation.
- Handwritten code and pseudocode are `Plain_Text`.
- Lists do not have a dedicated label. A list body is annotated as `Plain_Text`. Circled or decorated list numbers are part of the same `Plain_Text` block.

**Formula**
- One bounding box covers the entire expression. If three lines form one equation, one box covers all three. Fragmentation into per-line boxes is the single most common annotation error and directly causes fragmented inference.

**Figure**
- Any visual element that is not text or a table: diagrams, graphs, sketches, circuit drawings, flowcharts.
- A second model (v2) subclassifies figures into graph, chart, circuit, and sketch after layout detection.

**Table**
- Label the outer boundary of the table as `Table`.
- Also label elements inside the table cells using their respective classes (`Plain_Text`, `Formula`, etc.). Nested annotation is intentional — the content extraction stage needs to know what is inside each cell.

**Link**
- Any arrow or plain connecting line between two other elements on the page.
- Directionality (unidirectional, bidirectional, or plain connector) is determined during content extraction by detecting arrowheads at the stroke endpoints — it does not need to be captured during annotation.

**Callout**
- Text that a person has enclosed with a drawn shape: a circle around a word, a rectangle around a note, a cloud around a reminder.
- This is distinct from a figure. The enclosed content is text, not a drawing.
- Label the full bounding box including the drawn shape and its enclosed text as one `Callout` region.

**General**
- **Formula boxes span the full block** — fragmentation is the single most common annotation error.
- **Boxes are consistently loose** — due to ascender/descender overlap between handwritten lines, boxes will clip adjacent ruled lines. This is acceptable. Consistent loose boxes across all images are better than inconsistently tight ones.
- **Minimum annotation size** — do not annotate content smaller than approximately 20×20px at normalised resolution. Stray marks and marginalia are ignored.
- **Do not annotate** plain highlighted text or underlined text as separate regions. These are rendering details recovered after detection.



## System Architecture

PaperMd executes a three-stage pipeline.

### Stage 1 — Layout Detection (Model 1)

A custom YOLOv11 Nano model segments the page into discrete content blocks and classifies each into the schema above. YOLO Nano is chosen specifically for its edge-computing profile — it runs entirely offline via ONNX on low-end hardware including Intel Celeron.

**Training pipeline:**
1. Images annotated in Label Studio (YOLO format export)
2. Active learning loop — current model pre-labels; human reviews and corrects
3. Model trained on Google Colab (GPU)
4. Weights exported for local inference

**Known challenges:**
- Handwriting has no implicit grid — interleaved ascenders/descenders make bounding boxes inherently imprecise for text regions
- Dataset diversity across handwriting styles is critical for generalisation and requires contributions beyond the author's own notes
- Minimum viable dataset: 300 annotated images. Target for generalisation: 1000+

### Stage 2 — Content Extraction (Ink Runtime)

Each detected region is cropped from the page image and passed to the Ink Runtime — the component responsible for interpreting the ink within each bounding box and producing structured output. The Ink Runtime routes each crop to a specialist processor based on its class label:

| Class | Processor |
|---|---|
| `Plain_Text` | TrOCR (`microsoft/trocr-base-handwritten`) + inline style detectors |
| `Formula` | LaTeX-OCR (Pix2Tex) |
| `Figure` | Preserved as image crop (v1); subclassified by figure model (v2) |
| `Table` | Cell segmentation → TrOCR per cell (v2) |
| `Link` | Stroke skeleton analysis → arrowhead detection → directionality |
| `Callout` | Contour classification (circle, rectangle, cloud) + inner TrOCR |
| `Abandon` | Discarded |

The Ink Runtime also recovers inline style details from `Plain_Text` regions that are not captured during annotation: highlighting (HSV colour thresholding), underlines (horizontal line detection), and relative stroke weight (bold detection via stroke width analysis).

### Stage 3 — Document Reconstruction

The Ink Runtime assembles its output into a JSON AST. The AST represents the full page as a tree of typed nodes — `TextBlock`, `Formula`, `Figure`, `Table`, `Callout`, and `Link` — each carrying its bounding box coordinates and extracted content.

The AST is then passed to the Excalidraw renderer, which walks the tree and maps each node to an Excalidraw element, placing it at its original page coordinates. Text is rendered in Caveat — an open-source handwriting-style font — producing a document that looks like the original notes but is fully digital, searchable, and editable.

Output is serialised as an Excalidraw JSON file and opened in the PaperMd editor, with PDF and DOCX export targets planned.

### Application Stack

- **Frontend:** React + React Router v7 (framework mode) + shadcn/ui + Tailwind CSS
- **Editor:** Excalidraw (`@excalidraw/excalidraw`) embedded as a React component, A4-constrained canvas
- **Formula rendering:** KaTeX
- **Inference:** `onnxruntime-web` (browser WASM)
- **State:** Zustand
- **Runtime:** Bun

### Repository Structure

```
paper.md/
├── apps/
│   └── web/                        # React Router v7 frontend
├── packages/
│   ├── types/                      # Shared AST and detection types
│   ├── layout-model/               # YOLO inference wrapper
│   ├── figure-model/               # Figure subclassifier (v2)
│   ├── ink-runtime/                # Content extraction engine
│   └── excalidraw-renderer/        # AST → Excalidraw JSON
└── training/
    ├── notebooks/                  # Colab training notebooks
    ├── scripts/                    # Annotation and preprocessing scripts
    ├── models/                     # Model weight releases
    └── research/                   # Research findings and test data
```



## Roadmap

### v1 — Core Pipeline (Current)
- [x] Research phase: pre-trained model evaluation
- [x] Architecture decision: custom YOLOv11 Nano
- [x] Proof of concept: 61-image model, figure detection working
- [x] Active learning loop: model-assisted annotation in Label Studio
- [x] rclone backup sync for Label Studio data
- [ ] Annotation Batch 1: 50 images
- [ ] Annotation Batch 2: 100+ images (targeting diverse handwriting)
- [ ] First full training run with stable annotation schema
- [ ] TrOCR integration for Plain_Text crops
- [ ] LaTeX-OCR integration for Formula crops
- [ ] JSON AST schema
- [ ] Excalidraw-based document reconstruction with spatial awareness
- [ ] PDF export

### v2 — Extended Content
- [ ] Figure subclassification model (circuit, graph, flowchart, sketch)
- [ ] Table cell extraction
- [ ] Inline style recovery (underlines, highlights, bold detection)
- [ ] Callout shape classification
- [ ] DOCX and Typst export targets
- [ ] Circuit emulation and editing

### v3 — Generalisation
- [ ] Multi-language handwriting support
- [ ] Scan input support (flatbed scanner pipeline)
- [ ] Public dataset release



## Research Log

- **[Research Findings: Layout Analysis](./training/research/Research_Findings_Layout_Analysis.md)** — Why LayoutParser, OpenCV heuristics, and Tesseract segmentation all failed on handwritten notes, and the decision to train a custom model.
- **[Research Findings: YOLOv11 Nano Inference Analysis and Data Normalization Protocols](./training/research/Research_Findings_YOLOv11_Nano_Inference_Analysis_and_Data_Normalization_Protocols.md)** — Analysis of the first 24-image inference run, failure modes, confidence score distribution, and data normalisation requirements.



## Contributing

PaperMd's model quality is directly limited by dataset diversity. A model trained only on one person's handwriting will fail on everyone else's. We are actively collecting handwritten note images from anyone willing to contribute.

**What we need:**
- Photos of handwritten notes in any subject — math, science, engineering, humanities, anything
- Any pen, pencil, or writing instrument
- Any notebook type — ruled, blank, grid, dotted
- Neat or messy — messy notes are more valuable for robustness

**What we do with them:**
- Images are used exclusively to train and evaluate the layout detection model
- Nothing will be published, shared, or used outside this project
- Contributors are credited by name in this repository
- **Contributors receive a permanent free license to the PaperMd application**

[Submit your notes here →](https://forms.gle/W3XJPCD3nPThBQw4A)

To contribute code, open an issue or pull request. The model training code, dataset tooling, and annotation guidelines are all open under GPL-3.



## Licensing

PaperMd uses a split licensing model.

**Model, training code, and dataset tooling — GPL-3.0**

The machine learning components are fully open source. Anyone can use, study, modify, and redistribute them under the terms of GPL-3. Derivative works must also be GPL-3.

**Application — Business Source License 1.1 (BSL-1.1)**

The PaperMd application is source-available. The code is publicly readable on GitHub. Use is free for personal, non-commercial, and research purposes. Commercial use requires a paid license. Each release automatically converts to GPL-3 four years after its release date.

**Free licenses are granted to:**
NOTE: We havent setup the website yet :(

| Who | License | Verification |
|---|---|---|
| Note contributors | Permanent free commercial license | Automatic on submission |
| BIUST students and staff | 4-year free commercial license, renewable | Student email (`@studentmail.biust.ac.bw`) |

BIUST students and staff can claim their free license at `papermd.app/license` using their university email. No payment or card required.



## Development Setup

**Training (Google Colab):**
[Colab Training Script](https://colab.research.google.com/drive/1dAh-BjzS0RTTE1kF7Bv_9cwfVaie_BeL?usp=sharing)

**Application:**
```bash
bun install
bun dev
```

**Python annotation preprocessing (optional):**
```bash
pip install opencv-python pytesseract pillow
python training/scripts/label_images.py
```



## Hardware Target

PaperMd is designed to run on consumer hardware without a GPU. The reference development machine is an Intel Celeron N4020 with 8GB RAM running CachyOS Linux. If it runs well there, it runs well everywhere.
