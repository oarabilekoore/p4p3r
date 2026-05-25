import { IMAGES_COUNT } from "./CurrentRelease"

export default function VersionHistory() {
  const history = [
    {
      version: "v0.1.0-alpha",
      date: "May 2026",
      images: IMAGES_COUNT,
      map50: "0.58",
      notes: "First release targeting layout detection and basic class classification.",
    },
  ]

  return (
    <div className="overflow-x-auto border border-coffee-muted/10 rounded-lg bg-coffee-surface">
      <table className="w-full text-left border-collapse text-sm">
        <thead>
          <tr className="border-b border-coffee-muted/10 bg-coffee-card/50 text-coffee-text font-serif">
            <th className="p-4 font-semibold">Version</th>
            <th className="p-4 font-semibold">Date</th>
            <th className="p-4 font-semibold">Images</th>
            <th className="p-4 font-semibold">mAP50</th>
            <th className="p-4 font-semibold font-sans">Notes</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-coffee-muted/10 text-coffee-muted">
          {history.map((row) => (
            <tr key={row.version} className="hover:bg-coffee-card/25 transition-colors duration-300">
              <td className="p-4 font-mono font-semibold text-coffee-text">{row.version}</td>
              <td className="p-4">{row.date}</td>
              <td className="p-4 font-mono">{row.images}</td>
              <td className="p-4 font-mono">{row.map50}</td>
              <td className="p-4 max-w-xs truncate md:max-w-md">{row.notes}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
