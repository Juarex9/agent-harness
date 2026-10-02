import js from "@eslint/js";
import react from "eslint-plugin-react";
import globals from "globals";

export default [
  // No lintear salida generada del build (si no, `npm run lint` falla
  // con errores en archivos que no escribimos).
  { ignores: ["client/dist/"] },
  js.configs.recommended,
  {
    // Client React: el plugin aporta jsx-uses-vars (sin él, el lint no ve
    // los componentes usados en JSX) y reglas específicas de React.
    files: ["client/src/**/*.{js,jsx}"],
    ...react.configs.flat.recommended,
    languageOptions: {
      ...react.configs.flat.recommended.languageOptions,
      globals: { ...globals.browser },
    },
    settings: { react: { version: "detect" } },
  },
  {
    // Runtime automático de Vite: no hace falta importar React en cada archivo.
    // Va en entrada separada: `rules` reemplaza, no fusiona, dentro del mismo objeto.
    files: ["client/src/**/*.{js,jsx}"],
    rules: { "react/react-in-jsx-scope": "off" },
  },
  {
    // Server, e2e y configs: globals de Node.
    files: ["server/**/*.js", "e2e/**/*.js", "*.config.js"],
    languageOptions: { globals: { ...globals.node } },
  },
];
