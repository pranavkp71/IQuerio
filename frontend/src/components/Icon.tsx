type IconName =
  | 'bolt' | 'search' | 'brain' | 'wrench' | 'database' | 'robot' | 'chart'
  | 'compass' | 'chat' | 'code' | 'bar' | 'cube' | 'building'

export default function Icon({ name, className = 'h-6 w-6 text-white' }: { name: IconName, className?: string }) {
  switch (name) {
    case 'bolt':
      return (
        <svg viewBox="0 0 24 24" fill="currentColor" className={className} aria-hidden>
          <path d="M13 3L4 14h6l-1 7 9-11h-6l1-7z"/>
        </svg>
      )
    case 'search':
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={className} aria-hidden>
          <circle cx="11" cy="11" r="7"/>
          <path d="M20 20l-3.5-3.5"/>
        </svg>
      )
    case 'brain':
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={className} aria-hidden>
          <path d="M8 6a3 3 0 0 1 6 0v12a3 3 0 0 1-6 0V6z"/>
          <path d="M5 9a3 3 0 0 1 3-3M16 6a3 3 0 0 1 3 3M5 15a3 3 0 0 0 3 3M16 18a3 3 0 0 0 3-3"/>
        </svg>
      )
    case 'wrench':
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={className} aria-hidden>
          <path d="M14.7 6.3a4 4 0 1 0-5.4 5.4L3 18v3h3l6.3-6.3a4 4 0 0 0 2.4-8.4z"/>
        </svg>
      )
    case 'database':
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={className} aria-hidden>
          <ellipse cx="12" cy="5" rx="9" ry="3"/>
          <path d="M21 5v6c0 1.7-4 3-9 3s-9-1.3-9-3V5M3 11v6c0 1.7 4 3 9 3s9-1.3 9-3v-6"/>
        </svg>
      )
    case 'robot':
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={className} aria-hidden>
          <rect x="4" y="7" width="16" height="12" rx="2"/>
          <circle cx="9" cy="13" r="1.5"/><circle cx="15" cy="13" r="1.5"/>
          <path d="M12 7V4"/><rect x="10" y="3" width="4" height="2" rx="1"/>
        </svg>
      )
    case 'chart':
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={className} aria-hidden>
          <path d="M3 3v18h18"/>
          <rect x="6" y="14" width="3" height="5"/><rect x="11" y="10" width="3" height="9"/><rect x="16" y="7" width="3" height="12"/>
        </svg>
      )
    case 'compass':
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={className} aria-hidden>
          <circle cx="12" cy="12" r="9"/>
          <path d="M15 9l-2 6-6 2 2-6 6-2z"/>
        </svg>
      )
    case 'chat':
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={className} aria-hidden>
          <path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4v8z"/>
        </svg>
      )
    case 'code':
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={className} aria-hidden>
          <path d="M8 16l-4-4 4-4M16 8l4 4-4 4"/>
        </svg>
      )
    case 'bar':
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={className} aria-hidden>
          <rect x="4" y="10" width="4" height="8"/><rect x="10" y="6" width="4" height="12"/><rect x="16" y="13" width="4" height="5"/>
        </svg>
      )
    case 'cube':
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={className} aria-hidden>
          <path d="M12 2l9 5-9 5-9-5 9-5zm0 10l9-5v10l-9 5-9-5V7l9 5z"/>
        </svg>
      )
    case 'building':
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className={className} aria-hidden>
          <rect x="3" y="4" width="7" height="16"/><rect x="14" y="8" width="7" height="12"/>
          <path d="M6.5 8h.01M6.5 12h.01M6.5 16h.01M17.5 11h.01M17.5 15h.01"/>
        </svg>
      )
    default:
      return null
  }
}


