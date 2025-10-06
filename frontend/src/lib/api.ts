const BASE_URL = process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
    ...options,
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `HTTP ${res.status}`)
  }
  return res.json()
}

export const api = {
  dbTest: () => request<{ status: string; version?: string; error?: string }>(`/db-test`),
  optimize: (query: string) => request(`/optimize`, { method: 'POST', body: JSON.stringify({ query }) }),
  searchSimilar: (description: string, limit = 3) => request(`/search-similar`, { method: 'POST', body: JSON.stringify({ description, limit }) }),
}

export type OptimizeResult = {
  query: string
  optimized_query: string
  issues: string[]
  suggestions: string[]
  explain_plan: any
}


