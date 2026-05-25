import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Download } from "lucide-react"

export const IMAGES_COUNT = 38

export default function CurrentRelease() {
  const classes = ["Abandon", "Plain_Text", "Formula", "Figure", "Table", "Link", "Callout"]

  return (
    <Card className="bg-coffee-surface border-coffee-muted/10 p-6">
      <CardHeader className="p-0 pb-4 flex flex-row items-center justify-between">
        <div>
          <CardTitle className="text-2xl font-serif text-coffee-text">papermd-layout</CardTitle>
          <span className="text-xs text-coffee-muted font-mono">Architecture: YOLOv11 Nano</span>
        </div>
        <Badge variant="outline" className="border-coffee-accent/40 text-coffee-accent bg-coffee-accent/5">
          Early Access
        </Badge>
      </CardHeader>
      <CardContent className="p-0 space-y-6">
        <div>
          <span className="text-xs text-coffee-muted block mb-2 font-semibold uppercase tracking-wider">Detected Classes</span>
          <div className="flex flex-wrap gap-2">
            {classes.map((cls) => (
              <Badge key={cls} variant="secondary" className="bg-coffee-card text-coffee-text border-none">
                {cls}
              </Badge>
            ))}
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4 text-sm border-t border-b border-coffee-muted/10 py-4">
          <div>
            <span className="text-coffee-muted text-xs block">Training Images</span>
            <span className="text-coffee-text font-mono font-semibold">{IMAGES_COUNT}</span>
          </div>
          <div>
            <span className="text-coffee-muted text-xs block">License</span>
            <span className="text-coffee-text font-mono font-semibold">GPL-3.0</span>
          </div>
        </div>
        <div className="flex flex-col sm:flex-row gap-4 pt-2">
          {["weights (.pt)", "weights (.onnx)"].map((label, idx) => (
            <div key={idx} className="relative group flex-1">
              <Button disabled className="w-full bg-coffee-card text-coffee-muted border border-coffee-muted/20 cursor-not-allowed h-11 flex items-center justify-center gap-2">
                <Download className="size-4" />
                Download {label}
              </Button>
              <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 hidden group-hover:block bg-coffee-bg text-coffee-text text-xs rounded px-2.5 py-1.5 whitespace-nowrap shadow-lg border border-coffee-muted/20 z-10">
                Coming with v0.1.0 release
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
