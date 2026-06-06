export default function mdxSimplePlugin() {
  return {
    name: "vite-plugin-mdx-simple",
    transform(code: string, id: string) {
      if (!id.endsWith(".mdx")) return null
      const metadata: Record<string, string> = {}
      const fmMatch = code.match(/^---\n([\s\S]+?)\n---/)
      let content = code
      if (fmMatch) {
        content = code.slice(fmMatch[0].length)
        fmMatch[1].split("\n").forEach((line) => {
          const part = line.split(":")
          if (part.length >= 2) {
            metadata[part[0].trim()] = part.slice(1).join(":").trim().replace(/^['"]|['"]$/g, "")
          }
        })
      }
      let html = ""
      let inList = false
      let inCode = false
      let codeBlock: string[] = []
      content.split("\n").forEach((line) => {
        const trimmed = line.trim()
        if (trimmed.startsWith("```")) {
          if (inCode) {
            inCode = false
            const codeText = codeBlock.join("\n").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
            html += `<pre class="bg-coffee-surface text-coffee-text p-4 rounded-lg overflow-x-auto my-4 font-mono text-sm border border-coffee-muted/20"><code>${codeText}</code></pre>`
            codeBlock = []
          } else {
            inCode = true
          }
          return
        }
        if (inCode) {
          codeBlock.push(line)
          return
        }
        if (trimmed.startsWith("- ") || trimmed.startsWith("* ")) {
          if (!inList) {
            html += `<ul class="list-disc pl-6 my-4 space-y-2 text-coffee-muted">`
            inList = true
          }
          const inner = trimmed.slice(2).replace(/\*\*([\s\S]+?)\*\*/g, "<strong>$1</strong>")
          html += `<li>${inner}</li>`
        } else {
          if (inList) {
            html += "</ul>"
            inList = false
          }
          if (trimmed === "") {
            html += `<div class="h-4"></div>`
          } else if (trimmed.startsWith("# ")) {
            html += `<h1 class="text-3xl font-bold font-serif mt-8 mb-4 text-coffee-text">${trimmed.slice(2)}</h1>`
          } else if (trimmed.startsWith("## ")) {
            html += `<h2 class="text-2xl font-bold font-serif mt-6 mb-3 text-coffee-text">${trimmed.slice(3)}</h2>`
          } else {
            const inner = trimmed.replace(/\*\*([\s\S]+?)\*\*/g, "<strong>$1</strong>")
            html += `<p class="my-4 text-coffee-muted leading-relaxed">${inner}</p>`
          }
        }
      })
      if (inList) html += "</ul>"
      const result = `
        import React from "react"
        export const metadata = ${JSON.stringify(metadata)}
        export default function Post() {
          return React.createElement("div", {
            className: "prose max-w-none text-coffee-text",
            dangerouslySetInnerHTML: { __html: ${JSON.stringify(html)} }
          })
        }
      `
      return { code: result, map: null }
    },
  }
}
