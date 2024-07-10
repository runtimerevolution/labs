import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from polyglot.detect import Detector
from labs.config import get_logger
import spacy

# Download necessary NLTK data files if not already downloaded
nltk.download('stopwords', quiet=True)

class NLP_Interface:
    def __init__(self, text: str = None):
        self.logger = get_logger(__name__)
        self.nlp = None
        self.language_code = 'en'
        self.language_name = 'english'
        if text:
            self.text = text
            self.language_code = self.detect_language(text)
            self.load_spacy_language(self.language_code)
            self.preprocessed_text = ' '.join(self.preprocess_text(text))

    def detect_language(self, text: str = None) -> str:
        if text:
            self.text = text
        try:
            detector = Detector(text)
            self.language_code = detector.language.code
            self.language_name = detector.language.name.lower()
            self.logger.debug(f"Language: '{self.language_code}'")
            return self.language_code
        except Exception as e:
            self.logger.error(f"Error detecting language: {str(e)}")
            return None

    def load_spacy_language(self, language: str = None) -> str:
        if language:
            self.language_code = language
        try:
            if self.language_code == 'pt':
                self.nlp = spacy.load('pt_core_news_md')
            else:
                self.nlp = spacy.load('en_core_web_md')
        except Exception as e:
            self.logger.error(f"Error loading Spacy model: {str(e)}")
        return self.language_name

    def preprocess_text(self, text: str = None) -> list:
        if text:
            self.text = text
            self.detect_language(text)
            self.load_spacy_language(self.language_code)

        if not self.nlp:
            self.logger.error("Spacy language model is not loaded.")

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

    def sentiment_analysis(self, text: str = None):
        if text:
            self.text = text
            self.preprocessed_text = ' '.join(self.preprocess_text(text))
        try:
            if not self.nlp:
                self.logger.error("Spacy language model is not loaded.")
            self.nlp.add_pipe('spacytextblob')
            doc = self.nlp(self.preprocessed_text)
            return doc._.blob.sentiment_assessments.assessments
        except Exception as e:
            self.logger.error(f"Error during sentiment analysis: {str(e)}")

    def keyword_extraction(self, text: str = None) -> list:
        if text:
            self.text = text
            self.preprocessed_text = ' '.join(self.preprocess_text(text))
        try:
            if not self.nlp:
                self.logger.error("Spacy language model is not loaded.")
            doc = self.nlp(self.preprocessed_text)
            keywords = [chunk.text for chunk in doc.noun_chunks]
            return keywords
        except Exception as e:
            self.logger.error(f"Error during keyword extraction: {str(e)}")
        
    def ner(self, text: str = None):
        if text:
            self.text = text
            self.preprocessed_text = ' '.join(self.preprocess_text(text))
        try:
            if not self.nlp:
                self.logger.error("Spacy language model is not loaded.")
            doc = self.nlp(self.preprocessed_text)
            ner = self.nlp.add_pipe("ner")
            processed = ner(doc)
            return processed
        except Exception as e:
            self.logger.error(f"Error executing NER: {str(e)}")
            return None


