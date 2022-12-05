import pymongo
import os
import translator.functions as functions
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

if __name__ == '__main__':
  # initialize
  print('Initilizing translator...')
  client = pymongo.MongoClient('mongodb://localhost:27017')
  audio_path = os.path.join(os.getcwd(),'translation_request.wav')

  ckpt = 'facebook/m2m100_418M'
  model_tr = M2M100ForConditionalGeneration.from_pretrained(ckpt)
  toks={}

  toks["fr"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="fr")
  toks["es"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="es")
  toks["hi"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="hi")
  toks["de"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="de")
  # toks["jp"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="jp")
  print('Translator is initialized!')


  # user loop
  while True:
    audio_in=functions.record_audio(output_file_name=audio_path)
    num =input(
      "Press Enter for English transcription.\n" +
      "To translate your message:\n" +
      "For French, press 1.\n" +
      "For Spanish, press 2.\n" +
      "For Hindi, press 3.\n" +
      "For German, press 4.\n" +
      "Enter anything else to quit"
    )
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
      print('Execution unsuccessful')
  
  # remove audio artifact
  if os.path.exists(audio_path):
    os.remove(audio_path)
