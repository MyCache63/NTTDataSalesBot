#!/usr/bin/env python3
"""
NTT DATA / Trinity Health — Sentiment Analytics Demo
Powered by Kore.ai + Claude AI

Flask server that loads ServiceNow-style tickets from CSV,
runs sentiment analysis via Claude API, and serves a dashboard UI.
"""

import csv
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, jsonify, request, send_from_directory
from anthropic import Anthropic

app = Flask(__name__)

TICKETS_CSV = Path(__file__).parent / "trinity_health_service_tickets.csv"
CACHE_FILE = Path(__file__).parent / "analysis_cache.json"
MODEL = "claude-sonnet-4-6"
MAX_WORKERS = 10

VERSION = "1.0.0"
BUILD = "2026-04-17 12:45"

client = Anthropic()

tickets = []
analysis_results = {}
analysis_progress = {"total": 0, "completed": 0, "running": False}


def load_tickets():
    global tickets
    tickets = []
    with open(TICKETS_CSV, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tickets.append(row)
    return tickets


def load_cache():
    global analysis_results
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r") as f:
            analysis_results = json.load(f)
        return True
    return False


def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(analysis_results, f, indent=2)


ANALYSIS_PROMPT = """Analyze this IT service desk ticket for customer sentiment. Focus on the CUSTOMER's perspective (the person who opened the ticket and wrote comments), not the IT staff.

TICKET DATA:
- Ticket Number: {number}
- Date Opened: {opened}
- Short Description: {short_desc}
- Full Description: {description}
- Customer Comments: {comments}
- Priority: {priority}
- Category: {category} / {subcategory}
- State: {state}
- Location: {location}

IMPORTANT DISTINCTIONS:
1. "problem_itself" — frustration with the technical issue (e.g., "my laptop keeps crashing")
2. "service_provider" — frustration with IT support quality/speed (e.g., "I've called 4 times and nobody fixed it")
3. "both" — frustrated with the problem AND the service response
4. "none" — neutral or positive, no frustration detected

Return ONLY valid JSON (no markdown fences, no explanation outside the JSON):
{{
  "overall_sentiment": "positive" or "neutral" or "negative",
  "sentiment_score": float from -1.0 (very negative) to 1.0 (very positive),
  "frustration_target": "problem_itself" or "service_provider" or "both" or "none",
  "frustration_target_explanation": "1 sentence explaining who/what the frustration targets",
  "key_phrases": ["exact quote 1", "exact quote 2", "exact quote 3"],
  "reasoning": "2-3 sentences explaining your sentiment assessment with specific textual evidence",
  "urgency_emotional": "low" or "medium" or "high" or "critical",
  "recommended_action": "1-2 sentence recommended response approach for the service desk",
  "xla_impact": "low" or "medium" or "high"
}}"""


def analyze_single_ticket(ticket):
    prompt = ANALYSIS_PROMPT.format(
        number=ticket["Number"],
        opened=ticket["Opened"],
        short_desc=ticket["Short Description"],
        description=ticket["Description"],
        comments=ticket["Customer Comments"],
        priority=ticket["Priority"],
        category=ticket["Category"],
        subcategory=ticket["Subcategory"],
        state=ticket["State"],
        location=ticket["Location"],
    )
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=600,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        result = json.loads(text)
        result["ticket_number"] = ticket["Number"]
        result["analyzed_at"] = datetime.now().isoformat()
        return result
    except Exception as e:
        return {
            "ticket_number": ticket["Number"],
            "overall_sentiment": "error",
            "sentiment_score": 0,
            "frustration_target": "unknown",
            "frustration_target_explanation": f"Analysis failed: {e}",
            "key_phrases": [],
            "reasoning": f"Error: {e}",
            "urgency_emotional": "unknown",
            "recommended_action": "Manual review required",
            "xla_impact": "unknown",
            "analyzed_at": datetime.now().isoformat(),
            "error": str(e),
        }


# --- Routes ---


@app.route("/")
def index():
    return render_template("index.html", version=VERSION, build=BUILD)


@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)


@app.route("/api/tickets")
def get_tickets():
    result = []
    for ticket in tickets:
        t = dict(ticket)
        if ticket["Number"] in analysis_results:
            t["analysis"] = analysis_results[ticket["Number"]]
        result.append(t)
    return jsonify(result)


@app.route("/api/analyze", methods=["POST"])
def run_analysis():
    global analysis_progress
    if analysis_progress["running"]:
        return jsonify({"status": "already_running", "progress": analysis_progress})

    analysis_progress = {"total": len(tickets), "completed": 0, "running": True}

    def do_analysis():
        global analysis_results
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(analyze_single_ticket, t): t for t in tickets
            }
            for future in as_completed(futures):
                ticket = futures[future]
                result = future.result()
                analysis_results[ticket["Number"]] = result
                analysis_progress["completed"] += 1
        analysis_progress["running"] = False
        save_cache()

    threading.Thread(target=do_analysis, daemon=True).start()
    return jsonify({"status": "started", "total": len(tickets)})


