from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s2=re.sub(r'/assets/public-results\.js(?:\?v=[^"\']+)?','/assets/public-results.js?v=20260830-top10',s)
if s2==s and '/assets/public-results.js?v=20260830-top10' not in s:
    raise SystemExit('public-results.js reference not found')
p.write_text(s2,encoding='utf-8')
