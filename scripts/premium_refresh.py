from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove a previous premium override if this script is ever re-run.
s = re.sub(r'\n?<style id="las-premium-v2">.*?</style>\n?', '\n', s, flags=re.S)
s = re.sub(r'\n?<!-- LAS FLOATING WHATSAPP START -->.*?<!-- LAS FLOATING WHATSAPP END -->\n?', '\n', s, flags=re.S)

repls = {
    '<title>Ludhiana ke Business ke liye Ads — Free Demo</title>': '<title>Ludhiana Ad Service — Facebook & Instagram Ads for Local Businesses</title>',
    'content="Ludhiana ke local businesses ke liye Facebook & Instagram ads. Seedhe aapke area ke customers — leads, calls aur messages. Free demo ke liye WhatsApp karein."': 'content="Ludhiana ke local businesses ke liye professional Facebook & Instagram advertising, local targeting, creatives, campaign management and lead generation. Check our plans and pricing."',
    'content="Ludhiana ke Business ke liye Ads — Free Demo"': 'content="Ludhiana Ad Service — Professional Facebook & Instagram Ads"',
    'content="Aapke area ke customers seedhe aapke WhatsApp par. Facebook & Instagram ads — pehle free demo, phir baat."': 'content="Professional Facebook & Instagram ads for local businesses. Check our packages, pricing and campaign management plans."',
    'const PREFILL_MSG     = "Hi, mujhe aapka number ad se mila. Mujhe apne business ke liye free demo ke baare mein jaanna hai.";': 'const PREFILL_MSG     = "Hi, I got your number from your website. May I know your plans?";',
    '<span>Free Demo</span>': '<span>Check Pricing</span>',
    'FREE Demo ke liye message karein': 'Check Plans & Pricing',
    'Koi advance fees nahi · pehle result, phir baat': 'Transparent plans · Ad budget + service included',
    '<div class="step"><div class="num">02</div><h3>Free demo</h3><p>Main aapke liye ek demo ad plan banata hoon — bilkul free, bina charge ke.</p></div>': '<div class="step"><div class="num">02</div><h3>Plan choose karein</h3><p>Basic, Growth ya Monthly Pro plan mein se apne goal aur budget ke hisaab se package select karein.</p></div>',
    '<div class="step"><div class="num">03</div><h3>Results dekhein</h3><p>Leads aana shuru. Pasand aaye to monthly saath chalte hain.</p></div>': '<div class="step"><div class="num">03</div><h3>Campaign launch</h3><p>Creative, targeting, setup aur management main sambhalta hoon — enquiries seedhe aapke WhatsApp ya phone par aati hain.</p></div>',
    '<!-- DEMO DETAILS -->': '<!-- PLAN DETAILS -->',
    '<div class="eyebrow">Free demo mein kya milega</div>': '<div class="eyebrow">Professional Ad Service</div>',
    '<h2>7 din ka live demo — meri service bilkul free</h2>': '<h2>Plan ke saath complete ad setup aur management</h2>',
    '<p class="lead">Demo mein main apni fees nahi leta. Aap sirf ek chhota ad budget lagate ho jo seedha Facebook ko jaata hai — aur apni aankhon se result dekhte ho.</p>': '<p class="lead">Aapke selected package ke hisaab se creative, targeting, campaign setup, monitoring aur reporting professionally manage ki jaati hai.</p>',
    '<div class="check"><span class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg></span><div><h3>7 din ka live campaign</h3><p>Aapke business ke liye chalta hua asli ad.</p></div></div>': '<div class="check"><span class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg></span><div><h3>Live Meta campaign</h3><p>Selected package duration ke hisaab se Facebook & Instagram promotion.</p></div></div>',
    '<div class="check"><span class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg></span><div><h3>Main roz manage karta hoon</h3><p>Aap sirf apna kaam dekho, ads meri zimmedari.</p></div></div>': '<div class="check"><span class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg></span><div><h3>Active campaign management</h3><p>Monitoring aur optimization selected plan ke hisaab se manage ki jaati hai.</p></div></div>',
    '<div class="check"><span class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg></span><div><h3>End mein honest report</h3><p>Kitne leads, kitni reach, per-lead cost — saaf-saaf.</p></div></div>': '<div class="check"><span class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg></span><div><h3>Performance reporting</h3><p>Reach, enquiries aur campaign performance ka clear summary.</p></div></div>',
    '<div class="check"><span class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg></span><div><h3>Ad budget (~₹999–1499 for 7 days)</h3><p>Ye seedha Facebook ko jaata hai. Demo plan mein hamari fees zero.</p></div></div>': '<div class="check"><span class="tick"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg></span><div><h3>Apna package select karein</h3><p>₹2,000 Basic, ₹5,000 Growth ya ₹10,000 Monthly Pro — ad budget aur service charge clearly shown hain.</p></div></div>',
    'Pehle demo, phir aap decide karein.': 'Plans aur pricing check karein, phir apne business ke liye sahi package choose karein.',
    '<!-- DEMO MINI-FORM -->': '<!-- PLAN ENQUIRY FORM -->',
    '<div class="eyebrow">Free demo shuru karein</div>': '<div class="eyebrow">Plan enquiry</div>',
    '<h2>2 minute mein apni details bhejo</h2>': '<h2>Apne business ki details bhejein</h2>',
    '<p class="lead">Neeche bharo aur "WhatsApp par bhejo" dabao — aapki details ke saath meri chat khul jaayegi. Main aate hi aapka demo plan bhej dunga.</p>': '<p class="lead">Neeche details bharein aur WhatsApp par bhejein. Main aapke business ke liye suitable package recommend kar dunga.</p>',
    '<div class="hint">Koi advance fees nahi · pehle demo, phir baat</div>': '<div class="hint">Transparent pricing · apne budget ke hisaab se plan choose karein</div>',
    '<div class="qa"><button type="button">Demo sach mein free hai? <span class="plus"></span></button><div class="ans"><p>Haan. Demo mein meri service ki fees zero hai. Aap sirf ek chhota ad budget (~₹999–1499) lagate ho jo seedha Facebook ko jaata hai — aur woh bhi aapke control mein rehta hai.</p></div></div>': '<div class="qa"><button type="button">Mere business ke liye kaunsa plan sahi hai? <span class="plus"></span></button><div class="ans"><p>Testing ke liye Basic, serious lead generation ke liye Growth aur regular monthly promotion ke liye Monthly Pro plan choose kar sakte hain. Business type aur goal ke hisaab se main suitable option recommend karunga.</p></div></div>',
    '<div class="qa"><button type="button">Result kitne din mein aata hai? <span class="plus"></span></button><div class="ans"><p>Aksar 7 din ke demo mein hi messages aane lagte hain. Par marketing time leti hai — main jhoothe "raton-raat" vaade nahi karta. Har cheez ki honest reporting dunga, phir aap decide karein.</p></div></div>': '<div class="qa"><button type="button">Result kitne din mein aata hai? <span class="plus"></span></button><div class="ans"><p>Results business, offer, competition, location aur budget par depend karte hain. Main campaign ko professionally setup, monitor aur optimize karta hoon, lekin guaranteed result ka jhootha promise nahi karta.</p></div></div>',
    '<p>Free demo ke liye abhi message karein — sirf kuch businesses ke liye time hai.</p>': '<p>Apne business ke liye packages aur pricing check karein — aur suitable plan ke liye WhatsApp par baat karein.</p>',
    'FREE Demo — WhatsApp karein': 'WhatsApp — Check Plans',
    'var m = "Hi, mujhe " + plan + " plan ke baare mein jaanna hai. Free demo se shuru karna hai.";': 'var m = "Hi, I got your number from your website. I want to know more about " + plan + ".";',
    'var msg = "Hi, mujhe apne business ke liye FREE demo chahiye.\\n"': 'var msg = "Hi, I got your number from your website. May I know your plans?\\n"'
}
for a, b in repls.items():
    s = s.replace(a, b)

