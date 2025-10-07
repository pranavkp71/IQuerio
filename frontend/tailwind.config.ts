import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f2fbf6',
          100: '#e6f7ee',
          200: '#c7ecd8',
          300: '#9fdec0',
          400: '#5fc796',
          500: '#2fb878',
          600: '#1f9b62',
          700: '#197b4f',
          800: '#155f40',
          900: '#124f36',
        },
      },
    },
  },
  plugins: [],
}
export default config
