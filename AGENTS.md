# ttcn3.dev

https://ttcn3.dev is a hub for humans and agents who need TTCN-3 information: standards, skills, releases, and related resources. Edit `content/` and `assets/`. `make build` copies them into `public/` and refreshes the JSON APIs. Do not hand-edit `public/`.

## What to publish

Write for a person reading the page and for an agent fetching the same fact. Each entry has a stable URL and one sentence on what it is. Add structured data when the fact is a list.

- Standards: `api/v1/standards/index.json`, refreshed by `make standards-update`.
- ntt releases: `api/v1/ntt/releases/`.
- Skills and other material: a stable path on this site, plus one line on what the reader gets from it.
- Pages are a table of contents a person can scan. Link out to the source. Keep the local copy short.

Publish only current, TTCN-3-relevant material. A person gets a clear link and a short description. An agent gets the same fact from that page or from the JSON file.

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
