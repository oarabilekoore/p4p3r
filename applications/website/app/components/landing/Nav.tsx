import { useState, useEffect } from "react"
import { Link, useLocation } from "react-router"
import { Menu, X, FileText } from "lucide-react"
import { Sheet } from "@/components/ui/sheet"

export default function Nav() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)
  const location = useLocation()

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 60)
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  const items = [
    { label: "Models", path: "/models" },
    { label: "Docs", path: "/docs" },
    { label: "Blog", path: "/blog" },
    { label: "Pricing", path: "/pricing" },
  ]

  const activeClass = (path: string) =>
    location.pathname === path ? "text-coffee-accent" : "text-coffee-muted hover:text-coffee-text"

  return (
    <nav className={`fixed top-0 left-0 right-0 z-40 transition-all duration-300 ${scrolled ? "bg-coffee-bg border-b border-coffee-card" : "bg-transparent"}`}>
      <div className="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-serif text-lg font-bold text-coffee-text">
          <FileText className="size-5 text-coffee-accent" />
          <span>PaperMd</span>
        </Link>
        <div className="hidden md:flex items-center gap-8 text-sm font-medium">
          {items.map((item) => (
            <Link key={item.path} to={item.path} className={`transition-colors ${activeClass(item.path)}`}>
              {item.label}
            </Link>
          ))}
        </div>
        <div className="flex items-center gap-4">
          <a href="https://github.com/oarabilekoore/Paper.Md" target="_blank" rel="noopener noreferrer" className="text-coffee-muted hover:text-coffee-text">
            {/*<Github className="size-5" />*/}
          </a>
          <button className="md:hidden text-coffee-text" onClick={() => setOpen(true)}>
            <Menu className="size-6" />
          </button>
        </div>
      </div>
      <Sheet open={open} onOpenChange={setOpen}>
        <div className="flex justify-between items-center mb-8">
          <span className="font-serif text-lg font-bold text-coffee-text">Menu</span>
          <button onClick={() => setOpen(false)} className="text-coffee-text">
            <X className="size-6" />
          </button>
        </div>
        <div className="flex flex-col gap-6 text-lg font-medium">
          {items.map((item) => (
            <Link key={item.path} to={item.path} onClick={() => setOpen(false)} className={`transition-colors ${activeClass(item.path)}`}>
              {item.label}
            </Link>
          ))}
        </div>
      </Sheet>
    </nav>
  )
}
