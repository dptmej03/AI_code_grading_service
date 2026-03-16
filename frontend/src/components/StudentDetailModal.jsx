import React from 'react';

export default function StudentDetailModal({ student, onClose }) {
  const ratio = student.max_total_score > 0
    ? (student.total_score / student.max_total_score * 100).toFixed(1)
    : 0;

  return (
    <div style={s.overlay} onClick={onClose}>
      <div style={s.modal} onClick={e => e.stopPropagation()}>
        <div style={s.header}>
          <div>
            <h2 style={s.name}>{student.student_id}</h2>
            <p style={s.filename}>{student.filename}</p>
          </div>
          <div style={s.score}>
            <span style={s.scoreNum}>{student.total_score}</span>
            <span style={s.scoreDen}>/{student.max_total_score}</span>
            <span style={s.scorePct}>({ratio}%)</span>
          </div>
          <button style={s.closeBtn} onClick={onClose}>✕</button>
        </div>

        {student.error && (
          <div style={s.errorBox}>⚠️ {student.error}</div>
        )}

        <div style={s.body}>
          {student.problems.map(problem => (
            <div key={problem.problem_id} style={s.problem}>
              <div style={s.problemHeader}>
                <span style={s.problemTitle}>문제 {problem.problem_id}</span>
                <span style={s.problemScore}>
                  {problem.obtained_score} / {problem.full_score}점
                </span>
                {problem.output_match && (
                  <span style={s.badge}>✓ 출력 일치</span>
                )}
              </div>

              <div style={s.criteriaList}>
                {problem.partial_scores.map((ps, i) => (
                  <div key={i} style={s.criterion}>
                    <div style={s.criterionTop}>
                      <span style={s.criterionItem}>{ps.item}</span>
                      <span style={{
                        ...s.criterionScore,
                        color: ps.score === ps.max_score ? '#059669' : ps.score > 0 ? '#d97706' : '#dc2626'
                      }}>
                        {ps.score} / {ps.max_score}점
                      </span>
                    </div>
                    {ps.reason && (
                      <p style={s.reason}>{ps.reason}</p>
                    )}
                  </div>
                ))}
              </div>

              {problem.ai_feedback && (
                <div style={s.aiFeedback}>
                  <p style={s.aiFeedbackLabel}>💡 종합 피드백</p>
                  <p style={s.aiFeedbackText}>{problem.ai_feedback}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

const s = {
  overlay: { position:'fixed', inset:0, background:'rgba(0,0,0,0.5)', display:'flex', alignItems:'center', justifyContent:'center', zIndex:1000, padding:24 },
  modal: { background:'#fff', borderRadius:16, width:'100%', maxWidth:700, maxHeight:'85vh', display:'flex', flexDirection:'column', overflow:'hidden' },
  header: { display:'flex', alignItems:'flex-start', gap:16, padding:'24px 28px', borderBottom:'1px solid #e2e8f0' },
  name: { fontSize:20, fontWeight:700, color:'#1e293b', marginBottom:4 },
  filename: { fontSize:13, color:'#94a3b8' },
  score: { marginLeft:'auto', textAlign:'right' },
  scoreNum: { fontSize:32, fontWeight:700, color:'#1e293b' },
  scoreDen: { fontSize:18, color:'#94a3b8' },
  scorePct: { display:'block', fontSize:14, color:'#64748b', marginTop:2 },
  closeBtn: { background:'none', border:'1px solid #e2e8f0', borderRadius:8, width:36, height:36, cursor:'pointer', fontSize:16, color:'#64748b', flexShrink:0 },
  errorBox: { margin:'16px 28px 0', background:'#fef2f2', border:'1px solid #fecaca', color:'#dc2626', borderRadius:8, padding:'12px 16px', fontSize:14 },
  body: { overflowY:'auto', padding:'20px 28px', display:'flex', flexDirection:'column', gap:20 },
  problem: { border:'1px solid #e2e8f0', borderRadius:12, overflow:'hidden' },
  problemHeader: { display:'flex', alignItems:'center', gap:10, padding:'14px 18px', background:'#f8fafc', borderBottom:'1px solid #e2e8f0' },
  problemTitle: { fontWeight:700, fontSize:16, color:'#1e293b' },
  problemScore: { fontWeight:600, color:'#2563eb', marginLeft:'auto' },
  badge: { background:'#dcfce7', color:'#16a34a', borderRadius:20, padding:'2px 10px', fontSize:12, fontWeight:600 },
  criteriaList: { padding:'12px 18px', display:'flex', flexDirection:'column', gap:10 },
  criterion: { background:'#f8fafc', borderRadius:8, padding:'12px 14px' },
  criterionTop: { display:'flex', justifyContent:'space-between', marginBottom:6 },
  criterionItem: { fontWeight:600, fontSize:14, color:'#374151' },
  criterionScore: { fontWeight:700, fontSize:14 },
  reason: { fontSize:13, color:'#64748b', lineHeight:1.6, margin:0 },
  aiFeedback: { margin:'0 18px 14px', background:'#eff6ff', borderRadius:8, padding:'12px 14px' },
  aiFeedbackLabel: { fontSize:13, fontWeight:600, color:'#2563eb', marginBottom:6 },
  aiFeedbackText: { fontSize:13, color:'#374151', lineHeight:1.7, margin:0 }
};
