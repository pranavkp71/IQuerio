type Props = {
  title?: string
  code: string
}

export default function CodeBlock({ title, code }: Props) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-4 glow">
      {title && <div className="mb-2 text-xs uppercase tracking-wide text-white/60">{title}</div>}
      <pre className="overflow-auto text-sm leading-relaxed">
        <code>{code}</code>
      </pre>
    </div>
  )
}


