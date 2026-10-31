# TruffleHog Extension (optional)

Supporting material for **Extension 1** in the worksheet, the extension task on
*detection vs verification*.

`leaked-config.env` contains a credential in a **real Stripe key format** but it is **fake and dead**
— safe to scan, useless to an attacker. Students scan this folder with TruffleHog 3.99.7 to see it
**detected but unverified** (TruffleHog sends it to Stripe's API, which rejects it), then re-run with
`--results=verified` to watch it filtered out. The VM needs internet access for the verification
step; without it the result is reported as unknown.

This folder is deliberately kept **outside** `vulnerable-api/`, so it never affects the gitleaks
counts in Tasks 1 and 5. Distribute it to students only if you are running the extension.
