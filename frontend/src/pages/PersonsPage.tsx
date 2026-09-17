import React, { useEffect, useState, useCallback } from 'react';
import { api } from '../services/api';
import { Person } from '../types/person';
import { Search, User, Trash2 } from 'lucide-react';

export const PersonsPage = () => {
  const [persons, setPersons] = useState<Person[]>([]);
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const fetchPersons = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await api.getPersons(1, 50, search);
      setPersons(response.persons);
    } catch (error) {
      console.error('Failed to fetch persons', error);
    } finally {
      setIsLoading(false);
    }
  }, [search]);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      fetchPersons();
    }, 500);

    return () => clearTimeout(delayDebounceFn);
  }, [fetchPersons]);

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this person? This action cannot be undone.')) {
      try {
        await api.deletePerson(id);
        setPersons(persons.filter(p => p.id !== id));
      } catch (error) {
        console.error('Failed to delete person', error);
        alert('Failed to delete person');
      }
    }
  };

  return (
    <div className="animate-fade-in">
      <div className="flex items-center justify-between" style={{ marginBottom: '2rem' }}>
        <h2>Registered Persons</h2>
        
        <div style={{ position: 'relative', width: '300px' }}>
          <input
            type="text"
            className="input-field"
            style={{ width: '100%', paddingLeft: '2.5rem' }}
            placeholder="Search by name, ID, or dept..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <Search size={18} style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
        </div>
      </div>

      {isLoading && persons.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
          Loading persons...
        </div>
      ) : persons.length === 0 ? (
        <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
          No persons found matching your criteria.
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem' }}>
          {persons.map(person => (
            <div key={person.id} className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column' }}>
              <div className="flex items-center gap-md" style={{ marginBottom: '1rem' }}>
                <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: 'rgba(59, 130, 246, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent-primary)' }}>
                  <User size={24} />
                </div>
                <div>
                  <h3 style={{ margin: 0, fontSize: '1.125rem' }}>{person.name}</h3>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>ID: {person.person_id}</div>
                </div>
              </div>
              
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1.5rem', fontSize: '0.875rem' }}>
                {person.department && (
                  <div className="flex justify-between">
                    <span style={{ color: 'var(--text-muted)' }}>Department</span>
                    <span>{person.department}</span>
                  </div>
                )}
                {person.role && (
                  <div className="flex justify-between">
                    <span style={{ color: 'var(--text-muted)' }}>Role</span>
                    <span>{person.role}</span>
                  </div>
                )}
                <div className="flex justify-between">
                  <span style={{ color: 'var(--text-muted)' }}>Face Data</span>
                  <span className={`badge ${person.has_face_embedding ? 'badge-success' : 'badge-warning'}`}>
                    {person.has_face_embedding ? 'Registered' : 'Missing'}
                  </span>
                </div>
              </div>

              <div className="flex justify-between" style={{ paddingTop: '1rem', borderTop: '1px solid var(--glass-border)' }}>
                <button 
                  className="btn btn-danger" 
                  style={{ padding: '0.25rem 0.5rem', fontSize: '0.875rem' }}
                  onClick={() => handleDelete(person.id)}
                >
                  <Trash2 size={16} /> Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
