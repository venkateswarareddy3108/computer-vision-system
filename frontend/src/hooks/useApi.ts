import { useState, useCallback } from 'react';

export function useApi<T, P extends any[]>(
  apiFunction: (...args: P) => Promise<T>,
  initialData: T | null = null
) {
  const [data, setData] = useState<T | null>(initialData);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(
    async (...args: P) => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await apiFunction(...args);
        setData(result);
        return result;
      } catch (err: any) {
        setError(err.message || 'An error occurred');
        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [apiFunction]
  );

  return { data, isLoading, error, execute, setData };
}
