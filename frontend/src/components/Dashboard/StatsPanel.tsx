import React from 'react';
import { DetectionEvent } from '../../types/detection';
import { Users, AlertTriangle } from 'lucide-react';

interface StatsPanelProps {
  events: DetectionEvent[];
}

export const StatsPanel: React.FC<StatsPanelProps> = ({ events }) => {
  const totalPeople = events.length;
  const knownPeople = events.filter(e => !!e.person).length;
  const unknownPeople = totalPeople - knownPeople;
  
  const sleepyPeople = events.filter(e => e.awake_status === 'sleeping' || e.awake_status === 'drowsy').length;

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
      <div className="glass-panel" style={{ padding: '1rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{ padding: '0.75rem', background: 'rgba(59, 130, 246, 0.1)', borderRadius: 'var(--radius-md)', color: 'var(--accent-primary)' }}>
          <Users size={24} />
        </div>
        <div>
          <div style={{ fontSize: '2rem', fontWeight: 700, lineHeight: 1 }}>{totalPeople}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>People Detected</div>
        </div>
      </div>

      <div className="glass-panel" style={{ padding: '1rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{ padding: '0.75rem', background: sleepyPeople > 0 ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.1)', borderRadius: 'var(--radius-md)', color: sleepyPeople > 0 ? 'var(--status-danger)' : 'var(--status-success)' }}>
          <AlertTriangle size={24} />
        </div>
        <div>
          <div style={{ fontSize: '2rem', fontWeight: 700, lineHeight: 1 }}>{sleepyPeople}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Drowsy/Sleeping</div>
        </div>
      </div>
    </div>
  );
};
