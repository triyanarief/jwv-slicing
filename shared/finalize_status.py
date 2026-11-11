"""Write review status from persisted evidence, keeping blocked work incomplete."""
from pathlib import Path
from datetime import datetime, timezone
import json
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent
status=ROOT/'docs/status'
coverage=json.loads((status/'coverage.json').read_text())
stamp=datetime.now(timezone.utc).isoformat()
history=status/'tracker-history-before-final-review.md'
if not history.exists():history.write_text((status/'tracker.md').read_text())
def notes(slug):
    if slug.startswith('home'):
        return ('Corrected category crops, footer columns/spacing, source broadcast icon/gradient, light sample copy, complete fifth Trending card, mobile title wrapping and signed-light hero geometry. All carousel tracks reached both ends with keyboard activation.',
                'Gilroy headings use authorized Urbanist; title widths, weight and baselines differ. Footer copy wraps differently, original pattern artwork phase/opacity and some photograph crops are not pixel-identical. Signed-in pages append a 42px local-sample notice. Mobile/tablet layouts are adaptive interpretations, not separately approved Figma designs.',
                ['Missing playback, channel/game, reminder, other hero-slide, profile, Schedule/About/legal and store destination designs or URLs; source-state render blockers apply.'])
    if slug.startswith('club-dashboard'):
        return ('Corrected native section heights, grid ratios, original chart placement, hero crops/icons and mobile menu contrast. Light chart starts at 617.8px; native document heights are 1202px light and 1266px dark.',
                'Authorized Selawik replaces Segoe UI on light; Manrope replaces the dark VS label font. Sidebar text density and font metrics differ. Original dark chart export includes paint beyond its frame. Dark storage meter uses the stated 32%, while the source drawing is visibly fuller. Sample names/counts are not live data.',
                ['Missing live-game/profile/notification/date-range and broadcasting workflows; component-state renders remain unavailable.'])
    if slug.startswith(('login','register')):
        return ('Corrected label colors, native panel geometry and small-screen paired-field wrapping. Verified empty/invalid-email validation, empty-password visibility toggle, registration/theme navigation and keyboard focus without entering credentials.',
                'Browser text rasterization and native input controls differ slightly. Mobile reflow is implementation-derived. The source registration submit label Sign in is retained. Expanded country/club choices and recovery UI are absent.',
                ['Missing recovery design and expanded country/club options where present; hover/help state renders unavailable. Authentication is not implemented or simulated.'])
    if slug.startswith('teams'):
        return ('Corrected crests, image placement, table columns, active navigation, light text contrast and mobile row spacing. Verified local search, age filtering and preservation of search across list/grid navigation where designed.',
                'Extremely pale source light-team names are darkened for readability. Browser font rasterization differs; tablet/mobile arrangements are adaptive. Add/manage/edit/delete and overflow actions are not completed workflows.',
                ['Missing add/manage/edit/delete/overflow designs and additional pagination data; component hover renders unavailable.'])
    if slug.startswith('broadcasters-wallets'):
        return ('Implemented the approved current redesign and retained its light counterpart; corrected active destination and relative theme navigation. Verified redesigned wallet search, no-match state, restore and Manage wallets anchor.',
                'The redesign source incorrectly highlights Teams; implementation highlights Wallets. Fractional source paint produces a 923px export for the nominal 922px frame. Browser font rasterization and adaptive tablet/mobile reflow differ.',
                ['Missing status/access/transfer/overflow menu designs, payment workflow and additional records; component hover renders unavailable.'])
    return ('Corrected active navigation, rejected-page copy, count labels, table columns, responsive status badges and mobile empty-state headers. Verified density keyboard toggle where present, navigation, theme and menus.',
            'Rejected headings/counts and unrelated request badges are corrected intentionally. YouTube/storage pages include an explicit sample-connection notice, extending their source card. Browser font rasterization and adaptive responsive table/card layout differ.',
            ['Missing account authorization/manage/unlink destinations where present and additional pagination data; component hover/help renders unavailable.'])

