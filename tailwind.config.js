/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{html,js}',
    './src/main/templates/**/*.html',
    './src/main/static/**/*.js',
    './src/user/templates/**/*.html',
    './src/user/static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        gochujang: "#780000",
        crimson: "#C1121F",
        varden: "#f2ece1",
        cosmos: "#003049",
        bluish: "#669BBC",
      },
      fontFamily: {
        hubot: ['Hubot Sans', 'sans-serif'],
        work: ['Work Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}