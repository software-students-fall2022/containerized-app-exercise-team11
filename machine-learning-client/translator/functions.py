# ! pip install git+https://github.com/openai/whisper.git -q
# ! pip install -q transformers sentencepiece

# ! sudo apt update && sudo apt install ffmpeg

import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import warnings


def record_audio(duration=8, output_file_name='translation_request.wav'):
  freq = 44100
  recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
  print(f"Recording audio for {duration} seconds. Speak now.")
  sd.wait()
  print("Recording finished.")
  write(output_file_name, freq, recording)


def transcribe(audio):
  '''
  Given the name of an audio file, returns a dictionary containing
  'english_text': the english translation
  'input_language': the language the audio file is in
  'input_text': the transcription in the 
  '''
  print('Transcribing audio...')
  warnings.filterwarnings("ignore", category=UserWarning) # blocks out warnings about machine preferences
  model = whisper.load_model("base")
  input_result = model.transcribe(audio) # TODO: would be great to do these in parallel
  translated_result = model.transcribe(audio,task="translate")
  print('Transciption complete!')
  return {
    'english_text': translated_result['text'].strip(),
    'input_language': translated_result['language'],
    'input_text': input_result['text'].strip()
  }


def insert_translation_to_db(client, translation):
  try:
    print('Inserting translation into database...')
    client.translator.translations.insert_one(translation)
    print('Insertion complete! Navigate to the webpage to see your translation.')
  except Exception as e:
    print('Translation cannot be inserted into the database.')
    raise e


def decode_message(message, target_language, model_tr, tokenizer):
  '''
  Returns the translated message as a string
  '''
  encoded_msg = tokenizer(message, return_tensors="pt")
  generated_tokens = model_tr.generate(**encoded_msg, forced_bos_token_id=tokenizer.get_lang_id(target_language))
  texts_tr = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
  return texts_tr[0]


def translate(text, output_language, model_tr, tokenizers):
  '''
  Wrapper for decode_message that handles tokenizers, user choice of output language, and errors
  '''
  try:
    print('Translating text...')
    if output_language == "en":
      result = text
    else:
      result = decode_message(text, output_language, model_tr, tokenizers[output_language])
    print('Text successfully translated!')
    return result
  except KeyError as ke: # catches if output_language is not a supported tokenizer language
    print('The language you selected is not supported. Please try again.')
    raise ke


def transcribe_and_translate(audio, output_language, model_tr, tokenizers):
  '''
  Given an audio file, return a dictionary that contains
  'outputText': the translation in the output language
  'outputLanguage': the output language specified
  'inputLanguage': the language the audio file is in
  'inputText': the transcription in the 
  NOTE: keys are different from the output of transcribe to match the mongodb schema
  '''
  
  transcription = transcribe(audio)
  translated_message = translate(transcription['english_text'], output_language, model_tr, tokenizers)
  return {
    'outputText': translated_message,
    'outputLanguage': output_language,
    'inputLanguage': transcription['input_language'],
    'inputText': transcription['input_text']
  }
