import * as React from "react"
import { cn } from "@/lib/utils"

export function Separator({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      className={cn("h-[1px] w-full bg-coffee-muted/20", className)}
      {...props}
    />
  )
}
