import React, { useEffect, useRef, useState } from 'react';
import { Hands, HAND_CONNECTIONS } from '@mediapipe/hands';
import { Camera } from '@mediapipe/camera_utils';
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils';

const HandTracking = ({ onResults, scenario }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const hands = new Hands({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
      },
    });

    hands.setOptions({
      maxNumHands: 2,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });

    hands.onResults((results) => {
      setIsLoading(false);
      
      const canvasCtx = canvasRef.current.getContext('2d');
      const { width, height } = canvasRef.current;
      
      canvasCtx.save();
      canvasCtx.clearRect(0, 0, width, height);
      
      // Draw video frame
      canvasCtx.drawImage(results.image, 0, 0, width, height);
      
      if (results.multiHandLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
          // Choose colors based on scenario
          const connectorColor = scenario === 'embroidery' ? '#5796B3' : '#C04851'; // Cyan vs Vermilion
          const landmarkColor = scenario === 'embroidery' ? '#CCD4BF' : '#F7F5F0'; // Tea Green vs Rice Paper
          
          drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, { color: connectorColor, lineWidth: 5 });
          drawLandmarks(canvasCtx, landmarks, { color: landmarkColor, lineWidth: 2 });
        }
      }
      canvasCtx.restore();

      if (onResults) {
        onResults(results);
      }
    });

    if (videoRef.current) {
      const camera = new Camera(videoRef.current, {
        onFrame: async () => {
          await hands.send({ image: videoRef.current });
        },
        width: 640,
        height: 480,
      });
      camera.start();
    }

    return () => {
        // Cleanup if necessary, though Camera util handles stream stop mostly.
        // hands.close(); // Close method might be async/problematic in React strict mode re-renders
    };
  }, [scenario, onResults]);

  return (
    <div className="relative w-full max-w-[640px] aspect-[4/3] rounded-xl overflow-hidden shadow-lg bg-black mx-auto">
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center text-white z-20 bg-black/50">
          <div className="flex flex-col items-center">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-white mb-4"></div>
            <p>正在初始化视觉模型...</p>
          </div>
        </div>
      )}
      <video
        ref={videoRef}
        className="absolute top-0 left-0 w-full h-full object-cover transform scale-x-[-1] opacity-0"
        playsInline
      ></video>
      <canvas
        ref={canvasRef}
        className="absolute top-0 left-0 w-full h-full object-cover transform scale-x-[-1]"
        width={640}
        height={480}
      ></canvas>
    </div>
  );
};

export default HandTracking;