# Clean any remaining user-visible Free Demo wording that may survive capitalization variants.
s = re.sub(r'FREE\s+Demo', 'Check Pricing', s, flags=re.I)
s = re.sub(r'Free\s+demo', 'Check Pricing', s, flags=re.I)

premium_css = r'''
<style id="las-premium-v2">
:root{
  --ink:#071426;--ink-2:#0d1f3c;--paper:#f6f8fc;--paper-2:#eef3fb;
  --amber:#ffb000;--amber-deep:#ff7a00;--wa:#20c566;--wa-dark:#11994b;
  --text:#15213a;--muted:#667085;--line:#dbe3ef;
  --blue:#2878ff;--violet:#7657ff;--pink:#ff3d8d;
}
body{background:linear-gradient(180deg,#f8fbff 0%,#f6f8fc 100%);color:var(--text);overflow-x:hidden}
.bar{background:rgba(7,20,38,.88);border-bottom:1px solid rgba(255,255,255,.10);box-shadow:0 8px 30px rgba(0,0,0,.12)}
.brand{font-size:19px}.brand .dot{background:linear-gradient(135deg,var(--amber),var(--pink));box-shadow:0 0 0 5px rgba(255,176,0,.16)}
.cta-sm{background:linear-gradient(135deg,var(--blue),var(--violet));box-shadow:0 8px 22px rgba(40,120,255,.26)}
.cta-sm:hover{background:linear-gradient(135deg,#1768ee,#6745ef)}
.hero{background:radial-gradient(900px 480px at 80% -10%,rgba(118,87,255,.45),transparent 60%),radial-gradient(650px 440px at -10% 100%,rgba(32,197,102,.26),transparent 60%),linear-gradient(135deg,#061225 0%,#0b1d39 55%,#121d49 100%);padding-top:72px}
.tag{color:#ffe5a3;background:rgba(255,176,0,.10);border-color:rgba(255,176,0,.40);box-shadow:inset 0 0 24px rgba(255,176,0,.05)}
.hero h1{font-size:clamp(34px,5.7vw,58px);max-width:15ch;text-shadow:0 10px 35px rgba(0,0,0,.25)}
.hero .sub{font-size:clamp(16px,2.1vw,19px);line-height:1.72;color:#c9d5e8}.hero .sub b{color:#fff}
.btn-wa{background:linear-gradient(135deg,#20c566,#13a957);box-shadow:0 14px 34px rgba(32,197,102,.28);border:1px solid rgba(255,255,255,.16)}
.btn-wa:hover{background:linear-gradient(135deg,#24d46f,#11994b);transform:translateY(-3px)}
.phone{filter:drop-shadow(0 35px 65px rgba(0,0,0,.52))}.float-card{border:1px solid rgba(255,255,255,.6);box-shadow:0 20px 45px rgba(0,0,0,.28)}
.section{padding:76px 0}.section h2{font-size:clamp(27px,4.8vw,40px);max-width:22ch}.lead{line-height:1.72}
.eyebrow{background:linear-gradient(90deg,var(--blue),var(--violet),var(--pink));-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:800}
.pain,.svc-grid,.results-grid,.testimonial-grid,.plans,.steps{gap:20px}
.pain .item,.card,.quote-card,.check,.plan,.honest,.qa{border:1px solid rgba(140,160,190,.23);box-shadow:0 16px 42px rgba(26,43,74,.08);background:rgba(255,255,255,.92);backdrop-filter:blur(8px)}
.pain .item,.card,.check,.quote-card,.plan,.honest,.qa{transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease}
.pain .item:hover,.card:hover,.check:hover,.quote-card:hover,.plan:hover{transform:translateY(-4px);box-shadow:0 22px 50px rgba(26,43,74,.13);border-color:rgba(40,120,255,.28)}
.svc,.price{background:radial-gradient(700px 300px at 10% 0%,rgba(40,120,255,.08),transparent 65%),radial-gradient(650px 300px at 95% 100%,rgba(255,61,141,.07),transparent 65%),var(--paper-2)}
.card .ic{background:linear-gradient(135deg,rgba(40,120,255,.14),rgba(118,87,255,.14));border:1px solid rgba(40,120,255,.14)}
.card .ic svg{color:var(--blue)}
.result-card .stat{background:linear-gradient(90deg,var(--amber-deep),var(--pink));-webkit-background-clip:text;background-clip:text;color:transparent}
.step{background:linear-gradient(145deg,#0a1830,#14284b);box-shadow:0 18px 44px rgba(7,20,38,.18);border:1px solid rgba(255,255,255,.07)}
.step .num{-webkit-text-stroke:1.5px rgba(255,176,0,.7)}
.plan{border-radius:22px;padding:30px 24px;position:relative;overflow:hidden}
.plan::before{content:"";position:absolute;inset:0 0 auto 0;height:4px;background:linear-gradient(90deg,var(--blue),var(--violet),var(--pink));opacity:.82}
.plan.pop{border:2px solid rgba(255,176,0,.85);box-shadow:0 24px 60px rgba(255,122,0,.18);transform:translateY(-8px)}
.plan.pop::before{height:5px;background:linear-gradient(90deg,var(--amber),var(--pink))}.plan .badge{background:linear-gradient(90deg,var(--amber),#ffd058)}
.plan .amt{font-size:38px}.plan .bud{background:#f2f6ff;border:1px solid #dce7ff;border-radius:10px;padding:8px 10px;color:#34518b}
.plan .pick{background:linear-gradient(135deg,var(--ink),#183a69);padding:14px;border-radius:13px}.plan.pop .pick{background:linear-gradient(135deg,var(--wa),#12a453)}
.form-sec{background:radial-gradient(650px 300px at 90% 10%,rgba(118,87,255,.28),transparent 65%),linear-gradient(135deg,#071426,#10264a)}
.lead-form input,.lead-form select{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.18)}
.lead-form .send{background:linear-gradient(135deg,var(--wa),#11a653)}
.final{background:radial-gradient(700px 380px at 100% 0%,rgba(118,87,255,.38),transparent 60%),radial-gradient(600px 350px at 0% 100%,rgba(32,197,102,.24),transparent 60%),linear-gradient(135deg,#061225,#10264a)}
footer{background:#061225}
.sticky-cta{display:none!important}
.wa-float{position:fixed;right:22px;bottom:22px;z-index:100;width:62px;height:62px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(135deg,#25d366,#13a954);color:#fff;text-decoration:none;box-shadow:0 18px 42px rgba(18,166,84,.42),0 0 0 6px rgba(37,211,102,.12);transition:transform .2s ease,box-shadow .2s ease;animation:waPulse 2.4s ease-in-out infinite}
.wa-float:hover{transform:translateY(-4px) scale(1.04);box-shadow:0 22px 48px rgba(18,166,84,.5),0 0 0 8px rgba(37,211,102,.11)}
.wa-float svg{width:31px;height:31px}.wa-float .tip{position:absolute;right:72px;white-space:nowrap;background:#071426;color:#fff;font-size:12px;font-weight:700;padding:8px 11px;border-radius:9px;opacity:0;transform:translateX(6px);pointer-events:none;transition:.2s;box-shadow:0 10px 25px rgba(0,0,0,.18)}
.wa-float:hover .tip{opacity:1;transform:none}@keyframes waPulse{0%,100%{box-shadow:0 18px 42px rgba(18,166,84,.42),0 0 0 5px rgba(37,211,102,.11)}50%{box-shadow:0 18px 42px rgba(18,166,84,.42),0 0 0 11px rgba(37,211,102,.03)}}
@media(max-width:820px){.hero{padding-top:52px}.section{padding:62px 0}.plan.pop{transform:none}.wa-float{right:16px;bottom:16px;width:58px;height:58px}.wa-float .tip{display:none}}
@media(max-width:560px){.wrap{padding-left:18px;padding-right:18px}.hero h1{font-size:36px}.section h2{font-size:30px}.plan{padding:26px 20px}.testimonial-grid{grid-template-columns:1fr}.quote-card{padding:24px 21px}.honest{padding:22px}.wa-float{width:56px;height:56px}}
@media(prefers-reduced-motion:reduce){.wa-float{animation:none}}
</style>
'''
s = s.replace('</head>', premium_css + '\n</head>', 1)

