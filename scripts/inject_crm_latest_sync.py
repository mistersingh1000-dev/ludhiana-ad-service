from pathlib import Path
p=Path('crm/index.html')
s=p.read_text(encoding='utf-8')
tag='<script src="/crm/latest-screenshot-sync.js"></script>'
if tag not in s:
    marker="<script>const KEY='las_master_analytics_v1'"
    if marker not in s:
        raise SystemExit('CRM script marker not found')
    s=s.replace(marker,tag+marker,1)
p.write_text(s,encoding='utf-8')
