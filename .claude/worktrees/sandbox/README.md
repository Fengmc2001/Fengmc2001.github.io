# Fengmc Personal Portfolio

Personal GitHub Pages site based on the Astrofy template.

## Development

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

## Deploy

This repository includes a GitHub Actions workflow at `.github/workflows/deploy.yml`.
Push to `main`, then set GitHub Pages to deploy from GitHub Actions if the repository asks for a Pages source.

Expected public URL:

```text
https://Fengmc2001.github.io/
```

## Content to Personalize

- `src/config.ts`
- `src/pages/index.astro`
- `src/pages/projects.astro`
- `src/pages/cv.astro`
- `src/content/blog/*.md`
- `src/components/SideBarMenu.astro`
- `src/components/SideBarFooter.astro`
