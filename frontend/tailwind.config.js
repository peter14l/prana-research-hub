/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0C0F14",
        surface: {
          50: "#262E3D",
          100: "#1E2532",
          200: "#181E29",
          300: "#12161F",
          400: "#0F121A",
          DEFAULT: "#12161F",
        },
        prana: {
          yellow: "#FFE547",
          "yellow-hover": "#E6CD3F",
          sage: "#8A9A8F",
          "sage-light": "#A2B4A7",
          "sage-dark": "#5D6A61",
        },
        border: "rgba(255, 255, 255, 0.08)",
        "border-light": "rgba(255, 255, 255, 0.14)",
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "Consolas", "monospace"],
      },
    },
  },
  plugins: [],
};
