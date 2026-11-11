"""Build labeled source/browser comparisons without modifying the originals."""
from pathlib import Path
import sys
from PIL import Image, ImageDraw

root=Path(__file__).resolve().parent.parent
qa_pass=int(sys.argv[1]) if len(sys.argv)>1 else 2
for folder in (root/'qa').iterdir():
    browser=folder/f'pass-{qa_pass}-native.png'
    if not folder.is_dir() or not browser.exists() or not (folder/'figma.png').exists():continue
    source=Image.open(folder/'figma.png').convert('RGB')
    actual=Image.open(browser).convert('RGB')
    comparison=Image.new('RGB',(source.width+actual.width,max(source.height,actual.height)+46),'#eeeeee')
    draw=ImageDraw.Draw(comparison)
    draw.text((20,14),f'FIGMA SOURCE — {folder.name} — {source.width} × {source.height}',fill='#111111')
    draw.text((source.width+20,14),f'BROWSER — QA PASS {qa_pass} — {actual.width} × {actual.height}',fill='#111111')
    comparison.paste(source,(0,46));comparison.paste(actual,(source.width,46))
    comparison.save(folder/('figma-vs-browser.png' if qa_pass==2 else 'pass-1-comparison.png'))
