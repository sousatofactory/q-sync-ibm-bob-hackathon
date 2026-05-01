/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cosmic: {
          dark: '#0a0e27',
          darker: '#1a1f3a',
          green: '#00ff88',
          purple: '#9d4edd',
          black: '#000000',
        },
      },
      height: {
        'banner': '12vh',
        'workspace': '88vh',
      },
    },
  },
  plugins: [],
}
