from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
css='<link rel="stylesheet" href="/assets/public-results.css" />\n'
if '/assets/public-results.css' not in s:
    s=s.replace('</head>',css+'</head>')
start=s.find('  <!-- RESULTS / PROOF -->')
end=s.find('  <!-- TESTIMONIALS -->')
if start==-1 or end==-1 or end<=start:
    raise SystemExit('Results section markers not found')
section='''  <!-- RESULTS / PROOF -->
  <section class="crm-public" id="results">
    <div class="wrap">
      <div class="eyebrow">Live CRM Performance Dashboard</div>
      <h2>Real campaign analytics from Ludhiana Ad Service</h2>
      <p class="lead">Selected customer-facing performance data from our CRM — conversations, cost per result, reach, impressions and ad spend. Private client information is never shown here.</p>
      <div id="crmPublicDashboard"></div>
    </div>
  </section>

'''
s=s[:start]+section+s[end:]
js='<script src="/assets/public-results.js" defer></script>\n'
if '/assets/public-results.js' not in s:
    s=s.replace('</body>',js+'</body>')
p.write_text(s,encoding='utf-8')
