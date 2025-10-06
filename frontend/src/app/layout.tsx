import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'IQuerio — AI SQL Optimizer',
  description: 'Optimize SQL & search data with AI — instantly.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-screen bg-gradient-to-br from-[#0b0f1a] via-[#0a0814] to-[#120a2a] text-white antialiased">
        {children}
      </body>
    </html>
  )
}


