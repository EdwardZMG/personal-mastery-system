"""
NLP Module for Edward Growth System
Provides intent classification, entity extraction, and text analysis
"""
import re
from typing import Dict, List, Optional, Tuple
from enum import Enum


class IntentType(str, Enum):
    """Knowledge insight intent types"""
    IDEA = "idea"
    QUESTION = "question"
    NOTE = "note"
    TASK = "task"
    REFLECTION = "reflection"
    INSIGHT = "insight"


class DomainType(str, Enum):
    """Knowledge domain categories"""
    AI = "AI"
    MARKETING = "marketing"
    CHINESE_CLASSICS = "chinese_classics"
    ENGLISH = "english"
    SPEAKING = "speaking"
    GENERAL = "general"


class IntentClassifier:
    """
    Classify the intent of user input text
    
    Uses keyword matching and pattern recognition to determine
    whether the input is an idea, question, note, task, reflection, or insight.
    
    TODO: Replace with trained BERT model for higher accuracy
    """
    
    # Keyword patterns for each intent type
    PATTERNS = {
        IntentType.QUESTION: [
            r'如何', r'怎么', r'什么', r'为什么', r'能否', r'是否',
            r'what', r'how', r'why', r'can', r'is', r'are', r'\?'
        ],
        IntentType.IDEA: [
            r'想法', r'或许', r'也许', r'可能', r'建议', r'构思',
            r'idea', r'maybe', r'perhaps', r'think', r'suggest'
        ],
        IntentType.TASK: [
            r'任务', r'要做', r'待办', r'计划', r'目标', r'必须',
            r'task', r'todo', r'need to', r'must', r'should', r'plan'
        ],
        IntentType.REFLECTION: [
            r'反思', r'感悟', r'体会', r'心得', r'总结', r'回顾',
            r'reflect', r'review', r'feel', r'learned', r'realize'
        ],
        IntentType.INSIGHT: [
            r'洞察', r'启发', r'领悟', r'发现', r'理解', r'本质',
            r'insight', r'discover', r'realize', r'understand', r'essence'
        ]
    }
    
    @classmethod
    def classify(cls, text: str) -> Tuple[IntentType, float]:
        """
        Classify the intent of the given text
        
        Args:
            text: Input text to classify
            
        Returns:
            Tuple of (intent_type, confidence_score)
        """
        if not text or not text.strip():
            return IntentType.NOTE, 0.0
        
        text_lower = text.lower()
        scores = {}
        
        # Calculate score for each intent type
        for intent, patterns in cls.PATTERNS.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
                score += matches * 0.3  # Each match adds 0.3 confidence
            
            # Normalize score (cap at 1.0)
            scores[intent] = min(score, 1.0)
        
        # Find highest scoring intent
        if not scores or max(scores.values()) == 0:
            return IntentType.NOTE, 0.5  # Default to note with medium confidence
        
        best_intent = max(scores, key=scores.get)
        confidence = scores[best_intent]
        
        return best_intent, confidence


class DomainClassifier:
    """
    Classify text into knowledge domains
    
    Uses keyword matching to determine which learning domain
    the content belongs to.
    
    TODO: Replace with multi-label classification model
    """
    
    # Domain keywords
    DOMAIN_KEYWORDS = {
        DomainType.AI: [
            r'AI', r'人工智能', r'机器学习', r'深度学习', r'神经网络',
            r'agent', r'代理', r'算法', r'模型', r'训练',
            r'artificial intelligence', r'machine learning', r'deep learning'
        ],
        DomainType.MARKETING: [
            r'营销', r'市场', r'品牌', r'推广', r'转化', r'漏斗',
            r'marketing', r'brand', r'conversion', r'funnel', r'campaign'
        ],
        DomainType.CHINESE_CLASSICS: [
            r'道德经', r'金刚经', r'易经', r'孙子兵法', r'国学', r'经典',
            r'老子', r'孔子', r'孟子', r'庄子', r'禅宗',
            r'chinese classics', r'tao te ching', r'i ching'
        ],
        DomainType.ENGLISH: [
            r'英语', r'英文', r'单词', r'语法', r'口语', r'听力',
            r'english', r'vocabulary', r'grammar', r'speaking', r'listening'
        ],
        DomainType.SPEAKING: [
            r'演讲', r'表达', r'沟通', r'汇报', r'展示', r'说服',
            r'speech', r'presentation', r'communication', r'public speaking'
        ]
    }
    
    @classmethod
    def classify(cls, text: str) -> Tuple[DomainType, float]:
        """
        Classify text into a knowledge domain
        
        Args:
            text: Input text to classify
            
        Returns:
            Tuple of (domain_type, confidence_score)
        """
        if not text or not text.strip():
            return DomainType.GENERAL, 0.0
        
        text_lower = text.lower()
        scores = {}
        
        # Calculate score for each domain
        for domain, patterns in cls.DOMAIN_KEYWORDS.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
                score += matches * 0.4  # Each match adds 0.4 confidence
            
            scores[domain] = min(score, 1.0)
        
        # Find highest scoring domain
        if not scores or max(scores.values()) == 0:
            return DomainType.GENERAL, 0.3
        
        best_domain = max(scores, key=scores.get)
        confidence = scores[best_domain]
        
        return best_domain, confidence


