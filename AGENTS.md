# JWV — clean HTML/CSS website rebuild

## Authority and execution
Triyan requested this fresh project on 11 November 2026 at 12:40 WIB after rejecting the previous Cursor slicing: stray left/right gaps, incomplete screens, and non-working website behavior. Work only in this new project and a NEW Codex desktop-app thread. Runtime must be GPT-6 Astra, effort High. Do not use Cursor, cursor-agent, another model, or a separate Codex CLI executor. Togolist development is paused: do not open, resume, modify, or run its projects/threads.

## Source of truth and complete coverage
Figma: https://www.figma.com/design/qiE96RQiaLs1FX6jyb6JGB/Justin-Valinski---JWV-Streaming-UI-UX-Design?node-id=1-10
Use page `1:10`, `✅ Design Ready`; do not implement Archived, Inspo, Workspace, or Component-library pages as product pages. Read `docs/status/figma-inventory.json` and `docs/status/tracker.md` first, then inspect the LIVE Figma source and prototype connections. The intake inventory contains 44 screen-level/direct-section frames: 37 screen-sized candidates and 7 heading/banner frames. It is not a verified count of final approved pages. Inventory ALL candidates and all relevant nested state frames; assign every screen-level frame an explicit outcome so nothing is silently skipped.

The previous handoff identified only five latest screens:
- `8436:7027`: Club Dashboard light
- `8439:10585`: Team List images
- `8436:7470`: Club Dashboard dark
- `8438:9957`: Team List table/dark
- `8439:11243`: Broadcasters & Wallets redesign
These five are NOT an exhaustive scope limit: Triyan now requests EVERYTHING in the final Figma design. The Design Ready page also contains home/hero variants, login/registration, dashboard/menu screens and filled/empty variants. Resolve final/superseded/variant relationships from actual source/annotations; preserve traceability. If the final version or intended missing state is ambiguous, list the precise node and question as a blocker instead of inventing the UI. Continue independent confirmed screens rather than excluding the rest without explanation. Do not mark this goal complete while any required frame is unaccounted for.

## Deliverable and layout
Build production-quality static semantic HTML + separate maintainable CSS, with minimal vanilla JavaScript only for interaction. No heavy framework. One kebab-case folder per page with `index.html`, shared CSS/JS/assets in `shared/`, plus a root navigation index, English README and handoff instructions. All files, comments, status notes and user-facing documentation in English.

Use a real fluid full-width layout. Remove accidental outer margins/stray left and right gaps while preserving intentional Figma gutters and panel padding. Use grid/flex and responsive reflow, NOT a fixed absolute-positioned screenshot canvas, full-page raster image, CSS zoom, or transform-scale-to-fit. The UI must remain legible and usable at 1440, 1024, 768 and 390 CSS pixels with no unintended document-level horizontal overflow or clipped content.

Implement real relative navigation links between designed pages and a visibly correct active destination. Implement all designed hover, focus, active, dropdown, tab, search/filter, pagination, form validation, and toggle states supported by Figma. Include light/dark mode when designed. Preserve keyboard access, semantic buttons/links, clear focus, and accessible labels. For static-only actions, provide safe local demo behavior where the existing design permits it and document the boundary. Never fake successful authentication, payment, publishing, or backend connectivity. If a destination/state has no design, record it as a blocker rather than constructing an invented screen or leaving a misleading dead link.

## Fidelity
Read high-fidelity Figma design context and a reference render before implementing each frame; correlate metadata and visible nodes. Aim for exact Figma spacing, typography, colors, radii, geometry and asset placement. Download and use the real exported SVG/PNG/WebP assets and correct font family/weights. Do not substitute placeholders, emoji, guessed icons/photos, redraw provided assets, embed a whole-frame screenshot as UI, or leave temporary Figma URLs in output. Reuse shared tokens/components where exact. Never claim a 1:1 match without evidence; show measured remaining differences honestly.

## QA and evidence
Do two complete QA passes, fixing discrepancies before the second. For every page capture the source Figma render and the actual browser result at matching native frame dimensions, then save a labeled side-by-side image under `qa/<page>/figma-vs-browser.png`. Keep original source/browser images too. Test and save responsive evidence at 1440/1024/768/390 and interaction/keyboard results for each page. Full-height pages must be captured completely. Verify assets load, all in-scope links resolve, all required states function, and browser console errors are absent. A screenshot by itself is not proof of working interactions. Log exact source frame id, implementation path, source inspection status, asset status, pass-1/pass-2 result, responsive checks, interaction checks, evidence paths, blockers and remaining visual differences in `docs/status/tracker.md`. Update after each frame/QA pass. Write final `docs/status/handoff.md` with true implemented count versus inventory and any exclusions/blockers.

## Isolation and safety
The previous output is reference evidence only, rejected by the user, not an implementation baseline. Preserve it unchanged:
- `/Users/triyanwibowo/Documents/Codex/2026-10-09/task-4/Tim/work/JWV-HTML-CSS/`
- `/private/tmp/JWV - HTML CSS Slicing - 11 Nov 2026/`
No deletion, upload, publishing, Drive sharing, Slack/Upwork/email/client contact, external form submission, push, PR, remote commit, Jira, or Figma writes. Work locally only. Never read or disclose secret values, invent `.env`, enter passwords/2FA, bypass a blocked tool, or manipulate other agents' browser sessions. Do not change other queued jobs. If the same step fails twice, stop that step, log exact failures and a safe manual next action, and report; do not retry via an alternate route. Only use supported app tools and user-granted access.
