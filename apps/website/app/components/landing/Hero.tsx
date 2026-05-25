import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Download } from "lucide-react"

export default function Hero() {
  return (
    <section className="relative px-6 py-20 md:py-32 flex flex-col items-center text-center max-w-4xl mx-auto">
      <Badge variant="outline" className="mb-6 border-coffee-accent/40 text-coffee-accent bg-coffee-accent/5 px-4 py-1.5 text-sm tracking-wider uppercase">
        Early Access
      </Badge>
      <h1 className="text-5xl md:text-7xl font-bold text-coffee-text tracking-tight mb-6 font-serif">
        Your notes. <span className="text-coffee-accent">Finally digital.</span>
      </h1>
      <p className="text-lg md:text-xl text-coffee-muted max-w-2xl leading-relaxed mb-6">
        PaperMd turns a photo of your handwritten notes into a clean, editable document. Equations, diagrams, and all — laid out exactly as you wrote them. Runs entirely on your device.
      </p>
      <div className="w-full flex justify-center">
        <Button className="w-full md:w-auto bg-coffee-accent text-coffee-bg cursor-pointer hover:bg-coffee-accent/90 transition-colors duration-300 font-semibold px-10 py-6 h-auto text-base rounded-md flex items-center justify-center gap-2 border-none">
          <Download className="size-5" />
          Download for Linux (Early Access)
        </Button>
      </div>
      <div className="mt-6 text-xs text-coffee-muted/75 font-mono">
        v0.1.0 • AppImage & Flatpak
      </div>
    </section>
  )
}
