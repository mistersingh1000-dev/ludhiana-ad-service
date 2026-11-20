const SHEET_ID = "1BU8lQ-N3owo_xHXSvh-bOwEOiVjq3Sz1fxvTOU3N7uE";
let latestAdsPayload = null;

async function fetchSheetTab(tabName) {
  const url = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=out:json&sheet=${encodeURIComponent(tabName)}`;
  const resp = await fetch(url, { cache: "no-store" });
  if (!resp.ok) throw new Error(`Sheet fetch failed: ${resp.status}`);
  const text = await resp.text();
  const match = text.match(/google\.visualization\.Query\.setResponse\(([\s\S]+)\);?/);
  if (!match) return [];
  const json = JSON.parse(match[1]);
  const cols = (json.table?.cols || []).map((c, i) => (c.label || c.id || `col_${i}`).trim());
  const rows = json.table?.rows || [];
  return rows
    .map((r) => {
      const obj = {};
      (r.c || []).forEach((cell, idx) => {
        const key = cols[idx] || `col_${idx}`;
        obj[key] = cell ? (cell.f !== undefined && cell.f !== null ? cell.f : cell.v ?? "") : "";
      });
      return obj;
    })
    .filter((obj) => Object.values(obj).some((v) => String(v).trim() !== ""));
}

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

  if (req.method === "OPTIONS") return res.status(200).end();

  if (req.method === "GET") {
    try {
      const [summaryRows, rawRows] = await Promise.all([
        fetchSheetTab("Client_Summary").catch(() => []),
        fetchSheetTab("Raw_Ads_Data").catch(() => []),
      ]);
      const filteredSummary = summaryRows.filter(
        (r) => String(r.Portfolio_ID || "").toLowerCase() !== "grand total"
      );
      if (filteredSummary.length > 0 || rawRows.length > 0) {
        return res.status(200).json({
          ok: true,
          source: "google_sheet_live",
          synced_at: new Date().toISOString(),
          portfolios_summary: filteredSummary,
          ads_data: rawRows,
        });
      }
    } catch (e) {}

    if (latestAdsPayload) {
      return res.status(200).json({ ok: true, ...latestAdsPayload });
    }
    return res.status(200).json({
      ok: true,
      source: "empty",
      synced_at: null,
      portfolios_summary: [],
      ads_data: [],
    });
  }

  if (req.method === "POST") {
    const expectedKey = process.env.META_SYNC_API_KEY;
    const authHeader = req.headers.authorization || "";
    const token = authHeader.startsWith("Bearer ") ? authHeader.slice(7).trim() : "";

    if (!expectedKey || token !== expectedKey) {
      return res.status(401).json({ ok: false, error: "Unauthorized: Invalid or missing API key" });
    }

    const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body || {};
    if (!Array.isArray(body.ads_data)) {
      return res.status(400).json({ ok: false, error: "Invalid payload: ads_data array is required" });
    }

    latestAdsPayload = {
      source: String(body.source || "meta_ads_sync"),
      synced_at: String(body.synced_at || new Date().toISOString()),
      portfolios_summary: Array.isArray(body.portfolios_summary) ? body.portfolios_summary : [],
      ads_data: body.ads_data,
    };

    return res.status(200).json({
      ok: true,
      received_portfolios: latestAdsPayload.portfolios_summary.length,
      received_ads: latestAdsPayload.ads_data.length,
      synced_at: latestAdsPayload.synced_at,
    });
  }

  return res.status(405).json({ ok: false, error: "Method not allowed" });
}
