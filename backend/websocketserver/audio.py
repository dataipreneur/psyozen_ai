from model import whisper_model
import datetime
import wave


def transcribe(file_name):
  #audio_file= open(file_name, "rb")
  #transcription = client.audio.transcriptions.create(
  #model="whisper-1",
  #file=audio_file)
  result = whisper_model.transcribe(file_name)
  transcript = result["text"]
  return transcript

def save_audio_file(audio_bytes, file_extension):
  timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
  file_name = f"audio_{timestamp}.{file_extension}"
  with open(file_name, "wb") as f:
    f.write(audio_bytes)
  return file_name

def check_wav_file(file_path):
    try:
        with wave.open(file_path, 'rb') as wav_file:
            params = wav_file.getparams()
            frames = wav_file.readframes(params.nframes)
            if len(frames) == 0:
                return "The WAV file is empty."
            else:
                return (f"The WAV file is valid.\n"
                        f"Number of Channels: {params.nchannels}\n"
                        f"Sample Width: {params.sampwidth} bytes\n"
                        f"Frame Rate (Sample Rate): {params.framerate} Hz\n"
                        f"Number of Frames: {params.nframes}\n"
                        f"Duration: {params.nframes / params.framerate} seconds")
    except wave.Error as e:
        return f"Error in WAV file: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
