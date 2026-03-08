import { useEffect, useState } from 'react';

export function useWebSocket(wsUrl, shouldConnect) {
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!shouldConnect) return;

    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        if (message.type === 'metrics') {
          setData(message.data);
        }
      } catch (error) {
        console.error('WebSocket parse error:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [wsUrl, shouldConnect]);

  return data;
}