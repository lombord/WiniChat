/** @type {import('tailwindcss').Config} */

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
          ...require("daisyui/src/theming/themes")["[data-theme=light]"],
          ...customs,
        },
        dark: {
          ...require("daisyui/src/theming/themes")["[data-theme=dark]"],
          ...customs,
        },
      },
    ],
  },
  important: true,
};
