export default function DocsAst() {
  const jsonExample = `{
  "type": "Page",
  "children": [
    {
      "type": "TextBlock",
      "bbox": [10, 20, 200, 80],
      "text": "Introduction to Quantum Computing"
    },
    {
      "type": "Formula",
      "bbox": [10, 100, 150, 140],
      "latex": "\\\\psi = \\\\alpha|0\\\\rangle + \\\\beta|1\\\\rangle"
    }
  ]
}`

  return (
    <div className="space-y-8 text-coffee-muted text-sm leading-relaxed scroll-mt-24" id="ast">
      <div className="space-y-4">
        <h2 className="text-2xl font-bold font-serif text-coffee-text">Stage 3: Reconstruction & The AST</h2>
        <p>
          The output from the Ink Runtime is organized into a JSON Abstract Syntax Tree (AST) representing the global page coordinates. Nodes include <code>TextBlock</code>, <code>Formula</code>, <code>Figure</code>, <code>Table</code>, <code>Callout</code>, and <code>Link</code>.
        </p>
        <p>
          The Excalidraw renderer walks this AST and positions elements on an infinite canvas. Text is loaded in the handwriting-style <strong>Caveat</strong> font, making it fully searchable and editable while looking exactly like your original notes.
        </p>
      </div>

      <div className="space-y-2">
        <span className="text-xs font-semibold text-coffee-text uppercase tracking-wider block">AST JSON Schema Example</span>
        <pre className="bg-coffee-surface text-coffee-text p-4 rounded-lg overflow-x-auto font-mono text-xs border border-coffee-muted/20">
          <code>{jsonExample}</code>
        </pre>
      </div>
    </div>
  )
}
