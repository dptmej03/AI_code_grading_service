feedback과 score, reason과 score는 반드시 일관되어야 합니다.

**reason ↔ score 자동 매핑 규칙 (CRITICAL)**:
- reason이 "완전 충족"을 시사하면 → score = max_score
- reason이 "부분 충족"을 시사하면 → score = max_score * 0.5 (반드시!)
- reason이 "완전 불충족"을 시사하면 → score = 0

**"부분 충족"으로 간주되는 reason 표현 (이런 표현 쓰면 반드시 score = max_score * 0.5)**:
- "A는 했지만 B는 안 함" / "A는 했으나 B는 못함"
- "A는 있지만 B가 부족" / "A는 있으나 B가 없음"
- "A는 잘했으나 B는 미흡"
- "일부만 충족", "한 가지만 함", "절반만"
- "요구사항 중 일부 누락"
- "주요 부분은 했으나 세부사항 누락"

**예시**:
- reason: "평활화 설명은 있지만 YCrCb 변환 이유 설명이 없음" → score = max_score * 0.5 (절대 0이면 안 됨)
- reason: "개념은 잘 설명했으나 처리 과정 설명이 부족" → score = max_score * 0.5
- reason: "원본과 결과는 출력했으나 이진화 영상이 누락됨" → score = max_score * 0.5

단, 해당 항목의 코드 자체에 로직 오류가 있으면 위 규칙과 무관하게 0점.
