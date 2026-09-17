import React, { useState } from 'react';
import { api } from '../services/api';
import { ImageUpload } from '../components/Registration/ImageUpload';
import { CheckCircle, AlertCircle, Loader } from 'lucide-react';

export const RegistrationPage = () => {
  const [formData, setFormData] = useState({
    person_id: '',
    name: '',
    department: '',
    email: ''
  });
  
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [status, setStatus] = useState<{type: 'success' | 'error', message: string} | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleImageSelected = (file: File | null, url: string | null) => {
    setSelectedFile(file);
    setPreviewUrl(url);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedFile) {
      setStatus({ type: 'error', message: 'Please select a face image.' });
      return;
    }

    setIsSubmitting(true);
    setStatus(null);

    try {
      // 1. Create Person record
      const person = await api.createPerson(formData);
      
      // 2. Register Face
      await api.registerFace(person.id, selectedFile);
      
      setStatus({ type: 'success', message: 'Person and face registered successfully!' });
      
      // Reset form
      setFormData({ person_id: '', name: '', department: '', email: '' });
      setSelectedFile(null);
      setPreviewUrl(null);
    } catch (err: any) {
      setStatus({ type: 'error', message: err.message || 'An error occurred during registration.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="animate-fade-in" style={{ maxWidth: '800px', margin: '0 auto' }}>
      <h2 style={{ marginBottom: '1.5rem' }}>Register New Person</h2>
      
      <div className="glass-panel" style={{ padding: '2rem' }}>
        <form onSubmit={handleSubmit} className="flex-col gap-lg">
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
            <div className="input-group">
              <label className="input-label" htmlFor="person_id">Employee/Person ID *</label>
              <input 
                className="input-field" 
                id="person_id" 
                name="person_id"
                value={formData.person_id}
                onChange={handleInputChange}
                required
                placeholder="e.g. EMP001"
              />
            </div>
            
            <div className="input-group">
              <label className="input-label" htmlFor="name">Full Name *</label>
              <input 
                className="input-field" 
                id="name" 
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                required
                placeholder="John Doe"
              />
            </div>
            
            <div className="input-group">
              <label className="input-label" htmlFor="department">Department</label>
              <input 
                className="input-field" 
                id="department" 
                name="department"
                value={formData.department}
                onChange={handleInputChange}
                placeholder="Engineering"
              />
            </div>
            
            <div className="input-group">
              <label className="input-label" htmlFor="email">Email</label>
              <input 
                className="input-field" 
                id="email" 
                name="email"
                type="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="john.doe@example.com"
              />
            </div>
          </div>

          <div style={{ marginTop: '1rem' }}>
            <ImageUpload onImageSelected={handleImageSelected} previewUrl={previewUrl} />
          </div>

          {status && (
            <div className="glass-panel" style={{ 
              padding: '1rem', 
              display: 'flex', 
              alignItems: 'center', 
              gap: '0.75rem',
              backgroundColor: status.type === 'success' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
              borderColor: status.type === 'success' ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)',
              color: status.type === 'success' ? 'var(--status-success)' : 'var(--status-danger)'
            }}>
              {status.type === 'success' ? <CheckCircle size={20} /> : <AlertCircle size={20} />}
              <span>{status.message}</span>
            </div>
          )}

          <div className="flex justify-between items-center" style={{ marginTop: '1rem', paddingTop: '1.5rem', borderTop: '1px solid var(--glass-border)' }}>
            <button type="button" className="btn btn-secondary" onClick={() => {
              setFormData({ person_id: '', name: '', department: '', email: '' });
              setSelectedFile(null);
              setPreviewUrl(null);
              setStatus(null);
            }}>
              Clear Form
            </button>
            <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
              {isSubmitting ? <><Loader size={18} className="animate-spin" /> Registering...</> : 'Complete Registration'}
            </button>
          </div>
          
        </form>
      </div>
    </div>
  );
};
