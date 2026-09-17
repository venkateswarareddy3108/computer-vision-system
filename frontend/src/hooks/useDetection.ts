import { useState, useCallback } from 'react';
import { api } from '../services/api';

export function useDetection() {
  const [isDetecting, setIsDetecting] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const checkStatus = useCallback(async () => {
    try {
      const status = await api.getDetectionStatus();
      setIsDetecting(status.is_running);
    } catch (err: any) {
      console.error('Failed to get detection status', err);
    }
  }, []);

  const startDetection = async (cameraIndex = 0) => {
    setIsLoading(true);
    setError(null);
    try {
      await api.startDetection(cameraIndex);
      setIsDetecting(true);
    } catch (err: any) {
      setError(err.message || 'Failed to start detection');
    } finally {
      setIsLoading(false);
    }
  };

  const stopDetection = async () => {
    setIsLoading(true);
    setError(null);
    try {
      await api.stopDetection();
      setIsDetecting(false);
    } catch (err: any) {
      setError(err.message || 'Failed to stop detection');
    } finally {
      setIsLoading(false);
    }
  };

  return {
    isDetecting,
    isLoading,
    error,
    startDetection,
    stopDetection,
    checkStatus
  };
}
