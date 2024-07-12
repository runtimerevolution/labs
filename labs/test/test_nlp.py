import pytest
from labs.nlp import NLP_Interface

# Fixture for NLP_Interface instance with a sample text
@pytest.fixture
def NLP_Interface_fixture():
    return NLP_Interface("Sample text for testing purposes.")

# Test cases

def test_language_detection(NLP_Interface_fixture):  # Use NLP_Interface_fixture here
    NLP_Interface_instance = NLP_Interface_fixture
    assert NLP_Interface_instance.detect_language() == 'en'

def test_spacy_model_loading(NLP_Interface_fixture):  # Use NLP_Interface_fixture here
    NLP_Interface_instance = NLP_Interface_fixture
    result = NLP_Interface_instance.load_spacy_language()
    assert result is True

def test_text_preprocessing(NLP_Interface_fixture):  # Use NLP_Interface_fixture here
    NLP_Interface_instance = NLP_Interface_fixture
    preprocessed_text = NLP_Interface_instance.preprocess_text()
    assert len(preprocessed_text) > 0

def test_sentiment_analysis(NLP_Interface_fixture):  # Use NLP_Interface_fixture here
    NLP_Interface_instance = NLP_Interface_fixture
    sentiment = NLP_Interface_instance.sentiment_analysis()
    assert sentiment is not None

def test_keyword_extraction(NLP_Interface_fixture):  # Use NLP_Interface_fixture here
    NLP_Interface_instance = NLP_Interface_fixture
    keywords = NLP_Interface_instance.keyword_extraction()
    assert len(keywords) > 0

def test_ner(NLP_Interface_fixture):  # Use NLP_Interface_fixture here
    NLP_Interface_instance = NLP_Interface_fixture
    ner_result = NLP_Interface_instance.ner()
    assert ner_result is not None

def test_summarization(NLP_Interface_fixture):  # Use NLP_Interface_fixture here
    NLP_Interface_instance = NLP_Interface_fixture
    summary = NLP_Interface_instance.summarization()
    assert summary.strip() != ''

def test_run_method(NLP_Interface_fixture):  # Use NLP_Interface_fixture here
    NLP_Interface_instance = NLP_Interface_fixture
    result = NLP_Interface_instance.run()
    assert result is not None
