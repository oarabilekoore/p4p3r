# p4p3r

![Status](https://img.shields.io/badge/Status-Active_Development-green)
![Stage](https://img.shields.io/badge/Synthetic_Data_Generation-blue)
![Architecture](https://img.shields.io/badge/Model-YOLOv11_Nano-orange)

p4p3r is a local-first, offline application that converts photographs of handwritten notes into structured digital documents. A photo of a notebook page goes in — a clean, formatted, editable document comes out.

The core thesis is that layout understanding and handwriting recognition are two separate problems that must be solved independently before they can be composed. p4p3r solves them in sequence.
                    
## The Problem

I want to merge my digital notes and my handwritten notes into one system - an attempt to
end the digital vs handwritten notes debate. 



As of now the best method to do this is to take typed notes in markdown or magic markdown aka _Notion_. Then take images of your notes and ask a slave convolutional neural network selotaped onto an llm hidden behind a text box to output markdown.  


The problem is I want the document layout to be preserved, not just the text.


## Roadmap

- [x] Research phase: pre-trained model evaluation
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
- [ ] Multi-language handwriting support

## Research Log

- **[Research Findings: Layout Analysis](./training/research/Research_Findings_Layout_Analysis.md)** — Why LayoutParser, OpenCV heuristics, and Tesseract segmentation all failed on handwritten notes, and the decision to train a custom model.
- **[Research Findings: YOLOv11 Nano Inference Analysis and Data Normalization Protocols](./training/research/Research_Findings_YOLOv11_Nano_Inference_Analysis_and_Data_Normalization_Protocols.md)** — Analysis of the first 24-image inference run, failure modes, confidence score distribution, and data normalisation requirements.

## Licensing

MIT
