from gtts import gTTS
import io

def text_to_speech(text):
  tts = gTTS(text=text, lang='en')
  tts.save("response.mp3")
  # Play the audio as before


def generate_tts_stream(text):
  tts = gTTS(text=text, lang='en')
  audio_stream = io.BytesIO()
  tts.write_to_fp(audio_stream)
  audio_stream.seek(0)  # Reset stream position to the beginning
  return audio_stream