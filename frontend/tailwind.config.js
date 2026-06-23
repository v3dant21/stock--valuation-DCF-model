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
        dark: {
          bg: '#0a0b0d',
          card: '#13141a',
          input: '#1a1b26',
        }
      }
    },
  },
  plugins: [],
}