@app.route("/api/analyze-status")
def analyze_status():
    return jsonify(analysis_progress)


@app.route("/api/analyze/<ticket_number>", methods=["POST"])
def analyze_one(ticket_number):
    ticket = next((t for t in tickets if t["Number"] == ticket_number), None)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    result = analyze_single_ticket(ticket)
    analysis_results[ticket_number] = result
    save_cache()
    return jsonify(result)


@app.route("/api/dashboard")
def dashboard():
    if not analysis_results:
        return jsonify({"error": "No analysis results. Run analysis first."}), 404

    sentiments = {"positive": 0, "neutral": 0, "negative": 0}
    frustration_targets = {
        "problem_itself": 0,
        "service_provider": 0,
        "both": 0,
        "none": 0,
    }
    xla_impacts = {"low": 0, "medium": 0, "high": 0}
    scores = []
    category_data = {}
    location_data = {}
    weekly_data = {}
    priority_sentiment = {}

    for ticket in tickets:
        if ticket["Number"] not in analysis_results:
            continue
        a = analysis_results[ticket["Number"]]

        sent = a.get("overall_sentiment", "unknown")
        if sent in sentiments:
            sentiments[sent] += 1

        target = a.get("frustration_target", "unknown")
        if target in frustration_targets:
            frustration_targets[target] += 1

        xla = a.get("xla_impact", "unknown")
        if xla in xla_impacts:
            xla_impacts[xla] += 1

        score = a.get("sentiment_score", 0)
        scores.append(score)

        for group_key, group_dict, field in [
            ("category", category_data, "Category"),
            ("location", location_data, "Location"),
        ]:
            key = ticket.get(field, "Unknown")
            if key not in group_dict:
                group_dict[key] = {"scores": [], "count": 0, "negative": 0}
            group_dict[key]["scores"].append(score)
            group_dict[key]["count"] += 1
            if sent == "negative":
                group_dict[key]["negative"] += 1

        pri = ticket.get("Priority", "Unknown")
        if pri not in priority_sentiment:
            priority_sentiment[pri] = {"scores": [], "count": 0, "negative": 0}
        priority_sentiment[pri]["scores"].append(score)
        priority_sentiment[pri]["count"] += 1
        if sent == "negative":
            priority_sentiment[pri]["negative"] += 1

        try:
            dt = datetime.strptime(ticket["Opened"], "%Y-%m-%d %H:%M:%S")
            wk = f"{dt.year}-W{dt.isocalendar()[1]:02d}"
            if wk not in weekly_data:
                weekly_data[wk] = {"scores": [], "count": 0}
            weekly_data[wk]["scores"].append(score)
            weekly_data[wk]["count"] += 1
        except ValueError:
            pass

    avg_score = sum(scores) / len(scores) if scores else 0
    xla_score = round((avg_score + 1) * 5, 1)

    def summarize(data):
        out = {}
        for k, v in data.items():
            avg = sum(v["scores"]) / len(v["scores"]) if v["scores"] else 0
            out[k] = {
                "avg_score": round(avg, 2),
                "xla_score": round((avg + 1) * 5, 1),
                "ticket_count": v["count"],
                "negative_count": v.get("negative", 0),
                "negative_pct": (
                    round(v["negative"] / v["count"] * 100, 1) if v["count"] else 0
                ),
            }
        return out

    weekly_summary = {}
    for wk in sorted(weekly_data):
        v = weekly_data[wk]
        avg = sum(v["scores"]) / len(v["scores"]) if v["scores"] else 0
        weekly_summary[wk] = {
            "avg_score": round(avg, 2),
            "xla_score": round((avg + 1) * 5, 1),
            "ticket_count": v["count"],
        }

    return jsonify(
        {
            "total_tickets": len(tickets),
            "analyzed_tickets": len(analysis_results),
            "sentiment_distribution": sentiments,
            "frustration_targets": frustration_targets,
            "xla_impacts": xla_impacts,
            "overall_avg_score": round(avg_score, 2),
            "xla_score": xla_score,
            "category_breakdown": summarize(category_data),
            "location_breakdown": summarize(location_data),
            "priority_breakdown": summarize(priority_sentiment),
            "weekly_trend": weekly_summary,
        }
    )


if __name__ == "__main__":
    print("Loading tickets...")
    load_tickets()
    print(f"Loaded {len(tickets)} tickets")

    if load_cache():
        print(f"Loaded {len(analysis_results)} cached analysis results")
    else:
        print("No cached results. Use the UI to run analysis.")

    print()
    print("=" * 60)
    print("  NTT DATA / Trinity Health — Sentiment Analytics Demo")
    print("  Powered by Kore.ai + Claude AI")
    print(f"  Version {VERSION} | Build {BUILD}")
    print("=" * 60)
    print(f"\n  Open http://localhost:5001 in your browser\n")

    app.run(debug=True, port=5001)
