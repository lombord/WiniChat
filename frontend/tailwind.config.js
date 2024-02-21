/** @type {import('tailwindcss').Config} */

const commons = {
  info: "#0ea5e9",
  success: "#22c55e",
  warning: "#facc15",
  error: "#ef4444",
};

module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "primary-light": "hsl(var(--primary-light) / <alpha-value>)",
        "primary-medium": "hsl(var(--primary-medium) / <alpha-value>)",
      },
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        light: {
          "color-scheme": "light",
          primary: "#611DF2",
          "primary-content": "#F2F0F2",
          secondary: "#FF23A6",
          "secondary-content": "#f5d0fe",
          accent: "#2563eb",
          "accent-content": "#edf7fc",
          "--primary-light": "259 88% 58%",
          "--primary-medium": "259 89% 53%",
          "base-100": "hsl(259, 15%, 99%)",
          "base-200": "hsl(259, 15%, 96%)",
          "base-300": "hsl(259, 15%, 92%)",
          "base-content": "hsl(259, 25%, 25%)",
          "info-content": "#f0f9ff",
          "success-content": "#f0fdf4",
          "warning-content": "#fefce8",
          "warning-content": "#fef2f2",
          ...commons,
        },
        dark: {
          "color-scheme": "dark",
          primary: "hsl(266, 90%, 50%)",
          "primary-content": "#ffffff",
          secondary: "#ff2eaa",
          "secondary-content": "#ffffff",
          accent: "#2e6fff",
          "accent-content": "#ffffff",
          // hsl(259 96% 72%)
          "--primary-light": "259 100% 70%",
          // hsl(259 90% 60%)
          "--primary-medium": "259 90% 60%",
          "base-100": "hsl(213, 15%, 15%)",
          "base-200": "hsl(213, 15%, 12%)",
          "base-300": "	hsl(213, 15%, 9%)",
          "base-content": "hsl(220, 15%, 75%)",
          ...commons,
        },
      },
    ],
  },
  important: true,
};
