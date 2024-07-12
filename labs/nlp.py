import nltk
from nltk.corpus import stopwords
from polyglot.detect import Detector
from labs.config import get_logger, spacy_models, SUMMARIZATION_MODEL
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from transformers import pipeline
import json

# Download necessary NLTK data files if not already downloaded
nltk.download('stopwords', quiet=True)

class NLP_Interface:
    def __init__(self, text: str = None):
        self.logger = get_logger(__name__)
        self.nlp = None
        self.language_code = 'en'
        self.language_name = 'english'
        self.default_spacy_model = self.find_spacy_model(self.language_code)
        self.spacy_model = self.default_spacy_model
        self.text = text
        if text:
            self.language_code = self.detect_language()
            self.load_spacy_language()
            self.preprocessed_text = ' '.join(self.preprocess_text())
        else:
            self.text = ''
            self.preprocessed_text = ''

    def detect_language(self) -> str:
        try:
            detector = Detector(self.text)
            self.language_code = detector.language.code
            self.language_name = detector.language.name.lower()
            self.logger.debug(f"Language detected: '{self.language_code}'")
            return self.language_code
        except Exception as e:
            self.logger.error(f"Error detecting language: {str(e)}")
            return 'en'  # default to English if detection fails
        
    def find_spacy_model(self, language_code):
        for model in spacy_models:
            if model['language_code'] == language_code:
                return model['model']
        return None

    def load_spacy_language(self):
        try:
            model = self.find_spacy_model(self.language_code)
            if model:
                self.spacy_model = model
            self.nlp = spacy.load(self.spacy_model)
            self.logger.debug(f"Loaded Spacy model for language: '{self.language_code}'")
            return True
        except Exception as e:
            self.logger.error(f"Error loading Spacy model: {str(e)}")
            self.nlp = spacy.load(self.default_spacy_model)  # fallback to default model
            return False

    def preprocess_text(self) -> list:
        if not self.nlp:
            self.logger.error("Spacy language model is not loaded.")
            return []

        try:
            # Tokenization
            doc = self.nlp(self.text)
            tokens = [token.text for token in doc]

            # Normalization (lowercasing)
            tokens_normalized = [token.lower() for token in tokens]

            # Remove punctuation
            tokens_wo_punctuation = [token for token in tokens_normalized if token.isalnum()]

            # Stopword Removal
            stop_words = set(stopwords.words(self.language_name))
            tokens_wo_stopwords = [token for token in tokens_wo_punctuation if token not in stop_words]

            # Lemmatization
            doc = self.nlp(' '.join(tokens_wo_stopwords))
            output_tokens = [token.lemma_ for token in doc]

            return output_tokens
        except Exception as e:
            self.logger.error(f"Error during text preprocessing: {str(e)}")
            return []

    def sentiment_analysis(self):
        try:
            if not self.nlp:
                self.logger.error("Spacy language model is not loaded.")
                return None
            self.nlp.add_pipe('spacytextblob')
            doc = self.nlp(self.preprocessed_text)
            result = {
                'polarity': doc._.polarity,
                'subjectivity': doc._.subjectivity,
            }
            return result
        except Exception as e:
            self.logger.error(f"Error during sentiment analysis: {str(e)}")
            return None

    def keyword_extraction(self) -> list:
        try:
            if not self.nlp:
                self.logger.error("Spacy language model is not loaded.")
                return []
            doc = self.nlp(self.preprocessed_text)
            keywords = [chunk.text for chunk in doc.noun_chunks]
            return keywords
        except Exception as e:
            self.logger.error(f"Error during keyword extraction: {str(e)}")
            return []

    def ner(self):
        try:
            if not self.nlp:
                self.logger.error("Spacy language model is not loaded.")
                return None
            doc = self.nlp(text=self.preprocessed_text)
            return doc.ents
        except Exception as e:
            self.logger.error(f"Error executing NER: {str(e)}")
            return None
        
    def summarization(self):
        try:
            doc = self.nlp(self.text)
            tokens = [token.text for token in doc]
            minlen = 15
            maxlen = max(len(tokens), minlen +1)
            summarizer = pipeline("summarization", model=SUMMARIZATION_MODEL)
            result = summarizer(self.text, max_length=maxlen, min_length=15, do_sample=False)
            return result[0]['summary_text']
        except Exception as e:
            self.logger.error(f"Error during summarization: {str(e)}")
            return ''

    def run(self):
        keywords = self.keyword_extraction()
        sentiment = self.sentiment_analysis()
        summary = self.summarization()
        ner = self.ner()
        ner_list = []

        for ent in ner:
            ner_list.append({
                "text": ent.text,
                "label": ent.label_,
                "explanation": spacy.explain(ent.label_)
            })
        
        result = {
            "language": self.language_name,
            "language_code": self.language_code,
            "keywords": keywords,
            "sentiment": sentiment,
            "summary": summary,
            "named-entities": ner_list
        }
        
        return result
