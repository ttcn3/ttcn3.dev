# ttcn3.dev

Static site for https://ttcn3.dev. Edit `content/` and `assets/`. `make build` copies them into `public/` and refreshes the JSON APIs. Do not hand-edit `public/`.

## How to build pages

- Static HTML and one stylesheet. No JavaScript, frameworks, bundlers, CDNs, icon fonts, or analytics.
- Mobile first. Style the narrow screen as the default. Add `min-width` queries only when a wider layout needs them.
- Keep it simple: semantic HTML, short copy, obvious links, one column until the content needs more.
- Good UI means readable type, a comfortable line length, a clear heading order, and enough contrast in light and dark (`color-scheme`).
- No bloat. Do not add libraries, dependencies, or build steps. The Makefile and the existing favicon set are enough.
- Stay professional and conventional. Every page keeps the favicon, manifest, and touch-icon links already in `content/index.html`. Prefer boring, widely supported HTML and CSS.
- No animation. No `transition`, `@keyframes`, scroll effects, or motion on hover or focus.

```css
/* phone first */
body { padding: 1rem; }

@media (min-width: 40rem) {
  body { padding: 2rem; }
}
```
