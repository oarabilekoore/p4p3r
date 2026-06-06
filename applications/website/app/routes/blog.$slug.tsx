import { useParams, Link } from "react-router"
import { ArrowLeft } from "lucide-react"

const modules = import.meta.glob<{
  metadata: { title: string; date: string; description: string }
  default: React.ComponentType
}>("../blog/*.mdx", { eager: true })

export default function BlogPost() {
  const { slug } = useParams()
  const path = Object.keys(modules).find((p) => p.endsWith(`${slug}.mdx`))
  const matched = path ? modules[path] : null

  if (!matched) {
    return (
      <div className="max-w-3xl mx-auto px-6 py-32 text-center">
        <h1 className="text-2xl font-bold font-serif text-coffee-text mb-4">Post Not Found</h1>
        <Link to="/blog" className="text-coffee-accent hover:underline flex items-center justify-center gap-2">
          <ArrowLeft className="size-4" /> Back to blog
        </Link>
      </div>
    )
  }

  const PostComponent = matched.default
  const { title, date } = matched.metadata

  return (
    <article className="max-w-3xl mx-auto px-6 py-24 md:py-32">
      <Link to="/blog" className="text-coffee-accent hover:underline inline-flex items-center gap-2 mb-8 text-sm font-medium">
        <ArrowLeft className="size-4" /> Back to journal
      </Link>
      <header className="mb-12">
        <span className="text-xs text-coffee-accent font-mono">{date}</span>
        <h1 className="text-4xl md:text-5xl font-bold font-serif text-coffee-text mt-3 tracking-tight">
          {title}
        </h1>
      </header>
      <div className="border-t border-coffee-muted/10 pt-8">
        <PostComponent />
      </div>
    </article>
  )
}
