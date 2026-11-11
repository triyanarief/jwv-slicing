# JWV Streaming — HTML review

I sliced the Design Ready frames into static HTML and CSS so the layouts can be reviewed in a browser. This repository is a review copy. It is not an accepted delivery, and it is not connected to a backend.

## What is here

- 31 light and dark layouts. Each layout has its own folder and `index.html`. Start at the [page index](index.html).
- Shared CSS, JavaScript, local fonts, and the original image assets under `shared/`.
- QA evidence under `qa/`. The index links the Figma-versus-browser image for each layout.
- `alt-5-pages/` is an earlier five-screen slice. I kept it so the two passes can be compared. It is not the current 31-layout set.
- Coverage notes and the remaining source blockers are in `docs/status/`.

## Preview locally

From this folder:

```sh
python3 -m http.server 8765
```

Open the root `index.html` on that server. Every page link, stylesheet, and image path is relative, so the same files also work when the site is served from a subpath such as GitHub Pages.

The published review is [https://triyanarief.github.io/jwv-slicing/](https://triyanarief.github.io/jwv-slicing/).

## QA notes

I substituted fonts where I cannot ship the original files:

- Selawik stands in for Segoe UI.
- Urbanist stands in for Gilroy on the home headings.
- Manrope stands in for Gilroy Bold on the dark dashboard VS label.

These are disclosed substitutes. I am not claiming exact typography parity.

I did not invent states or flows that Design Ready does not include. Controls for those missing flows stay disabled and say why. That includes team creation, account recovery, payments and transfers, schedule, legal pages, store destinations, and game playback. Signed-in screens show the sample data from the frames. They do not sign anyone in.

The 31 layouts have two local QA passes. Source blockers remain, so this is not a finished sign-off. Per-page notes are in `qa/<page>/review.md` and [docs/status/tracker.md](docs/status/tracker.md).

QA result JSON still records the local URLs from the original review run. Those records are evidence. The pages themselves do not navigate to them.

## What I left out

I did not commit ZIP exports, files larger than 50 MB, `node_modules`, `.DS_Store`, the QA virtualenv, the Playwright profile, or secrets. I recompressed QA PNGs larger than 400 KB so this review copy stays a practical size. The product images in `shared/assets/` are unchanged. The original uncompressed QA images stay in my local slicing folder.
