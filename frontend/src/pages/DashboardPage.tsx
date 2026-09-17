import React, { useEffect } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';
import { useDetection } from '../hooks/useDetection';
import { VideoFeed } from '../components/Dashboard/VideoFeed';
import { PersonCard } from '../components/Dashboard/PersonCard';
import { StatsPanel } from '../components/Dashboard/StatsPanel';
import { Play, Square } from 'lucide-react';

export const DashboardPage = () => {
  const { latestMessage, isConnected } = useWebSocket();
  const { isDetecting, isLoading, startDetection, stopDetection, checkStatus } = useDetection();

  useEffect(() => {
    checkStatus();
  }, [checkStatus]);

  const frame = latestMessage?.frame || null;
  const events = latestMessage?.events || [];

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', height: '100%', gap: '1.5rem' }}>
      <div className="flex items-center justify-between">
        <h2>Live Dashboard</h2>
        <div className="flex gap-sm">
          {!isDetecting ? (
            <button 
              className="btn btn-primary" 
              onClick={() => startDetection()}
              disabled={isLoading}
            >
              <Play size={18} /> Start Camera
            </button>
          ) : (
            <button 
              className="btn btn-danger" 
              onClick={() => stopDetection()}
              disabled={isLoading}
            >
              <Square size={18} /> Stop Camera
            </button>
          )}
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.5rem', flex: 1, minHeight: 0 }}>
        {/* Left Column - Video */}
        <div style={{ display: 'flex', flexDirection: 'column', borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
          <VideoFeed frame={frame} isDetecting={isDetecting} />
        </div>

        {/* Right Column - Stats & People */}
        <div style={{ display: 'flex', flexDirection: 'column', overflowY: 'auto', paddingRight: '0.5rem' }}>
          <StatsPanel events={events} />
          
          <h3 style={{ marginBottom: '1rem', fontSize: '1.125rem' }}>Detected Individuals</h3>
          
          {events.length === 0 ? (
            <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              No individuals currently detected in frame.
            </div>
          ) : (
            <div className="flex-col">
              {events.map((event) => (
                <PersonCard key={event.tracking_id} event={event} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
