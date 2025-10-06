"use client"

import { useState } from 'react'

export default function FAQ({ items }: { items: { q: string; a: string }[] }) {
  return (
    <div className="space-y-3">
      {items.map((it, i) => (
        <Item key={i} q={it.q} a={it.a} />
      ))}
    </div>
  )
}

function Item({ q, a }: { q: string; a: string }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="rounded-xl border border-white/10 bg-white/5">
      <button onClick={() => setOpen(v=>!v)} className="w-full px-4 py-3 flex items-center justify-between text-left">
        <span className="font-medium">{q}</span>
        <span className="text-white/60">{open ? '−' : '+'}</span>
      </button>
      {open && (
        <div className="px-4 pb-4 text-white/70 text-sm">{a}</div>
      )}
    </div>
  )
}