class EntityExtractor:
    """
    Extract key entities from text
    
    Identifies people, organizations, concepts, dates, and other
    important entities mentioned in the text.
    
    TODO: Integrate spaCy or BERT NER for better accuracy
    """
    
    @staticmethod
    def extract_entities(text: str) -> Dict[str, List[str]]:
        """
        Extract entities from text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with entity types as keys and lists of entities as values
        """
        entities = {
            "concepts": [],
            "people": [],
            "organizations": [],
            "dates": [],
            "numbers": []
        }
        
        # Extract quoted terms (potential concepts)
        quoted = re.findall(r'["""](.*?)["""]', text)
        entities["concepts"].extend(quoted)
        
        # Extract numbers
        numbers = re.findall(r'\d+\.?\d*%', text)
        entities["numbers"].extend(numbers)
        
        # Extract dates (simple patterns)
        dates = re.findall(r'\d{4}年\d{1,2}月\d{1,2}日|\d{4}-\d{2}-\d{2}', text)
        entities["dates"].extend(dates)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities


class TagGenerator:
    """
    Generate relevant tags for knowledge content
    
    Creates descriptive tags that help with categorization
    and searchability.
    
    TODO: Use TF-IDF or TextRank for better tag generation
    """
    
    @staticmethod
    def generate_tags(text: str, max_tags: int = 5) -> List[str]:
        """
        Generate tags from text
        
        Args:
            text: Input text
            max_tags: Maximum number of tags to generate
            
        Returns:
            List of generated tags
        """
        if not text:
            return []
        
        # Simple approach: extract meaningful phrases
        # Remove common stop words
        stop_words = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
            '都', '一', '一个', '上', '也', '很', '到', '说', '要',
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been'
        }
        
        # Extract potential keywords (simplified)
        words = re.findall(r'[\w]+', text.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 1]
        
        # Count frequency
        freq = {}
        for word in keywords:
            freq[word] = freq.get(word, 0) + 1
        
        # Sort by frequency and take top tags
        sorted_tags = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        tags = [tag for tag, _ in sorted_tags[:max_tags]]
        
        return tags


class NLPPipeline:
    """
    Complete NLP processing pipeline
    
    Orchestrates intent classification, domain classification,
    entity extraction, and tag generation.
    """
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.domain_classifier = DomainClassifier()
        self.entity_extractor = EntityExtractor()
        self.tag_generator = TagGenerator()
    
    def process(self, text: str, language: str = 'zh') -> Dict:
        """
        Process text through complete NLP pipeline
        
        Args:
            text: Input text to process
            language: Language code ('zh' or 'en')
            
        Returns:
            Dictionary with all NLP results
        """
        if not text or not text.strip():
            return {
                "intent": IntentType.NOTE.value,
                "intent_confidence": 0.0,
                "domain": DomainType.GENERAL.value,
                "domain_confidence": 0.0,
                "entities": {},
                "tags": [],
                "language": language
            }
        
        # Run all classifiers
        intent, intent_conf = self.intent_classifier.classify(text)
        domain, domain_conf = self.domain_classifier.classify(text)
        entities = self.entity_extractor.extract_entities(text)
        tags = self.tag_generator.generate_tags(text)
        
        return {
            "intent": intent.value,
            "intent_confidence": round(intent_conf, 2),
            "domain": domain.value,
            "domain_confidence": round(domain_conf, 2),
            "entities": entities,
            "tags": tags,
            "language": language,
            "word_count": len(text)
        }


# Convenience function for quick use
def analyze_text(text: str, language: str = 'zh') -> Dict:
    """
    Quick text analysis using NLP pipeline
    
    Args:
        text: Text to analyze
        language: Language code
        
    Returns:
        Analysis results dictionary
    """
    pipeline = NLPPipeline()
    return pipeline.process(text, language)
