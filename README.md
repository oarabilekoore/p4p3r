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

## Roadmap

- [x] Research phase: pre-trained model evaluation
- [x] Architecture decision: custom YOLOv11 Nano
- [x] Proof of concept: 61-image model, figure detection working
- [x] Active learning loop: model-assisted annotation in Label Studio
- [ ] TrOCR integration for Plain_Text crops
- [x] LaTeX-OCR integration for Formula crops
- [x] JSON AST schema
- [ ] Excalidraw-based document reconstruction with spatial awareness
- [ ] PDF export
- [ ] Figure subclassification model (circuit, graph, flowchart, sketch)
- [ ] Table cell extraction
- [ ] Inline style recovery (underlines, highlights, bold detection)
- [x] Callout shape classification
- [ ] DOCX and Typst export targets
- [ ] Circuit emulation and editing
- [ ] Multi-language handwriting support

### Important Dates

0. June 10th Application source License review.
0. June 14th 300 Image PaperMd Scanner Model Release. 
0. June 21st MVP

## Research Log

- **[Research Findings: Layout Analysis](./training/research/Research_Findings_Layout_Analysis.md)** — Why LayoutParser, OpenCV heuristics, and Tesseract segmentation all failed on handwritten notes, and the decision to train a custom model.
- **[Research Findings: YOLOv11 Nano Inference Analysis and Data Normalization Protocols](./training/research/Research_Findings_YOLOv11_Nano_Inference_Analysis_and_Data_Normalization_Protocols.md)** — Analysis of the first 24-image inference run, failure modes, confidence score distribution, and data normalisation requirements.

## Contributing

PaperMd's model quality is directly limited by dataset diversity. A model trained only on one person's handwriting will fail on everyone else's. We are actively collecting handwritten note images from anyone willing to contribute.

**What is needed:**
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

To be reviewed.
