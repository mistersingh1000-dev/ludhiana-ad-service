from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove/replace every visible and metadata reference to free demo.
replacements = [
    (r'FREE Demo', 'Check Packages'),
    (r'Free Demo', 'Check Our Plans'),
    (r'FREE demo', 'check our pricing'),
    (r'free demo', 'check our pricing'),
]
for pattern, repl in replacements:
    s = re.sub(pattern, repl, s)

# Exact website WhatsApp prefilled message requested by owner.
s = re.sub(
    r'const PREFILL_MSG\s*=\s*"[^"]*";',
    'const PREFILL_MSG     = "Hi, I got your number from your website. May I know your plans?";',
    s,
    count=1
)

# Make package-card WhatsApp messages pricing-focused, not demo-focused.
s = s.replace(
    'var m = "Hi, mujhe " + plan + " plan ke baare mein jaanna hai. check our pricing se shuru karna hai.";',
    'var m = "Hi, I got your number from your website. May I know more about " + plan + "?";'
)

# Replace form WhatsApp intro if present after global demo replacement.
s = s.replace(
    'var msg = "Hi, mujhe apne business ke liye check our pricing chahiye.\\n"',
    'var msg = "Hi, I got your number from your website. May I know your plans?\\n"'
)

# Add a true desktop/mobile floating WhatsApp icon at bottom-right.
css = r'''

  /* floating WhatsApp button — bottom right */
  .wa-float{position:fixed;right:22px;bottom:22px;z-index:999;display:grid;place-items:center;width:60px;height:60px;border-radius:50%;background:#25D366;color:#fff;text-decoration:none;box-shadow:0 10px 28px rgba(0,0,0,.28);transition:transform .15s ease,box-shadow .15s ease}
  .wa-float:hover{transform:translateY(-3px) scale(1.04);box-shadow:0 14px 32px rgba(0,0,0,.34)}
  .wa-float svg{width:31px;height:31px}
  .wa-float:focus-visible{outline:3px solid #fff;outline-offset:3px}
  @media(max-width:640px){.wa-float{right:16px;bottom:82px;width:56px;height:56px}.wa-float svg{width:29px;height:29px}}
'''
if '.wa-float{' not in s:
    s = s.replace('</style>', css + '\n</style>', 1)

float_html = r'''
  <a class="wa-float" id="waFloat" href="#" target="_blank" rel="noopener" aria-label="Chat on WhatsApp" title="Check our plans on WhatsApp">
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M.06 24l1.68-6.13A11.9 11.9 0 0 1 .16 11.9C.16 5.33 5.5 0 12.06 0a11.8 11.8 0 0 1 8.4 3.49 11.8 11.8 0 0 1 3.48 8.41c0 6.56-5.34 11.9-11.9 11.9a11.9 11.9 0 0 1-5.7-1.45L.06 24zm6.6-3.8c1.7.99 3.3 1.58 5.4 1.58 5.44 0 9.87-4.43 9.88-9.88a9.8 9.8 0 0 0-2.9-6.99A9.8 9.8 0 0 0 12.07 2c-5.45 0-9.88 4.43-9.88 9.88 0 2.02.6 3.6 1.6 5.28l-.98 3.58 3.85-1.54zM17.4 14.3c-.07-.12-.27-.2-.56-.34-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.25-.46-2.38-1.47-.88-.78-1.47-1.75-1.65-2.05-.17-.3-.02-.46.13-.6.13-.14.3-.35.44-.53.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.21-.24-.58-.49-.5-.67-.5l-.57-.01c-.2 0-.52.07-.79.37-.27.3-1.04 1.01-1.04 2.47 0 1.46 1.06 2.87 1.21 3.07.15.2 2.1 3.2 5.08 4.48.71.31 1.26.49 1.69.62.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.42z"/></svg>
  </a>
'''
if 'id="waFloat"' not in s:
    s = s.replace('\n<script>\n  (function(){', float_html + '\n<script>\n  (function(){', 1)

# Ensure floating icon receives the same WhatsApp URL and exact prefilled message.
s = s.replace(
    '["waTop","waHero","waFinal","waFoot"].forEach',
    '["waTop","waHero","waFinal","waFoot","waFloat"].forEach'
)

p.write_text(s, encoding='utf-8')
