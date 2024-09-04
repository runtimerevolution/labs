from langdetect import detect
from labs.config import get_logger, spacy_models, SUMMARIZATION_MODEL
import spacy

# Do not remove this import as it is used for self.nlp.add_pipe("spacytextblob")
from spacytextblob.spacytextblob import SpacyTextBlob  # noqa: F401
from spacy.lang.en.stop_words import STOP_WORDS as stop_words_en
from spacy.lang.pt.stop_words import STOP_WORDS as stop_words_pt
from string import punctuation
from heapq import nlargest
from transformers import pipeline


class NLP_Interface:
    def __init__(self, text: str = None):
        self.logger = get_logger(__name__)
        self.nlp = None
        self.language_code = "en"
        self.language_name = "english"
        self.default_spacy_model = self.find_spacy_model(self.language_code)
        self.spacy_model = self.default_spacy_model
        self.text = text
        self.text = self.text.replace("\n\n", "\n")
        if text:
            self.language_code = self.detect_language()
            self.load_spacy_language()
            if self.language_code == "pt":
                self.stop_words = stop_words_pt
            else:
                self.stop_words = stop_words_en
            self.preprocessed_text = " ".join(self.preprocess_text())
        else:
            self.text = ""
            self.preprocessed_text = ""
            self.stop_words = []

    def detect_language(self) -> str:
        try:
            language = detect(self.text)
            self.language_code = language
            self.language_name = language
            self.logger.debug(f"Language detected: '{self.language_code}'")
            return self.language_code
        except Exception as e:
            self.logger.error(f"Error detecting language: {str(e)}")
            return "en"  # default to English if detection fails

    def find_spacy_model(self, language_code):
        for model in spacy_models:
            if model["language_code"] == language_code:
                return model["model"]
        return None

    def load_spacy_language(self):
        try:
            model = self.find_spacy_model(self.language_code)
            if model:
                self.spacy_model = model
            self.nlp = spacy.load(self.spacy_model)
            self.logger.debug(
                f"Loaded Spacy model for language: '{self.language_code}'"
            )
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
            tokens_wo_punctuation = [
                token for token in tokens_normalized if token.isalnum()
            ]

            # Stopword Removal
            tokens_wo_stopwords = [
                token for token in tokens_wo_punctuation if token not in self.stop_words
            ]

            # Lemmatization
            doc = self.nlp(" ".join(tokens_wo_stopwords))
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
            self.nlp.add_pipe("spacytextblob")
            doc = self.nlp(self.preprocessed_text)
            result = {
                "polarity": doc._.polarity,
                "subjectivity": doc._.subjectivity,
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

    def summarization(self, percentage):
        try:
            doc = self.nlp(self.text)
            tokens = [token.text for token in doc]
            minlen = 1
            maxlen = max(int(len(tokens) * percentage), minlen + 1)
            summarizer = pipeline("summarization", model=SUMMARIZATION_MODEL)
            result = summarizer(
                self.text, max_length=maxlen, min_length=minlen, do_sample=False
            )
            return result[0]["summary_text"]
        except Exception as e:
            self.logger.error(f"Error during summarization: {str(e)}")
            return ""

    def spacy_summarization(self, percentage):
        try:
            doc = self.nlp(self.text)
            # tokens=[token.text for token in doc]
            freq_of_word = dict()
            # Text cleaning and vectorization
            for word in doc:
                if word.text.lower() not in list(self.stop_words):
                    if word.text.lower() not in punctuation:
                        if word.text not in freq_of_word.keys():
                            freq_of_word[word.text] = 1
                        else:
                            freq_of_word[word.text] += 1

            # Maximum frequency of word
            max_freq = max(freq_of_word.values())

            # Normalization of word frequency
            for word in freq_of_word.keys():
                freq_of_word[word] = freq_of_word[word] / max_freq

            # In this part, each sentence is weighed based on how often it contains the token.
            sent_tokens = [sent for sent in doc.sents]
            # If there is only one sentence, just return the text.
            if len(sent_tokens) == 1:
                return self.text
            sent_scores = dict()
            for sent in sent_tokens:
                for word in sent:
                    if word.text.lower() in freq_of_word.keys():
                        if sent not in sent_scores.keys():
                            sent_scores[sent] = freq_of_word[word.text.lower()]
                        else:
                            sent_scores[sent] += freq_of_word[word.text.lower()]

            num_sent = len(sent_tokens) * percentage
            len_tokens = int(num_sent)

            # It must write at least one sentence
            if len_tokens < 1:
                len_tokens = 1

            # If the number of sentences is not integer, add one sentence
            if (num_sent - len_tokens) > 0:
                len_tokens += 1

            # print("Number of sentences: ", len_tokens)

            # Summary for the sentences with maximum score. Here, each sentence in the list is of spacy.span type
            summary = nlargest(n=len_tokens, iterable=sent_scores, key=sent_scores.get)

            # Sort the selected sentences based on their original order in the text
            summary_sorted = sorted(summary, key=lambda sent: sent.start)

            # Prepare for final summary
            final_summary = [word.text for word in summary_sorted]

            # convert to a string
            result = " ".join(final_summary)

            # Return final summary
            return result
        except Exception as e:
            self.logger.error(f"Error during spacy summarization: {str(e)}")
            return ""

    def generate_title(self):
        try:
            doc = self.nlp(self.text)

            # Extract named entities and noun chunks as potential title candidates
            entities = [ent.text for ent in doc.ents]
            noun_chunks = [chunk.text for chunk in doc.noun_chunks]

            # Combine entities and noun chunks to form the title
            title_candidates = entities + noun_chunks

            # Filter out very short candidates
            title_candidates = [
                cand for cand in title_candidates if len(cand.split()) > 1
            ]
            # Join the top few candidates to create a title
            title = " ".join(title_candidates[0])

            return title
        except Exception as e:
            self.logger.error(f"Error during title generation: {str(e)}")
            return ""

    def run(self):
        keywords = self.keyword_extraction()
        sentiment = self.sentiment_analysis()
        summary = self.spacy_summarization(0.5)
        ner = self.ner()
        ner_list = []

        for ent in ner:
            ner_list.append(
                {
                    "text": ent.text,
                    "label": ent.label_,
                    "explanation": spacy.explain(ent.label_),
                }
            )

        result = {
            "language": self.language_name,
            "language_code": self.language_code,
            "keywords": keywords,
            "sentiment": sentiment,
            "summary": summary,
            "named-entities": ner_list,
        }

        return result
