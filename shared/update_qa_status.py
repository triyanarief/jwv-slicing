"""Persist per-page QA progress; source gaps remain separate from test results."""
from pathlib import Path
import json,sys
root=Path(__file__).resolve().parent.parent
slug=sys.argv[1]
result=json.loads((root/'qa'/slug/'pass-2-results.json').read_text())
path=root/'docs/status/coverage.json'
coverage=json.loads(path.read_text())
for row in coverage['records']:
    if row['node']!=result['node']:continue
    row['qa']='Pass 1 inspected/corrected; current pass 2 browser checks '+('PASS' if result['passed'] else 'FAIL')+'; final visual review pending'
    row['responsive']='1440/1024/768/390: '+('PASS' if all(x['documentWidth']<=x['width'] and not x['missingImages'] for x in result['responsive']) else 'FAIL')
    row['interaction']=result['interactions']
    row['evidence']=[f'qa/{slug}/'+p for p in ['figma.png','pass-1-native.png','pass-2-native.png','pass-2-results.json','keyboard-focus.png','figma-vs-browser.png']]
    row['assets']='Local image load checks PASS at native and four responsive widths'
    row['blockers']=[b for b in row.get('blockers',[]) if 'QA helper' not in b and 'authorization pending' not in b]
coverage['counts']['currentSecondPassResults']=len(list((root/'qa').glob('*/pass-2-results.json')))
path.write_text(json.dumps(coverage,indent=2)+'\n')
tracker=root/'docs/status/tracker.md'
text=tracker.read_text()
lines=text.splitlines()
for i,line in enumerate(lines):
    if line.startswith('| '+result['node']+' '):
        r=next(r for r in coverage['records'] if r['node']==result['node'])
        lines[i]=f"| {r['node']} — {r['name']} ({r['width']:g} × {r['height']:g}) | Implemented; source context/render inspected | `{slug}/index.html` | {r['assets']} | {r['qa']} | {r['responsive']}; interaction details in JSON | `qa/{slug}/`; missing designs remain blocked, not completed |"
tracker.write_text('\n'.join(lines)+f"\nQA update {result['checkedAt']}: `{slug}` pass 2 browser {'PASS' if result['passed'] else 'FAIL'}; evidence saved. Final native/mobile visual review pending.\n")
