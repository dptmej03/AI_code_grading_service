# ⚡ 빠른 시작 가이드 (5분)

## 1️⃣ 필수 설치 (처음 한 번만)

### Python 설치 확인
```bash
python --version
# Python 3.9 이상 필요
```

### Node.js 설치 확인
```bash
node --version
npm --version
# Node.js 16 이상 필요
```

---

## 2️⃣ 백엔드 설정

### 터미널 1 (백엔드 실행)
```bash
cd backend
cp .env.example .env
```

**.env 파일 수정:**
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

**필요한 경우만:**
```env
LLM_PROVIDER=openai  # 기본값
OPENAI_BASE_URL=https://api.openai.com/v1
```

**설치 및 실행:**
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

✅ 성공 메시지:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

## 3️⃣ 프론트엔드 설정

### 터미널 2 (새로운 터미널 창에서)
```bash
cd frontend
npm install
npm start
```

✅ 브라우저가 자동으로 열리고:
```
http://localhost:3000
```

---

## 4️⃣ 로그인

| 항목 | 값 |
|------|-----|
| 아이디 | `professor` |
| 비밀번호 | `secret` |

---

## 5️⃣ 테스트 파일 준비

### Option A: 샘플 파일 사용 (권장 - 3분)

```bash
cd examples
python create_test_zip.py
```

생성된 파일:
- ✅ `answer.ipynb` (정답 파일)
- ✅ `students.zip` (학생 제출물 2명)
- ✅ `rubric.json` (채점 기준)

### Option B: 자신의 파일 사용

필요한 파일:
1. **answer.ipynb** - 모범 답안
2. **students.zip** - 학생들의 .ipynb 파일들을 압축
3. **rubric.json** - 채점 기준 (JSON 형식)

---

## 6️⃣ 채점 실행

### 웹 페이지에서:

1. **로그인** (professor / secret)
2. **파일 업로드**
   - 정답 노트북: `answer.ipynb` 드래그
   - 학생 ZIP: `students.zip` 드래그
   - 채점 기준: `rubric.json` 드래그
3. **채점 시작** 클릭

### 채점 진행 상황
- 실시간 진행률 표시
- 학생 수 / 처리 중인 학생 표시
- 약 1-2분 내 완료 (2명 기준)

### 결과 확인
1. 전체 통계 보기
2. 학생명 검색 또는 정렬
3. **[보기]** 버튼으로 상세 채점 결과 확인
4. **📥 Excel 다운로드** 버튼으로 다운로드

---

## 🎯 전체 흐름 (5분)

```
시간    작업                          터미널
─────────────────────────────────────────────────
0:00    backend 터미널 실행           터미널 1
0:30    frontend 터미널 실행          터미널 2
1:00    로그인 (professor/secret)
1:30    파일 업로드 (3개 파일)
2:00    채점 시작 클릭
2:30    실시간 진행률 모니터링
3:00    ✅ 채점 완료
3:30    결과 확인 및 Excel 다운로드
```

---

## 📋 체크리스트

- [ ] Python 3.9+ 설치됨
- [ ] Node.js 16+ 설치됨
- [ ] 터미널 1에서 backend 실행 중 (http://localhost:8000)
- [ ] 터미널 2에서 frontend 실행 중 (http://localhost:3000)
- [ ] 로그인 성공 (professor/secret)
- [ ] 파일 3개 준비 완료 (answer.ipynb, students.zip, rubric.json)
- [ ] 채점 시작 후 실시간 진행률 보임
- [ ] 결과 테이블 표시됨
- [ ] Excel 다운로드 성공

---

## ⚠️ 일반적인 문제 해결

### 문제 1: "http://localhost:3000에 접속 불가"
```bash
# 프론트엔드 프로세스 재시작
Ctrl+C (터미널 2에서)
npm start
```

### 문제 2: "OPENAI_API_KEY가 필요합니다"
```
1. backend/.env 파일 확인
2. OPENAI_API_KEY=sk-... 설정 추가
3. 백엔드 재시작
```

### 문제 3: "students.zip이 없습니다"
```bash
cd examples
python create_test_zip.py
```

### 문제 4: "npm: command not found"
```bash
# Node.js 재설치
# https://nodejs.org/ 에서 다운로드
```

### 문제 5: "pip install 오류"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔗 유용한 링크

| 항목 | 주소 |
|------|------|
| 프론트엔드 | http://localhost:3000 |
| API 문서 | http://localhost:8000/docs |
| OpenAI API | https://platform.openai.com/api-keys |
| 프로젝트 README | README.md |
| 사용 가이드 | USAGE_GUIDE.md |
| 샘플 파일 | examples/README.md |

---

## 📞 추가 정보

더 자세한 정보는:
- **README.md** - 프로젝트 개요 및 설정
- **USAGE_GUIDE.md** - 상세 화면 설명
- **examples/README.md** - 샘플 파일 설명
- **backend/.env.example** - 환경변수 옵션

---

## 🎓 다음 단계

### 자신의 과제에 적용하기

1. **answer.ipynb 준비**
   - Jupyter에서 모범 답안 작성
   - 각 문제를 "## 문제 N" 마크다운으로 분리
   - 모든 셀 실행하여 출력값 저장

2. **학생 제출물 수집**
   - 모든 학생 .ipynb 파일 수집
   - 파일명을 "학번_이름.ipynb" 형식으로 통일
   - 모두 하나의 ZIP 파일로 압축

3. **채점 기준 작성**
   - rubric.json 형식으로 작성
   - 문제별, 항목별 점수 설정
   - UTF-8로 저장

4. **채점 실행**
   - 위의 1-6단계 반복
   - 결과 확인 및 피드백 검토

---

**준비 완료! 이제 시작하세요! 🚀**
