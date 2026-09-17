import { useEffect, useState } from 'react';
import { wsService } from '../services/websocket';
import { WebSocketMessage } from '../types/websocket';

export function useWebSocket() {
  const [latestMessage, setLatestMessage] = useState<WebSocketMessage | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Connect to WebSocket
    wsService.connect();
    setIsConnected(true);

    // Subscribe to messages
    const unsubscribe = wsService.subscribe((data) => {
      setLatestMessage(data);
    });

    return () => {
      unsubscribe();
      wsService.disconnect();
      setIsConnected(false);
    };
  }, []);

  return { latestMessage, isConnected };
}
