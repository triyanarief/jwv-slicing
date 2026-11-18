# Dashboard update — 18 November 2026

Design Ready file `qiE96RQiaLs1FX6jyb6JGB`. Screenshots for this pass are in `qa/dashboard-update-1118/`.

## Frames

| Frame | Page |
| --- | --- |
| 8587:3922 Club Dashboard dark | `club-dashboard-dark/` |
| 8623:14720 Club Dashboard light | `club-dashboard-light/` |
| 8623:5750 Teams List dark | `teams-list/` |
| 8623:15797 Teams List light | `teams-list-light/` |
| 8623:6800 Broadcasters & Wallet dark | `broadcasters-wallets/` |
| 8623:17140 Broadcasters & Wallet light | `broadcasters-wallets-light/` |
| 8623:7593 Broadcaster Request dark | `broadcaster-requests-dark/` |
| 8623:17459 Broadcaster Request light | `broadcaster-requests-light/` |
| 8623:8189 Rejected Broadcasters dark | `rejected-broadcasters-dark/` |
| 8623:17764 Rejected Broadcasters light | `rejected-broadcasters-light/` |
| 8623:8751 Authorize YouTube dark | `youtube-channel-dark/` |
| 8623:19783 Authorize YouTube light | `youtube-channel-light/` |
| 8623:8931 Storage Services dark | `storage-services-dark/` |
| 8623:20190 Storage Services light | `storage-services-light/` |
| 8623:9261 named Storage Services, content is Transaction History | `transaction-history-dark/` |
| 8623:20367 Transaction History light | `transaction-history-light/` |
| 8586:3042 Channels List | `channels-list-dark/` and derived `channels-list-light/` |
| 8647:30309 Channels List detail | `channel-detail-dark/` and derived `channel-detail-light/` |
| 8649:31837 Channels List offline | `channel-offline-dark/` and derived `channel-offline-light/` |

There is no light Channel List frame. Light channel pages reuse the dark layout with the light dashboard palette (white sidebar, mint page, Urbanist, existing light components).

The approved stadium hero treatment in `shared/site.css` is unchanged. New heroes use the same backdrop.

## Designer decisions

The designer approved all three open questions.

- Frame `8623:9261` stays Transaction History. `transaction-history-dark/` already uses that title, heading, and nav label, with `data-figma-node="8623:9261"`. Storage Services remains the separate connected-services pages. No copy change.
- The light dashboard chart title is **Streaming Activity**. Every HTML page was checked for the Figma spelling “Steaming”. Only `club-dashboard-light/` had it. The dark dashboard already reads “Streaming activity”.
- The light Broadcasters & Wallet column that shows the Allowed badge now uses **ACCESS STATUS**, the same header as the dark table. The narrow-screen row label is “Access status”.

1440px screenshots for this pass stay in `qa/dashboard-update-1118/`. The `before/` images remain the pre-update baselines. The `after/` images for `club-dashboard-light` and `broadcasters-wallets-light` were recaptured after these copy corrections.

## Open points

- Frame 8623:9261 does not include the Channel List nav item. The slice adds that item because the later dashboard and channel frames do, and the request asked for the link in both themes.
- The sidebar “Dark Mode” label in Figma is Montserrat. The slice uses Urbanist, per the written request to keep Urbanist everywhere on these pages.
- Search fields in the Figma variable set use Inter. The slice uses Urbanist.
- Channel playback, add team, approve, and transfer stay local previews. No account, payment, or stream is started.
- The live channel player uses the existing face-off photograph. The Figma player crop is a tighter youth face-off; that exact crop was not a separate small export.
