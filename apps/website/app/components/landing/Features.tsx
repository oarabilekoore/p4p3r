import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ShieldAlert, PenTool, LayoutTemplate, Cpu, Code2 } from "lucide-react"

export default function Features() {
  const items = [
    {
      title: "Fully offline",
      desc: "No cloud, no API, no tracking. Your notes and files never leave your machine.",
      icon: ShieldAlert,
    },
    {
      title: "Handwriting-native",
      desc: "The model is trained specifically on handwritten notes, not typed or scanned documents.",
      icon: PenTool,
    },
    {
      title: "Layout preserved",
      desc: "Spatial positions, equations, diagrams, and paragraphs all land exactly where you wrote them.",
      icon: LayoutTemplate,
    },
    {
      title: "Low-end hardware",
      desc: "Highly optimized on-device inference runs smoothly on an Intel Celeron. No GPU required.",
      icon: Cpu,
    }
  ]

  return (
    <section className="px-6 py-20 max-w-5xl mx-auto">
      <h2 className="text-3xl font-bold text-coffee-text text-center mb-4 font-serif">
        Features Built for Privacy & Speed
      </h2>
      <p className="text-coffee-muted text-center max-w-xl mx-auto mb-12 text-sm">
        Everything runs locally on-device. No API keys, no monthly fees, and no internet required.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {items.map((item, idx) => {
          const Icon = item.icon
          return (
            <Card key={idx} className="bg-coffee-surface border-coffee-muted/10">
              <CardHeader className="pb-2">
                <Icon className="size-5 text-coffee-accent mb-2" />
                <CardTitle className="text-base text-coffee-text font-serif">
                  {item.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-coffee-muted text-xs leading-relaxed">
                  {item.desc}
                </p>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </section>
  )
}
