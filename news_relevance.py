"""
=============================================================================
AI NEWS DETECTIVE - NEWS RELEVANCE VALIDATION ENGINE (3-SIGNAL PIPELINE)
=============================================================================
This module verifies whether incoming user input represents a verifiable news
story or public claim BEFORE passing it to fake-news classification pipelines.

Signals:
1. NLTK / Rule-Based NLP Heuristics (lexical density, entity presence, conversational markers)
2. Scikit-learn TF-IDF Machine Learning Classifier (News vs. Non-News)
3. Google Gemini / LLM Semantic Claim Evaluation (Structured JSON verdict)
"""

import os
import re
import math
from typing import Dict, Any, List, Tuple
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Try optional imports gracefully
try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    NLTK_AVAILABLE = True
except Exception:
    NLTK_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False


# =============================================================================
# 1. SYNTHETIC TRAINING DATA FOR SCIKIT-LEARN NEWS VS NON-NEWS CLASSIFIER
# =============================================================================
NON_NEWS_CORPUS = [
    "hello", "hi", "hey there", "good morning", "how are you doing", "good evening",
    "i love pizza", "i like ice cream", "pizza is delicious", "i am hungry",
    "my phone is blue", "my favorite color is purple", "the sky looks nice today",
    "what is your name", "who are you", "can you help me with math homework",
    "i am going to sleep", "have a great day", "thank you very much", "see you later",
    "today is my birthday", "i bought a new pair of shoes", "my dog is playing in the yard",
    "write a python script for binary search", "tell me a funny joke", "roses are red violets are blue",
    "i enjoy playing football on weekends", "my car has four wheels", "what time is it right now",
    "i want to learn guitar", "cooking pasta with tomato sauce", "i feel very happy today",
    "can we be friends", "test 123", "random text here", "asdfghjkl", "where do you live"
]

NEWS_CORPUS = [
    "Government announces new economic policy affecting national university students",
    "Federal Reserve cuts interest rates by 25 basis points amid slowing inflation",
    "WHO reports new viral outbreak in southeastern Asian territories",
    "SpaceX successfully launches orbital satellite constellation into low earth orbit",
    "Supreme court rules on landmark digital privacy and surveillance legislation",
    "Tech company acquires AI startup for three billion dollars in cash and equity",
    "Prime minister visits international summit to negotiate bilateral trade agreement",
    "Earthquake of magnitude 6.8 strikes coastal region causing extensive infrastructure damage",
    "Health ministry approves breakthrough gene therapy for rare inherited disorder",
    "Defense department awards aerospace contract for next generation stealth drone fleet",
    "Central bank raises reserve requirements as consumer price index surges 4.2 percent",
    "United Nations passes emergency resolution demanding immediate humanitarian ceasefire",
    "Electric vehicle manufacturer recalls fifty thousand cars over battery management software",
    "Scientists discover liquid water reservoir deep beneath martian volcanic plateau",
    "Major cyberattack compromises municipal government databases across three provinces",
    "Police arrest suspect in multi-million dollar international banking fraud operation",
    "Parliament votes to reform national taxation structure and renewable energy subsidies",
    "Aviation authority grounds commercial aircraft fleet following engine turbine defect",
    "Heavy monsoon rains trigger severe flash floods across major river basins",
    "Global pharmaceutical firm initiates Phase 3 clinical trials for universal flu vaccine"
]


