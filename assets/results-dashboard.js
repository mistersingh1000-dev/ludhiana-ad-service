(() => {
  'use strict';
  const mount = document.getElementById('crmPublicDashboard');
  if (!mount) return;
  const n = value => value == null ? '—' : Number(value).toLocaleString('en-IN', { maximumFractionDigits: 0 });
  const money = value => value == null ? '—' : '₹' + Number(value).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const leadType = row => ['Leads (Form)', 'Meta leads'].includes(row.type);
  const groupTotals = rows => {
    const groups = new Map();
    rows.forEach(row => {
      if (!groups.has(row.client)) groups.set(row.client, { name: row.client, spend: 0, campaigns: 0, types: new Map() });
      const group = groups.get(row.client);
      group.spend += row.spend || 0; group.campaigns++;
      if (row.results != null) group.types.set(row.type, (group.types.get(row.type) || 0) + row.results);
    });
    return [...groups.values()].sort((a, b) => b.spend - a.spend);
  };
  const bars = (items, formatter) => {
    const max = Math.max(1, ...items.map(item => item.value));
    return items.map(item => `<div class="result-bar"><div><span>${esc(item.label)}</span><b>${formatter(item.value)}</b></div><div class="result-track"><i style="width:${item.value / max * 100}%"></i></div></div>`).join('');
  };
  async function init() {
    mount.innerHTML = '<p class="result-loading" role="status">Loading campaign results…</p>';
    try {
      const response = await fetch('/assets/campaign-results.json?v=20261024');
      if (!response.ok) throw new Error('Results unavailable');
      const data = await response.json();
      const rows = data.campaigns;
      const leads = rows.filter(leadType);
      const leadCount = leads.reduce((sum, row) => sum + (row.results || 0), 0);
      const leadSpend = leads.reduce((sum, row) => sum + (row.spend || 0), 0);
      const costs = leads.filter(row => row.results > 0 && row.cost != null).map(row => row.cost);
      const conversations = rows.filter(row => row.type === 'Messaging conversations started').reduce((sum, row) => sum + (row.results || 0), 0);
      const totalSpend = rows.reduce((sum, row) => sum + (row.spend || 0), 0);
      const metrics = new Map();
      rows.forEach(row => { if (row.results != null) metrics.set(row.type, (metrics.get(row.type) || 0) + row.results); });
      const businesses = groupTotals(rows);
      const metricCards = [
        [n(data.clientProfiles), 'Client / business profiles', 'Grouped business labels; excludes our own agency'],
        [n(data.portfolios), 'Business portfolios', 'Plus 1 personal account'],
        [n(data.adAccounts), 'Ad accounts reviewed', `${data.accountsWithData} with campaign data · ${data.emptyAccounts} with no data`],
        [n(rows.length), 'Campaign records', 'Published campaigns with identified business labels'],
        [n(conversations), 'Messaging conversations', 'Reported conversations, not confirmed sales'],
        [n(leadCount), 'Form & Meta leads', 'Kept separate from messages and clicks'],
        [money(totalSpend), 'Total ad spend', 'Published campaign spend · INR'],
        [n(rows.reduce((sum, row) => sum + (row.impressions || 0), 0)), 'Ad impressions', 'Total impressions across campaigns']
      ];
      mount.innerHTML = `<div class="result-meta"><span class="result-dot"></span>Meta Ads Manager export <span>Updated ${esc(data.updated)}</span></div>
        <div class="result-kpis">${metricCards.map(([value, label, note]) => `<article class="result-kpi"><small>${label}</small><strong>${value}</strong><span>${note}</span></article>`).join('')}</div>
        <div class="lead-costs"><div><span class="result-label">COST PER LEAD</span><h3>What our lead campaigns delivered</h3><p>Campaign-level minimum and maximum. Average = lead campaign spend ÷ reported leads.</p></div><div><small>Minimum</small><b>${money(Math.min(...costs))}</b></div><div><small>Maximum</small><b>${money(Math.max(...costs))}</b></div><div class="lead-average"><small>Weighted average</small><b>${money(leadSpend / leadCount)}</b></div></div>
        <div class="result-charts"><article class="result-panel"><div class="result-panel-head"><div><span class="result-label">AD BUDGET IN ACTION</span><h3>Highest spend by business</h3></div><span>INR · descending</span></div>${bars(businesses.slice(0, 8).map(group => ({ label: group.name, value: group.spend })), money)}<p class="result-caption">Campaigns belonging to the same business are grouped together.</p></article>
        <article class="result-panel"><div class="result-panel-head"><div><span class="result-label">EVERY RESULT HAS A PURPOSE</span><h3>Explore result types</h3></div></div><div class="result-mix">${[...metrics.entries()].sort((a,b)=>b[1]-a[1]).map(([label,value])=>`<div><span>${esc(label)}</span><b>${n(value)}</b></div>`).join('')}</div><p class="result-caption">Different result types are shown separately. Reach can overlap between campaigns.</p></article></div>
        <div class="result-section-heading"><div><span class="result-label">BUSINESS PERFORMANCE</span><h3>Ad spend by client / business</h3></div><span>Largest spend first</span></div>
        <div class="result-business-grid">${businesses.map((group,index) => `<article class="result-business"><div><span class="result-rank">${String(index+1).padStart(2,'0')}</span><h4>${esc(group.name)}</h4></div><strong>${money(group.spend)}</strong><small>${n(group.campaigns)} campaign records${group.name === 'Ludhiana Ad Service' ? ' · own promotions' : ''}</small><dl>${[...group.types.entries()].sort((a,b)=>b[1]-a[1]).map(([label,value])=>`<div><dt>${esc(label)}</dt><dd>${n(value)}</dd></div>`).join('') || '<div><dt>No reported results</dt><dd>—</dd></div>'}</dl></article>`).join('')}</div>
        <div class="result-section-heading"><div><span class="result-label">THE COMPLETE PICTURE</span><h3>All ${n(rows.length)} campaigns</h3></div><a href="/results.html">Open full results page ↗</a></div>
        <div class="result-controls"><label>Search business or campaign<input id="result-search" type="search" placeholder="e.g. Lumecasa, immigration, leads"></label><label>Result type<select id="result-type"><option value="">All result types</option>${[...new Set(rows.map(row=>row.type))].sort().map(type=>`<option>${esc(type)}</option>`).join('')}</select></label><label>Sort by<select id="result-sort"><option value="spend">Ad spend: high to low</option><option value="results">Results: high to low</option><option value="cost">Cost per result: high to low</option></select></label></div>
        <p id="result-count" class="result-count" aria-live="polite"></p><div class="result-table-wrap"><table class="result-table"><caption class="sr-only">Historical campaign performance. Default order is ad spend descending.</caption><thead><tr><th>Business / campaign</th><th>Results</th><th>Cost / result</th><th>Ad spend</th><th>Reach</th><th>Impressions</th><th>Reporting dates</th></tr></thead><tbody id="result-rows"></tbody></table></div>
        <details class="result-method"><summary>How these figures are calculated</summary><p>Historical snapshot from Meta’s Maximum reporting preset, with exported dates preserved per campaign. Published campaigns and deleted campaigns with delivery data are included. 55 historical campaigns with unconfirmed client attribution are excluded from all published totals and graphs. Drafts are excluded by Meta. Six reviewed accounts returned no campaign data. Shared accounts are counted once.</p><p>Client / business profiles group identifiable account and campaign labels. They are not a verified count of unique paying customers. The agency’s own promotions remain in campaign and spend totals but are excluded from the client / business profile count.</p><p>Lead costs include form leads and Meta leads only. Messages, calls, visits, views, interactions and clicks have separate totals. Average lead cost uses spend only from lead-type campaigns. Zero or missing results have no valid cost per result. Awareness cost may be quoted per 1,000 people reached. Reach is shown per campaign and is not summed as unique people.</p><p>These are historical advertising outcomes, not guaranteed future results or confirmed sales. Account IDs, contact details and downloadable internal sheets are not published here.</p></details>
        <div class="result-cta"><div><h3>Your business could be next.</h3><p>Let’s plan a campaign around your offer, area and budget.</p></div><a href="https://wa.me/917009732517?text=Hi%2C%20I%20saw%20your%20campaign%20results.%20I%20want%20to%20discuss%20ads%20for%20my%20business.">Discuss my campaign ↗</a></div>`;
      const search = document.getElementById('result-search'), type = document.getElementById('result-type'), sort = document.getElementById('result-sort');
      function render() {
        const query = search.value.trim().toLowerCase();
        const filtered = rows.filter(row => (!type.value || row.type === type.value) && (!query || `${row.client} ${row.campaign}`.toLowerCase().includes(query))).sort((a,b)=>(b[sort.value] ?? -1)-(a[sort.value] ?? -1));
        document.getElementById('result-count').textContent = `${filtered.length} of ${rows.length} campaigns · ${sort.value === 'results' ? 'Compare results within the same result type.' : 'Highest values first.'}`;
        document.getElementById('result-rows').innerHTML = filtered.map(row=>`<tr><td><b>${esc(row.client)}</b><span>${esc(row.campaign)}</span></td><td><b>${n(row.results)}</b><span>${esc(row.type)}</span></td><td>${money(row.cost)}${row.type === 'Reach' ? '<span>Per 1,000 people</span>' : ''}</td><td><b>${money(row.spend)}</b></td><td>${n(row.reach)}</td><td>${n(row.impressions)}</td><td><span>${esc(row.start)}<br>to ${esc(row.end)}</span></td></tr>`).join('') || '<tr><td colspan="7">No campaigns match your search.</td></tr>';
      }
      [search,type,sort].forEach(control=>control.addEventListener('input',render));render();
    } catch(error) { mount.innerHTML = '<p role="alert">Campaign results could not load. Please refresh the page or contact us on WhatsApp.</p>'; }
  }
  init();
})();
