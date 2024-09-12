from fastapi import FastAPI, WebSocket
import uvicorn
import io
import wave
import json
from audio import save_audio_file, transcribe, check_wav_file
from emotion_analyser import analyze_emotion
from psyozen_agent import process_input, should_continue, generate_recommendation
from text_processor import text_to_speech, generate_tts_stream
from psyozen_langgraph import workflow
import os
import logging


#app = FastAPI()
#
#app2 = workflow.compile()
#
#logging.basicConfig(filename='psy_logs.log', level=logging.DEBUG)
#    
#
#@app.websocket("/ws/audio")
#async def websocket_endpoint(websocket: WebSocket):
#
#    state = {
#          'summary': "",
#          'last_response': "Hello, I'm PsyOzen AI. How can I help you today?",
#          'conversation': []
#          }
#    await websocket.accept()
#
#    
#    try:
#        while True:
#            try:
#                # Receive binary data (audio file)
#                data = await websocket.receive_bytes()
#
#                file_name = save_audio_file(data, "wav")
#                
#                # Check the saved WAV file
#                try:
#
#                    file_check_result = check_wav_file(file_name)
#
#                except Exception as e:
#                    print(f'The error is {e}')
#
#                
#                # Transcribe the audio
#                transcript = transcribe(file_name)
#
#                # Combine the results
#                transcription_result = {
#                    "entity": "user",
#                    "message": transcript
#                }
#
#                # Convert the Python dictionary to a JSON string
#                json_result = json.dumps(transcription_result, indent=2)
#
#                # Send back the transcription result as JSON
#                await websocket.send_text(json_result)
#
#                # Get model response based on transcription
#                emotions = analyze_emotion(transcript)
#               
#                state, response = process_input(state, transcript, emotions)
#                
#                transcription_response = {
#                    "entity": "assistant",
#                    "message": response
#                }
#                json_response = json.dumps(transcription_response, indent=2)
#
#                await websocket.send_text(json_response)
#                # Generate TTS response stream from the model's response
#                tts_audio_stream = generate_tts_stream(response)
#                
#                # Send the TTS audio directly to the client
#                await websocket.send_bytes(tts_audio_stream.read())
#
#                next_step = should_continue(state)
#
#
#                if next_step == "generate_recommendation":
#
#                    state, recommendation = generate_recommendation(state)
#
#                    transcription_response = {
#                    "entity": "assistant",
#                    "message": recommendation
#                }
#                    json_response = json.dumps(transcription_response, indent=2)
#                    print(json_response)
#
#                    await websocket.send_text(json_response)
#                    # Generate TTS response stream from the model's response
#                    tts_audio_stream = generate_tts_stream(recommendation)
#                
#                    # Send the TTS audio directly to the client
#                    await websocket.send_bytes(tts_audio_stream.read())
#               
#                os.remove(file_name)
#                
#            except Exception as e:
#                print(f"Error during message processing: {e}")
#                break
#            
#
#    except Exception as e:
#        print(f"WebSocket connection error: {e}")
#
#    finally:
#        await websocket.close()
#    
#    
#
#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, WebSocket
import uvicorn
import io
import wave
import json
from audio import save_audio_file, transcribe, check_wav_file
from emotion_analyser import analyze_emotion
from psyozen_agent import process_input, should_continue, generate_recommendation
from text_processor import text_to_speech, generate_tts_stream
from psyozen_langgraph import workflow
import os
import logging

app = FastAPI()
app2 = workflow.compile()
logging.basicConfig(filename='psy_logs.log', level=logging.DEBUG)
state = {
        'summary': "",
        'last_response': "Hello, I'm PsyOzen AI. How can I help you today?",
        'conversation': []
    }

@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):

    global state
    await websocket.accept()
    try:

       

        while True:
            try:
                # Receive binary data (audio file)
                data = await websocket.receive_bytes()
                file_name = save_audio_file(data, "wav")
                
                # Check the saved WAV file
                try:
                    file_check_result = check_wav_file(file_name)
                except Exception as e:
                    logging.error(f'Error checking WAV file: {e}')
                
                # Transcribe the audio
                transcript = transcribe(file_name)
                
                # Combine the results
                transcription_result = {
                    "entity": "user",
                    "message": transcript
                }
                
                # Convert the Python dictionary to a JSON string
                json_result = json.dumps(transcription_result, indent=2)
                
                # Send back the transcription result as JSON
                await websocket.send_text(json_result)
                
                # Get model response based on transcription
                emotions = analyze_emotion(transcript)
                state, response = process_input(state, transcript, emotions)
                
                transcription_response = {
                    "entity": "assistant",
                    "message": response
                }
                json_response = json.dumps(transcription_response, indent=2)
                await websocket.send_text(json_response)
                
                # Generate TTS response stream from the model's response
                tts_audio_stream = generate_tts_stream(response)
                
                # Send the TTS audio directly to the client
                await websocket.send_bytes(tts_audio_stream.read())

                logging.info(f"State_Priestley: {state['conversation']}")
                
                next_step = should_continue(state)
                if next_step == "generate_recommendation":
                    state, recommendation = generate_recommendation(state)
                    transcription_response = {
                        "entity": "assistant",
                        "message": recommendation
                    }
                    json_response = json.dumps(transcription_response, indent=2)
                    logging.info(f"Recommendation generated: {json_response}")
                    await websocket.send_text(json_response)
                    
                    # Generate TTS response stream from the model's response
                    tts_audio_stream = generate_tts_stream(recommendation)
                    
                    # Send the TTS audio directly to the client
                    await websocket.send_bytes(tts_audio_stream.read())
                
                os.remove(file_name)
                
            except Exception as e:
                logging.error(f"Error during message processing: {e}")
                break
    except Exception as e:
        logging.error(f"WebSocket connection error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)