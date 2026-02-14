from typing import Dict, Any, List
import re
import json
import spacy

class NLPService:
    def __init__(self):
        # Load the spaCy model
        try:
            self.nlp = spacy.load('en_core_web_sm')
            self.model_loaded = True
            print('✓ spaCy model loaded successfully')
        except Exception as e:
            print(f'⚠ Could not load spaCy model: {e}')
            self.model_loaded = False
            self.nlp = None
    
    async def extract_information(self, message: str, questions: List[Dict]) -> Dict[str, Any]:
        """Extract structured information using spaCy NLP"""
        extracted = {}
        
        # Process with spaCy if available
        if self.model_loaded and self.nlp:
            doc = self.nlp(message)
        
        for question in questions:
            field_id = question['id']
            field_type = question.get('type', 'text')
            
            # Use spaCy for better extraction when possible
            if self.model_loaded and self.nlp:
                extracted[field_id] = self._extract_with_spacy(doc, field_type, question)
            else:
                # Fallback to rule-based
                extracted[field_id] = self._extract_rule_based(message, field_type, question)
        
        return extracted
    
    def _extract_with_spacy(self, doc, field_type: str, question: Dict) -> Any:
        """Extract information using spaCy"""
        if field_type == 'name':
            # Extract person names
            names = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
            return names[0] if names else None
            
        elif field_type == 'email':
            # Look for email pattern
            import re
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            match = re.search(email_pattern, doc.text)
            return match.group(0) if match else None
            
        elif field_type == 'phone':
            # Look for phone numbers
            import re
            phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            match = re.search(phone_pattern, doc.text)
            return match.group(0) if match else None
            
        elif field_type == 'location':
            # Extract locations (GPE = Geopolitical Entity)
            locations = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
            return locations[0] if locations else None
            
        elif field_type == 'date':
            # Extract dates
            dates = [ent.text for ent in doc.ents if ent.label_ == 'DATE']
            return dates[0] if dates else None
            
        elif field_type == 'organization':
            # Extract organizations
            orgs = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
            return orgs[0] if orgs else None
            
        elif field_type == 'number':
            # Extract numbers
            import re
            numbers = re.findall(r'\d+', doc.text)
            return int(numbers[0]) if numbers else None
            
        else:
            # For text fields, return the whole message
            return doc.text.strip()
    
    def _extract_rule_based(self, message: str, field_type: str, question: Dict) -> Any:
        """Fallback rule-based extraction"""
        import re
        
        if field_type == 'email':
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            match = re.search(email_pattern, message)
            return match.group(0) if match else None
            
        elif field_type == 'phone':
            phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            match = re.search(phone_pattern, message)
            return match.group(0) if match else None
            
        elif field_type == 'number':
            numbers = re.findall(r'\d+', message)
            return int(numbers[0]) if numbers else None
            
        elif field_type == 'date':
            date_pattern = r'\d{4}-\d{2}-\d{2}'
            match = re.search(date_pattern, message)
            return match.group(0) if match else None
            
        else:
            return message.strip()
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment using spaCy or fallback"""
        if self.model_loaded and self.nlp:
            doc = self.nlp(text)
            
            # Simple sentiment analysis based on adjective polarity
            positive_words = 0
            negative_words = 0
            
            # Common positive/negative words (simplified)
            positive_adj = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
            negative_adj = ['bad', 'terrible', 'awful', 'horrible', 'poor', 'worst']
            
            for token in doc:
                if token.pos_ == 'ADJ':
                    if token.text.lower() in positive_adj:
                        positive_words += 1
                    elif token.text.lower() in negative_adj:
                        negative_words += 1
            
            total = positive_words + negative_words
            if total == 0:
                return {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
            
            return {
                'positive': positive_words / total,
                'negative': negative_words / total,
                'neutral': 0.0
            }
        else:
            # Fallback to simple word-based sentiment
            return self._rule_based_sentiment(text)
    
    def _rule_based_sentiment(self, text: str) -> Dict[str, float]:
        """Simple rule-based sentiment analysis"""
        positive_words = ['good', 'great', 'excellent', 'happy', 'love', 'best', 'amazing']
        negative_words = ['bad', 'worst', 'terrible', 'hate', 'awful', 'poor']
        
        text_lower = text.lower()
        words = text_lower.split()
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        total_words = len(words)
        if total_words == 0:
            return {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
        
        return {
            'positive': positive_count / total_words,
            'negative': negative_count / total_words,
            'neutral': 1 - ((positive_count + negative_count) / total_words)
        }
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using spaCy"""
        skills = []
        
        if self.model_loaded and self.nlp:
            doc = self.nlp(text)
            
            # Common tech skills to look for
            tech_skills = [
                'python', 'java', 'javascript', 'react', 'angular', 'vue',
                'sql', 'mongodb', 'postgresql', 'mysql', 'aws', 'azure',
                'docker', 'kubernetes', 'jenkins', 'git', 'machine learning',
                'data science', 'ai', 'artificial intelligence', 'deep learning'
            ]
            
            text_lower = text.lower()
            for skill in tech_skills:
                if skill in text_lower and skill not in skills:
                    skills.append(skill)
        
        return skills
