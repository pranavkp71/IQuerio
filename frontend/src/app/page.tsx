"use client"

import { useEffect, useState } from 'react'
import Navbar from '@/components/Navbar'
import CodeBlock from '@/components/CodeBlock'
import { api, OptimizeResult } from '@/lib/api'
import FAQ from '@/components/FAQ'

const beforeSQL = `SELECT * FROM users WHERE age + 1 > 30;`
const afterSQL = `SELECT id, name FROM users WHERE age > 29;`

export default function Home() {
  const [dbStatus, setDbStatus] = useState<string>("")
  const [input, setInput] = useState(beforeSQL)
  const [result, setResult] = useState<OptimizeResult | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    api.dbTest().then(r => setDbStatus(r.status === 'Connected' ? `DB: ${r.version}` : `DB: ${r.error}`)).catch(() => {})
  }, [])

  async function runOptimize() {
    setLoading(true)
    try {
      const res = await api.optimize(input)
      setResult(res as OptimizeResult)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Navbar />
      <main className="relative">
        <div className="absolute inset-0 -z-10 aura" />
        {/* Hero */}
        <section className="mx-auto max-w-7xl px-6 pt-20 pb-16">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-4xl md:text-6xl font-semibold leading-tight">
                Optimize SQL & Search Data with AI — Instantly.
              </h1>
              <p className="mt-6 text-white/80 max-w-xl">
                Write smarter queries, perform vector search, and debug databases — all in one playground.
              </p>
              <div className="mt-8 flex gap-4">
                <a href="#demo" className="rounded-lg bg-brand.glow px-5 py-3 text-sm font-medium glow pulse-glow">Try Demo</a>
                <a href="https://github.com/pranavkp71/IQuerio" target="_blank" className="rounded-lg border border-white/20 px-5 py-3 text-sm font-medium hover:border-white/40">View GitHub</a>
              </div>
              {dbStatus && <p className="mt-4 text-xs text-white/60">{dbStatus}</p>}
            </div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-5 glow fade-up">
              <div className="flex items-center gap-2 text-white/60 text-xs mb-3">
                <span className="h-2 w-2 rounded-full bg-red-400" />
                <span className="h-2 w-2 rounded-full bg-yellow-400" />
                <span className="h-2 w-2 rounded-full bg-green-400" />
                <span className="ml-auto">AI assistant</span>
              </div>
              <CodeBlock title="Terminal" code={`$ db-toolkit optimize --query "${beforeSQL}"`} />
            </div>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="mx-auto max-w-7xl px-6 py-16 grid md:grid-cols-2 gap-10">
          <Feature title="AI Query Optimizer" icon="⚡" desc="Paste SQL — get back optimized, indexed, and explained output." />
          <Feature title="Vector Embedding Playground" icon="🔍" desc="Upload or enter data — perform similarity search intuitively." />
          <Feature title="Natural Language → SQL" icon="🧠" desc="Ask “Top paying customers last month” and get executable SQL." />
          <Feature title="Schema-Aware Debugging" icon="🛠️" desc="AI auto-detects schema and improves your queries." />
        </section>

        {/* How It Works */}
        <section id="how" className="mx-auto max-w-7xl px-6 py-16">
          <h2 className="text-2xl font-semibold mb-8">How It Works</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Step n="1" t="Connect Database or Paste SQL" />
            <Step n="2" t="IQuerio Analyzes & Refactors" />
            <Step n="3" t="You Get Optimized Output & Insights" />
          </div>
        </section>

        {/* Demo */}
        <section id="demo" className="mx-auto max-w-7xl px-6 py-16">
          <h2 className="text-2xl font-semibold mb-6">Demo — Optimization</h2>
          <div className="grid md:grid-cols-2 gap-6 mb-6">
            <textarea value={input} onChange={e=>setInput(e.target.value)} className="h-40 w-full rounded-xl bg-black/40 p-4 border border-white/10" />
            <CodeBlock title="After" code={result?.optimized_query || afterSQL} />
          </div>
          <button onClick={runOptimize} disabled={loading} className="rounded-lg bg-brand.aqua/20 px-5 py-3 border border-brand.aqua/40 hover:bg-brand.aqua/30">
            {loading ? 'Optimizing…' : 'Run Optimizer against API'}
          </button>
        </section>

        {/* Personas */}
        <section className="mx-auto max-w-7xl px-6 py-16">
          <h2 className="text-2xl font-semibold mb-8">Who Is It For?</h2>
          <div className="grid md:grid-cols-4 gap-6">
            <Persona title="Backend Developers" value="Ship faster with AI query suggestions" emoji="🧑‍💻" />
            <Persona title="Data Analysts" value="Query datasets without writing raw SQL" emoji="📊" />
            <Persona title="Indie Hackers" value="Add AI-powered database intelligence easily" emoji="🧱" />
            <Persona title="SaaS Teams" value="Improve performance without hiring DBAs" emoji="🏢" />
          </div>
        </section>

        {/* Use Cases */}
        <section className="mx-auto max-w-7xl px-6 py-16">
          <h2 className="text-2xl font-semibold mb-8">Popular Use Cases</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              {t:'Speed up dashboards',d:'Trim heavy queries, add missing indexes, and reduce p95 latency.'},
              {t:'Find similar users',d:'Upload descriptions and search via pgvector semantic similarity.'},
              {t:'Answer NL questions',d:'Prompt “top orders last week” and turn it into safe SQL.'},
            ].map((u,i)=> (
              <div key={i} className="rounded-xl border border-white/10 bg-white/5 p-6">
                <div className="font-medium">{u.t}</div>
                <p className="text-white/70 text-sm mt-2">{u.d}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Sample Queries */}
        <section className="mx-auto max-w-7xl px-6 py-16">
          <h2 className="text-2xl font-semibold mb-6">Sample Queries</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <CodeBlock title="Before" code={`SELECT * FROM orders WHERE created_at + interval '1 day' > now();`} />
            <CodeBlock title="After (suggested)" code={`SELECT id, total FROM orders WHERE created_at > now() - interval '1 day'; -- add index on created_at`} />
          </div>
          <p className="text-white/60 text-xs mt-3">Imaginary examples for demonstration.</p>
        </section>

        {/* Tech Stack */}
        <section className="mx-auto max-w-7xl px-6 py-16">
          <h2 className="text-2xl font-semibold mb-6">Tech Stack</h2>
          <div className="flex flex-wrap gap-3 text-sm">
            {['FastAPI','PostgreSQL','pgvector','Sentence Transformers','Next.js','Tailwind CSS','TypeScript'].map(b=> (
              <span key={b} className="rounded-full border border-white/15 bg-white/5 px-3 py-1">{b}</span>
            ))}
          </div>
        </section>

        {/* Testimonials */}
        <section className="mx-auto max-w-7xl px-6 py-16">
          <h2 className="text-2xl font-semibold mb-8">What people might say</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              {n:'A. Dev',q:'Cut our dashboard query time from 2.4s to 320ms.'},
              {n:'B. Analyst',q:'Loved the NL→SQL flow for quick ad-hoc questions.'},
              {n:'C. Founder',q:'Vector search helped us build smart “similar users” in a day.'},
            ].map((t,i)=> (
              <div key={i} className="rounded-xl border border-white/10 bg-white/5 p-6">
                <p className="text-white/80">“{t.q}”</p>
                <div className="text-white/60 text-sm mt-3">— {t.n}</div>
              </div>
            ))}
          </div>
        </section>

        {/* Security & Privacy */}
        <section className="mx-auto max-w-7xl px-6 py-16">
          <h2 className="text-2xl font-semibold mb-4">Security & Privacy</h2>
          <ul className="list-disc pl-6 text-white/80 space-y-2">
            <li>Credentials loaded via environment; no secrets in client.</li>
            <li>Read-only demo endpoints by default; safe sample data.</li>
            <li>Optional JWT-auth endpoints ready for protected flows.</li>
          </ul>
        </section>

        {/* FAQ */}
        <section className="mx-auto max-w-7xl px-6 py-16">
          <h2 className="text-2xl font-semibold mb-6">FAQ</h2>
          <FAQ items={[
            {q:'Does it require pgvector?', a:'Vector features use pgvector; SQL optimizer works without it.'},
            {q:'Which model is used?', a:'all-MiniLM-L6-v2 by Sentence Transformers for 384-dim embeddings.'},
            {q:'Can I host on my infra?', a:'Yes. Run the FastAPI server and point the frontend env to it.'},
          ]} />
        </section>

        {/* Early Access */}
        <section className="mx-auto max-w-2xl px-6 py-16 text-center">
          <h2 className="text-2xl font-semibold">Join Early Access</h2>
          <p className="text-white/70 mt-2">Get updates, release notes, and invites to try new features.</p>
          <form className="mt-6 flex gap-3 justify-center">
            <input type="email" placeholder="you@company.com" className="min-w-0 w-full md:w-96 rounded-lg bg-black/40 px-4 py-3 border border-white/10" />
            <button type="button" className="rounded-lg bg-brand.glow px-6 py-3 font-medium glow">Notify Me</button>
          </form>
          <p className="text-white/50 text-xs mt-2">No spam. Unsubscribe anytime.</p>
        </section>

        {/* Roadmap */}
        <section id="roadmap" className="mx-auto max-w-7xl px-6 py-16">
          <h2 className="text-2xl font-semibold mb-6">Roadmap</h2>
          <ul className="grid md:grid-cols-3 gap-4 text-white/90">
            <li className="rounded-xl border border-white/10 p-4 bg-white/5">✅ MVP: SQL Optimizer</li>
            <li className="rounded-xl border border-white/10 p-4 bg-white/5">🔜 Vector Playground</li>
            <li className="rounded-xl border border-white/10 p-4 bg-white/5">🚧 Collaboration + Query History</li>
          </ul>
          <p className="mt-4 text-sm text-white/60">Open Source — Built with ❤️ by Developers for Developers</p>
        </section>

        {/* Final CTA */}
        <section className="mx-auto max-w-7xl px-6 py-20 text-center">
          <h2 className="text-3xl md:text-4xl font-semibold">Power up your SQL workflow — Join early access now.</h2>
          <div className="mt-8 flex justify-center gap-4">
            <a href="#demo" className="rounded-lg bg-brand.glow px-6 py-3 font-medium glow pulse-glow">Get Started Free</a>
            <a href="https://github.com/pranavkp71/IQuerio" target="_blank" className="rounded-lg border border-white/20 px-6 py-3 font-medium">Star on GitHub</a>
          </div>
        </section>
      </main>
      <footer className="border-t border-white/10 py-8 text-center text-white/60 text-sm">© {new Date().getFullYear()} IQuerio</footer>
    </>
  )
}

function Feature({ title, desc, icon }: { title: string; desc: string; icon: string }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-6">
      <div className="text-2xl mb-2">{icon}</div>
      <div className="font-medium">{title}</div>
      <p className="text-white/70 text-sm mt-2">{desc}</p>
    </div>
  )
}

function Step({ n, t }: { n: string; t: string }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-6">
      <div className="text-white/60 text-sm">Step {n}</div>
      <div className="font-medium mt-1">{t}</div>
    </div>
  )
}

function Persona({ emoji, title, value }: { emoji: string; title: string; value: string }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-6 text-center">
      <div className="text-2xl">{emoji}</div>
      <div className="font-medium mt-2">{title}</div>
      <div className="text-white/70 text-sm mt-1">{value}</div>
    </div>
  )
}


