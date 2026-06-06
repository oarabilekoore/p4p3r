
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
