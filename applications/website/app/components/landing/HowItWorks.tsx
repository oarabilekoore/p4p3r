import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Camera, Cpu, FileSpreadsheet } from "lucide-react"

export default function HowItWorks() {
  return (
    <section className="px-6 py-16 bg-coffee-surface border-y border-coffee-muted/10">
      <div className="max-w-5xl mx-auto">
        <h2 className="text-3xl font-bold text-coffee-text text-center mb-12 font-serif">
          How It Works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <Card className="bg-coffee-card border-coffee-muted/10 relative overflow-hidden">
            <CardHeader className="pb-2">
              <div className="w-12 h-12 rounded-lg bg-coffee-accent/10 flex items-center justify-center text-coffee-accent mb-4">
                <Camera className="size-6" />
              </div>
              <CardTitle className="text-lg text-coffee-text">1. Photograph</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-coffee-muted text-sm leading-relaxed">
                Take a photo of any page of handwritten notes with your camera or phone.
              </p>
            </CardContent>
          </Card>
          <Card className="bg-coffee-card border-coffee-muted/10 relative overflow-hidden">
            <CardHeader className="pb-2">
              <div className="w-12 h-12 rounded-lg bg-coffee-accent/10 flex items-center justify-center text-coffee-accent mb-4">
                <Cpu className="size-6" />
              </div>
              <CardTitle className="text-lg text-coffee-text">2. Analyse</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-coffee-muted text-sm leading-relaxed">
                PaperMd detects every element on the page and classifies it: paragraphs, equations, tables, and diagrams.
              </p>
            </CardContent>
          </Card>
          <Card className="bg-coffee-card border-coffee-muted/10 relative overflow-hidden">
            <CardHeader className="pb-2">
              <div className="w-12 h-12 rounded-lg bg-coffee-accent/10 flex items-center justify-center text-coffee-accent mb-4">
                <FileSpreadsheet className="size-6" />
              </div>
              <CardTitle className="text-lg text-coffee-text">3. Export</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-coffee-muted text-sm leading-relaxed">
                Get back a clean digital document rendered on an Excalidraw canvas, with your layout fully preserved.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}
