export default function DocsContributing() {
  return (
    <div className="space-y-12 text-coffee-muted text-sm leading-relaxed">
      <section id="contribute" className="scroll-mt-24 space-y-4">
        <h2 className="text-2xl font-bold font-serif text-coffee-text">Contributing Notes</h2>
        <p>
          PaperMd's accuracy depends on dataset diversity. We collect photographs of handwritten notes in any subject, written on any paper type. Messy notes are highly valuable for refining model generalisation.
        </p>
        <p>
          Images are used strictly for training and dataset building. Contributors receive a permanent, free commercial license to PaperMd. Submit notes using the{" "}
          <a
            href="https://docs.google.com/forms/d/e/1FAIpQLSdNDJS9-WdjWSeT46h5IAuNevDcGbEXjD-5-b23OaZlJLpwwQ/viewform?usp=sharing&ouid=102676538571789075260"
            target="_blank"
            rel="noopener noreferrer"
            className="text-coffee-accent hover:underline font-semibold"
          >
            Google Form Submission Link
          </a>
          .
        </p>
      </section>

      <section id="license" className="scroll-mt-24 space-y-4">
        <h2 className="text-2xl font-bold font-serif text-coffee-text">Licensing & Tiers</h2>
        <p>
          PaperMd uses a split licensing model. The core YOLO model, training scripts, and preprocessing code are open-source under <strong>GPL-3.0</strong>.
        </p>
        <p>
          The desktop application is source-available under <strong>BSL-1.1</strong>. It is free for personal, educational, and research use. Commercial use requires a paid license. The application code converts to GPL-3.0 four years after each release.
        </p>
        <p>
          Free commercial licenses are automatically granted to note contributors and BIUST students and staff (claimed via university email validation).
        </p>
      </section>
    </div>
  )
}
