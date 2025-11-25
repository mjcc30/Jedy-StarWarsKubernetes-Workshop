/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      {
        starwars: {
          ...require("daisyui/src/theming/themes")["dracula"],
          primary: "#FFD700", // Gold for Jedi lightsabers/text
          secondary: "#E63946", // Red for Sith lightsabers/accents
          accent: "#457B9D", // Blue for Rebel Alliance/links
          neutral: "#1D3557", // Deep space blue
          "base-100": "#0D1B2A", // Dark background
          info: "#A8DADC",
          success: "#6A994E",
          warning: "#F4A261",
          error: "#D00000",
        },
      },
    ],
  },
}
