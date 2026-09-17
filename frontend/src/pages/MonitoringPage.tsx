import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Activity, Cpu, Server, Clock } from 'lucide-react';

export const MonitoringPage = () => {
  const [health, setHealth] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const response = await fetch('/api/v1/health/');
        const data = await response.json();
        setHealth(data);
      } catch (error) {
        console.error('Failed to fetch health status', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchHealth();
    const interval = setInterval(fetchHealth, 5000);
    return () => clearInterval(interval);
  }, []);

  if (isLoading && !health) {
    return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading system metrics...</div>;
  }

  return (
    <div className="animate-fade-in">
      <h2 style={{ marginBottom: '1.5rem' }}>System Monitoring</h2>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        
        {/* API Status */}
        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ padding: '0.75rem', background: health?.status === 'ok' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)', borderRadius: 'var(--radius-md)', color: health?.status === 'ok' ? 'var(--status-success)' : 'var(--status-danger)' }}>
            <Activity size={24} />
          </div>
          <div>
            <div style={{ fontSize: '1.25rem', fontWeight: 700, textTransform: 'uppercase' }}>{health?.status || 'UNKNOWN'}</div>
            <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>API Health</div>
          </div>
        </div>

        {/* Components */}
        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ padding: '0.75rem', background: health?.components?.database === 'connected' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)', borderRadius: 'var(--radius-md)', color: health?.components?.database === 'connected' ? 'var(--status-success)' : 'var(--status-danger)' }}>
            <Server size={24} />
          </div>
          <div>
            <div style={{ fontSize: '1.25rem', fontWeight: 700, textTransform: 'capitalize' }}>{health?.components?.database || 'UNKNOWN'}</div>
            <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Database Status</div>
          </div>
        </div>

        {/* Vision Models */}
        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ padding: '0.75rem', background: 'rgba(59, 130, 246, 0.1)', borderRadius: 'var(--radius-md)', color: 'var(--accent-primary)' }}>
            <Cpu size={24} />
          </div>
          <div>
            <div style={{ fontSize: '1.25rem', fontWeight: 700 }}>Active</div>
            <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Vision Models</div>
          </div>
        </div>
        
        <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ padding: '0.75rem', background: 'rgba(245, 158, 11, 0.1)', borderRadius: 'var(--radius-md)', color: 'var(--status-warning)' }}>
            <Clock size={24} />
          </div>
          <div>
            <div style={{ fontSize: '1.25rem', fontWeight: 700 }}>{health?.timestamp ? new Date(health.timestamp).toLocaleTimeString() : '--:--'}</div>
            <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Last Updated</div>
          </div>
        </div>
      </div>

      <div className="glass-panel" style={{ padding: '1.5rem' }}>
        <h3 style={{ marginBottom: '1rem' }}>System Info</h3>
        <pre style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: 'var(--radius-md)', overflowX: 'auto', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          {JSON.stringify(health, null, 2)}
        </pre>
      </div>
    </div>
  );
};
