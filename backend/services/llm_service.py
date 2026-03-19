import os
import json
from typing import List, Dict, Any, Tuple
import anthropic
from schemas import PartialScoreCriterion


def get_anthropic_client() -> anthropic.AsyncAnthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    return anthropic.AsyncAnthropic(api_key=api_key)


async def grade_with_ai(
    student_code: str,
    answer_code: str,
    criteria: List[PartialScoreCriterion],
    problem_id: int
) -> Tuple[List[Dict[str, Any]], str]:
    """
    Claude claude-sonnet-4-6으로 채점 기준 기반 채점.
    유사도 비교 없이 채점 기준 항목 충족 여부만 평가합니다.
    """
    if not student_code.strip():
        results = [
            {
                "item": c.item,
                "max_score": c.score,
                "score": 0,
                "reason": "제출된 코드가 없습니다."
            }
            for c in criteria
        ]
        return results, "코드가 제출되지 않았습니다."

    criteria_text = "\n".join([
        f"- {c.item}: 최대 {c.score}점"
        for c in criteria
    ])

    system_prompt = """당신은 대학 프로그래밍 과목의 채점 전문가입니다.
학생의 코드를 채점 기준 항목에 따라 평가합니다.
중요: 정답 코드와의 유사도가 아니라, 각 채점 기준 항목을 코드가 충족하는지만 평가하세요.
학생이 다른 방식으로 풀었더라도 기준을 충족하면 정답으로 인정하세요.
반드시 JSON 형식으로만 응답하세요."""

    user_prompt = f"""[문제 {problem_id}] 채점을 수행하세요.

## 학생 코드
```python
{student_code[:3000]}
```

## 채점 기준
{criteria_text}

각 채점 기준 항목을 학생 코드가 충족하는지 평가하세요.
기준을 충족하면 해당 배점 전부, 부분 충족이면 부분점수, 미충족이면 0점을 부여하세요.
피드백은 구체적이고 교육적으로 작성하세요.

다음 JSON 형식으로만 응답하세요:
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
}}"""

    client = get_anthropic_client()

    try:
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        content = response.content[0].text

        # JSON 파싱 (마크다운 코드블록 제거)
        content = content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1]) if lines[-1] == "```" else "\n".join(lines[1:])

        data = json.loads(content)
        results = data.get("results", [])
        overall = data.get("overall_feedback", "")

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

    except json.JSONDecodeError as e:
        return [
            {
                "item": c.item,
                "max_score": c.score,
                "score": 0,
                "reason": f"AI 응답 파싱 오류: {str(e)}"
            }
            for c in criteria
        ], f"AI 응답을 파싱하는 중 오류 발생: {str(e)}"

    except Exception as e:
        return [
            {
                "item": c.item,
                "max_score": c.score,
                "score": 0,
                "reason": f"AI 채점 오류: {str(e)}"
            }
            for c in criteria
        ], f"AI 채점 중 오류 발생: {str(e)}"
