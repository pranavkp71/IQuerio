"use client"

import { useEffect, useState } from 'react'
import { Github, Lock, Play, Rocket, Database, Sparkles, FileCode } from 'lucide-react'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'

const sampleQuery = `SELECT * FROM customers WHERE age > 30`
const sampleOutput = `-- Optimized with index hint\nSELECT name, region\nFROM customers\nWHERE age > 30\nORDER BY last_purchase DESC\n-- EXPLAIN: 2.4x faster using index idx_age`

function Section({ children, className }: { children: React.ReactNode, className?: string }) {
  return <section className={`mx-auto w-full max-w-6xl px-4 sm:px-6 lg:px-8 ${className || ''}`}>{children}</section>
}

const DEMO_LIMIT = 3
const STORAGE_KEY = 'iquerio_demo_runs_left'

export default function HomePage() {
  const [query, setQuery] = useState(sampleQuery)
  const [output, setOutput] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [runsLeft, setRunsLeft] = useState(DEMO_LIMIT)

  useEffect(() => {
    const saved = Number(localStorage.getItem(STORAGE_KEY))
    if (!isNaN(saved) && saved >= 0 && saved <= DEMO_LIMIT) {
      setRunsLeft(saved)
    } else {
      localStorage.setItem(STORAGE_KEY, String(DEMO_LIMIT))
    }
  }, [])

  async function runOptimization() {
    if (runsLeft <= 0) return
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/optimize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })
      const data = await res.json()
      const out = `-- AI-Optimized Query\n${data.optimized_query || '/* No change */'}\n-- Explain: ${typeof data.explain_plan === 'string' ? data.explain_plan : 'see server'}`
      setOutput(out)
      const next = Math.max(runsLeft - 1, 0)
      setRunsLeft(next)
      localStorage.setItem(STORAGE_KEY, String(next))
    } catch (e) {
      setOutput('Failed to optimize. Please ensure backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const isLocked = runsLeft === 0

  return (
    <main className="flex min-h-screen flex-col">
      {/* Hero */}
      <div className="border-b bg-white">
        <Section className="py-16 sm:py-24">
          <div className="grid gap-8 lg:grid-cols-2 lg:items-center">
            <div className="space-y-6">
              <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">Optimize SQL & Search Data with AI — Instantly.</h1>
              <p className="text-lg text-slate-600 max-w-prose">Write smarter queries, debug databases faster, and explore vector search — all in one playground.</p>
              <div className="flex flex-wrap items-center gap-3">
                <a href="#demo" className="inline-flex items-center rounded-md bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-700 transition">Start Free Demo</a>
                <a href="https://github.com/pranavkp71/IQuerio" target="_blank" className="inline-flex items-center gap-2 rounded-md border px-4 py-2 text-slate-700 hover:bg-slate-50 transition">
                  <Github className="h-4 w-4" /> View on GitHub
                </a>
              </div>
            </div>
            <div className="rounded-xl border bg-gradient-to-b from-slate-50 to-white p-6">
              <div id="features" className="grid grid-cols-2 gap-4">
                <Feature icon={<Sparkles className="h-5 w-5" />} title="AI Query Optimizer" desc="Paste SQL—get optimized, indexed, and explained output." />
                <Feature icon={<Database className="h-5 w-5" />} title="Vector Playground" desc="Upload or enter data—perform similarity search intuitively." />
                <Feature icon={<FileCode className="h-5 w-5" />} title="Natural Language → SQL" desc="Ask in plain English and get executable SQL." />
                <Feature icon={<Rocket className="h-5 w-5" />} title="Schema Debugging" desc="Auto-detects schema issues and suggests fixes." />
              </div>
            </div>
          </div>
        </Section>
      </div>

      {/* Demo Section */}
      <div id="demo" className="bg-white">
        <Section className="py-16">
          <div className="mb-8">
            <h2 className="text-2xl font-semibold">Try IQuerio in Action</h2>
            <p className="text-slate-600">Paste a query and see how our AI optimizes it instantly.</p>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            {/* Query Editor */}
            <div className="space-y-2">
              <label className="text-sm text-slate-500">Try this example or type your own (preview mode)</label>
              <textarea
                className="font-mono w-full min-h-[160px] rounded-md border p-4 outline-none focus:ring-2 focus:ring-emerald-500"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <div className="flex items-center gap-3">
                <button disabled={loading || isLocked} onClick={runOptimization} className="inline-flex items-center gap-2 rounded-md bg-black px-4 py-2 text-white hover:bg-slate-800 disabled:opacity-60 transition">
                  <Play className="h-4 w-4" /> {loading ? 'Optimizing…' : 'Run Optimization'}
                </button>
                <span className="text-sm text-slate-500">{runsLeft} of {DEMO_LIMIT} runs left</span>
              </div>
            </div>

            {/* Output Area */}
            <div className="relative">
              <pre className={`font-mono whitespace-pre-wrap rounded-md border p-4 min-h-[200px] bg-slate-50 ${isLocked ? 'blur-[2px]' : ''}`}>
                {(output || sampleOutput)}
              </pre>
              {isLocked && (
                <div className="absolute inset-0 flex items-end justify-between rounded-md bg-white/70 backdrop-blur-sm p-4">
                  <div className="flex items-center gap-2 text-slate-700">
                    <Lock className="h-4 w-4" />
                    <span>You've reached the free preview limit. Sign up to explore more.</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <a href="#signup" className="rounded-md bg-emerald-600 px-3 py-2 text-white hover:bg-emerald-700">Sign Up to Continue</a>
                  </div>
                </div>
              )}
            </div>
          </div>
        </Section>
      </div>

      {/* Other Sections (How It Works, Roadmap, etc.) */}
      {/* ... (no changes needed for these) */}

      {/* Signup CTA */}
      <div className="border-t bg-white" id="signup">
        <Section className="py-16">
          <div className="grid gap-6 lg:grid-cols-2 lg:items-center">
            <div>
              <h3 className="text-2xl font-semibold">Ready to go beyond the preview?</h3>
              <ul className="mt-4 space-y-2 text-slate-700">
                <li>Save & track past queries</li>
                <li>Run SQL on your own database</li>
                <li>Access full vector search tools</li>
              </ul>
            </div>
            <div className="flex gap-3">
              <a className="rounded-md bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-700" href="#">Create Free Account</a>
              <a className="rounded-md border px-4 py-2 hover:bg-slate-50" href="#">Login</a>
            </div>
          </div>
        </Section>
      </div>

      {/* Footer */}
      <footer className="mt-auto border-t bg-white">
        <Section className="py-8">
          <div className="flex flex-wrap items-center justify-between gap-4 text-sm text-slate-600">
            <div className="font-medium">IQuerio</div>
            <nav className="flex flex-wrap items-center gap-4">
              <a href="#features">Features</a>
              <a href="#how">How it works</a>
              <a href="#roadmap">Roadmap</a>
              <a href="https://github.com/pranavkp71/IQuerio" target="_blank">GitHub</a>
            </nav>
          </div>
        </Section>
      </footer>
    </main>
  )
}

// Feature component and Step component (already in your original code)
function Feature({ icon, title, desc }: { icon: React.ReactNode, title: string, desc: string }) {
  return (
    <div className="rounded-lg border bg-white p-4">
      <div className="mb-2 inline-flex h-9 w-9 items-center justify-center rounded-md bg-emerald-100 text-emerald-700">
        {icon}
      </div>
      <div className="font-medium">{title}</div>
      <div className="text-sm text-slate-600">{desc}</div>
    </div>
  )
}

function Step({ title, desc }: { title: string, desc: string }) {
  return (
    <div className="rounded-lg border bg-white p-6">
      <div className="text-base font-medium">{title}</div>
      <div className="mt-1 text-sm text-slate-600">{desc}</div>
    </div>
  )
}
