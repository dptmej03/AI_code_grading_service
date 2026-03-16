# 🚀 지금 바로 실행하기 (npm start)

## 📋 준비 사항 확인

```bash
python --version      # 3.9 이상 필요
node --version        # 16 이상 필요
npm --version         # 7 이상 필요
```

---

## 🎯 3단계로 실행

### Step 1️⃣: 백엔드 실행 (터미널 1)

```bash
cd backend

# 1. .env 파일 생성
cp .env.example .env

# 2. .env 파일 편집 (아래 항목 추가)
# OPENAI_API_KEY=sk-your-actual-key-here
# (또는 나중에 추가해도 됨)

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 서버 실행
uvicorn main:app --reload --port 8000
```

**✅ 성공 메시지:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**📍 주소:** http://localhost:8000

---

### Step 2️⃣: 프론트엔드 실행 (터미널 2)

```bash
cd frontend

# 1. 의존성 설치 (처음 한 번만)
npm install

# 2. 개발 서버 실행
npm start
```

**✅ 성공 메시지:**
```
Compiled successfully!

You can now view ipynb-grading-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
Press q to quit.
```

**📍 주소:** http://localhost:3000

---

### Step 3️⃣: 브라우저에서 접속

```
http://localhost:3000
```

**로그인:**
```
아이디: professor
비밀번호: secret
```

---

## ⚡ 빠른 체크리스트

- [ ] 터미널 1: `uvicorn` 실행 중
- [ ] 터미널 2: `npm start` 완료
- [ ] 브라우저에서 http://localhost:3000 접속
- [ ] 로그인 성공 (professor/secret)
- [ ] 파일 업로드 페이지 보임

---

## 🧪 테스트하기

### 1. 샘플 ZIP 파일 생성

```bash
cd examples
python create_test_zip.py
```

**생성 결과:**
```
✓ 20210001_홍길동.ipynb 추가됨
✓ 20210002_김영희.ipynb 추가됨

✅ students.zip 생성 완료!
   위치: c:/Users/User/Desktop/UNI Esthr/ipynb-grading-system/examples/students.zip
```

### 2. 웹에서 파일 업로드

**3개 파일 준비:**
```
examples/answer.ipynb        ← 정답 파일
examples/students.zip         ← 학생 제출물 (ZIP)
examples/rubric.json          ← 채점 기준
```

**업로드:**
1. 로그인 후 "파일 업로드" 페이지
2. 3개 파일 드래그&드롭
3. "채점 시작" 클릭

### 3. 결과 확인

- ✅ 진행률 바 실시간 표시
- ✅ 약 1-2분 후 채점 완료
- ✅ 학생별 점수 테이블 표시
- ✅ Excel 다운로드 가능

---

## 🔌 포트 정보

| 서비스 | 포트 | URL | 용도 |
|--------|------|-----|------|
| 백엔드 | 8000 | http://localhost:8000 | API 서버 |
| 프론트엔드 | 3000 | http://localhost:3000 | 웹 페이지 |
| FastAPI Docs | 8000 | http://localhost:8000/docs | API 문서 |

---

## 📝 API 문서 (선택사항)

백엔드가 실행 중이면 API 문서 확인 가능:

```
http://localhost:8000/docs
```

여기서 모든 API 엔드포인트 테스트 가능:
- POST /auth/login
- POST /grading/start
- GET /grading/session/{id}
- GET /grading/session/{id}/download
- 등등...

---

## ⚙️ 환경 변수 설정 (.env)

**중요:** GPT 채점을 사용하려면 API 키 필요

```bash
# backend/.env 파일
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...  # ← OpenAI 키 입력
OPENAI_BASE_URL=https://api.openai.com/v1
```

**OpenAI 키 구하기:**
1. https://platform.openai.com/api-keys 방문
2. "Create new secret key" 클릭
3. 키 복사
4. .env에 붙여넣기

---

## 🛑 서버 중지하기

```bash
# 터미널에서:
Ctrl + C

# 또는 터미널 창 닫기
```

---

## 🔄 재시작하기

```bash
# 터미널 1
cd backend && uvicorn main:app --reload --port 8000

# 터미널 2
cd frontend && npm start
```

---

## 📱 다른 기기에서 접속

프론트엔드가 실행되면 로컬 네트워크 주소 표시:

```
On Your Network:  http://192.168.x.x:3000
```

같은 와이파이 네트워크의 다른 컴퓨터에서 이 주소로 접속 가능!

---

## 🆘 문제 해결

### 에러: "npm: command not found"
```bash
→ Node.js 재설치 (https://nodejs.org)
→ 터미널 재시작
```

### 에러: "포트 3000 이미 사용 중"
```bash
→ 기존 Node 프로세스 종료
→ 또는 다른 포트 사용: PORT=3001 npm start
```

### 에러: "uvicorn: command not found"
```bash
→ pip install -r requirements.txt 다시 실행
→ 터미널 재시작
```

### 에러: "OPENAI_API_KEY 없음"
```bash
→ .env 파일에 키 추가
→ 백엔드 재시작 (Ctrl+C, 다시 실행)
```

### 에러: "학생 노트북 실행 실패"
```bash
→ python 3.9+ 설치 확인
→ 백엔드 콘솔에서 에러 메시지 확인
```

---

## 🎯 다음 단계

✅ 현재: 로컬에서 npm start로 개발

🔮 향후:
- 프로덕션 빌드 (`npm run build`)
- Docker 배포
- 데이터베이스 연동

지금은 **개발 모드로 충분합니다!** 🚀

---

**준비 완료! 터미널 2개를 열고 아래 명령어를 실행하세요:**

```bash
# 터미널 1
cd backend && uvicorn main:app --reload --port 8000

# 터미널 2
cd frontend && npm start
```

**3초 후 브라우저에서 http://localhost:3000 이 자동으로 열립니다!** 🎉
