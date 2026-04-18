---
title: "Kore.ai Sentiment Analytics for Enterprise ITO"
subtitle: "Solution Requirements — Trinity Health / NTT DATA"
date: "v01 — 2026-04-18 06:45 PT"
---

# Kore.ai Sentiment Analytics for Enterprise ITO

**Prepared for:** NTT DATA Services — Shreeshan Rangayan, Arun Mishra

**Prepared by:** Kore.ai — Mike Ashe, Michael Dsouza

**Version:** v01 — 2026-04-18

---

## 1. Executive Summary

NTT DATA manages IT service operations for Trinity Health across multiple facilities. Today, service quality is measured through traditional SLAs (uptime, ticket closure time). However, SLA compliance alone does not capture how end users *feel* about the support they receive.

This solution applies AI-powered sentiment analytics to IT service desk tickets, enabling NTT DATA to measure **Experience Level Agreements (XLAs)** — quantifying user satisfaction alongside traditional SLAs. The result is an early warning system that identifies emerging dissatisfaction before it becomes a formal complaint or contract risk.

**Key value proposition:** Replace or augment the existing Foresight sentiment tool ($142K) with a more capable, lower-cost solution that provides deeper insight — specifically, the ability to distinguish between frustration with the *problem itself* versus frustration with *NTT DATA's service response*.

---

## 2. Business Requirements

### 2.1 Problem Statement

- NTT DATA can meet every SLA while Trinity Health employees remain frustrated with IT support.
- Negative sentiment trends in specific departments (e.g., Pharmacy, Radiology) can indicate systemic issues before they escalate to management complaints or contract renewal risk.
- The current Foresight tool provides basic sentiment scoring but lacks nuanced analysis of *what* users are frustrated about.

### 2.2 Business Objectives

| # | Objective | Success Metric |
|---|-----------|---------------|
| 1 | Measure user experience beyond SLAs | XLA score computed weekly per department/location |
| 2 | Early warning for dissatisfaction spikes | Alerts when department sentiment drops below threshold |
| 3 | Distinguish problem frustration from service frustration | Each ticket tagged with frustration target |
| 4 | Provide actionable response recommendations | Per-ticket recommended action for service desk |
| 5 | Reduce sentiment analytics cost | Total cost below current Foresight spend ($142K/yr) |

### 2.3 Scope

**In scope for initial deployment:**

- Sentiment analysis of ServiceNow incident tickets (description, customer comments, work notes)
- Per-ticket scoring: sentiment (positive/neutral/negative), frustration target, key phrases, reasoning
- Aggregate dashboards: XLA scores by department, location, category, and time period
- Alert generation for negative sentiment trends
- Integration with ServiceNow data exports (CSV/API)

**Future phases (not in initial scope):**

- Real-time chat/email sentiment analysis
- Agent empathy scoring (evaluating IT staff responses)
- Sentiment-based ticket routing (auto-escalate angry users)
- Voice call sentiment analysis
- Integration with additional ITSM platforms beyond ServiceNow

---

## 3. Functional Requirements

### 3.1 Ticket Sentiment Analysis

| ID | Requirement | Priority |
|----|-------------|----------|
| F-01 | Analyze free-text fields (description, comments, work notes) for customer sentiment | Must Have |
| F-02 | Classify each ticket as Positive, Neutral, or Negative with a numeric score (-1.0 to +1.0) | Must Have |
| F-03 | Identify frustration target: Problem Itself, Service Provider, Both, or None | Must Have |
| F-04 | Extract key phrases that drove the sentiment classification | Must Have |
| F-05 | Provide 2-3 sentence reasoning explaining the sentiment assessment | Must Have |
| F-06 | Generate recommended response action for service desk agents | Should Have |
| F-07 | Assess XLA impact level (Low/Medium/High) per ticket | Should Have |
| F-08 | Assess emotional urgency independent of technical priority | Should Have |

### 3.2 Dashboard and Reporting

| ID | Requirement | Priority |
|----|-------------|----------|
| F-09 | Display overall XLA score (0-10 scale) across all analyzed tickets | Must Have |
| F-10 | Show sentiment distribution (positive/neutral/negative counts and percentages) | Must Have |
| F-11 | Break down sentiment by department, location, and ticket category | Must Have |
| F-12 | Show weekly sentiment trend over time | Must Have |
| F-13 | Generate alerts for departments/locations where negative sentiment exceeds threshold | Must Have |
| F-14 | Frustration target breakdown (how many tickets target the problem vs. service provider) | Must Have |
| F-15 | Drill-down from dashboard to individual ticket detail with full analysis | Should Have |
| F-16 | Filterable/sortable ticket list by sentiment, priority, category, frustration target | Should Have |

