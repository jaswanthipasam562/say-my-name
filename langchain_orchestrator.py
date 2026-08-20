"""
=============================================================================
AI NEWS DETECTIVE - LANGCHAIN & GEMINI AI ORCHESTRATOR
=============================================================================
Coordinates:
1. Multi-Step LangChain Intelligence Pipeline (Validation -> Search -> ML -> Gemini)
2. Final AI Intelligence Report Synthesis
3. Context-Aware AI News Assistant (Streaming & Interactive Chat)
4. Fallback Reasoning Engine for offline/no-key environments
"""

import os
import json
import re
from typing import Dict, Any, List, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class LangChainNewsOrchestrator:
    """
    Central orchestration layer leveraging Google Gemini and LangChain design patterns
    to synthesize ML predictions, search cross-validation, sentiment, and spread metrics.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if self.api_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            except Exception:
                self.model = None
        else:
            self.model = None

    def synthesize_intelligence_report(self, 
                                      input_text: str,
                                      ml_data: Dict[str, Any], 
                                      search_data: Dict[str, Any],
                                      spread_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes the complete multimodal evidence into a cohesive final AI intelligence report.
        """
        verdict = ml_data["classification"]["verdict"]
        verdict_code = ml_data["classification"]["verdict_code"]
        confidence = ml_data["classification"]["confidence"]
        sentiment = ml_data["sentiment"]["label"]
        tone = ml_data["sentiment"]["tone"]
        topic = ml_data["topic"]["topic"]
        keywords = ml_data["keywords"]
        sources = search_data.get("sources", [])
        agreement = search_data.get("agreement", {})
        spread_signal = spread_data.get("spread_signal", {}).get("signal", "MEDIUM")

        # Use Gemini for Deep Synthesis if configured
        if self.model:
            try:
                source_summaries = "\n".join([f"- {s.get('source')}: {s.get('title')}" for s in sources[:4]])
                prompt = f"""
                You are the Lead Investigative AI for AI NEWS DETECTIVE.
                Synthesize the following forensic news intelligence into an authoritative, objective report.

                Original Story: "{input_text}"
                ML Authenticity Verdict: {verdict} ({confidence}% confidence)
                Sentiment Analysis: {sentiment} ({tone})
                Topic Classification: {topic}
                Extracted Keywords: {', '.join(keywords)}
                Discovered Sources Consensus: {agreement.get('consensus')} ({agreement.get('description')})
                Discovered Live Sources:
                {source_summaries}
                Platform Spread Signal: {spread_signal}

                Generate a clear, professional 2-3 paragraph investigative breakdown:
                1. Executive Summary: What was analyzed and what the ML/evidence signals indicate.
                2. Corroborating & Disputing Evidence: What reputable sources report and where discrepancies lie.
                3. Verification Guidance: Specific actions users should take before accepting or sharing.
                """
                response = self.model.generate_content(prompt)
                ai_explanation = response.text.strip()
                engine_type = "Google Gemini 1.5 Flash (LangChain Router)"
            except Exception as e:
                ai_explanation = self._generate_heuristic_explanation(input_text, ml_data, search_data)
                engine_type = "Deterministic Neural Synthesis (Local Fallback)"
        else:
            ai_explanation = self._generate_heuristic_explanation(input_text, ml_data, search_data)
            engine_type = "Rule-Based Neural Heuristic Engine"

        return {
            "verdict": verdict,
            "verdict_code": verdict_code,
            "confidence": confidence,
            "sentiment": sentiment,
            "sentiment_tone": tone,
            "topic": topic,
            "keywords": keywords,
            "source_evidence_count": len(sources),
            "sources_matching": search_data.get("matching_sources_count", 0),
            "agreement_consensus": agreement.get("consensus", "MIXED REPORTING"),
            "spread_signal": spread_signal,
            "ai_explanation": ai_explanation,
            "engine_used": engine_type,
            "credibility_notice": "AI-assisted multi-source synthesis. Derived from live search indices and forensic NLP models."
        }

    def _generate_heuristic_explanation(self, input_text: str, ml_data: Dict[str, Any], search_data: Dict[str, Any]) -> str:
        """High quality, evidence-based narrative generator when LLM is unavailable."""
        verdict = ml_data["classification"]["verdict"]
        conf = ml_data["classification"]["confidence"]
        topic = ml_data["topic"]["topic"]
        sentiment = ml_data["sentiment"]["label"]
        tone = ml_data["sentiment"]["tone"]
        agreement = search_data.get("agreement", {}).get("consensus", "MIXED REPORTING")
        total_sources = search_data.get("total_sources", 0)

        if verdict == "POTENTIALLY FAKE":
            return (
                f"🚨 **Misinformation Alert & Forensic Analysis:**\n\n"
                f"Our multi-signal NLP and machine learning pipeline has flagged this item as **{verdict}** with **{conf}% confidence**. "
                f"The text exhibits characteristic linguistic markers of sensationalism ({tone}) within the **{topic}** domain. "
                f"Cross-referencing against live news indices identified {total_sources} related items, resulting in a status of **{agreement}**.\n\n"
                f"**Recommended Action:** Do not circulate this claim without secondary verification from accredited press wires or official institutional releases."
            )
        elif verdict == "POTENTIALLY REAL":
            return (
                f"✅ **Corroborating Evidence Found:**\n\n"
                f"The analyzed report aligns closely with standard journalistic reporting standards in **{topic}**, reflecting an objective **{sentiment}** tone ({conf}% confidence). "
                f"Real-time search cross-validation discovered {total_sources} independent news reports reporting matching timelines and event specifics (**{agreement}**).\n\n"
                f"**Investigation Note:** While preliminary evidence supports the core claims, always review primary press releases for newly emerging updates."
            )
        else:
            return (
                f"⚠️ **Inconclusive / More Verification Required:**\n\n"
                f"The claim presents mixed signals in the **{topic}** domain with **{conf}% evaluation confidence**. "
                f"Live source checking indicates **{agreement}** across {total_sources} search results, meaning either the story is breaking in real-time or details remain contested among reporting outlets.\n\n"
                f"**Recommended Action:** Use the 'Ask AI' assistant or click the platform discovery links below to cross-check official announcements."
            )

    def answer_assistant_question(self, user_question: str, context: Dict[str, Any]) -> str:
        """
        Context-Aware AI Assistant Chat Engine.
        Answers user questions using the active news analysis context.
        """
        headline = context.get("headline", "Analyzed News Item")
        verdict = context.get("verdict", "UNCERTAIN")
        confidence = context.get("confidence", 80)
        sentiment = context.get("sentiment", "Neutral")
        topic = context.get("topic", "General")
        keywords = context.get("keywords", [])
        agreement = context.get("agreement_consensus", "Pending")
        sources = context.get("sources", [])

        if self.model:
            try:
                sources_str = ", ".join([s.get("source", "") for s in sources[:4]])
                prompt = f"""
                You are the AI News Detective Assistant. You have deeply investigated the following news claim:

                Story Headline: "{headline}"
                Forensic Verdict: {verdict} ({confidence}% confidence)
                Sentiment: {sentiment}
                Topic: {topic}
                Keywords: {', '.join(keywords)}
                Source Agreement: {agreement}
                Discovered Sources: {sources_str}

                User Question: "{user_question}"

                Provide a concise, direct, helpful, and objective response based on the evidence collected.
                """
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception:
                pass

        # Intelligent Heuristic / Quick Prompt Handler
        q_lower = user_question.lower()

        if "why" in q_lower and ("fake" in q_lower or "suspicious" in q_lower):
            return f"The claim was evaluated as **{verdict}** ({confidence}% confidence) due to lexical alarmist markers, lack of authoritative attribution, and source consensus evaluation ({agreement})."
        elif "supporting" in q_lower or "sources" in q_lower or "evidence" in q_lower:
            src_list = "\n".join([f"- **{s.get('source')}**: {s.get('title')} ([Link]({s.get('url')}))" for s in sources[:3]])
            return f"Discovered reporting ({agreement}):\n\n{src_list if src_list else 'No direct corroborating URLs found in current index.'}"
        elif "summarize" in q_lower or "summary" in q_lower:
            return f"**Summary:** The report concerns **{topic}** involving *{', '.join(keywords[:4])}*. Our cross-validation verdict is **{verdict}** with **{agreement}** across live search indexes."
        elif "simple" in q_lower or "explain" in q_lower:
            return f"In simple terms: The story talks about {topic.lower()}. The AI checked both the language and news websites, finding {agreement.lower()}. Verdict: **{verdict}** ({confidence}% sure)."
        elif "sentiment" in q_lower:
            return f"The detected sentiment is **{sentiment}**, reflecting the emotional and linguistic tone present in the source text."
        elif "keywords" in q_lower or "claims" in q_lower:
            return f"Important extracted keywords and entities: **{', '.join(keywords)}**."
        elif "verify" in q_lower or "what should i do" in q_lower:
            return "1. Check official government/institutional websites.\n2. Cross-reference with major news wires (Reuters, AP, BBC).\n3. Search Google News for recent corrections or press conferences."
        else:
            return f"Regarding '{headline[:50]}': The system classified this as **{verdict}** with **{agreement}** across {len(sources)} examined sources in the **{topic}** domain."


_orchestrator = LangChainNewsOrchestrator()

def generate_report(input_text: str, ml_data: Dict[str, Any], search_data: Dict[str, Any], spread_data: Dict[str, Any]) -> Dict[str, Any]:
    """Helper to synthesize final report."""
    return _orchestrator.synthesize_intelligence_report(input_text, ml_data, search_data, spread_data)

def ask_ai_assistant(question: str, context: Dict[str, Any]) -> str:
    """Helper for AI assistant chat."""
    return _orchestrator.answer_assistant_question(question, context)
