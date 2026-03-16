import React from 'react';
import { useDropzone } from 'react-dropzone';

export default function FileDropzone({ label, icon, accept, onDrop, file }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept, multiple: false });
  return (
    <div {...getRootProps()} style={{
      border: `2px dashed ${file ? '#22c55e' : isDragActive ? '#2563eb' : '#cbd5e1'}`,
      borderRadius: 12, padding: '28px 20px', textAlign: 'center', cursor: 'pointer',
      background: file ? '#f0fdf4' : isDragActive ? '#eff6ff' : '#f8fafc', transition: 'all 0.2s'
    }}>
      <input {...getInputProps()} />
      <div style={{ fontSize: 32, marginBottom: 8 }}>{file ? '✅' : icon}</div>
      <div style={{ fontWeight: 600, color: '#374151', marginBottom: 4 }}>{label}</div>
      {file
        ? <div style={{ fontSize: 13, color: '#22c55e', fontWeight: 500 }}>{file.name}</div>
        : <div style={{ fontSize: 13, color: '#94a3b8' }}>클릭하거나 드래그하세요</div>
      }
    </div>
  );
}
