"use client"

import { useState } from 'react'
import Navbar from '@/components/Navbar'
import { api } from '@/lib/api'
import CodeBlock from '@/components/CodeBlock'

export default function PlaygroundPage() {
  const [description, setDescription] = useState('Tech enthusiast into AI')
  const [limit, setLimit] = useState(3)
  const [similar, setSimilar] = useState<any[] | null>(null)

  const [nl, setNl] = useState('Show users over 30 similar to Tech enthusiast into AI')
  const [nlOut, setNlOut] = useState<any | null>(null)
  const [loading, setLoading] = useState(false)

  async function runSimilar() {
    setLoading(true)
    try {
      const res = await api.searchSimilar(description, limit)
      setSimilar(res.results)
    } finally {
      setLoading(false)
    }
  }

  async function runNl() {
    setLoading(true)
    try {
      const res = await api.nlQuery(nl)
      setNlOut(res)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-7xl px-6 py-12">
        <h1 className="text-3xl font-semibold">Playground</h1>
        <p className="text-white/70 mt-2">Try vector similarity and NL→SQL endpoints.</p>

        <section className="mt-10 grid md:grid-cols-2 gap-8">
          <div className="rounded-xl border border-white/10 bg-white/5 p-6">
            <h2 className="font-medium">Search Similar</h2>
            <div className="mt-4 space-y-3">
              <input className="w-full rounded-lg bg-black/40 px-3 py-2 border border-white/10" value={description} onChange={e=>setDescription(e.target.value)} />
              <input type="number" min={1} className="w-24 rounded-lg bg-black/40 px-3 py-2 border border-white/10" value={limit} onChange={e=>setLimit(parseInt(e.target.value||'1'))} />
              <div>
                <button onClick={runSimilar} disabled={loading} className="rounded-lg bg-brand.glow px-4 py-2 glow">{loading ? 'Running…' : 'Run /search-similar'}</button>
              </div>
            </div>
            {similar && (
              <div className="mt-6 overflow-auto">
                <table className="w-full text-sm">
                  <thead className="text-white/60">
                    <tr>
                      <th className="text-left py-2 pr-4">ID</th>
                      <th className="text-left py-2 pr-4">Name</th>
                      <th className="text-left py-2 pr-4">Description</th>
                      <th className="text-left py-2">Distance</th>
                    </tr>
                  </thead>
                  <tbody>
                    {similar.map((r:any)=> (
                      <tr key={r.id} className="border-t border-white/10">
                        <td className="py-2 pr-4">{r.id}</td>
                        <td className="py-2 pr-4">{r.name}</td>
                        <td className="py-2 pr-4">{r.description}</td>
                        <td className="py-2">{r.distance?.toFixed?.(3) ?? r.distance}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          <div className="rounded-xl border border-white/10 bg-white/5 p-6">
            <h2 className="font-medium">Natural Language → SQL</h2>
            <div className="mt-4 space-y-3">
              <input className="w-full rounded-lg bg-black/40 px-3 py-2 border border-white/10" value={nl} onChange={e=>setNl(e.target.value)} />
              <div>
                <button onClick={runNl} disabled={loading} className="rounded-lg bg-brand.aqua/20 px-4 py-2 border border-brand.aqua/40 hover:bg-brand.aqua/30">{loading ? 'Running…' : 'Run /nl-query'}</button>
              </div>
            </div>
            {nlOut && (
              <div className="mt-6 grid gap-3">
                <CodeBlock title="Generated SQL" code={nlOut.sql} />
                <CodeBlock title="Params" code={JSON.stringify(nlOut.params)} />
              </div>
            )}
          </div>
        </section>
      </main>
    </>
  )
}


