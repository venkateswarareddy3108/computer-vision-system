import React from 'react';

interface VideoFeedProps {
  frame: string | null;
  isDetecting: boolean;
}

export const VideoFeed: React.FC<VideoFeedProps> = ({ frame, isDetecting }) => {
  return (
    <div className="glass-panel" style={{ position: 'relative', overflow: 'hidden', backgroundColor: '#000', height: '100%', minHeight: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      {isDetecting ? (
        frame ? (
          <img 
            src={`data:image/jpeg;base64,${frame}`} 
            alt="Live Feed" 
            style={{ width: '100%', height: '100%', objectFit: 'contain' }}
          />
        ) : (
          <div className="flex-col items-center gap-sm">
            <div className="animate-pulse" style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: 'var(--accent-primary)' }}></div>
            <p style={{ color: 'var(--text-secondary)' }}>Waiting for video stream...</p>
          </div>
        )
      ) : (
        <div style={{ color: 'var(--text-muted)' }}>
          <p>Detection is currently offline.</p>
        </div>
      )}
    </div>
  );
};
