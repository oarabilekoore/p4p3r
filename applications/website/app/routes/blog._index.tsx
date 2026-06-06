import { Link } from "react-router"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

const modules = import.meta.glob<{
  metadata: { title: string; date: string; description: string }
  default: React.ComponentType
}>("../blog/*.mdx", { eager: true })

export default function BlogIndex() {
  const posts = Object.entries(modules).map(([path, mod]) => {
    const slug = path.split("/").pop()?.replace(".mdx", "") || ""
    return { slug, ...mod.metadata }
  })

  return (
    <div className="max-w-5xl mx-auto px-6 py-24 md:py-32">
      <div className="text-center mb-16">
        <Badge variant="outline" className="mb-4 border-coffee-accent/40 text-coffee-accent">
          Research Blog
        </Badge>
        <h1 className="text-4xl md:text-5xl font-bold text-coffee-text font-serif">
          The PaperMd Journal
        </h1>
        <p className="text-coffee-muted mt-4 max-w-xl mx-auto text-sm leading-relaxed">
          Documenting our journey building a high-performance, local-first document layout analyzer.
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {posts.map((post) => (
          <Link key={post.slug} to={`/blog/${post.slug}`} className="group block">
            <Card className="bg-[#3D2512] border-coffee-muted/10 transition-all duration-300 group-hover:border-coffee-accent/30 h-full">
              <CardHeader className="pb-2">
                <span className="text-xs text-coffee-accent font-mono">{post.date}</span>
                <CardTitle className="text-xl font-bold font-serif text-coffee-text mt-2 group-hover:text-coffee-accent transition-colors duration-300">
                  {post.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-coffee-muted text-sm leading-relaxed">
                  {post.description}
                </p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}
