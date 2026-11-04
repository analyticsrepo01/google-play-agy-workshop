---
trigger: always_on
description: Global Google Play Store app quality, Backend TDD, Human Confirmation, UX, and security standards
---

# Google Play & Agentic TDD Standards (Global Export Ready)

1. **Global Market First (US / Tier-1 Export)**:
   - Use natural, concise English (`en-US`) as the primary UI language for global Tier-1 Google Play markets (US, UK, AU, EU).
   - Keep user-facing strings cleanly separated in a constants/i18n module so additional locales can be added effortlessly.

2. **Backend Test-Driven Development First (`RED -> GREEN`)**:
   - Write executable backend API & Gemini structured JSON schema tests (e.g., `tests/backend.test.js` covering health check, HTTP 400 empty/invalid input validation, HTTP 200 structured JSON contract, and secret scanning) **BEFORE** implementing backend application code.
   - Run the test suite first to confirm it fails (`RED`), then implement the backend and re-run until 100% of checks pass (`GREEN`).

3. **Human-in-the-Loop Use-Case Confirmation**:
   - After turning tests `GREEN`, execute an end-to-end backend use-case test using realistic domain input, display the pass/fail summary table alongside the actual returned structured JSON payload, and **explicitly ask the user to confirm** that the results match their expected use case before generating store listing artifacts.

4. **Mobile-First Material 3 UX & Play Security**:
   - Design responsive mobile portrait layouts (`390x844` standard viewport) with touch targets `>= 48px`, high-contrast styling, and 2–3 one-tap realistic sample inputs.
   - Default to `gemini-2.5-flash` with structured JSON outputs (`responseSchema` / `responseMimeType: "application/json"`). **Never hardcode API keys** in source or test files; read `GEMINI_API_KEY` from the environment or a runtime Settings modal, with a deterministic offline demo fallback.
