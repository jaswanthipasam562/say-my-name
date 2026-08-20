#!/usr/bin/env python3
"""
=============================================================================
AI NEWS DETECTIVE - FULL-STACK REST API BACKEND SERVER
=============================================================================
Provides REST endpoints and static web application serving on port 3000:
- POST /api/news/validate      -> 3-Signal News Relevance Validation Radar
- POST /api/news/investigate   -> Complete Multimodal News Forensics Pipeline
- POST /api/ai/chat            -> Context-Aware Gemini AI News Assistant
- POST /api/news/search-live   -> Live Real-Time Web Search & Source Consensus
- POST /api/news/spread-intel  -> Cross-Platform Spread Intelligence (YouTube, X, Instagram)
- GET  /api/health             -> Telemetry & Model Status Check
"""

import http.server
import json
import os
import sys
import time
import urllib.parse
from datetime import datetime, timezone

# Add current directory to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from news_relevance import is_news_related
from ml_engine import process_news
from search_engine import search_news
from spread_tracker import track_spread
from langchain_orchestrator import generate_report, ask_ai_assistant

PORT = 3000


class AINewsRESTHandler(http.server.SimpleHTTPRequestHandler):
    """Production-grade HTTP Request Handler with CORS and REST API routing."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_OPTIONS(self):
        """Handle CORS pre-flight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/health':
            self._send_json({
                "status": "ONLINE",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "service": "AI News Detective Intelligence Engine",
                "features": {
                    "news_relevance_radar": "3-Signal Active",
                    "ml_classifier": "TF-IDF + Scikit-Learn",
                    "live_search": "Google Custom Search / News RSS",
                    "spread_tracker": "YouTube, Google News, X, Instagram, Web",
                    "ai_orchestrator": "LangChain + Gemini 1.5"
                }
            })
        else:
            # Serve index.html or other static files
            super().do_GET()

    def do_POST(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path

            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'

            try:
                req = json.loads(post_data) if post_data else {}
            except Exception:
                req = {}

            if path in ['/api/news/validate', '/api/news/validate-gateway', '/api/news/validate-relevance']:
                self.handle_validate(req)
            elif path == '/api/news/investigate':
                self.handle_investigate(req)
            elif path == '/api/ai/chat':
                self.handle_ai_chat(req)
            elif path == '/api/news/search-live':
                self.handle_search_live(req)
            elif path == '/api/news/spread-intel':
                self.handle_spread_intel(req)
            else:
                self._send_json({"error": "Not Found", "path": path}, status=404)
        except Exception as e:
            self._send_json({"error": "Internal Server Error", "details": str(e)}, status=500)

    def handle_validate(self, req):
        text = req.get("text", "").strip()
        result = is_news_related(text)
        self._send_json(result)

    def handle_investigate(self, req):
        text = req.get("text", "").strip()
        if not text:
            self._send_json({"error": "Empty input provided"}, status=400)
            return

        # Step 1: News Relevance Radar
        relevance = is_news_related(text)
        if not relevance["is_news_related"]:
            self._send_json({
                "is_news": False,
                "relevance": relevance
            })
            return

        # Step 2: ML Analysis
        ml_data = process_news(text)

        # Step 3: Real-Time Search & Source Cross-Validation
        search_data = search_news(
            ml_data["headline"],
            ml_data["keywords"],
            ml_data["classification"]["verdict_code"]
        )

        # Step 4: Real-Time Spread Tracking
        spread_data = track_spread(
            ml_data["headline"],
            ml_data["keywords"],
            search_data["sources"],
            ml_data["classification"]["verdict_code"]
        )

        # Step 5: Gemini / LangChain Dossier Synthesis
        report = generate_report(text, ml_data, search_data, spread_data)

        self._send_json({
            "is_news": True,
            "relevance": relevance,
            "ml": ml_data,
            "search": search_data,
            "spread": spread_data,
            "report": report
        })

    def handle_ai_chat(self, req):
        question = req.get("question", "")
        context = req.get("context", {})
        answer = ask_ai_assistant(question, context)
        self._send_json({"answer": answer})

    def handle_search_live(self, req):
        headline = req.get("headline", "")
        keywords = req.get("keywords", [])
        ml_verdict = req.get("verdict_code", "UNCERTAIN")
        data = search_news(headline, keywords, ml_verdict)
        self._send_json(data)

    def handle_spread_intel(self, req):
        headline = req.get("headline", "")
        keywords = req.get("keywords", [])
        sources = req.get("sources", [])
        ml_verdict = req.get("verdict_code", "UNCERTAIN")
        data = track_spread(headline, keywords, sources, ml_verdict)
        self._send_json(data)

    def _send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server():
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    server_address = ('', PORT)
    httpd = http.server.ThreadingHTTPServer(server_address, AINewsRESTHandler)
    print("================================================================")
    print(f"[ONLINE] AI NEWS DETECTIVE - REST API & INTELLIGENCE SERVER ACTIVE")
    print(f"[ACCESS] Local Access URL: http://localhost:{PORT}")
    print(f"[ROUTES] Endpoints: /api/news/validate | /api/news/investigate | /api/ai/chat | /api/health")
    print("================================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully.")
        httpd.server_close()


if __name__ == '__main__':
    run_server()