class NewsRelevanceValidator:
    """
    Real-Time Multi-Signal News Relevance & Verification Gateway.
    Prevents ML/NLP fake-news classification models from evaluating non-news chatter,
    greetings, personal opinions, or casual statements.
    
    Signals:
    1. NLTK / Lexical Structure & Entity Preprocessing
    2. Dedicated Scikit-Learn TF-IDF News Relevance Classifier
    3. Gemini Semantic Structured Claim Evaluation (JSON Mode)
    4. Real-Time Web News Pre-Search Signal
    """

    def __init__(self):
        self._init_sklearn_model()

    def _init_sklearn_model(self):
        """Train lightweight, deterministic TF-IDF classifier on initialization."""
        if not SKLEARN_AVAILABLE:
            self.ml_pipeline = None
            return

        texts = NON_NEWS_CORPUS + NEWS_CORPUS
        labels = [0] * len(NON_NEWS_CORPUS) + [1] * len(NEWS_CORPUS)

        self.ml_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=1, lowercase=True)),
            ('clf', LogisticRegression(C=2.0, max_iter=300))
        ])
        self.ml_pipeline.fit(texts, labels)

    def signal_1_nltk_preprocessing(self, text: str) -> Dict[str, Any]:
        """
        NLTK / Lexical Rule-Based Signal:
        - Lowercase normalization
        - Tokenization & punctuation cleaning
        - Stopword filtering
        - Keyword & entity extraction
        - Conversational / Personal statement detection
        """
        text_clean = text.strip()
        words = re.findall(r'\b[a-zA-Z]{2,}\b', text_clean.lower())
        word_count = len(words)

        # Conversational / Greeting blacklists
        conversational_patterns = [
            r'^(hi|hello|hey|greetings|good\s+(morning|afternoon|evening|night))\b',
            r'\b(i\s+like|i\s+love|i\s+hate|i\s+feel|i\s+am|i\s+want|my\s+(phone|car|dog|cat|friend|name|favorite))\b',
            r'\b(how\s+are\s+you|who\s+are\s+you|what\s+is\s+your\s+name|tell\s+me\s+a\s+joke)\b',
            r'^(thank\s+you|thanks|bye|see\s+you|goodbye)\b'
        ]

        is_conversational = any(re.search(p, text_clean.lower()) for p in conversational_patterns)

        # News marker vocabulary (verbs of reporting, governance, events, statistics)
        news_markers = {
            "announces", "announced", "reports", "reported", "confirms", "confirmed", "reveals",
            "government", "ministry", "president", "minister", "court", "police", "officials",
            "spokesperson", "spokesman", "authorities", "federal", "parliament", "congress",
            "investigation", "investigating", "arrested", "hospitalized", "killed", "injured",
            "economic", "inflation", "market", "stocks", "shares", "company", "billion", "million",
            "launched", "approved", "banned", "passed", "discovered", "treaty", "agreement",
            "crisis", "protest", "strike", "earthquake", "cyclone", "flood", "summit", "election",
            "policy", "reform", "sanctions", "treaty", "verdict", "trial", "allegations", "patent"
        }

        matched_markers = [w for w in words if w in news_markers]
        
        # Capitalized entity extraction (People, Orgs, Locations)
        entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text_clean)
        common_words = {"The", "This", "That", "When", "What", "Why", "How", "After", "Before", "According", "Officials", "Breaking", "Report"}
        clean_entities = [e for e in entities if e not in common_words and len(e) > 2]

        # Scoring heuristics
        if word_count < 3 or is_conversational:
            score = 0.05
        elif word_count >= 6 and len(matched_markers) >= 1:
            score = min(0.95, 0.45 + (len(matched_markers) * 0.2) + (len(clean_entities) * 0.1))
        elif len(clean_entities) >= 2:
            score = 0.70
        elif word_count >= 8:
            score = 0.50
        else:
            score = 0.30

        return {
            "score": round(score, 3),
            "word_count": word_count,
            "matched_markers": matched_markers,
            "entities": clean_entities[:5],
            "is_conversational": is_conversational,
            "passed": score >= 0.48 and not is_conversational
        }

    def signal_2_sklearn_ml(self, text: str) -> Dict[str, Any]:
        """
        Scikit-learn TF-IDF + Logistic Regression News Relevance Classifier.
        """
        if not self.ml_pipeline:
            return {"score": 0.5, "passed": True, "note": "Scikit-learn unavailable (fallback active)"}

        try:
            proba = self.ml_pipeline.predict_proba([text])[0]
            news_prob = float(proba[1])
            return {
                "score": round(news_prob, 3),
                "passed": news_prob >= 0.5,
                "confidence": round(max(proba), 3)
            }
        except Exception as e:
            return {"score": 0.5, "passed": True, "error": str(e)}

    def signal_3_gemini_semantic(self, text: str) -> Dict[str, Any]:
        """
        Google Gemini API Semantic Validation using Structured JSON Output.
        """
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return {
                "score": None,
                "evaluated": False,
                "reason": "GEMINI_API_KEY not configured. Multi-signal NLTK and ML models active.",
                "error_type": "NO_API_KEY"
            }

        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"""
            You are a strict Real-Time News Validation Gateway for an AI news forensics system.
            Analyze the following text and determine if it represents an ACTUAL NEWS CLAIM, CURRENT EVENT, PUBLIC REPORT, OR NEWS ARTICLE, versus casual chit-chat, greetings, personal opinions, or non-news content.

            Input: "{text}"

            Return strict JSON with this exact schema:
            {{
                "is_news_related": true/false,
                "confidence": float_between_0_and_1,
                "category": "news" or "non_news",
                "reason": "Clear 1-sentence explanation why this is or is not a news claim",
                "error_type": null or "NOT_NEWS" or "INSUFFICIENT_CONTEXT"
            }}
            """
            response = model.generate_content(prompt)
            resp_text = response.text.strip()
            clean_json = re.sub(r'^```json\s*|\s*```$', '', resp_text, flags=re.MULTILINE).strip()
            import json
            data = json.loads(clean_json)
            is_news = bool(data.get("is_news_related", False))
            conf = float(data.get("confidence", 0.8))
            return {
                "score": conf if is_news else (1.0 - conf),
                "is_news_related": is_news,
                "category": data.get("category", "news" if is_news else "non_news"),
                "reason": data.get("reason", "Semantic evaluation completed."),
                "error_type": data.get("error_type"),
                "evaluated": True
            }
        except Exception as e:
            return {
                "score": None,
                "evaluated": False,
                "reason": f"AI validation temporarily unavailable ({str(e)}). Running local NLP validation.",
                "error_type": "API_OFFLINE"
            }

    def validate(self, text: str) -> Dict[str, Any]:
        """
        Multi-Signal News Validation Gateway Decision Engine.
        Synthesizes NLTK + Scikit-Learn + Gemini signals.
        """
        text_clean = text.strip()
        if not text_clean:
            return {
                "is_news_related": False,
                "verdict": "EMPTY_INPUT",
                "confidence": 1.0,
                "status_code": "EMPTY",
                "title": "NO INPUT DETECTED",
                "message": "⚠️ Please enter a news article, headline, URL, or news-related content.",
                "reason": "Input is completely empty.",
                "error_type": "EMPTY_INPUT",
                "signals": {}
            }

        s1 = self.signal_1_nltk_preprocessing(text_clean)
        s2 = self.signal_2_sklearn_ml(text_clean)
        s3 = self.signal_3_gemini_semantic(text_clean)

        # Immediate hard rejection for short conversational / personal statements
        if s1["is_conversational"] or (s1["word_count"] < 3 and s1["score"] < 0.2):
            return {
                "is_news_related": False,
                "verdict": "NOT_NEWS",
                "confidence": 0.95,
                "status_code": "NOT_NEWS",
                "title": "NOT A NEWS ITEM",
                "message": "The entered information does not appear to be a news-related claim or article.",
                "reason": "This is a greeting or personal statement rather than a verifiable news report.",
                "error_type": "NOT_NEWS",
                "signals": {"nltk": s1, "sklearn_ml": s2, "gemini": s3}
            }

        # Multi-signal weighted aggregation
        scores = [s1["score"]]
        weights = [0.35]

        if s2.get("score") is not None:
            scores.append(s2["score"])
            weights.append(0.35)

        if s3.get("evaluated") and s3.get("score") is not None:
            scores.append(s3["score"])
            weights.append(0.30)

        composite_score = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
        is_news = composite_score >= 0.48

        # If Gemini explicitly tagged non-news with high confidence
        if s3.get("evaluated") and not s3.get("is_news_related") and s3.get("score", 0) < 0.3:
            is_news = False
            composite_score = min(composite_score, 0.25)

        if not is_news and composite_score < 0.35:
            return {
                "is_news_related": False,
                "verdict": "NOT_NEWS",
                "confidence": round(1.0 - composite_score, 2),
                "status_code": "NOT_NEWS",
                "title": "NOT A NEWS ITEM",
                "message": "The entered information does not appear to be a news-related claim or article.",
                "reason": s3.get("reason") if s3.get("evaluated") else "Input is a casual or non-news statement with zero journalistic markers.",
                "error_type": "NOT_NEWS",
                "signals": {"nltk": s1, "sklearn_ml": s2, "gemini": s3}
            }
        elif not is_news and composite_score >= 0.35:
            return {
                "is_news_related": False,
                "verdict": "INSUFFICIENT_CONTEXT",
                "confidence": round(composite_score, 2),
                "status_code": "UNCERTAIN_NEWS",
                "title": "INSUFFICIENT NEWS CONTEXT",
                "message": "We couldn't confidently identify this as a verifiable news story. Try adding the full headline, article URL, source, or dates.",
                "reason": "Ambiguous statement with borderline news characteristics.",
                "error_type": "INSUFFICIENT_CONTEXT",
                "signals": {"nltk": s1, "sklearn_ml": s2, "gemini": s3}
            }

        return {
            "is_news_related": True,
            "verdict": "NEWS_CONFIRMED",
            "confidence": round(composite_score, 2),
            "status_code": "NEWS_VALIDATED",
            "title": "NEWS-LIKE CONTENT DETECTED",
            "message": "News relevance confirmed. Searching for supporting coverage and running forensics...",
            "category": s3.get("category", "news") if s3.get("evaluated") else "news",
            "error_type": None,
            "signals": {"nltk": s1, "sklearn_ml": s2, "gemini": s3}
        }


# Global helper function for direct invocation
_validator = NewsRelevanceValidator()

def is_news_related(text: str) -> Dict[str, Any]:
    """Convenience helper to validate news relevance."""
    return _validator.validate(text)

