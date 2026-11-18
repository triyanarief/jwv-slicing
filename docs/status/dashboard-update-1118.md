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

## Open points

- Figma labels the light activity chart “Steaming Activity”. The slice keeps that spelling.
- The light wallet table header says AGE GROUP while the cell is the Allowed status badge. Both are in the frame.
- Frame 8623:9261 is named Storage Services and shows the empty transaction history. It does not include the Channel List nav item; the slice adds that item because the later dashboard and channel frames do, and the request asked for the link in both themes.
- The sidebar “Dark Mode” label in Figma is Montserrat. The slice uses Urbanist, per the written request to keep Urbanist everywhere on these pages.
- Search fields in the Figma variable set use Inter. The slice uses Urbanist.
- Channel playback, add team, approve, and transfer stay local previews. No account, payment, or stream is started.
- The live channel player uses the existing face-off photograph. The Figma player crop is a tighter youth face-off; that exact crop was not a separate small export.
