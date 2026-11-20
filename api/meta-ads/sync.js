let latestAdsPayload = null;

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method === "GET") {
    if (!latestAdsPayload) {
      return res.status(200).json({
        ok: true,
        synced_at: null,
        portfolios_summary: [],
        ads_data: [],
      });
    }
    return res.status(200).json({ ok: true, ...latestAdsPayload });
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
