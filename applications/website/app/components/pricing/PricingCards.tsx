import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Check } from "lucide-react"

export default function PricingCards() {
  const tiers = [
    {
      title: "Personal", price: "Free", period: "forever",
      features: ["Local inference, all features", "Personal and educational use", "No account required"],
      cta: "Download", note: "Early Access", disabled: true,
    },
    {
      title: "BIUST", price: "Free", period: "for 4 years",
      features: ["Everything in Personal", "Renew with university email", "For students and staff at BIUST"],
      cta: "Claim with university email", note: "Coming Soon", disabled: true,
    },
    {
      title: "Commercial", price: "Paid", period: "price TBD",
      features: ["Everything in Personal", "Production and commercial use", "Pipeline API access (hosted inference)", "Priority support"],
      cta: "Contact", note: "mailto:oarabile42@gmail.com", disabled: false, href: "mailto:oarabile42@gmail.com",
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
      {tiers.map((t) => (
        <Card key={t.title} className="bg-coffee-surface border-coffee-muted/10 flex flex-col justify-between p-6">
          <div>
            <CardHeader className="p-0 pb-4">
              <span className="text-coffee-accent font-mono text-xs uppercase tracking-wider">{t.title}</span>
              <div className="flex items-baseline gap-2 mt-2">
                <span className="text-3xl font-bold font-serif text-coffee-text">{t.price}</span>
                <span className="text-xs text-coffee-muted">{t.period}</span>
              </div>
            </CardHeader>
            <CardContent className="p-0 py-4 border-t border-coffee-muted/10">
              <ul className="space-y-3">
                {t.features.map((f, i) => (
                  <li key={i} className="flex items-start gap-2.5 text-xs text-coffee-muted">
                    <Check className="size-4 text-coffee-accent shrink-0 mt-0.5" />
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </div>
          <CardFooter className="p-0 pt-6">
            {t.href ? (
              <a href={t.href} className="w-full">
                <Button className="w-full bg-coffee-accent text-coffee-bg hover:bg-coffee-accent/90 transition-colors duration-300 font-semibold h-11">
                  {t.cta}
                </Button>
              </a>
            ) : (
              <div className="w-full relative group">
                <Button disabled className="w-full bg-coffee-card text-coffee-muted border border-coffee-muted/20 cursor-not-allowed h-11">
                  {t.cta}
                </Button>
                <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 hidden group-hover:block bg-coffee-bg text-coffee-text text-xs rounded px-2.5 py-1.5 whitespace-nowrap shadow-lg border border-coffee-muted/20 z-10">
                  {t.note}
                </div>
              </div>
            )}
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}
