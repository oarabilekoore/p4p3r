import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Heart, Scale } from "lucide-react"

export default function OpenSource() {
  return (
    <section className="px-6 py-20 bg-coffee-surface border-y border-coffee-muted/10">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-12">
          <Badge variant="outline" className="mb-4 border-coffee-accent/40 text-coffee-accent">
            Source Available
          </Badge>
          <h2 className="text-3xl font-bold text-coffee-text font-serif">
            Open Licensing & Community
          </h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <Card className="bg-coffee-card border-coffee-muted/10">
            <CardContent className="p-6 flex gap-4 items-start">
              <Scale className="size-6 text-coffee-accent shrink-0 mt-1" />
              <div>
                <h3 className="text-lg font-semibold text-coffee-text mb-2 font-serif">
                  Dual Licensing Model
                </h3>
                <p className="text-coffee-muted text-sm leading-relaxed mb-3">
                  The ML model, training code, and dataset tooling are fully open under <strong>GPL-3</strong>.
                </p>
                <p className="text-coffee-muted text-sm leading-relaxed">
                  The application is source-available under <strong>BSL-1.1</strong>, automatically converting to GPL-3 four years after each release.
                </p>
              </div>
            </CardContent>
          </Card>
          <Card className="bg-coffee-card border-coffee-muted/10">
            <CardContent className="p-6 flex gap-4 items-start">
              <Heart className="size-6 text-coffee-accent shrink-0 mt-1" />
              <div>
                <h3 className="text-lg font-semibold text-coffee-text mb-2 font-serif">
                  Contributor License Program
                </h3>
                <p className="text-coffee-muted text-sm leading-relaxed mb-3">
                  We need diverse handwritten notes to train and refine our custom model.
                </p>
                <p className="text-coffee-muted text-sm leading-relaxed mb-3">
                  Contributors who submit anonymized handwritten notes for our training dataset receive a permanent, free commercial application license.
                </p>
                <a href="https://docs.google.com/forms/d/e/1FAIpQLSdNDJS9-WdjWSeT46h5IAuNevDcGbEXjD-5-b23OaZlJLpwwQ/viewform?usp=sharing&ouid=102676538571789075260" target="_blank" rel="noopener noreferrer" className="text-coffee-accent hover:underline inline-flex items-center gap-1 text-xs font-semibold">
                  Submit Handwritten Notes Form →
                </a>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}
