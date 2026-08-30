from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")

new_pricing = r'''  <!-- PRICING -->
  <section class="section price">
    <div class="wrap">
      <div class="eyebrow">Facebook &amp; Instagram Ad Packages</div>
      <h2>Apne business ke liye sahi plan chuniye</h2>
      <div class="plans">
        <div class="plan">
          <div class="pname">📌 Basic Ad Package</div>
          <div class="amt">₹2,000</div>
          <div class="bud">Ad Budget: ₹1,000 + Service Charge: ₹1,000</div>
          <ul>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>⏳ 5 Days</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>🎨 1 Professional Poster Design</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>⚙️ Complete Meta Ad Setup</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>✍️ Engaging Text &amp; Catchy Headline</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>📍 Local Area Audience Targeting</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>📲 Direct WhatsApp / Call Setup</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>📊 5 Days Active Management &amp; Performance Report</li>
          </ul>
          <a class="pick" data-plan="Basic Ad Package (₹2,000)" href="#">Start Basic Plan</a>
        </div>

        <div class="plan pop">
          <span class="badge">Most Popular</span>
          <div class="pname">🚀 Growth Ad Package</div>
          <div class="amt">₹5,000</div>
          <div class="bud">Ad Budget: ₹3,000 + Service Charge: ₹2,000</div>
          <ul>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>⏳ 15 Days</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>🎨 2 High-Converting Posters</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>🎯 In-depth Audience Research &amp; Setup</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>🧪 2 Creative Testing</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>📲 Direct WhatsApp &amp; Call Lead Generation</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>🛠️ Daily Monitoring &amp; Ad Optimization</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>📈 15 Days Complete Progress Report</li>
          </ul>
          <a class="pick" data-plan="Growth Ad Package (₹5,000)" href="#">Start Growth Plan</a>
        </div>

        <div class="plan">
          <div class="pname">⭐ Monthly Pro Package</div>
          <div class="amt">₹10,000</div>
          <div class="bud">Ad Budget: ₹6,000 + Service Charge: ₹4,000</div>
          <ul>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>⏳ 30 Days</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>🎨 3 Premium Posters / Creatives</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>🛠️ Advanced Meta Ads Setup &amp; Funnel Strategy</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>🧪 Multi-Creative &amp; Audience A/B Testing</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>🔍 Regular Optimization &amp; Weekly Checks</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>📊 Detailed Monthly Performance Report</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>💡 Next Month Strategy &amp; Scale-up Suggestions</li>
          </ul>
          <a class="pick" data-plan="Monthly Pro Package (₹10,000)" href="#">Start Monthly Pro</a>
        </div>
      </div>
      <p class="price-note"><b>Package price mein Meta Ad Budget + Ludhiana Ad Service management fee dono included hain.</b> ⚠️ Results aapke offer, location aur market response par depend karte hain.</p>
    </div>
  </section>
'''

pattern = re.compile(
    r'  <!-- PRICING -->\n  <section class="section price">.*?</section>\n(?=\n  <section class="section" style="padding-top:0">)',
    re.S,
)

updated, count = pattern.subn(new_pricing.rstrip("\n"), text, count=1)
if count != 1:
    raise SystemExit(f"Expected exactly one pricing section, found {count}. No file was changed.")

path.write_text(updated, encoding="utf-8")
print("Pricing section updated successfully; all other homepage content preserved.")
