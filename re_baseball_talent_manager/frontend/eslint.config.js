import js from "@eslint/js";
import globals from "globals";
import pluginVue from "eslint-plugin-vue";
import prettier from "eslint-plugin-prettier";
import configPrettier from "eslint-config-prettier";
import { defineConfig } from "eslint/config";
import tsParser from "@typescript-eslint/parser";

export default defineConfig([
  {
    files: ["**/*.{js,mjs,cjs,vue}"],
    plugins: { js },
    extends: ["js/recommended"],
    languageOptions: { globals: globals.browser },
  },

  {
    ...pluginVue.configs["flat/essential"],
    files: ["**/*.vue"],
    languageOptions: {
      parser: pluginVue.processors ? undefined : tsParser,
      parserOptions: {
        parser: tsParser,
        extraFileExtensions: [".vue"],
      },
    },
  },

  {
    plugins: { prettier },
    rules: {
      "prettier/prettier": "error",
    },
  },

  configPrettier,
]);
