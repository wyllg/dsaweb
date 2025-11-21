/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/main/templates/**/*.html',
    './src/main/static/**/*.js',
    './src/users/templates/**/*.html',
    './src/users/static/**/*.js',
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
      },
    },
  },
  plugins: [],
}