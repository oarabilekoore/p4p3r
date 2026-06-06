import PricingCards from "../components/pricing/PricingCards"
import { Badge } from "@/components/ui/badge"

export default function Pricing() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-24 md:py-32 space-y-16">
      <div className="text-center">
        <Badge variant="outline" className="mb-4 border-coffee-accent/40 text-coffee-accent">
          Simple Pricing
        </Badge>
        <h1 className="text-4xl md:text-5xl font-bold text-coffee-text font-serif">
          Choose Your Tier
        </h1>
        <p className="text-coffee-muted mt-4 max-w-xl mx-auto text-sm leading-relaxed">
          PaperMd is built local-first for absolute privacy. Select the license model that fits your needs.
        </p>
      </div>
      <PricingCards />
      <div className="max-w-2xl mx-auto border-t border-coffee-muted/10 pt-8 text-center space-y-4">
        <p className="text-xs text-coffee-muted leading-relaxed">
          Dataset contributors receive a permanent free commercial license automatically on submission.
        </p>
        <p className="text-xs text-coffee-accent font-mono">
          The underlying ML model and training code are GPL-3 and always free.
        </p>
      </div>
    </div>
  )
}
