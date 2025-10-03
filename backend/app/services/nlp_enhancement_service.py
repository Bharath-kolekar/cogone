"""
NLP Enhancement Service for advanced natural language processing
"""

import structlog
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import asyncio
import json
import re
from dataclasses import dataclass
from enum import Enum

logger = structlog.get_logger()


class NLPTask(str, Enum):
    """NLP task types"""
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    ENTITY_EXTRACTION = "entity_extraction"
    INTENT_CLASSIFICATION = "intent_classification"
    TEXT_SUMMARIZATION = "text_summarization"
    LANGUAGE_DETECTION = "language_detection"
    KEYWORD_EXTRACTION = "keyword_extraction"
    TEXT_CLASSIFICATION = "text_classification"
    NAMED_ENTITY_RECOGNITION = "named_entity_recognition"


@dataclass
class NLPAnalysis:
    """NLP analysis result"""
    task: NLPTask
    input_text: str
    result: Dict[str, Any]
    confidence: float
    processing_time: float
    timestamp: datetime


@dataclass
class SentimentResult:
    """Sentiment analysis result"""
    sentiment: str  # positive, negative, neutral
    score: float  # -1 to 1
    confidence: float
    emotions: Dict[str, float]  # anger, joy, fear, sadness, surprise


@dataclass
class EntityResult:
    """Entity extraction result"""
    entities: List[Dict[str, Any]]
    total_count: int
    categories: Dict[str, int]


@dataclass
class IntentResult:
    """Intent classification result"""
    intent: str
    confidence: float
    entities: List[Dict[str, Any]]
    parameters: Dict[str, Any]


