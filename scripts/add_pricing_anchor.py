from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='<section class="section price">'
new='<section class="section price" id="pricing">'
if 'id="pricing"' not in s:
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