### 3.3 Data Integration

| ID | Requirement | Priority |
|----|-------------|----------|
| F-17 | Accept ServiceNow ticket data via CSV upload | Must Have |
| F-18 | Accept ServiceNow ticket data via API integration | Should Have |
| F-19 | Cache analysis results to avoid re-processing previously scored tickets | Must Have |
| F-20 | Support batch analysis (process hundreds/thousands of tickets efficiently) | Must Have |
| F-21 | Support on-demand re-analysis of individual tickets | Should Have |

---

## 4. Non-Functional Requirements

| ID | Requirement | Detail |
|----|-------------|--------|
| NF-01 | Performance | Analyze 100 tickets in under 60 seconds (batch mode) |
| NF-02 | Scalability | Support up to 10,000 tickets per analysis run |
| NF-03 | Accuracy | Sentiment classification accuracy > 90% vs. human review |
| NF-04 | Availability | Dashboard accessible 24/7 via web browser |
| NF-05 | Security | No PHI/PII transmitted to external AI services; ticket text only |
| NF-06 | Data Retention | Analysis results retained for 12 months minimum |
| NF-07 | Cost Efficiency | Per-ticket analysis cost < $0.01 at scale |

---

## 5. Solution Architecture (High Level)

```
ServiceNow → CSV/API Export → Kore.ai Sentiment Engine → Dashboard
                                      ↓
                              AI Analysis (LLM)
                                      ↓
                              Structured Results
                              (score, target, reasoning)
                                      ↓
                              Results Cache (JSON/DB)
```

**Key components:**

1. **Data Ingestion** — ServiceNow ticket data via CSV upload or API connector
2. **Sentiment Engine** — AI/LLM-powered analysis with structured output (sentiment, frustration target, key phrases, reasoning, recommendations)
3. **Results Store** — Cached analysis results with incremental updates (only new/changed tickets re-analyzed)
4. **Dashboard UI** — Web-based dashboard with charts, alerts, drill-down to individual tickets
5. **Alert System** — Configurable thresholds for sentiment alerts by department/location

---

## 6. Competitive Differentiation vs. Foresight

| Capability | Foresight ($142K/yr) | Kore.ai Solution |
|-----------|---------------------|------------------|
| Basic sentiment (pos/neg/neutral) | Yes | Yes |
| Frustration target analysis | No | **Yes — distinguishes problem vs. service provider** |
| Per-ticket reasoning | No | **Yes — explains why each score was assigned** |
| Key phrase extraction | Limited | **Yes — exact quotes highlighted** |
| Recommended response action | No | **Yes — actionable guidance for agents** |
| XLA scoring | Basic | **Yes — 0-10 scale with department breakdown** |
| Department-level alerts | Limited | **Yes — configurable thresholds** |
| Cost per ticket | Flat $142K/yr | **~$0.005/ticket — scales with usage** |
| Cross-account deployment | Separate instance | **Same engine, any NTT DATA account** |

---

## 7. Pricing Model (Preliminary)

| Component | Estimated Cost |
|-----------|---------------|
| Per-ticket analysis | ~$0.005 per ticket |
| 1,000 tickets/month | ~$60/year |
| 10,000 tickets/month | ~$600/year |
| 100,000 tickets/month | ~$6,000/year |
| Platform/dashboard hosting | TBD based on deployment model |
| Implementation & configuration | TBD |

*Exact pricing subject to final architecture and volume commitments.*

---

## 8. Open Questions for Discussion

1. **Data access:** Can NTT DATA provide a sample CSV export of real Trinity Health tickets (with PHI/PII redacted) for validation?
2. **Volume:** How many tickets per month does NTT DATA process for Trinity Health?
3. **Integration preference:** CSV batch upload vs. real-time ServiceNow API integration?
4. **Deployment:** Cloud-hosted (Kore.ai managed) vs. on-premise within NTT DATA infrastructure?
5. **Alert routing:** Where should sentiment alerts be delivered (email, Teams, ServiceNow)?
6. **Cross-account timeline:** If Trinity Health is successful, what is the rollout plan for other NTT DATA accounts?
7. **Compliance:** Are there specific data handling or residency requirements for Trinity Health ticket data?
