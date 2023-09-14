/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  purge: ['./app/templates/**/*.html'],
  content: [
    './app/templates/**/*.html',
    './app/static/**/*.js',  // Adjusted this path too, in case you add JS files later.
  ],
  theme: {
    extend: {
      colors: {
        "medyk-purple": "#8f489c",
        "medyk-dark-purple": "rgba(80,9,94,1)",
      },
      backgroundColor: {
        "medyk-purple": "#8f489c",
        "medyk-dark-purple": "rgba(80,9,94,0.25)",
        "medyk-orange": "#f9ab80"
      },
      fontFamily: {
        'oswald': ['Oswald', 'sans-serif'],   // Use Oswald for class `font-oswald`
        'questrial': ['Questrial', 'sans-serif'], // Use Questrial for class `font-questrial`
      },
    },
  },
  plugins: [],
}