wa_button = r'''
<!-- LAS FLOATING WHATSAPP START -->
<a class="wa-float" href="https://wa.me/917009732517?text=Hi%2C%20I%20got%20your%20number%20from%20your%20website.%20May%20I%20know%20your%20plans%3F" target="_blank" rel="noopener" aria-label="WhatsApp Ludhiana Ad Service">
  <span class="tip">Chat on WhatsApp</span>
  <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M.06 24l1.68-6.13A11.9 11.9 0 0 1 .16 11.9C.16 5.33 5.5 0 12.06 0a11.8 11.8 0 0 1 8.4 3.49 11.8 11.8 0 0 1 3.48 8.41c0 6.56-5.34 11.9-11.9 11.9a11.9 11.9 0 0 1-5.7-1.45L.06 24zm6.6-3.8c1.7.99 3.3 1.58 5.4 1.58 5.44 0 9.87-4.43 9.88-9.88a9.8 9.8 0 0 0-2.9-6.99A9.8 9.8 0 0 0 12.07 2c-5.45 0-9.88 4.43-9.88 9.88 0 2.02.6 3.6 1.6 5.28l-.98 3.58 3.85-1.54zM17.4 14.3c-.07-.12-.27-.2-.56-.34-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.25-.46-2.38-1.47-.88-.78-1.47-1.75-1.65-2.05-.17-.3-.02-.46.13-.6.13-.14.3-.35.44-.53.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.21-.24-.58-.49-.5-.67-.5l-.57-.01c-.2 0-.52.07-.79.37-.27.3-1.04 1.01-1.04 2.47 0 1.46 1.06 2.87 1.21 3.07.15.2 2.1 3.2 5.08 4.48.71.31 1.26.49 1.69.62.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.42z"/></svg>
</a>
<!-- LAS FLOATING WHATSAPP END -->
'''
s = s.replace('</body>', wa_button + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('Premium homepage refresh applied successfully.')