native=[]
for row in coverage['records']:
    if not row.get('implementation'):
        if row['node']=='8411:22575':row['relationship']='8439:11243 latest wallet redesign, explicitly approved and implemented'
        continue
    slug=row['implementation'].split('/')[0]; folder=ROOT/'qa'/slug
    result=json.loads((folder/'pass-2-results.json').read_text())
    assert result['passed'],slug
    required=['figma.png','pass-1-native.png','pass-1-comparison.png','pass-2-native.png','figma-vs-browser.png','keyboard-focus.png']
    required += [f'pass-{p}-{w}.png' for p in (1,2) for w in (1440,1024,768,390)]
    assert all((folder/p).exists() for p in required),slug
    corrections,differences,blockers=notes(slug)
    # Report the controls on this page, not unrelated gaps from its page family.
    controls=result.get('unavailableControls',[])
    blockers=list(dict.fromkeys(c['reason'] for c in controls))
    blockers.append('Shared hover/help component-state visual acceptance remains blocked by the 12 inaccessible source variants; see handoff target table.')
    if not controls:
        blockers.insert(0,'No page-local unavailable action is present; do not attribute missing account/payment workflows to this screen.')
    if slug.startswith('home-') and 'signed-in' not in slug:
        corrections='Corrected category crop, footer columns/spacing and source icon treatment. Category carousel reached both ends with keyboard activation.'
        differences=differences.replace(' Signed-in pages append a 42px local-sample notice.','')
    if slug=='broadcasters-wallets-light':
        corrections='Implemented retained light wallet source, correct active navigation and theme destination; verified local navigation, density and responsive layout.'
        differences='Browser font rasterization differs slightly. Tablet/mobile wallet rows reflow into labeled records; no separate approved mobile frame was supplied. Payment/status/transfer/edit flows and further pagination records are absent.'
    if slug.startswith(('broadcaster-requests','rejected-broadcasters','transaction-history')):
        differences='Browser font rasterization and adaptive responsive table/card layout differ. Native source assets and page geometry are retained.'
        if slug.startswith('rejected-broadcasters'):
            differences+=' Incorrect source headings, rejected counts and sidebar labels are corrected intentionally.'
        if slug.startswith('transaction-history'):
            differences+=' The source request-count badge is relabeled as transactions.'
    if slug.startswith('login'):
        differences='Browser text rasterization and native input controls differ slightly. Mobile reflow is implementation-derived. Recovery design is absent; country/club fields are not on this page.'
    row.update(completed=False,outcome='implemented and QA-reviewed; missing states/workflows blocked',qa1='Complete: native and four widths inspected; discrepancies corrected',qa2='Complete: current browser checks PASS; source/native, mobile and tablet visual review recorded',qa='Two review passes completed; full acceptance remains blocked',blockers=blockers,remaining_differences=differences,corrections=corrections,assets='776-file project integrity audit PASS; page image loading PASS; local fonts and original assets used')
    row['evidence'].append(f'qa/{slug}/review.md')
    row['evidence']=list(dict.fromkeys(row['evidence']))
    source=Image.open(folder/'figma.png').size; browser=Image.open(folder/'pass-2-native.png').size
    native.append({'page':slug,'node':row['node'],'frame':[row['width'],row['height']],'sourceExport':source,'browserCapture':browser,'browserDocumentHeight':result['responsive'][0]['height']})
    (folder/'review.md').write_text(f'''# {slug} — two-pass review

Source: `{row['node']}`; nominal frame {row['width']:g} × {row['height']:g}. Implementation: `{row['implementation']}`.
Review recorded: {stamp}. Status: **implemented and tested; blocked workflows are not completed**.

## Pass 1

Source context/render and initial native/1440/1024/768/390 captures inspected. {corrections}

## Pass 2

Current browser result: PASS. Native and four requested widths have no document overflow or missing images. No browser console/page errors, failed requests or HTTP errors were recorded. Local links resolve. The exact interaction assertions and unavailable-control reasons are in `pass-2-results.json`. Native/source and mobile captures were visually reviewed; 1024/768 contact sheets were also inspected. Corrections were recaptured before this status was written.

The full original source export is {source[0]} × {source[1]}; the browser capture is {browser[0]} × {browser[1]}. Fractional frame sizes round to CSS pixels, and some source exports include outside paint. The comparison preserves both originals without scaling either side.

## Remaining differences

{differences}

## Blocked work

{' '.join(blockers)} See `docs/status/handoff.md` and `docs/source/nested-state-render-failures.json`. These are not passed interactions. No authentication, payment, publishing, connection or playback success is fabricated. No 1:1 claim is made.

## Evidence

`figma.png`, `pass-1-native.png`, `pass-1-comparison.png`, `pass-1-1440/1024/768/390.png`, `pass-2-native.png`, `pass-2-1440/1024/768/390.png`, `figma-vs-browser.png`, `keyboard-focus.png`, `interaction-end.png`, `pass-2-results.json`.
''')
coverage['updated']=stamp
coverage['counts'].update(firstPassCaptures=31,currentSecondPassResults=31,twoPassReviewed=31,fullyCompleted=0)
coverage['counts'].pop('earlierSecondPassCaptures',None)
(status/'coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
(ROOT/'qa/native-dimensions.json').write_text(json.dumps(native,indent=2)+'\n')
lines=['# JWV coverage and QA tracker','',f'Updated {stamp}. All 44 intake frames are accounted for. **31 implemented, two-pass reviewed page/theme/state layouts; 0 fully completed against unresolved workflow/state requirements; 6 inferred superseded candidates; 7 non-page labels.** A blocked page is not counted as complete.','',
'Wallet 8439:11243 approval, alternative-font authorization and direct-browser QA authorization were received and acted on. Those are no longer blockers. Current work is local to the verified GPT-6 Astra High JWV desktop thread.','',
'Every implemented page has source context/render inspection, original local assets, two native/four-width capture sets, a labeled comparison, interaction results and a per-page review. Browser checks pass; visual differences and missing designs remain explicit. The old chronological log is preserved in [tracker-history-before-final-review.md](tracker-history-before-final-review.md).','',
'## Every screen-level frame','',
'| Figma node / frame | Outcome and source inspection | Implementation / replacement | QA and assets | Blockers / remaining differences |','| --- | --- | --- | --- | --- |']
for r in coverage['records']:
    if r.get('implementation'):
        slug=r['implementation'].split('/')[0]
        lines.append(f"| {r['node']} — {r['name']} ({r['width']:g} × {r['height']:g}) | Implemented; source context/render inspected; not fully complete | [{r['implementation']}](../../{r['implementation']}) | Pass 1 corrected; Pass 2 browser PASS + visual review; 1440/1024/768/390 PASS; assets local. [Evidence](../../qa/{slug}/review.md) | {' '.join(r['blockers'])} {r['remaining_differences']} |")
    else:lines.append(f"| {r['node']} — {r['name']} ({r['width']:g} × {r['height']:g}) | {r['outcome']}; {r['source_inspection']} | {r['relationship']} | Not a delivered page; source relationship recorded | Supersession is a source-based version inference, not a separate approval claim. |" if 'superseded' in r['outcome'] else f"| {r['node']} — {r['name']} | Non-page heading/banner; live label inspected | {r['relationship']} | Not applicable | Not a product page |")
lines += ['', '## Nested states and stopped steps','',
'Live source contained 214 reaction-bearing nodes, 12 distinct CHANGE_TO component targets, no navigation reactions and no flow starts. Five collapsed dropdown controls were inspected; expanded country/club/status lists were not supplied. Twelve context/render pairs failed with invalid visible-node selection and remain stopped. Exact errors and node IDs: [nested-state-render-failures.json](../source/nested-state-render-failures.json). Source properties were read, but that is not a rendered-state acceptance.','',
'To unblock: in Figma select a visible control → Go to main component → select its hover/open variant → Copy link to selection. Supply those visible links. Supply missing workflow node links or explicitly approve the documented static boundaries in the [handoff](handoff.md). No retries or alternate render route were used after the two failures.','',
'The old filesystem-import QA helper remains stopped. User-authorized direct browser calls completed the current checks; [resume diagnostics](../../qa/resume-diagnostics.md) records harness issues separately from product defects.','',
'## Verification totals','',
'31/31 current browser results PASS; 155 native/responsive viewport checks; 31 source/browser comparisons; 31 keyboard evidence captures. Sixteen home carousel track/viewport end-and-back checks PASS. Image/SVG audit: 776 files, zero integrity failures, zero missing or remote runtime references. Static HTML audit: 31 pages plus directory, zero broken anchors/duplicate IDs/missing image alt/form endpoints. Font sources/licenses and substitutions are documented in docs/source/.','',
'Review limitations: one Chromium runtime; no separately approved mobile designs; authorized font substitutions; unresolved component-state fidelity and workflows. Browser pass is not full design acceptance or backend integration. No 1:1 claim.']
(status/'tracker.md').write_text('\n'.join(lines)+'\n')
print('Wrote 31 page reviews and complete 44-frame tracker; fully completed remains 0.')
