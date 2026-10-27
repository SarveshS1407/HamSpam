/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#070b14',
          900: '#0b1324',
          850: '#101a33',
          800: '#162344',
          700: '#20325d',
          600: '#2f4780',
        },
        charcoal: {
          900: '#111418',
          800: '#1b2028',
          700: '#282e3a',
          600: '#3a4252',
        },
        ham: {
          500: '#10b981',
          600: '#059669',
          700: '#047857',
        },
        spam: {
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
        }
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      }
    },
  },
  plugins: [],
}
