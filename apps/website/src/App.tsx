import { Routes, Route } from "react-router"
import Nav from "../app/components/landing/Nav"
import Index from "../app/routes/_index"
import Models from "../app/routes/models"
import Docs from "../app/routes/docs"
import Pricing from "../app/routes/pricing"
import BlogIndex from "../app/routes/blog._index"
import BlogPost from "../app/routes/blog.$slug"

export default function App() {
  return (
    <div className="bg-coffee-bg min-h-screen text-coffee-text selection:bg-coffee-accent/20 selection:text-coffee-text font-sans antialiased">
      <Nav />
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/models" element={<Models />} />
        <Route path="/docs" element={<Docs />} />
        <Route path="/pricing" element={<Pricing />} />
        <Route path="/blog" element={<BlogIndex />} />
        <Route path="/blog/:slug" element={<BlogPost />} />
      </Routes>
    </div>
  )
}
