module.exports = {
  "env": {
    "es2021": true,
    "node": true
  },
  "extends": "eslint:recommended",
  "parserOptions": {
    "ecmaVersion": "latest"
  },
  "rules": {
    "max-len": ["error", { "code": 120 }],
    "no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
  }
};
