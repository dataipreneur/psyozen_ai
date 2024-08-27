import { useState, useRef } from 'react';
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Mic, MicOff, Bot, User } from 'lucide-react';
import RecordRTC from 'recordrtc';
import * as WavEncoder from 'wav-encoder';
import AudioVisualizer from './AudioVisualizer';

export default function VoiceAssistant() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! How can I assist you today?' },
  ]);
  const [isRecording, setIsRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState('');
  const [recorder, setRecorder] = useState(null);
  const wsRef = useRef(null);

  const startRecording = () => {
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        const newRecorder = new RecordRTC(stream, { type: 'audio', mimeType: 'audio/webm' });
        setRecorder(newRecorder);
        newRecorder.startRecording();
        setIsRecording(true);

        wsRef.current = new WebSocket("ws://localhost:8000/ws/audio");

        wsRef.current.onopen = () => {
          console.log("WebSocket connection opened");
        };

        wsRef.current.onmessage = async (event) => {
          if (event.data instanceof Blob) {
            console.log("Received audio data");
            playReceivedAudio(event.data);
            setMessages(prevMessages => [
              ...prevMessages,
              { role: 'assistant', content: 'Received' }
            ]);
          } else {
            console.log("Received JSON data");
            try {
              const textData = await event.data;
              const data = JSON.parse(textData);
              if (data.entity === 'user') {
                setMessages(prevMessages => [
                  ...prevMessages,
                  { role: 'user', content: data.message }
                ]);
              } else {
                setMessages(prevMessages => [
                  ...prevMessages,
                  { role: 'assistant', content: 'Audio received' }
                ]);
              }
            } catch (error) {
              console.error('Error parsing message:', error);
            }
          }
        };

        wsRef.current.onerror = (error) => {
          console.error("WebSocket error:", error);
        };

        wsRef.current.onclose = () => {
          console.log("WebSocket connection closed");
        };
      });
  };

  const stopRecording = () => {
    if (recorder) {
      recorder.stopRecording(async () => {
        const blob = recorder.getBlob();
        const arrayBuffer = await blob.arrayBuffer();
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        try {
          const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
          const wavData = {
            sampleRate: audioBuffer.sampleRate,
            channelData: [audioBuffer.getChannelData(0)]
          };
          const wavBlob = await WavEncoder.encode(wavData);
          const wavUrl = URL.createObjectURL(new Blob([wavBlob], { type: 'audio/wav' }));
          // setAudioUrl(wavUrl);
          wsRef.current.send(wavBlob);
        } catch (error) {
          console.error('Error encoding audio data:', error);
        }

        setIsRecording(false);
      });
    }
  };

  const playReceivedAudio = (audioBlob) => {
    const audioUrl = URL.createObjectURL(audioBlob);
    setAudioUrl(audioUrl); // Set audioUrl to trigger visualization
  };

  return (
    <div className="flex flex-col h-screen">
      <div className="flex flex-grow">
        <div className="hidden md:flex flex-col border-r border-gray-300 w-1/4">
          <div className="p-4 font-semibold text-lg border-gray-300"></div>
          <ScrollArea className="flex-grow p-2">
            <h3 className="font-semibold ml-4 mb-2">Today</h3>
            <div className="space-y-2">
              {['Weather forecast', 'Set a reminder', 'Play music'].map((item, index) => (
                <Button key={index} variant="ghost" className="w-full justify-start rounded-md">
                  {item}
                </Button>
              ))}
            </div>
          </ScrollArea>
        </div>

        <div className="flex-grow flex flex-col border-r border-gray-300 w-1/4">
          <div className="p-4 font-semibold text-lg border-b border-gray-300">Audio Visualization</div>
          <div className="flex-grow flex">
            <AudioVisualizer audioUrl={audioUrl} />
          </div>
        </div>

        <div className="flex-grow flex flex-col">
          <ScrollArea className="h-[600px]  rounded-md border p-4">
            {messages.map((message, index) => (
              <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`flex items-start space-x-2 ${message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                  <Avatar>
                    <AvatarFallback>{message.role === 'user' ? <User /> : <Bot />}</AvatarFallback>
                  </Avatar>
                  <div className={`rounded-lg p-3 m-3 ${message.role === 'user' ? 'text-white bg-primary' : 'bg-gray-200'}`}>
                    {message.content}
                  </div>
                </div>
              </div>
            ))}
          </ScrollArea>
          <div className="p-4 border-t border-gray-300">
            <Button
              onClick={isRecording ? stopRecording : startRecording}
              className="w-full rounded-md"
            >
              {isRecording ? <MicOff className="mr-2" /> : <Mic className="mr-2" />}
              {isRecording ? 'Stop Recording' : 'Start Recording'}
            </Button>
            {audioUrl && (
              <div className="mt-4">
                {/* <audio src={audioUrl} controls /> */}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
