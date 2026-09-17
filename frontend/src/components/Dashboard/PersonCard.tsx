import React from 'react';
import { DetectionEvent } from '../../types/detection';
import { User, Activity, Smile } from 'lucide-react';

interface PersonCardProps {
  event: DetectionEvent;
}

export const PersonCard: React.FC<PersonCardProps> = ({ event }) => {
  const isKnown = !!event.person;

  return (
    <div className="glass-panel" style={{ padding: '1rem', marginBottom: '1rem' }}>
      <div className="flex items-center justify-between" style={{ borderBottom: '1px solid var(--glass-border)', paddingBottom: '0.75rem', marginBottom: '0.75rem' }}>
        <div className="flex items-center gap-sm">
          <User size={20} color={isKnown ? 'var(--status-success)' : 'var(--text-muted)'} />
          <h3 style={{ margin: 0, fontSize: '1rem' }}>
            {isKnown ? event.person!.name : `Unknown (Track ${event.tracking_id})`}
          </h3>
        </div>
        {isKnown && event.distance !== undefined && (
          <span className="badge badge-success" style={{ fontSize: '0.7rem' }}>
            Score: {(1 - event.distance).toFixed(2)}
          </span>
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', fontSize: '0.875rem' }}>
        <div className="flex-col gap-sm">
          <div className="flex items-center gap-sm text-secondary">
            <Activity size={16} />
            <span>Status</span>
          </div>
          <div>
            <span className={`badge ${event.awake_status === 'awake' ? 'badge-success' : 'badge-danger'}`}>
              {event.awake_status.toUpperCase()}
            </span>
          </div>
        </div>

        <div className="flex-col gap-sm">
          <div className="flex items-center gap-sm text-secondary">
            <Smile size={16} />
            <span>Emotion</span>
          </div>
          <div>
            <span style={{ textTransform: 'capitalize', fontWeight: 500 }}>
              {event.estimated_expression}
            </span>
          </div>
        </div>

        <div className="flex-col gap-sm">
          <span style={{ color: 'var(--text-secondary)' }}>Fingers Count</span>
          <span style={{ fontWeight: 600 }}>{event.fingers_count} ({event.hands_count} hands)</span>
        </div>

        {isKnown && event.person?.department && (
          <div className="flex-col gap-sm">
            <span style={{ color: 'var(--text-secondary)' }}>Department</span>
            <span style={{ fontWeight: 500 }}>{event.person.department}</span>
          </div>
        )}
      </div>
    </div>
  );
};
