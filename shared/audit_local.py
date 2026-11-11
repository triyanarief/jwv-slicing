"""Audit local file integrity and links without making network requests."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
from datetime import datetime, timezone
import hashlib, json, re, xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(); self.path=path; self.ids=[]; self.refs=[]; self.issues=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for key in ('href','src'):
            if a.get(key):self.refs.append(a[key])
        if tag=='img' and 'alt' not in a:self.issues.append('Image without alt')
        if tag=='form' and a.get('action'):self.issues.append('Form endpoint present')

pages=[ROOT/'index.html',*sorted(ROOT.glob('*/index.html'))]
documents={p:Document(p) for p in pages}
issues=[]; missing=[]; remote=[]; referenced=set()
for p,d in documents.items():
    d.feed(p.read_text())
    issues.extend({'file':str(p.relative_to(ROOT)),'issue':x} for x in d.issues)
    issues.extend({'file':str(p.relative_to(ROOT)),'duplicateId':k} for k,v in Counter(d.ids).items() if v>1)
def check_ref(p,ref):
    u=urlsplit(ref)
    if u.scheme or u.netloc:
        if ref.startswith(('http:','https:')) and not (p.name=='index.html' and p.parent==ROOT):remote.append({'file':str(p.relative_to(ROOT)),'reference':ref})
        return
    dest=(p.parent/unquote(u.path)).resolve() if u.path else p
    if dest.is_dir():dest=dest/'index.html'
    if not dest.exists():missing.append({'file':str(p.relative_to(ROOT)),'reference':ref})
    else:
        referenced.add(str(dest.relative_to(ROOT)))
        if u.fragment and dest in documents and unquote(u.fragment) not in documents[dest].ids:issues.append({'file':str(p.relative_to(ROOT)),'brokenAnchor':ref})
for p,d in documents.items():
    for ref in d.refs:check_ref(p,ref)
for p in (ROOT/'shared').glob('*.css'):
    for ref in re.findall(r'url\([\s\'"]*([^\)\'"\s]+)',p.read_text()):check_ref(p,ref)
assets=[]; errors=[]
for p in sorted((ROOT/'shared/assets').rglob('*')):
    if not p.is_file():continue
    try:
        if p.suffix=='.svg':ET.parse(p)
        else:
            with Image.open(p) as im:im.verify()
    except Exception as e:errors.append({'file':str(p.relative_to(ROOT)),'error':str(e)})
    assets.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
stamp=datetime.now(timezone.utc).isoformat()
audit={'checkedAt':stamp,'asset_files_validated':len(assets),'asset_validation_errors':errors,'missing_local_references':missing,'remote_runtime_references':remote,'referenced_paths':sorted(referenced),'files':assets}
(ROOT/'qa/asset-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
revision=pages+list((ROOT/'shared').glob('*.css'))+list((ROOT/'shared').glob('*.js'))+list((ROOT/'shared/fonts').glob('*.ttf'))+list((ROOT/'shared/fonts').glob('*.woff*'))
static={'checkedAt':stamp,'pages':len(pages)-1,'rootDirectory':True,'issues':issues,'scope':'Static IDs, alt attributes, local paths, anchors, form endpoints and revision hashes; browser behavior is checked separately.','revisionHashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in revision}}
(ROOT/'qa/static-audit.json').write_text(json.dumps(static,indent=2)+'\n')
print(json.dumps({'pages':len(pages)-1,'assets':len(assets),'invalidAssets':len(errors),'missingReferences':len(missing),'remoteRuntimeReferences':len(remote),'staticIssues':issues}))
