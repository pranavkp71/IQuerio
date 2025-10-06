import Link from 'next/link'

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 backdrop-blur supports-[backdrop-filter]:bg-black/30">
      <div className="mx-auto max-w-7xl px-6 py-4 flex items-center justify-between">
        <Link href="/" className="font-semibold tracking-tight text-white">
          IQuerio
        </Link>
        <nav className="hidden md:flex gap-6 text-sm text-white/80">
          <a href="#features" className="hover:text-white">Features</a>
          <a href="#how" className="hover:text-white">How it works</a>
          <a href="#roadmap" className="hover:text-white">Roadmap</a>
          <a href="https://github.com/pranavkp71/IQuerio" target="_blank" className="hover:text-white">GitHub</a>
        </nav>
        <div className="flex gap-3">
          <a href="#demo" className="rounded-md bg-brand.glow px-4 py-2 text-sm font-medium glow">Try Demo</a>
        </div>
      </div>
    </header>
  )
}


