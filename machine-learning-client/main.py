# ! pip install git+https://github.com/openai/whisper.git -q
# ! pip install -q transformers sentencepiece

# ! sudo apt update && sudo apt install ffmpeg


from gtts import gTTS
import os
import subprocess
import sounddevice as sd
from scipy.io.wavfile import write,read
import wavio as wv
import whisper
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


def record_audio():
    freq = 44100
    duration = 8
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)
    print("Recording audio for 8 seconds. Speak now.")
    sd.wait()
    print("Recording finished.")
    write("translation_request.wav", freq, recording)
    return "translation_request.wav"

model = whisper.load_model("base")

#taking audio file and returning transcription with details

def transcription(audio):
  result = model.transcribe(audio,task="translate")
  #print(result)
  return result

def text_translate(msg,model_tr,tokenizer,tr_lang):
  encoded_msg = tokenizer(msg, return_tensors="pt")
  generated_tokens = model_tr.generate(**encoded_msg, forced_bos_token_id=tokenizer.get_lang_id(tr_lang))
  texts_tr = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
  return texts_tr

ckpt = 'facebook/m2m100_418M'
model_tr = M2M100ForConditionalGeneration.from_pretrained(ckpt)
toks={}

toks["fr"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="fr")
toks["es"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="es")
toks["hi"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="hi")
toks["de"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="de")
toks["jp"] = M2M100Tokenizer.from_pretrained(ckpt,src_lang="en", tr_lang="jp")

traslationCount = 1

def translate(audio, outputlang):
    # SNEHEEL'S CODE HERE
    raw_msg = transcription(audio)
    text= raw_msg["text"]

    if outputlang == "en":
      return text
    else:
      result = text_translate(text,model_tr,toks[outputlang], outputlang)
      return result

def speak(text, lang):
    global traslationCount
    gtts_object = gTTS(text=text, lang=lang, slow=False)

    if os.path.exists('translations'):
        gtts_object.save("translations/"+str(traslationCount)+".wav")
        subprocess.call(["afplay","translations/"+str(traslationCount)+".wav"])
        traslationCount += 1
    else:
        os.mkdir('translations')
        gtts_object.save("translations/"+str(traslationCount)+".wav")
        subprocess.call(["afplay","translations/"+str(traslationCount)+".wav"])
        traslationCount += 1

def translate_and_speak(text, lang):
    try:
        translated_text = translate(text, lang)
        print(translated_text)
    except:
        print("An error occured while translating the text")
        raise Exception("An error occured while translating the text")
    try:
        speak(translated_text, lang)
    except:
        print("An error occured while speaking the text, but it was translated correctly")
        raise Exception("An error occured while speaking the text, but it was translated correctly")

if __name__ =="__main__":
  
  while True:
    choice=input("Enter 1 to record and translate audio, 2 to exit")
    if choice=="1":
      audio_in=record_audio()
      num =input("Press Enter for English transcription.\nTo translate your message: \n For French, press 1.\n For Spanish, press 2.\n For Hindi, press 3.\n For German, press 4.\n For Japanese, press 5")
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
      elif num=="5":
        tr_lang="jp"
      else:
        print("Invalid input, Translation could not proceed")
      translate_and_speak(audio_in,tr_lang)
    else:
      break
