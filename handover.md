# NTT DATA Sales Bot — Handover

**Last updated:** 2026-04-18 06:15 PT

---

## Current State

### Sentiment Analytics Demo (NEW — for Monday 4/20 call)

**Demo is fully functional and ready for Monday's call with Shreeshan/Arun.**

A Flask web app that:
1. Displays 100 fictitious Trinity Health IT service tickets in a ServiceNow-style interface
2. Runs AI-powered sentiment analysis on each ticket via Claude API (Sonnet 4.6)
3. Shows per-ticket sentiment scores, frustration targeting, key phrases, and reasoning
4. Provides an executive dashboard with XLA scores, charts, and department-level alerts

#### How to Run
```bash
cd /Users/michaelashe/Documents/NTT_Data_SalesBot
./start_sentiment_demo.sh
```
Opens at http://localhost:5001. API key is in `.env` file (not committed to git).

#### Analysis Results (Pre-cached — loads instantly)
- 100 tickets analyzed, 0 errors
- Sentiments: 44 neutral, 32 negative, 24 positive
- Frustration targets: 58 none, 25 problem itself, 17 both

#### Demo Flow for Monday
1. Open http://localhost:5001 — ServiceNow incident list with all sentiment data
2. Click a negative ticket (e.g., INC0091001 VPN drops) — show Kore.ai analysis panel
3. Show frustration target: "Both" — user frustrated with VPN AND IT response time
4. Click "Sentiment Dashboard" in sidebar — charts, XLA score, department breakdown
5. Point out alerts for departments with high negative sentiment
6. Pitch: "This replaces Foresight ($142K) at a fraction of the cost"

#### Business Context
- NTT DATA's current tool "Foresight" costs $142K ($71K + $71K/yr)
- Kore.ai needs to demo cheaper/better sentiment analytics
- If successful with Trinity Health, rolls out across all NTT accounts
- Key differentiator: frustration TARGET analysis (problem vs. service provider)
- XLA (Experience Level Agreements) framing — measuring user happiness, not just SLAs

### Original Sales Bot Chatbot POC (v1.3)
- **HTML Chatbot POC (v1.3)** is live and functional at:
  - GitHub Pages: https://mycache63.github.io/NTTDataSalesBot/
  - Local file: `ntt_data_salesbot_poc.html` (has API key baked in for demos)
- Chatbot uses **Claude Haiku 4.5** via Anthropic API with full NTT DATA Cloud Services knowledge base embedded as system prompt
- Features: 3-mode responses (Brief/Moderate/Verbose), conversation history sidebar, Discovery Questions toggle, Show Sources toggle, real PNG logos (NTT DATA + Kore.ai)
- API key is baked into both `index.html` (GitHub) and local file — works without prompting
- **Demo to Shreeshan completed April 2** — he liked it, confirmed direction

### Documents Created
- `OneNTTData_SalesBot_Requirements_v03_April2026.docx` — **Latest.** Updated after Apr 2 demo.
- `OneNTTData_SalesBot_Requirements_v02_April2026.docx` — Prior version (requirements only)
- `OneNTTData_SalesBot_RequirementsAndDesign_v01_April2026.docx` — Original v01 with design
- `NTT_DATA_Cloud_Services_Knowledge_Base.md` — All crawled NTT DATA product data
- `NTTDATA - Sales Bot Discovery - 20260401.txt` — April 1 discovery call transcript
- `NTT Data - Sales Bot Requirements.txt` — April 2 demo/discovery call transcript
- `follow_up_email_apr2.txt` — Follow-up email to Shreeshan (ready to send)

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
| Arun Mishra | Network-Technical Solutions Architect | NTT DATA |
| Radhika Menon | (cc'd on emails) | NTT DATA |
| Wiley Oliver | Executive Sponsor | NTT DATA |
| Gradius | Implementation Partner | Kore.ai vendor |
| Mike Ashe | Account Lead | Kore.ai |
| Michael Dsousa | Relationship Manager | Kore.ai |
| Deepak Anand | Solutions Architect | Kore.ai |
| Madhu Gilada | India Partner | Gradious (Kore partner) |

---

## Key Decisions Made

1. **Sentiment demo approach:** Python Flask + HTML, Claude API for analysis
2. **Model:** Claude Sonnet 4.6 — best quality/speed for nuanced sentiment reasoning
3. **Frustration targeting:** Key differentiator vs. Foresight — we distinguish problem vs. service provider frustration
4. **Pre-cached results:** Analysis runs once and caches to JSON — demo loads instantly
5. **Original chatbot:** Giant prompt with embedded data (not RAG) — simplest path
6. **API key:** Stored in `.env` file (gitignored), same key used for both demos

---

## Next Steps

1. **Monday 4/20 call with Shreeshan/Arun** — Demo the sentiment analytics, discuss pricing
2. **Get real Trinity Health ticket data** — If Shreeshan can share a CSV dump, we can run it live
3. **Pricing model:** ~$0.005 per ticket analysis — pennies vs. Foresight's $142K/yr
4. **If demo goes well:** Hand off to Madhu/Gradious for implementation, assign an Account Captain for ongoing pursuit
5. **Sales Bot follow-up:** Send follow-up email to Shreeshan, wait for sample PPT data

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
├── .env                                 ← API key (gitignored)
├── CLAUDE.md
├── handover.md                          ← this file
├── server.py                            ← Flask backend for sentiment demo
├── templates/index.html                 ← ServiceNow-style UI + Kore.ai panels
├── static/kore_logo.png                 ← Kore.ai logo
├── static/nttdata_logo.png              ← NTT DATA logo
├── generate_tickets.py                  ← Generates 100 sample tickets
├── trinity_health_service_tickets.csv   ← The 100 sample tickets
├── analysis_cache.json                  ← Pre-cached analysis results (gitignored)
├── start_sentiment_demo.sh              ← Start/stop/restart script
├── index.html                           ← Original chatbot (GitHub Pages)
├── ntt_data_salesbot_poc.html           ← Original chatbot (local, gitignored)
├── Kore.ai_Logo (1).png                 ← Original logo file
├── NTTDAtaLogo.png                      ← Original logo file
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
