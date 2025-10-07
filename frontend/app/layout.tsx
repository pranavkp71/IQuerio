import './globals.css'
import { ReactNode } from 'react'

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="text-slate-900">
        <header className="sticky top-0 z-40 w-full border-b bg-white/85 backdrop-blur">
          <div className="mx-auto flex h-14 w-full max-w-6xl items-center justify-between px-4 sm:px-6 lg:px-8">
            <a href="/" className="font-semibold tracking-tight">IQuerio</a>
            <nav className="hidden md:flex items-center gap-6 text-sm text-slate-600">
              <a href="#features" className="hover:text-slate-900">Features</a>
              <a href="#how" className="hover:text-slate-900">How it works</a>
              <a href="#roadmap" className="hover:text-slate-900">Roadmap</a>
              <a href="https://github.com/pranavkp71/IQuerio" target="_blank" className="hover:text-slate-900">GitHub</a>
            </nav>
            <a href="#demo" className="inline-flex items-center rounded-md bg-emerald-600 px-3 py-1.5 text-white hover:bg-emerald-700 text-sm">Try Demo</a>
          </div>
        </header>
        {children}
      </body>
    </html>
  )
}
