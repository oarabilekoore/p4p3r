import { FileText } from "lucide-react"

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="px-6 py-12 max-w-5xl mx-auto border-t border-coffee-muted/10 text-center sm:text-left flex flex-col sm:flex-row justify-between items-center gap-6">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-coffee-accent/15 flex items-center justify-center text-coffee-accent">
          <FileText className="size-4" />
        </div>
        <div>
          <span className="font-serif text-sm font-semibold text-coffee-text block">
            PaperMd
          </span>
          <span className="text-coffee-muted text-xs">
            Quiet local-first notes.
          </span>
        </div>
      </div>
      <div className="flex flex-wrap justify-center gap-6 text-xs text-coffee-muted">
        <a href="https://github.com/oarabilekoore/Paper.Md" target="_blank" rel="noopener noreferrer" className="hover:text-coffee-accent transition-colors duration-300">GitHub</a>
        <a href="#dataset" className="hover:text-coffee-accent transition-colors duration-300">Dataset</a>
        <a href="#license" className="hover:text-coffee-accent transition-colors duration-300">License (GPL-3)</a>
      </div>
      <div className="text-xs text-coffee-muted font-mono">
        © {currentYear} PaperMd.
      </div>
    </footer>
  )
}
