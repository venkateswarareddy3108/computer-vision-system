import React, { useRef, useState } from 'react';
import { Upload, X } from 'lucide-react';

interface ImageUploadProps {
  onImageSelected: (file: File | null, previewUrl: string | null) => void;
  previewUrl: string | null;
}

export const ImageUpload: React.FC<ImageUploadProps> = ({ onImageSelected, previewUrl }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFile = (file: File) => {
    if (file && file.type.startsWith('image/')) {
      const url = URL.createObjectURL(file);
      onImageSelected(file, url);
    } else {
      alert("Please upload a valid image file");
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const clearImage = () => {
    onImageSelected(null, null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="input-group">
      <label className="input-label">Face Image</label>
      
      {previewUrl ? (
        <div style={{ position: 'relative', width: '100%', maxWidth: '300px', margin: '0 auto', borderRadius: 'var(--radius-lg)', overflow: 'hidden', border: '1px solid var(--glass-border)' }}>
          <img src={previewUrl} alt="Preview" style={{ width: '100%', display: 'block' }} />
          <button 
            type="button" 
            onClick={clearImage}
            style={{ position: 'absolute', top: '0.5rem', right: '0.5rem', background: 'rgba(0,0,0,0.5)', border: 'none', color: 'white', borderRadius: '50%', padding: '0.25rem', cursor: 'pointer' }}
          >
            <X size={20} />
          </button>
        </div>
      ) : (
        <div 
          className="glass-panel"
          style={{ 
            padding: '3rem 2rem', 
            textAlign: 'center', 
            borderStyle: 'dashed', 
            borderWidth: '2px', 
            borderColor: dragActive ? 'var(--accent-primary)' : 'var(--glass-border)',
            cursor: 'pointer',
            transition: 'all 0.2s ease'
          }}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input 
            ref={fileInputRef}
            type="file" 
            accept="image/*" 
            onChange={handleChange} 
            style={{ display: 'none' }} 
          />
          <div className="flex-col items-center gap-sm">
            <Upload size={32} color={dragActive ? 'var(--accent-primary)' : 'var(--text-secondary)'} />
            <p style={{ color: dragActive ? 'var(--accent-primary)' : 'var(--text-primary)', fontWeight: 500 }}>
              Drag and drop an image here
            </p>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
              or click to browse from your computer
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
