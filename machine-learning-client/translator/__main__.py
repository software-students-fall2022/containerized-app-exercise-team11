import pymongo
import os
import translator.functions as functions
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

if __name__ == '__main__':
  # initialize
  print('Initializing translator, please wait...')
  client = pymongo.MongoClient('mongodb://localhost:27017')
  audio_path = os.path.join(os.getcwd(),'translation_request.wav')

  ckpt = 'facebook/m2m100_418M'
  model_tr = M2M100ForConditionalGeneration.from_pretrained(ckpt)
  toks={}

  toks["fr"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="fr")
  toks["es"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="es")
  toks["hi"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="hi")
  toks["de"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="de")
  print('Translator is initialized!')

  # user loop
  while True:
    # Ask the user how long to record audio for.
    print("How long would you like to record audio for? (Default: 8 seconds)\n" +
    "If you would like to quit, enter any non-numeric value.\n" +
    "!!!! Note: The recording will start once you hit Enter. !!!!\n"
    )

    # Parse input, decide what to do.
    duration = input("Audio recording length (in seconds): ")
    if duration == "":
      duration = 8
    else:
      try:
        duration = int(duration)
      except ValueError:
        break

    # Start recording audio.
    audio_in=functions.record_audio(duration=duration, output_file_name=audio_path)

    # Ask the user what they would like to do with their recorded audio.
    print(
      "What would you like to do today? Press Enter for English transcription.\n" +
      "Or, translate your message, use one of the following numbers:\n" +
      "    1. French\n" +
      "    2. Spanish\n" +
      "    3. Hindi\n" +
      "    4. German\n" +
      "Enter anything else to quit.\n"
    )
    num = input("Make a selection: ")
    
    if num=="":
      tr_lang="en"
    elif num=="1":
      tr_lang="fr"
    elif num=="2":
      tr_lang="es"
    elif num=="3":
      tr_lang="hi"
    elif num=="4":
      tr_lang="de"
    else:
      break
    try:
      translation = functions.transcribe_and_translate(audio_path, tr_lang, model_tr, toks)
      functions.insert_translation_to_db(client, translation)
    except Exception as e:
      print('Execution unsuccessful.')
  
  # remove audio artifact
  if os.path.exists(audio_path):
    os.remove(audio_path)
