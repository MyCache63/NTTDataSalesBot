# NTT DATA Sales Bot — Handover

**Last updated:** 2026-04-01 17:30 PT

---

## Current State

### What's Working
- **HTML Chatbot POC (v1.3)** is live and functional at:
  - GitHub Pages: https://mycache63.github.io/NTTDataSalesBot/
  - Local file: `ntt_data_salesbot_poc.html` (has API key baked in for demos)
- Chatbot uses **Claude Haiku 4.5** via Anthropic API with full NTT DATA Cloud Services knowledge base embedded as system prompt
- Features: 3-mode responses (Brief/Moderate/Verbose), conversation history sidebar, Discovery Questions toggle, Show Sources toggle, real PNG logos (NTT DATA + Kore.ai)
- API key is baked into both `index.html` (GitHub) and local file — works without prompting

### Documents Created
- `OneNTTData_SalesBot_Requirements_v02_April2026.docx` — Clean requirements doc (no design speculation), with correct stakeholder names and priority column
- `OneNTTData_SalesBot_RequirementsAndDesign_v01_April2026.docx` — Original v01 with full design/architecture (kept for reference)
- `NTT_DATA_Cloud_Services_Knowledge_Base.md` — All crawled NTT DATA product data
- `NTTDATA - Sales Bot Discovery - 20260401.txt` — Original discovery call transcript

### Build Status
- No build system — it's a single HTML file, opens in any browser
- GitHub repo: https://github.com/MyCache63/NTTDataSalesBot (public, for GitHub Pages)
- GitHub Pages deployed from `main` branch

---

## Key People

| Name | Role | Org |
|------|------|-----|
| Shreeshan Rangayan | Project Lead | NTT DATA |
| Wiley Oliver | Executive Sponsor | NTT DATA |
| Mike Ashe | Account Lead | Kore.ai |
| Michael Dsousa | Relationship Manager | Kore.ai |
| Deepak Anand | Solutions Architect | Kore.ai |
| Gupreet | SE (currently out sick) | Kore.ai |

---

## Key Decisions Made

1. **POC approach:** Giant prompt with embedded data (not RAG) — simplest path to demo
2. **LLM:** Claude Haiku 4.5 via Anthropic API — fast, cheap, good quality
3. **Hosting:** GitHub Pages (public repo) + local file with baked-in key
4. **API key in repo:** Michael's limited demo key is baked into `index.html` — he's aware the repo is public, the key has usage limits
5. **Doc v02:** Requirements only, no design speculation — let Srishan drive the design conversation

---

## Next Steps

1. **Demo to Srishan (scheduled 2026-04-02)** — Show the chatbot POC, walk through requirements doc v02, do further discovery
2. **Get sample data from NTT DATA** — Need 20-30 PPTs/brochures from Cloud Services Group to make the demo more real
3. **Resolve open questions** — Volume, pricing model, build vs. deliver, voice priority (see Section 7 of v02 doc)
4. **If demo goes well:** Scope a proper POC on the Kore.ai platform with RAG, Teams integration, and voice

---

## Open Issues

- **SecOps opportunity** appears dead — Srishan tried to get time extensions but doesn't have bandwidth to chase it
- **Gupreet is out sick** — no SE backup currently up to speed on this opportunity
- The $3.5M budget exists but unclear how this project fits into it (implementation + special cost)
- Need clarity on whether this is internal-only or also customer-facing

---

## File Inventory

```
NTT_Data_SalesBot/
├── .gitignore
├── CLAUDE.md
├── handover.md                          ← this file
├── index.html                           ← GitHub Pages version (no baked key... wait, key IS baked in now)
├── ntt_data_salesbot_poc.html           ← Local demo (key baked in, gitignored)
├── Kore.ai_Logo (1).png                ← Kore.ai logo
├── NTTDAtaLogo.png                      ← NTT DATA logo
├── NTT_DATA_Cloud_Services_Knowledge_Base.md
├── NTTDATA - Sales Bot Discovery - 20260401.txt
├── OneNTTData_SalesBot_Requirements_v02_April2026.docx
├── OneNTTData_SalesBot_RequirementsAndDesign_v01_April2026.docx
├── generate_requirements_doc.py         ← Script that built v01
└── generate_requirements_v02.py         ← Script that built v02
```
