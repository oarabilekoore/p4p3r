import CurrentRelease from "../components/models/CurrentRelease"
import VersionHistory from "../components/models/VersionHistory"
import { Badge } from "@/components/ui/badge"

export default function Models() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-24 md:py-32 space-y-16">
      <div className="text-center">
        <Badge variant="outline" className="mb-4 border-coffee-accent/40 text-coffee-accent">
          Layout Models
        </Badge>
        <h1 className="text-4xl md:text-5xl font-bold text-coffee-text font-serif">
          Model Repository
        </h1>
        <p className="text-coffee-muted mt-4 max-w-xl mx-auto text-sm leading-relaxed">
          Download pre-trained weights for the custom YOLOv11 layout detector and view model training history.
        </p>
      </div>
      <div className="space-y-8">
        <h2 className="text-2xl font-bold font-serif text-coffee-text border-b border-coffee-muted/10 pb-2">
          Current Release
        </h2>
        <CurrentRelease />
      </div>
      <div className="space-y-8">
        <h2 className="text-2xl font-bold font-serif text-coffee-text border-b border-coffee-muted/10 pb-2">
          Version History
        </h2>
        <VersionHistory />
      </div>
    </div>
  )
}
