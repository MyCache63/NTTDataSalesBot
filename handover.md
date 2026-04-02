# NTT DATA Sales Bot — Handover

**Last updated:** 2026-04-02 14:00 PT

---

## Current State

### What's Working
- **HTML Chatbot POC (v1.3)** is live and functional at:
  - GitHub Pages: https://mycache63.github.io/NTTDataSalesBot/
  - Local file: `ntt_data_salesbot_poc.html` (has API key baked in for demos)
- Chatbot uses **Claude Haiku 4.5** via Anthropic API with full NTT DATA Cloud Services knowledge base embedded as system prompt
- Features: 3-mode responses (Brief/Moderate/Verbose), conversation history sidebar, Discovery Questions toggle, Show Sources toggle, real PNG logos (NTT DATA + Kore.ai)
- API key is baked into both `index.html` (GitHub) and local file — works without prompting
- **Demo to Shreeshan completed April 2** — he liked it, confirmed direction

### Documents Created
- `OneNTTData_SalesBot_Requirements_v03_April2026.docx` — **Latest.** Updated after Apr 2 demo. Confirmed decisions, new requirements (voice, digital assistant, demo catalog, Hot Spot), reduced open questions.
- `OneNTTData_SalesBot_Requirements_v02_April2026.docx` — Prior version (requirements only)
- `OneNTTData_SalesBot_RequirementsAndDesign_v01_April2026.docx` — Original v01 with full design/architecture (kept for reference)
- `NTT_DATA_Cloud_Services_Knowledge_Base.md` — All crawled NTT DATA product data
- `NTTDATA - Sales Bot Discovery - 20260401.txt` — April 1 discovery call transcript
- `NTT Data - Sales Bot Requirements.txt` — April 2 demo/discovery call transcript
- `follow_up_email_apr2.txt` — Follow-up email to Shreeshan (ready to send)

### Build Status
- No build system — it's a single HTML file, opens in any browser
- GitHub repo: https://github.com/MyCache63/NTTDataSalesBot (public, for GitHub Pages)
- GitHub Pages deployed from `main` branch

---

## What Happened in the April 2 Demo

Shreeshan saw the chatbot POC and confirmed the direction. Key takeaways:

1. **Virtual Teammate Model** — The bot should join Teams calls as a participant. It listens, presents slides on command, answers Q&A from Confluence/docs, and logs questions it can't answer.

2. **Demo Catalog** — Shreeshan wants a configurable catalog of demos by product/practice (One NTT Platform, NTT Composable, NTT Flash, Cloud, FinOps). Growing library over time.

3. **Digital Assistant** — Beyond formal demos, the bot is a 24/7 assistant for quick product questions. Replaces the pattern of reps coming to Shreeshan for answers.

4. **Voice is critical** — Both voice input (ask questions by voice) and voice output (narrate slides). But voice responses should be concise — for long answers, send a doc instead.

5. **Data sources confirmed** — Confluence (technical docs), Hot Spot portal (pre-sales support, NOT HubSpot), Salesforce (CRM), PPT decks + scripts.

6. **Volume** — 200+ users, ~10 sessions each/month = 2,000+ sessions/month.

7. **Gradius builds it** — Kore.ai vendor, already onboarded by NTT DATA, ex-Kore employees. Handles MetLife and other Kore platform work for NTT DATA.

8. **Internal use confirmed** — Presentations go to external customers, but the tool is internal.

9. **Continuous improvement loop** — Bot logs unanswered questions → human updates Confluence → bot syncs daily → bot can now answer those questions.

---

## Key People

| Name | Role | Org |
|------|------|-----|
| Shreeshan Rangayan | Project Lead | NTT DATA |
| Wiley Oliver | Executive Sponsor | NTT DATA |
| Gradius | Implementation Partner | Kore.ai vendor |
| Mike Ashe | Account Lead | Kore.ai |
| Michael Dsousa | Relationship Manager | Kore.ai |
| Deepak Anand | Solutions Architect | Kore.ai |

---

## Next Steps

1. **Send follow-up email to Shreeshan** — `follow_up_email_apr2.txt` is ready. Attach `OneNTTData_SalesBot_Requirements_v03_April2026.docx`.
2. **Wait for sample data from Shreeshan** — 20-30 PPTs + associated docs from Cloud Services Group. This is the main blocker.
3. **Resolve remaining open questions** — Pricing model, security/compliance, Confluence scope, Teams deployment, Hot Spot integration details (see Section 8 of v03 doc).
4. **When data arrives:** Build next POC iteration with real slide content, slide recommendation, and script generation.
5. **Future:** Scope proper build on Kore.ai platform with Gradius — RAG, Teams integration, voice, Hot Spot integration.

---

## Open Issues

- **SecOps opportunity is dead** — Shreeshan doesn't have bandwidth to chase it
- **Gupreet is out sick** — no SE backup currently up to speed
- **$3.5M budget** — exists but pricing model for this project TBD
- **Gradius relationship** — Mike doesn't know them yet; Michael Dsousa does (they're ex-Kore)

---

## File Inventory

```
NTT_Data_SalesBot/
├── .gitignore
├── CLAUDE.md
├── handover.md                          ← this file
├── index.html                           ← GitHub Pages version (API key baked in)
├── ntt_data_salesbot_poc.html           ← Local demo (key baked in, gitignored)
├── Kore.ai_Logo (1).png                ← Kore.ai logo
├── NTTDAtaLogo.png                      ← NTT DATA logo
├── NTT_DATA_Cloud_Services_Knowledge_Base.md
├── NTTDATA - Sales Bot Discovery - 20260401.txt     ← Apr 1 transcript
├── NTT Data - Sales Bot Requirements.txt            ← Apr 2 transcript
├── OneNTTData_SalesBot_Requirements_v03_April2026.docx  ← LATEST
├── OneNTTData_SalesBot_Requirements_v02_April2026.docx
├── OneNTTData_SalesBot_RequirementsAndDesign_v01_April2026.docx
├── follow_up_email_apr2.txt             ← Ready to send
├── generate_requirements_doc.py         ← Script that built v01
├── generate_requirements_v02.py         ← Script that built v02
└── generate_requirements_v03.py         ← Script that built v03
```
