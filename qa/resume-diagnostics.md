# Resumed QA diagnostics

The old Node-import batch helper remains stopped after its two failures. User explicitly authorized direct browser calls.

During setup of the new direct calls, replacing a placeholder in a comment instead of the data expression produced `ReferenceError: __FRAMES__ is not defined` before page work. The placeholder substitution was corrected.

The first wallet action check then reached the aria-disabled boundary control. Playwright click waits for an enabled control, so the dialog event timed out. This is a different step from data setup. Use keyboard focus + Enter to verify the deliberately focusable boundary explanation; do not wait for aria-disabled controls to become enabled. Native and four-width screenshots completed before that action check.

The wallet keyboard activation produced the exact native alert: “Streaming-time purchase and payment designs are not supplied. No payment has been made.” The tool surfaced modal state before returning the surrounding batch result; its dialog handler had already dismissed it when the modal tool was called. Stop the combined alert/batch step. Remaining independent responsive, navigation, filtering and keyboard captures do not invoke blocked backend controls. Shared boundary behavior is evidenced by the observed native wallet alert.

The first four admin result files recorded aborted link-audit GET bodies because the test read only response headers before theme navigation. Every response had HTTP 200. The audit now consumes each local HTML response before navigating; these test-induced aborts are retained here and the affected checks are rerun.

Carousel end/back check: the first direct click batch hit an enabled-state race during smooth scrolling (one failure). A settled keyboard activation check then passed all 16 track/viewport combinations; results are in carousel-results.json. No product change was needed for the timing race.

Final size audit detected cached CSS immediately after edits. Local-only page routing now disables HTTP cache for QA. All 31 pages are recaptured after this correction; earlier sheet previews are historical.

One cache-disabled signed-in-home QA invocation observed the static fullscreen fallback alert before producing a result. The alert was dismissed through the supported dialog handler; the next full check passed for both signed-in pages. The QA template now waits for fullscreenElement before checking/exiting to avoid navigating during the asynchronous request. A shell quoting edit failed once before execution; apply_patch applied that template change. No source-state retry was involved.
