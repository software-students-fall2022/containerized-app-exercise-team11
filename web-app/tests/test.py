from flaskr import create_app
from flaskr.db import get_translations_collection, insert_sample_data
import pytest
import mongomock
import os

class Tests: # pragma: no cover
    @pytest.fixture
    def mongo_client(self):
        mock_client = mongomock.MongoClient('mongodb://localhost:27017')
        mock_translations_collection = mock_client.translator.translations
        mock_translations_collection.insert_one({
            "inputLanguage": "de",
            "inputText": "Guten tag.",
            "outputText": "Good morning."
        })
        mock_translations_collection.insert_one({
            "inputLanguage": "es",
            "inputText": "Mucho gusto.",
            "outputText": "Nice to meet you."
        })
        mock_translations_collection.insert_one({
            "inputLanguage": "fr",
            "inputText": "Pardon, excusez-moi.",
            "outputText": "Pardon, excuse me."
        })
        mock_translations_collection.insert_one({
            "inputLanguage": "ja",
            "inputText": "ごめんなさい。",
            "outputText": "I am sorry."
        })
        yield mock_client
        mock_translations_collection.drop()

    @pytest.fixture
    def app(self, mongo_client):
        app = create_app({
            "TESTING": True,
            "MONGO_CLIENT": mongo_client
        })
        return app

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_insert_sample_data(self, mongo_client): 
        mongo_client.translator.translations.drop()
        assert get_translations_collection(mongo_client).find_one({"inputLanguage":"de"}) is None

        dir_path = os.path.dirname(os.path.realpath(__file__))
        sample_data_path = os.path.join(dir_path, './sample_data.json')
        insert_sample_data(mongo_client, sample_data_path)

        assert get_translations_collection(mongo_client).find_one({"inputLanguage":"de"}) is not None
        

    def test_get_translations_collection(self, mongo_client):
        translations_collection = get_translations_collection(mongo_client)
        input_languages = ["de", "es", "fr", "ja"]
        for input_language in input_languages:
            assert translations_collection.find_one({"inputLanguage": input_language}) is not None
        assert translations_collection.find_one({"inputLanguage": "zh"}) is None

    # TODO: testing the homepage may prove difficult because of the javascript in it

    def test_get_history(self, client):
        response = client.get("/history")
        assert b"<td>de</td>" in response.data
        assert b"<td>es</td>" in response.data
        assert b"<td>fr</td>" in response.data
        assert b"<td>ja</td>" in response.data
        assert b"<td>zh</td>" not in response.data

    def test_translation_endpoint(self, client):
        response = client.get("/translation")
        assert b'"inputLanguage":"ja"' in response.data
        assert b'"inputLanguage":"fr"' not in response.data

    def test_translation_endpoint_update(self, client, mongo_client):
        response1 = client.get("/translation")
        assert b'"inputLanguage":"ja"' in response1.data
        assert b'"inputLanguage":"zh"' not in response1.data

        mongo_client.translator.translations.insert_one({
            "inputLanguage": "zh",
            "inputText": "不用谢。",
            "outputText": "You're welcome."
        })

        response2 = client.get("/translation")
        assert b'"inputLanguage":"zh"' in response2.data
        assert b'"inputLanguage":"ja"' not in response2.data
