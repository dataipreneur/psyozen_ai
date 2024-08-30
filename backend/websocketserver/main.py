from fastapi import FastAPI, WebSocket
import uvicorn
import io
import wave
import speech_recognition as sr
import json
from gtts import gTTS
import ollama

app = FastAPI()
modelfile='''
FROM mistral
SYSTEM You are therapist who listens to people and talks to them emphatethically and gives solutions when necessary
'''
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

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)  # Read the entire audio file
            transcription = recognizer.recognize_google(audio)  # Use Google Web Speech API
            return transcription
    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from Speech Recognition service; {e}"
    except Exception as e:
        return f"An error occurred during transcription: {e}"

def generate_tts_stream(text):
    tts = gTTS(text=text, lang='en')
    audio_stream = io.BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)  # Reset stream position to the beginning
    return audio_stream

async def get_model_response(text):
    try:
        response = ollama.chat(
            model='mistral',
            messages=[{'role': 'user', 'content': text}],
            stream=False
        )
        return response['message']['content']
    except Exception as e:
        return f"An error occurred with the model: {e}"

@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                # Receive binary data (audio file)
                data = await websocket.receive_bytes()
                
                # Save the audio data to a file
                file_path = "received_audio.wav"
                with open(file_path, "wb") as f:
                    f.write(data)

                # Check the saved WAV file
                file_check_result = check_wav_file(file_path)
                
                # Transcribe the audio
                transcription = transcribe_audio(file_path)

                # Combine the results
                transcription_result = {
                    "entity": "user",
                    "message": transcription
                }

                # Convert the Python dictionary to a JSON string
                json_result = json.dumps(transcription_result, indent=2)

                # Send back the transcription result as JSON
                await websocket.send_text(json_result)

                # Get model response based on transcription
               
                model_response = await get_model_response(transcription)
                transcription_response = {
                    "entity": "assistant",
                    "message": model_response
                }
                json_response = json.dumps(transcription_response, indent=2)
                await websocket.send_text(json_response)
                # Generate TTS response stream from the model's response
                tts_audio_stream = generate_tts_stream(model_response)
                
                # Send the TTS audio directly to the client
                await websocket.send_bytes(tts_audio_stream.read())
               
            except Exception as e:
                print(f"Error during message processing: {e}")
                break

    except Exception as e:
        print(f"WebSocket connection error: {e}")

    finally:
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
