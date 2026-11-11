# JWV Streaming — HTML / CSS handoff

Static slices of the approved screens in the Figma file
[Justin Valinski - JWV Streaming UI UX Design](https://www.figma.com/design/qiE96RQiaLs1FX6jyb6JGB/Justin-Valinski---JWV-Streaming-UI-UX-Design?node-id=1-10).
Page used: **Design Ready**. Archived, Cover, Inspo, Workspace, and Component were not sliced.
Older frames still on Design Ready (`Dashboard / …`, login, and homepage) were left out. The approved update is the redesign cluster: one light dashboard, the image team list, and three dark screens.

## Pages

| Folder | Screen | Figma node | Frame |
| --- | --- | --- | --- |
| `01-club-dashboard-light` | Club Dashboard, light | `8436:7027` | 1528 × 1202, fill `#F5F8F7` |
| `02-team-list-images` | Team List with photos | `8439:10585` | 1512 × 913, fill `#111620` |
| `03-club-dashboard-dark` | Club Dashboard, dark | `8436:7470` | 1512 × 1266, fill `#121A20` |
| `04-team-list-dark` | Team List table | `8438:9957` | 1512 × 913, fill `#111620` |
| `05-broadcasters-wallets-dark` | Broadcasters & Wallets | `8439:11243` | 1528 × 922, fill `#121422` |

Each folder contains `index.html`, `styles.css`, and `assets/`. Open `index.html` in a browser. No build step.

The light dashboard theme switch links to the dark dashboard. The team-list Cards / List control links the image screen and the table screen. Sidebar items that were not part of this handoff are labels only.

## Fonts

The frames use Segoe UI on the light dashboard, Urbanist on the dark screens, plus Inter, Arimo, and Arial for smaller labels. The pages load Urbanist, Inter, Arimo, and Outfit from Google Fonts, and use a local Segoe UI when the machine has it.

## Color

- Page light `#F5F8F7`, cards `#FFFFFF`, line `#E5ECE8`, ink `#172222`, muted `#789087`
- Green `#129A39`, `#1DA448`, `#31BB41`, active text `#076A26`, active wash `#E4F8E7`
- Card radius 13px, border 0.8px, shadow `0 10px 32px rgba(20, 46, 34, 0.04)`
- Sidebar width 251px, padding `29px 19px 24px 19px` (light dashboard, from Dev Mode)
- Dark pages use the frame fill listed above, cards around `#1A242C`, and the same green

## Breakpoints

Frames are 1512 or 1528 wide. Below that width the layout is fluid (`width: min(frame, 100%)`).

Checked viewports: **1440, 1024, 768, 390**. At each width, `documentElement.scrollWidth` matched the viewport (no horizontal page scroll). Tables that need more than the viewport scroll inside their own card.

- 1440 and 1024: sidebar plus content. At 1024, stat cards and split panels stack to two columns or one column.
- 768 and 390: sidebar becomes a wrapping bar above the content. Stats stack to one column at 390.

## Assets

Photos and the stadium plate were exported from the open Figma file (the images the editor had already loaded). Icons in the slices are inline SVG or CSS shapes. Live-game thumbnails keep the LIVE badge that is baked into the exported PNG.

## QA

11 Nov 2026. Each page is positioned from the Design Ready frame (text, fills, radii, and exported icons/photos). Below the frame width the page scales down, so it does not add a horizontal scrollbar.

Side-by-side comparisons, Figma on the left and the HTML screenshot on the right, are in `_qa/`:

- `01-club-dashboard-light-figma-vs-html.png`
- `02-team-list-images-figma-vs-html.png`
- `03-club-dashboard-dark-figma-vs-html.png`
- `04-team-list-dark-figma-vs-html.png`
- `05-broadcasters-wallets-dark-figma-vs-html.png`

Those files are local evidence. They are not required to open the pages.

## Handoff notes for implementation

- These are static screens, not a logged-in app. Buttons do not call an API.
- Build the real app from these measurements, then replace placeholder team IDs if production data differs. The four team rows in the file read as `#8189` in the slice.
- Frame width is 1512 or 1528, not 1440. 1440 is the browser viewport used for QA, and the layout fits it without a horizontal scrollbar.
