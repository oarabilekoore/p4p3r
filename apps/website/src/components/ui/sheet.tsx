import * as React from "react"

export function Sheet({ open, onOpenChange, children }: { open: boolean, onOpenChange: (open: boolean) => void, children: React.ReactNode }) {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-50 flex">
      <div className="fixed inset-0 bg-black/60 backdrop-blur-sm" onClick={() => onOpenChange(false)} />
      <div className="relative ml-auto flex h-full w-3/4 max-w-sm flex-col bg-coffee-bg p-6 text-coffee-text shadow-xl border-l border-coffee-muted/20">
        {children}
      </div>
    </div>
  )
}
