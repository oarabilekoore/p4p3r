import DocsSidebar from "../components/docs/DocsSidebar"
import DocsPipeline from "../components/docs/DocsPipeline"
import DocsAst from "../components/docs/DocsAst"
import DocsRoadmap from "../components/docs/DocsRoadmap"
import DocsContributing from "../components/docs/DocsContributing"

export default function Docs() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-24 md:py-32">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
        <div className="md:col-span-1">
          <DocsSidebar />
        </div>
        <div className="md:col-span-3 space-y-16">
          <DocsPipeline />
          <DocsAst />
          <DocsRoadmap />
          <DocsContributing />
        </div>
      </div>
    </div>
  )
}
