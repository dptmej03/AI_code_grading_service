import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import { useAuth } from '../App';
import { gradingAPI } from '../services/api';
import StepIndicator from '../components/StepIndicator';

const STEPS = ['파일 업로드', '채점 기준 설정', '채점 실행'];

function DropZone({ label, icon, accept, onDrop, file }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, accept, multiple: false
  });
  return (
    <div {...getRootProps()} style={{
      ...dz.zone,
      borderColor: isDragActive ? '#2563eb' : file ? '#22c55e' : '#cbd5e1',
      background: isDragActive ? '#eff6ff' : file ? '#f0fdf4' : '#f8fafc',
    }}>
      <input {...getInputProps()} />
      <div style={dz.icon}>{file ? '✅' : icon}</div>
      <div style={dz.label}>{label}</div>
      {file
        ? <div style={dz.filename}>{file.name}</div>
        : <div style={dz.hint}>클릭하거나 파일을 드래그하세요</div>
      }
    </div>
  );
}

const dz = {
  zone: {
    border: '2px dashed', borderRadius: 12, padding: '28px 20px',
    textAlign: 'center', cursor: 'pointer', transition: 'all 0.2s'
  },
  icon: { fontSize: 32, marginBottom: 8 },
  label: { fontWeight: 600, color: '#374151', marginBottom: 4 },
  hint: { fontSize: 13, color: '#94a3b8' },
  filename: { fontSize: 13, color: '#22c55e', fontWeight: 500, marginTop: 4 }
};

export default function UploadPage() {
  const [step] = useState(0);
  const [answerFile, setAnswerFile] = useState(null);
  const [zipFile, setZipFile] = useState(null);
  const [criteriaFile, setCriteriaFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleStart = async () => {
    if (!answerFile || !zipFile || !criteriaFile) {
      setError('모든 파일을 업로드해주세요');
      return;
    }
    setError('');
    setLoading(true);
    try {
      const fd = new FormData();
      fd.append('answer_notebook', answerFile);
      fd.append('student_zip', zipFile);
      fd.append('criteria_file', criteriaFile);
      const res = await gradingAPI.startGrading(fd);
      navigate(`/dashboard/${res.data.session_id}`);
    } catch (err) {
      setError(err.response?.data?.detail || '채점 시작에 실패했습니다');
    } finally {
      setLoading(false);
    }
  };

  const allReady = answerFile && zipFile && criteriaFile;

  return (
    <div style={s.page}>
      <header style={s.header}>
        <div style={s.headerLeft}>
          <span style={{fontSize:24}}>📓</span>
          <span style={s.headerTitle}>Jupyter 자동 채점 시스템</span>
        </div>
        <div style={s.headerRight}>
          <span style={s.userName}>{user?.username} ({user?.role})</span>
          <button style={s.logoutBtn} onClick={logout}>로그아웃</button>
        </div>
      </header>

      <main style={s.main}>
        <StepIndicator steps={STEPS} current={step} />

        <div style={s.card}>
          <h2 style={s.cardTitle}>파일 업로드</h2>
          <p style={s.cardDesc}>채점에 필요한 파일을 모두 업로드해주세요</p>

          <div style={s.grid}>
            <DropZone
              label="정답 노트북"
              icon="📝"
              accept={{ 'application/x-ipynb+json': ['.ipynb'] }}
              onDrop={([f]) => setAnswerFile(f)}
              file={answerFile}
            />
            <DropZone
              label="학생 제출물 (ZIP)"
              icon="📦"
              accept={{ 'application/zip': ['.zip'], 'application/x-zip-compressed': ['.zip'] }}
              onDrop={([f]) => setZipFile(f)}
              file={zipFile}
            />
            <DropZone
              label="채점 기준 (JSON)"
              icon="📋"
              accept={{ 'application/json': ['.json'] }}
              onDrop={([f]) => setCriteriaFile(f)}
              file={criteriaFile}
            />
          </div>

          {error && <div style={s.error}>{error}</div>}

          <div style={s.actions}>
            <button
              style={allReady && !loading ? s.primaryBtn : {...s.primaryBtn, opacity:0.5, cursor:'not-allowed'}}
              onClick={handleStart}
              disabled={!allReady || loading}
            >
              {loading ? '채점 시작 중...' : '채점 시작 →'}
            </button>
          </div>

          <div style={s.formatHint}>
            <h3 style={s.hintTitle}>채점 기준 JSON 형식</h3>
            <pre style={s.pre}>{JSON.stringify({
              problems: [{
                problem_id: 1, full_score: 20,
                partial_score_criteria: [
                  { item: "변수명 적절성", score: 5 },
                  { item: "알고리즘 정확성", score: 10 },
                  { item: "출력값 일치", score: 5 }
                ]
              }]
            }, null, 2)}</pre>
          </div>
        </div>
      </main>
    </div>
  );
}

const s = {
  page: { minHeight: '100vh', background: '#f8fafc' },
  header: {
    background: '#fff', borderBottom: '1px solid #e2e8f0',
    padding: '0 32px', height: 64, display: 'flex',
    alignItems: 'center', justifyContent: 'space-between'
  },
  headerLeft: { display: 'flex', alignItems: 'center', gap: 10 },
  headerTitle: { fontSize: 18, fontWeight: 700, color: '#1e293b' },
  headerRight: { display: 'flex', alignItems: 'center', gap: 16 },
  userName: { fontSize: 14, color: '#64748b' },
  logoutBtn: {
    background: 'none', border: '1px solid #e2e8f0', borderRadius: 6,
    padding: '6px 14px', cursor: 'pointer', fontSize: 14, color: '#64748b'
  },
  main: { maxWidth: 900, margin: '0 auto', padding: '32px 24px' },
  card: { background: '#fff', borderRadius: 16, padding: 32, boxShadow: '0 1px 8px rgba(0,0,0,0.07)' },
  cardTitle: { fontSize: 20, fontWeight: 700, color: '#1e293b', marginBottom: 8 },
  cardDesc: { color: '#64748b', marginBottom: 24 },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 },
  error: { background: '#fef2f2', border: '1px solid #fecaca', color: '#dc2626', borderRadius: 8, padding: '12px 16px', marginBottom: 16 },
  actions: { display: 'flex', justifyContent: 'flex-end', marginBottom: 32 },
  primaryBtn: {
    background: '#2563eb', color: '#fff', border: 'none',
    borderRadius: 10, padding: '13px 32px', fontSize: 16, fontWeight: 600, cursor: 'pointer'
  },
  formatHint: { background: '#f8fafc', borderRadius: 10, padding: 20, border: '1px solid #e2e8f0' },
  hintTitle: { fontSize: 14, fontWeight: 600, color: '#374151', marginBottom: 12 },
  pre: { fontSize: 12, color: '#374151', overflowX: 'auto', lineHeight: 1.6 }
};
