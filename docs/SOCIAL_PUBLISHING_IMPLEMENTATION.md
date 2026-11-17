# Las Media Agency — Social Publishing Integration

Target application: `las-media-agency` Vercel project  
Repository: `mistersingh1000-dev/ludhiana-ad-service`  
Working branch: `feature/social-publishing-las-media`  
CRM route: `/crm/social-media.html`

## Current implementation facts

- The Social Media dashboard is a static HTML page.
- The current CRM sign-in and records use browser-side JavaScript/localStorage; this is not a trusted server-side identity system.
- This Vercel project currently has no configured environment variables for social publishing.
- Do not enable publishing or persist customer credentials until authenticated server-side user identity and per-client authorization exist.
- Never put provider app secrets, access tokens, encryption keys, or Redis credentials in browser JavaScript.

## Required server-side environment variables

| Variable | Purpose |
|---|---|
| `META_APP_ID` | Meta application ID |
| `META_APP_SECRET` | Meta app secret |
| `SOCIAL_TOKEN_ENCRYPTION_KEY` | 32-byte key for encrypting provider tokens at rest |
| `UPSTASH_REDIS_REST_URL` | Persistent token/state store URL |
| `UPSTASH_REDIS_REST_TOKEN` | Persistent token/state store credential |
| `X_CLIENT_ID` | X OAuth 2.0 client ID |
| `X_CLIENT_SECRET` | X OAuth 2.0 client secret |

Set secrets in Vercel Environment Variables, never in GitHub source or chat. Configure Preview first; promote to Production only after tests and approval.

## OAuth callback URLs

- Meta: `https://lasmediaagency.online/api/social/meta/callback`
- X: `https://lasmediaagency.online/api/social/x/callback`

These are proposed callback URLs and must be added to the corresponding developer consoles after the routes are implemented.

## Configuration health endpoint

`GET /api/social/status` reports whether required server-side settings exist. It reveals booleans and missing variable names only, never secret values. It is not an account connection test.

## Safe implementation order

1. Establish trusted server-side CRM sessions and admin/client workspace authorization.
2. Add OAuth state/PKCE, callback validation, token exchange, encrypted persistent token storage, revocation and disconnect.
3. Implement Meta Page discovery, Facebook publishing and Instagram Business publishing.
4. Implement X OAuth and publishing according to the selected X API access tier.
5. Add draft/schedule queue, idempotency, audit log, retries and per-client permissions.
6. Test using a dedicated test Page/account in Preview; only then request owner approval for Production.

## Important

The current frontend's localStorage demo login is not sufficient to protect publishing credentials or isolate clients. Do not bypass this by accepting a client ID from a browser request. No real provider connection should be advertised as connected until OAuth completes and a server-side test succeeds.
