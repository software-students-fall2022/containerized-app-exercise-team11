import os
import pytest
import mongomock
import translator.functions as functions
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

class Tests: # pragma: no cover
    @pytest.fixture
    def mongo_client(self):
        mock_client = mongomock.MongoClient('mongodb://localhost:27017')
        yield mock_client
        mock_client.translator.translations.drop()

    @pytest.fixture
    def model_tr(self):
        ckpt = 'facebook/m2m100_418M'
        model_tr = M2M100ForConditionalGeneration.from_pretrained(ckpt)
        return model_tr
    
    @pytest.fixture
    def tokenizers(self):
        toks={}
        ckpt = 'facebook/m2m100_418M'
        toks["fr"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="fr")
        toks["es"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="es")
        toks["hi"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="hi")
        toks["de"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="de")
        return toks

    def test_transcription(self):
        french_audio_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'./test_audio/french_speech.mp3')
        french_transcription = functions.transcribe(french_audio_path)

        assert french_transcription['input_language'] == 'fr'
        assert 'my name is tristan' in french_transcription['english_text'].lower()
        assert "je m'appelle tristan" in french_transcription['input_text'].lower()
    
    def test_insert_translation_to_db(self, mongo_client):
        translation = {
            'outputText': 'Bonjour',
            'outputLanguage': 'fr',
            'inputLanguage': 'en',
            'inputText': 'Hello'
        }
        functions.insert_translation_to_db(mongo_client, translation)
        assert mongo_client.translator.translations.find_one(translation) is not None
    
    def test_decode_message(self, model_tr, tokenizers):
        decoded_message = functions.decode_message('Hello', 'fr', model_tr, tokenizers['fr'])
        assert decoded_message == 'Bonjour'
    
    def test_translate(self, model_tr, tokenizers):
        translated_message = functions.translate('Hello', 'fr', model_tr, tokenizers)
        assert translated_message == 'Bonjour'

    def test_translate_key_error(self, model_tr, tokenizers):
        with pytest.raises(KeyError):
            translated_message = functions.translate('Hello', 'invalid_output_language', model_tr, tokenizers)

    def test_transcribe_and_translate(self, model_tr, tokenizers):
        french_audio_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'./test_audio/french_speech.mp3')
        translation = functions.transcribe_and_translate(french_audio_path, 'de', model_tr, tokenizers)

        assert 'mein name ist tristan' in translation['outputText'].lower()
        assert 'de' == translation['outputLanguage']
        assert "je m'appelle tristan" in translation['inputText'].lower()
        assert 'fr' == translation['inputLanguage']
