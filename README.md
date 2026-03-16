# Jupyter Notebook 자동 채점 시스템

## 시작하기

### 1. 백엔드 설정

```bash
cd backend
cp .env.example .env
# .env 파일에서 OPENAI_API_KEY 설정
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. 프론트엔드 실행

```bash
cd frontend
npm install
npm start
```

### 3. 접속

- 프론트엔드: http://localhost:3000
- 백엔드 API 문서: http://localhost:8000/docs

## 로그인 계정

- 아이디: `professor`
- 비밀번호: `secret`

## 사용 방법

1. 로그인
2. 정답 `.ipynb` 파일 업로드
3. 학생 제출물 `.zip` 파일 업로드
4. 채점 기준 `.json` 파일 업로드
5. 채점 시작
6. 결과 확인 및 Excel 다운로드

## 채점 기준 JSON 예시

```json
{
  "problems": [
    {
      "problem_id": 1,
      "full_score": 20,
      "partial_score_criteria": [
        { "item": "변수명 적절성", "score": 5 },
        { "item": "알고리즘 정확성", "score": 10 },
        { "item": "출력값 일치", "score": 5 }
      ]
    }
  ]
}
```

## .env 설정

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
```
