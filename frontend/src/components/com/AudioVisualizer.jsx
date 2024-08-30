import { useRef, useEffect, useState } from 'react';
import './AudioVisualizer.css'; // Import the CSS file for styling

const AudioVisualizer = ({ audioUrl }) => {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false); // State to track if audio is playing

  useEffect(() => {
    if (!audioUrl) return;

    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    // Resize the canvas when the container size changes
    const updateCanvasSize = () => {
      canvas.width = container.offsetWidth;
      canvas.height = container.offsetHeight;
    };

    // Set initial canvas size
    updateCanvasSize();

    // Add resize observer to update canvas size on resize
    const resizeObserver = new ResizeObserver(() => updateCanvasSize());
    resizeObserver.observe(container);

    const audio = new Audio(audioUrl);
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioCtx.createAnalyser();
    const source = audioCtx.createMediaElementSource(audio);
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    const canvasCtx = canvas.getContext('2d');

    source.connect(analyser);
    analyser.connect(audioCtx.destination);

    const animateBars = () => {
      analyser.getByteFrequencyData(dataArray);

      canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
      const HEIGHT = canvas.height / 2;
      const barWidth = Math.ceil(canvas.width / bufferLength) * 2.5;
      let barHeight;
      let x = 0;

      // Draw the top waveform
      canvasCtx.fillStyle = '#000';
      for (let i = 0; i < bufferLength; i++) {
        barHeight = (dataArray[i] / 255) * HEIGHT;
        const r = 59 + Math.floor(Math.random() * 10 - 5);
        const g = 5 + Math.floor(Math.random() * 10 - 5);
        const b = 167 + Math.floor(Math.random() * 10 - 5);
        canvasCtx.fillStyle = `rgb(${r},${g},${b})`;
        canvasCtx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);
        x += barWidth + 1;
      }

      // Draw the mirrored waveform on the bottom
      x = 0;
      canvasCtx.save(); // Save the current state
      canvasCtx.translate(0, HEIGHT * 2); // Move to the bottom half
      canvasCtx.scale(1, -1); // Mirror vertically
      for (let i = 0; i < bufferLength; i++) {
        barHeight = (dataArray[i] / 255) * HEIGHT;
        const r =59 + Math.floor(Math.random() * 10 - 5);
        const g = 5 + Math.floor(Math.random() * 10 - 5);
        const b = 165 + Math.floor(Math.random() * 10 - 5);
        canvasCtx.fillStyle = `rgb(${r},${g},${b})`;
        canvasCtx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);
        x += barWidth + 1;
      }
      canvasCtx.restore(); // Restore the previous state

      requestAnimationFrame(animateBars);
    };

    audio.onplay = () => setIsPlaying(true); // Set isPlaying to true when audio starts playing
    audio.onpause = () => setIsPlaying(false); // Set isPlaying to false when audio pauses
    audio.onended = () => {
      setIsPlaying(false); // Set isPlaying to false when audio ends
      URL.revokeObjectURL(audioUrl);
    };

    audio.play();
    animateBars();

    return () => {
      audio.pause();
      setIsPlaying(false);
      URL.revokeObjectURL(audioUrl);
      resizeObserver.disconnect();
    };
  }, [audioUrl]);

  return (
    <div ref={containerRef} className="visualizer-container">
      <div className="glass-overlay"></div>
      <canvas
        ref={canvasRef}
        className="visualizer-canvas"
      />
      <div className={`centered-text ${isPlaying ? 'playing' : ''}`}>PsyOzen</div>
    </div>
  );
};

export default AudioVisualizer;
