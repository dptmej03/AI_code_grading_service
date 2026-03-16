#!/bin/bash
echo "=== Jupyter 자동 채점 시스템 시작 ==="

# Backend
cd backend
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo ".env 파일이 생성되었습니다. API 키를 설정해주세요."
fi
pip install -r requirements.txt -q
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Frontend
cd frontend
npm install -q
npm start &
FRONTEND_PID=$!

echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Ctrl+C to stop"
wait
