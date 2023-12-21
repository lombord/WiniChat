/** @type {import('tailwindcss').Config} */

const themes = require("daisyui/src/theming/themes");

const customs = {
  accent: "#2563eb",
};

module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        light: {
          ...themes["[data-theme=light]"],
          ...customs,
        },
        dark: {
          ...themes["[data-theme=dark]"],
          ...customs,
        },
      },
    ],
  },
  important: true,
};
