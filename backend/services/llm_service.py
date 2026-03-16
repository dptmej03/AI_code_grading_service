import os
import json
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from schemas import PartialScoreCriterion


def get_openai_client() -> AsyncOpenAI:
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    api_key = os.getenv("OPENAI_API_KEY", "")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    return AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )


async def grade_with_ai(
    student_code: str,
    answer_code: str,
    criteria: List[PartialScoreCriterion],
    problem_id: int
) -> List[Dict[str, Any]]:
    """
    GPT-4o로 학생 코드를 분석하여 채점 기준별 점수 및 피드백 반환.
    반환: [{"item": str, "max_score": float, "score": float, "reason": str}, ...]
    """
    client = get_openai_client()

    criteria_text = "\n".join([
        f"- {c.item}: 최대 {c.score}점"
        for c in criteria
    ])

    system_prompt = """당신은 대학 프로그래밍 과목의 채점 전문가입니다.
학생의 코드를 분석하여 각 채점 항목에 대해 점수와 상세한 피드백을 제공해주세요.
반드시 JSON 형식으로만 응답하세요."""

    user_prompt = f"""[문제 {problem_id}] 채점을 수행하세요.

## 정답 코드
```python
{answer_code[:3000]}
```

## 학생 코드
```python
{student_code[:3000]}
```

## 채점 기준
{criteria_text}

다음 JSON 형식으로 각 채점 항목을 평가하세요:
{{
  "results": [
    {{
      "item": "채점 항목명",
      "max_score": 최대점수(숫자),
      "score": 획득점수(숫자),
      "reason": "점수 부여 이유 및 상세 피드백 (한국어로 작성)"
    }}
  ],
  "overall_feedback": "전체적인 코드 품질 및 개선 제안"
}}

채점 시 유의사항:
- 부분점수를 적극 활용하세요
- 학생이 노력한 부분을 인정하세요
- 오류가 있더라도 로직이 맞으면 부분점수를 주세요
- 피드백은 구체적이고 교육적으로 작성하세요"""

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        data = json.loads(content)
        results = data.get("results", [])
        overall = data.get("overall_feedback", "")

        # Map results back to criteria
        graded = []
        for c in criteria:
            found = next((r for r in results if r.get("item") == c.item), None)
            if found:
                graded.append({
                    "item": c.item,
                    "max_score": c.score,
                    "score": min(float(found.get("score", 0)), c.score),
                    "reason": found.get("reason", "")
                })
            else:
                graded.append({
                    "item": c.item,
                    "max_score": c.score,
                    "score": 0,
                    "reason": "채점 항목을 찾을 수 없습니다"
                })

        return graded, overall
    except Exception as e:
        # Fallback: return 0 scores with error message
        return [
            {
                "item": c.item,
                "max_score": c.score,
                "score": 0,
                "reason": f"AI 채점 오류: {str(e)}"
            }
            for c in criteria
        ], f"AI 채점 중 오류 발생: {str(e)}"
