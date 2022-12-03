from gtts import gTTS
import os
import subprocess
import pytest
from functions import *


def translation_accuracy_test():
    print("testing translation_accuracy_test...")
    text_to_translate = ["Você está com fome?", "Eu preciso de um carro!", "Donde esta mi madre?", "انا أحبك", "أنت كبير "]
    expected_result = ["Are you hungry?", "I need a car!", "Where is my mom?", "I love you", "You are big"]
    for i in range(len(text_to_translate)):
        assert expected_result[i] == translate(text_to_translate[i], "en"), "translation_accuracy_test: test failed"
        print("translation_accuracy_test: test passed")

def speech_to_text_test():
    print("testing speech_to_text_test...")
    sentences_to_speak = ["Are you hungry?", "I need a car!", "Where is my mom?", "I love you", "No problem"]
    for i in range(len(sentences_to_speak)):
        try:
            speak(sentences_to_speak[i], "en")
            print("speech_to_text_test: test passed")
        except:
            print("failed")
            assert False, "speech_to_text_test: test failed"

def translation_and_speech_test():
    print("testing translation_and_speech_test...")
    sentences_to_translate_and_speak = ["Você está com fome?", "Eu preciso de um carro!", "Donde esta mi madre?", "انا أحبك", "أنت كبير "]
    for i in range(len(sentences_to_translate_and_speak)):
        try:
            translate_and_speak(sentences_to_translate_and_speak[i], "en")
            print("Test passed")
        except:
            print("failed")
            assert False, "translation_and_speech_test: test failed"
    
def record_audio_test():
    print("testing record_audio_test...")
    try:
        record_audio()
        print("Test passed")
    except:
        print("failed")
        assert False, "record_audio_test: test failed"

if __name__ == "__main__":
    # translation_accuracy_test()
    speech_to_text_test()
    translation_and_speech_test()