class NLPEnhancementService:
    """Advanced NLP enhancement service"""
    
    def __init__(self):
        self.supported_languages = ["en", "hi", "ta", "te", "bn", "es", "fr", "de"]
        self.intent_patterns = {
            "create_app": [
                "create", "build", "make", "develop", "generate", "construct"
            ],
            "ask_question": [
                "what", "how", "why", "when", "where", "who", "which", "can you", "could you"
            ],
            "get_help": [
                "help", "assist", "support", "guide", "explain", "show me"
            ],
            "schedule_task": [
                "schedule", "remind", "set", "plan", "organize", "arrange"
            ],
            "send_message": [
                "send", "message", "text", "email", "notify", "contact"
            ]
        }
        self.sentiment_keywords = {
            "positive": ["good", "great", "excellent", "amazing", "wonderful", "fantastic", "love", "like", "happy", "pleased"],
            "negative": ["bad", "terrible", "awful", "horrible", "hate", "dislike", "angry", "frustrated", "sad", "disappointed"],
            "neutral": ["okay", "fine", "alright", "normal", "average", "standard", "regular"]
        }
    
    async def analyze_text(self, text: str, tasks: List[NLPTask] = None) -> Dict[str, NLPAnalysis]:
        """Perform comprehensive NLP analysis"""
        try:
            if not tasks:
                tasks = [NLPTask.SENTIMENT_ANALYSIS, NLPTask.ENTITY_EXTRACTION, NLPTask.INTENT_CLASSIFICATION]
            
            results = {}
            
            for task in tasks:
                start_time = datetime.now()
                
                if task == NLPTask.SENTIMENT_ANALYSIS:
                    result = await self._analyze_sentiment(text)
                elif task == NLPTask.ENTITY_EXTRACTION:
                    result = await self._extract_entities(text)
                elif task == NLPTask.INTENT_CLASSIFICATION:
                    result = await self._classify_intent(text)
                elif task == NLPTask.TEXT_SUMMARIZATION:
                    result = await self._summarize_text(text)
                elif task == NLPTask.LANGUAGE_DETECTION:
                    result = await self._detect_language(text)
                elif task == NLPTask.KEYWORD_EXTRACTION:
                    result = await self._extract_keywords(text)
                elif task == NLPTask.TEXT_CLASSIFICATION:
                    result = await self._classify_text(text)
                elif task == NLPTask.NAMED_ENTITY_RECOGNITION:
                    result = await self._recognize_named_entities(text)
                else:
                    continue
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                analysis = NLPAnalysis(
                    task=task,
                    input_text=text,
                    result=result,
                    confidence=result.get("confidence", 0.8),
                    processing_time=processing_time,
                    timestamp=datetime.now()
                )
                
                results[task.value] = analysis
            
            logger.info("NLP analysis completed", text_length=len(text), tasks=len(tasks))
            return results
            
        except Exception as e:
            logger.error("NLP analysis failed", error=str(e))
            raise e
    
    async def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        try:
            text_lower = text.lower()
            
            # Count sentiment keywords
            positive_count = sum(1 for word in self.sentiment_keywords["positive"] if word in text_lower)
            negative_count = sum(1 for word in self.sentiment_keywords["negative"] if word in text_lower)
            neutral_count = sum(1 for word in self.sentiment_keywords["neutral"] if word in text_lower)
            
            # Calculate sentiment score
            total_words = len(text.split())
            if total_words == 0:
                return {"sentiment": "neutral", "score": 0.0, "confidence": 0.5}
            
            positive_ratio = positive_count / total_words
            negative_ratio = negative_count / total_words
            neutral_ratio = neutral_count / total_words
            
            # Determine sentiment
            if positive_ratio > negative_ratio and positive_ratio > neutral_ratio:
                sentiment = "positive"
                score = positive_ratio - negative_ratio
            elif negative_ratio > positive_ratio and negative_ratio > neutral_ratio:
                sentiment = "negative"
                score = negative_ratio - positive_ratio
            else:
                sentiment = "neutral"
                score = 0.0
            
            # Calculate confidence
            confidence = max(positive_ratio, negative_ratio, neutral_ratio)
            
            # Extract emotions
            emotions = {
                "joy": positive_ratio,
                "anger": negative_ratio * 0.8,
                "fear": negative_ratio * 0.6,
                "sadness": negative_ratio * 0.7,
                "surprise": 0.1
            }
            
            return {
                "sentiment": sentiment,
                "score": score,
                "confidence": confidence,
                "emotions": emotions,
                "positive_ratio": positive_ratio,
                "negative_ratio": negative_ratio,
                "neutral_ratio": neutral_ratio
            }
            
        except Exception as e:
            logger.error("Sentiment analysis failed", error=str(e))
            return {"sentiment": "neutral", "score": 0.0, "confidence": 0.0}
    
    async def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text"""
        try:
            entities = []
            
            # Email extraction
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            for email in emails:
                entities.append({"text": email, "type": "email", "start": text.find(email), "end": text.find(email) + len(email)})
            
            # Phone number extraction
            phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
            phones = re.findall(phone_pattern, text)
            for phone in phones:
                phone_text = ''.join(phone)
                entities.append({"text": phone_text, "type": "phone", "start": text.find(phone_text), "end": text.find(phone_text) + len(phone_text)})
            
            # URL extraction
            url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            urls = re.findall(url_pattern, text)
            for url in urls:
                entities.append({"text": url, "type": "url", "start": text.find(url), "end": text.find(url) + len(url)})
            
            # Date extraction
            date_pattern = r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})\b'
            dates = re.findall(date_pattern, text)
            for date in dates:
                entities.append({"text": date, "type": "date", "start": text.find(date), "end": text.find(date) + len(date)})
            
            # Money extraction
            money_pattern = r'\$\d+(?:\.\d{2})?|\d+(?:\.\d{2})?\s*(?:dollars?|USD|rupees?|INR)'
            money = re.findall(money_pattern, text)
            for amount in money:
                entities.append({"text": amount, "type": "money", "start": text.find(amount), "end": text.find(amount) + len(amount)})
            
            # Categorize entities
            categories = {}
            for entity in entities:
                entity_type = entity["type"]
                categories[entity_type] = categories.get(entity_type, 0) + 1
            
            return {
                "entities": entities,
                "total_count": len(entities),
                "categories": categories,
                "confidence": 0.8
            }
            
        except Exception as e:
            logger.error("Entity extraction failed", error=str(e))
            return {"entities": [], "total_count": 0, "categories": {}, "confidence": 0.0}
    
    async def _classify_intent(self, text: str) -> Dict[str, Any]:
        """Classify intent from text"""
        try:
            text_lower = text.lower()
            
            # Calculate scores for each intent
            intent_scores = {}
            for intent, patterns in self.intent_patterns.items():
                score = sum(1 for pattern in patterns if pattern in text_lower)
                intent_scores[intent] = score
            
            # Find best intent
            if not intent_scores or max(intent_scores.values()) == 0:
                best_intent = "general_query"
                confidence = 0.3
            else:
                best_intent = max(intent_scores, key=intent_scores.get)
                confidence = min(0.9, intent_scores[best_intent] / len(text.split()) * 2)
            
            # Extract entities for intent
            entities = await self._extract_entities(text)
            
            # Extract parameters based on intent
            parameters = {}
            if best_intent == "create_app":
                parameters["app_type"] = self._extract_app_type(text)
                parameters["features"] = self._extract_features(text)
            elif best_intent == "schedule_task":
                parameters["date"] = self._extract_date(text)
                parameters["time"] = self._extract_time(text)
                parameters["task"] = self._extract_task_description(text)
            
            return {
                "intent": best_intent,
                "confidence": confidence,
                "entities": entities["entities"],
                "parameters": parameters,
                "intent_scores": intent_scores
            }
            
        except Exception as e:
            logger.error("Intent classification failed", error=str(e))
            return {"intent": "general_query", "confidence": 0.0, "entities": [], "parameters": {}}
    
    async def _summarize_text(self, text: str) -> Dict[str, Any]:
        """Summarize text"""
        try:
            sentences = text.split('.')
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) <= 2:
                return {"summary": text, "compression_ratio": 1.0, "confidence": 0.9}
            
            # Simple extractive summarization
            # Score sentences by word frequency
            word_freq = {}
            for sentence in sentences:
                words = sentence.lower().split()
                for word in words:
                    if len(word) > 3:  # Ignore short words
                        word_freq[word] = word_freq.get(word, 0) + 1
            
            # Score sentences
            sentence_scores = []
            for sentence in sentences:
                words = sentence.lower().split()
                score = sum(word_freq.get(word, 0) for word in words if len(word) > 3)
                sentence_scores.append((sentence, score))
            
            # Get top sentences
            sentence_scores.sort(key=lambda x: x[1], reverse=True)
            top_sentences = sentence_scores[:max(1, len(sentences) // 3)]
            summary = '. '.join([s[0] for s in top_sentences])
            
            compression_ratio = len(summary) / len(text)
            
            return {
                "summary": summary,
                "compression_ratio": compression_ratio,
                "confidence": 0.7,
                "original_length": len(text),
                "summary_length": len(summary)
            }
            
        except Exception as e:
            logger.error("Text summarization failed", error=str(e))
            return {"summary": text, "compression_ratio": 1.0, "confidence": 0.0}
    
    async def _detect_language(self, text: str) -> Dict[str, Any]:
        """Detect language of text"""
        try:
            # Simple language detection based on common words
            language_indicators = {
                "en": ["the", "and", "is", "in", "to", "of", "a", "that", "it", "with"],
                "hi": ["है", "और", "में", "के", "का", "की", "को", "से", "पर", "तो"],
                "ta": ["உள்ளது", "மற்றும்", "இல்", "ஆக", "என்று", "இது", "அது", "நான்", "நீங்கள்"],
                "te": ["ఉంది", "మరియు", "లో", "కు", "యొక్క", "ఇది", "అది", "నేను", "మీరు"],
                "bn": ["এবং", "এতে", "এটি", "একটি", "যা", "কি", "হয়", "থাকে", "করতে"]
            }
            
            text_lower = text.lower()
            language_scores = {}
            
            for lang, indicators in language_indicators.items():
                score = sum(1 for indicator in indicators if indicator in text_lower)
                language_scores[lang] = score
            
            if not language_scores or max(language_scores.values()) == 0:
                detected_lang = "en"  # Default to English
                confidence = 0.3
            else:
                detected_lang = max(language_scores, key=language_scores.get)
                confidence = min(0.9, language_scores[detected_lang] / len(text.split()) * 10)
            
            return {
                "language": detected_lang,
                "confidence": confidence,
                "language_scores": language_scores
            }
            
        except Exception as e:
            logger.error("Language detection failed", error=str(e))
            return {"language": "en", "confidence": 0.0}
    
    async def _extract_keywords(self, text: str) -> Dict[str, Any]:
        """Extract keywords from text"""
        try:
            # Remove common stop words
            stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should"}
            
            words = text.lower().split()
            words = [word.strip(".,!?;:") for word in words if len(word) > 2 and word not in stop_words]
            
            # Count word frequency
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top keywords
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            keywords = [word for word, freq in sorted_words[:10]]
            
            return {
                "keywords": keywords,
                "keyword_count": len(keywords),
                "total_words": len(words),
                "confidence": 0.8
            }
            
        except Exception as e:
            logger.error("Keyword extraction failed", error=str(e))
            return {"keywords": [], "keyword_count": 0, "total_words": 0, "confidence": 0.0}
    
    async def _classify_text(self, text: str) -> Dict[str, Any]:
        """Classify text into categories"""
        try:
            categories = {
                "question": ["what", "how", "why", "when", "where", "who", "which", "?"],
                "request": ["please", "can you", "could you", "would you", "help me"],
                "complaint": ["problem", "issue", "error", "bug", "broken", "not working"],
                "compliment": ["good", "great", "excellent", "amazing", "wonderful", "love", "like"],
                "instruction": ["create", "build", "make", "generate", "do", "perform", "execute"]
            }
            
            text_lower = text.lower()
            category_scores = {}
            
            for category, indicators in categories.items():
                score = sum(1 for indicator in indicators if indicator in text_lower)
                category_scores[category] = score
            
            if not category_scores or max(category_scores.values()) == 0:
                predicted_category = "general"
                confidence = 0.3
            else:
                predicted_category = max(category_scores, key=category_scores.get)
                confidence = min(0.9, category_scores[predicted_category] / len(text.split()) * 5)
            
            return {
                "category": predicted_category,
                "confidence": confidence,
                "category_scores": category_scores
            }
            
        except Exception as e:
            logger.error("Text classification failed", error=str(e))
            return {"category": "general", "confidence": 0.0}
    
    async def _recognize_named_entities(self, text: str) -> Dict[str, Any]:
        """Recognize named entities"""
        try:
            entities = []
            
            # Person names (simple pattern)
            person_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
            persons = re.findall(person_pattern, text)
            for person in persons:
                entities.append({"text": person, "type": "PERSON", "start": text.find(person), "end": text.find(person) + len(person)})
            
            # Organization names
            org_pattern = r'\b[A-Z][a-z]+ (?:Inc|Corp|LLC|Ltd|Company|Corporation)\b'
            orgs = re.findall(org_pattern, text)
            for org in orgs:
                entities.append({"text": org, "type": "ORG", "start": text.find(org), "end": text.find(org) + len(org)})
            
            # Location names (cities, countries)
            location_pattern = r'\b[A-Z][a-z]+(?: City| Town| State| Country)\b'
            locations = re.findall(location_pattern, text)
            for location in locations:
                entities.append({"text": location, "type": "LOCATION", "start": text.find(location), "end": text.find(location) + len(location)})
            
            return {
                "entities": entities,
                "entity_count": len(entities),
                "confidence": 0.7
            }
            
        except Exception as e:
            logger.error("Named entity recognition failed", error=str(e))
            return {"entities": [], "entity_count": 0, "confidence": 0.0}
    
    def _extract_app_type(self, text: str) -> str:
        """Extract app type from text"""
        app_types = {
            "todo": ["todo", "task", "reminder", "checklist"],
            "ecommerce": ["shop", "store", "buy", "sell", "product", "cart"],
            "blog": ["blog", "article", "post", "content"],
            "social": ["social", "chat", "message", "friend", "follow"],
            "dashboard": ["dashboard", "analytics", "report", "data"]
        }
        
        text_lower = text.lower()
        for app_type, keywords in app_types.items():
            if any(keyword in text_lower for keyword in keywords):
                return app_type
        
        return "general"
    
    def _extract_features(self, text: str) -> List[str]:
        """Extract features from text"""
        features = []
        feature_keywords = {
            "authentication": ["login", "signup", "auth", "user", "password"],
            "database": ["database", "data", "store", "save"],
            "api": ["api", "endpoint", "service", "integration"],
            "ui": ["ui", "interface", "design", "layout", "frontend"],
            "mobile": ["mobile", "app", "phone", "responsive"]
        }
        
        text_lower = text.lower()
        for feature, keywords in feature_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                features.append(feature)
        
        return features
    
    def _extract_date(self, text: str) -> str:
        """Extract date from text"""
        date_pattern = r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b'
        dates = re.findall(date_pattern, text)
        return dates[0] if dates else ""
    
    def _extract_time(self, text: str) -> str:
        """Extract time from text"""
        time_pattern = r'\b\d{1,2}:\d{2}(?:\s?[AP]M)?\b'
        times = re.findall(time_pattern, text)
        return times[0] if times else ""
    
    def _extract_task_description(self, text: str) -> str:
        """Extract task description from text"""
        # Simple extraction - could be enhanced
        return text.strip()
