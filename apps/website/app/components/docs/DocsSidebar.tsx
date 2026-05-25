export default function DocsSidebar() {
  const links = [
    { href: "#intro", label: "What PaperMd Does" },
    { href: "#problems", label: "Existing Tools" },
    { href: "#pipeline", label: "Pipeline Stages" },
    { href: "#ast", label: "The AST" },
    { href: "#roadmap", label: "Roadmap" },
    { href: "#contribute", label: "Contributing" },
    { href: "#license", label: "Licensing" },
  ]

  return (
    <aside className="md:sticky md:top-24 h-fit space-y-2">
      <h3 className="font-serif font-bold text-coffee-text mb-4 text-lg">Documentation</h3>
      <div className="flex flex-wrap md:flex-col gap-2 md:gap-3 text-sm">
        {links.map((link) => (
          <a
            key={link.href}
            href={link.href}
            className="text-coffee-muted hover:text-coffee-accent transition-colors duration-300 px-3 py-1.5 md:px-0 md:py-0 bg-coffee-surface md:bg-transparent rounded-full md:rounded-none border border-coffee-muted/10 md:border-none whitespace-nowrap"
          >
            {link.label}
          </a>
        ))}
      </div>
    </aside>
  )
}
