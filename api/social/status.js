const REQUIRED = [
  "META_APP_ID",
  "META_APP_SECRET",
  "SOCIAL_TOKEN_ENCRYPTION_KEY",
  "UPSTASH_REDIS_REST_URL",
  "UPSTASH_REDIS_REST_TOKEN"
];

module.exports = function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  const configured = Object.fromEntries(
    REQUIRED.map((key) => [key, Boolean(process.env[key])])
  );
  const missing = REQUIRED.filter((key) => !configured[key]);

  return res.status(200).json({
    ok: true,
    product: "Las Media Agency Social Publishing",
    providers: {
      facebook: { appConfigured: configured.META_APP_ID && configured.META_APP_SECRET },
      instagram: { appConfigured: configured.META_APP_ID && configured.META_APP_SECRET },
      x: { appConfigured: Boolean(process.env.X_CLIENT_ID && process.env.X_CLIENT_SECRET) }
    },
    storage: {
      encryptedTokenKeyConfigured: configured.SOCIAL_TOKEN_ENCRYPTION_KEY,
      persistentStoreConfigured: configured.UPSTASH_REDIS_REST_URL && configured.UPSTASH_REDIS_REST_TOKEN
    },
    missing,
    callbackUrls: {
      meta: "https://lasmediaagency.online/api/social/meta/callback",
      x: "https://lasmediaagency.online/api/social/x/callback"
    },
    note: "This endpoint reports configuration presence only. It never returns credentials or access tokens."
  });
};
