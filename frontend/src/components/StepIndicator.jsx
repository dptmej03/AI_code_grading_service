import React from 'react';

export default function StepIndicator({ steps, current }) {
  return (
    <div style={s.wrapper}>
      {steps.map((step, i) => (
        <React.Fragment key={i}>
          <div style={s.step}>
            <div style={{
              ...s.circle,
              background: i < current ? '#22c55e' : i === current ? '#2563eb' : '#e2e8f0',
              color: i <= current ? '#fff' : '#94a3b8'
            }}>
              {i < current ? '✓' : i + 1}
            </div>
            <span style={{ ...s.label, color: i === current ? '#2563eb' : i < current ? '#22c55e' : '#94a3b8', fontWeight: i === current ? 600 : 400 }}>
              {step}
            </span>
          </div>
          {i < steps.length - 1 && (
            <div style={{ ...s.line, background: i < current ? '#22c55e' : '#e2e8f0' }} />
          )}
        </React.Fragment>
      ))}
    </div>
  );
}

const s = {
  wrapper: { display:'flex', alignItems:'center', marginBottom:32, padding:'20px 0' },
  step: { display:'flex', flexDirection:'column', alignItems:'center', gap:6 },
  circle: { width:32, height:32, borderRadius:'50%', display:'flex', alignItems:'center', justifyContent:'center', fontSize:14, fontWeight:700 },
  label: { fontSize:12, whiteSpace:'nowrap' },
  line: { flex:1, height:2, margin:'0 8px', marginTop:-16 }
};
