import os
import json
from typing import List, Dict, Any, Tuple, Optional
from openai import AsyncOpenAI
import openai
from schemas import PartialScoreCriterion


class APIQuotaError(Exception):
    """OpenAI API 사용량 초과 시 발생하는 예외"""
    pass


def get_openai_client() -> AsyncOpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "")
    return AsyncOpenAI(api_key=api_key)


async def grade_with_ai(
    student_code: str,
    answer_code: str,
    criteria: List[PartialScoreCriterion],
    problem_id: int,
    problem_description: Optional[str] = None,
    execution_output: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], str]:
    """
    GPT-4o를 사용하여 채점 기준 기반 부분 점수 제도로 평가합니다.

    - 모범 답안과 실제 풀이가 달라도 논리가 타당하면 정답으로 인정
    - 다양한 구현 방식(List Comprehension, Map/Filter, For 루프 등) 모두 인정
    - 루브릭 기반 단계별 부분 점수 부여
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

    # 루브릭을 문자열로 포맷팅
    rubric_text = "\n".join([
        f"- {c.item}: 최대 {c.score}점"
        for c in criteria
    ])

    # 문제 설명 (있으면 포함)
    problem_context = ""
    if problem_description:
        problem_context = f"\n\n[문제 설명]\n{problem_description}"

    # 실행 결과 (있으면 포함)
    execution_context = ""
    if execution_output:
        execution_context = f"\n\n[코드 실행 결과]\n{execution_output}"

    system_prompt = """당신은 현업 시니어 개발자이자 꼼꼼한 컴퓨터공학 전공 조교입니다.

## 채점 원칙
1. **다양성 존중**: 학생의 구현 방식이 모범 답안과 다르더라도, 논리가 타당하고 결과가 올바르면 정답으로 인정하세요.
   - List Comprehension, Map/Filter, 일반 For 루프 등 모든 풀이 방식을 동등하게 평가합니다.

2. **유연한 부분 점수 부여**: 루브릭 항목이 "가이드라인에 부합 시"처럼 단일 기준으로 되어 있어도, 반드시 0점 아니면 만점의 이분법적 채점을 하지 마세요.
   - 문제 가이드라인에서 요구하는 세부 조건들을 스스로 파악하여 달성도에 따라 비례적으로 점수를 부여하세요.
   - 예: 요구 조건 4개 중 3개 충족 → 약 75% 점수 부여
   - 핵심 로직은 맞으나 사소한 오류가 있다면 → 70~90% 점수 부여
   - 방향은 맞으나 결과가 틀렸다면 → 30~50% 점수 부여
   - 전혀 시도하지 않았거나 완전히 무관한 코드 → 0점

3. **교육적 피드백**: 잘한 점을 먼저 인정하고, 개선할 점은 이유와 함께 설명하세요.

## 평가 절차
1. Analysis: 학생 코드의 핵심 로직과 가이드라인 달성도 분석
2. Rubric Evaluation: 각 항목별 달성 정도를 근거와 함께 점수 부여
3. Feedback: 잘한 점과 개선 방향을 친절하게 설명

반드시 다음 JSON 형식으로만 응답하세요:
{
  "analysis": "학생 코드의 핵심 로직과 문제 가이드라인 달성도에 대한 설명",
  "rubric_scores": [
    {"item": "항목명", "score": 점수, "max_score": 최대점수, "reason": "이유"},
    ...
  ],
  "total_score": 합계,
  "feedback": "잘한 점, 개선할 점, 제안사항"
}"""

    user_prompt = f"""[문제 {problem_id}] 다음 학생 코드를 평가해주세요.{problem_context}

## 모범 답안 (참고 자료 - 구현 방식이 다르면 틀린 것 아님)
```python
{answer_code[:2000]}
```

## 학생 코드
```python
{student_code[:3000]}
```{execution_context}

## 채점 루브릭
{rubric_text}

위의 루브릭에 기반하여 학생 코드를 평가하세요.
모범 답안의 구현 방식과 다르더라도, 문제를 올바르게 해결했고 루브릭의 기준들을 충족한다면 정답으로 인정하세요."""

    client = get_openai_client()

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            max_tokens=2048,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        content = response.choices[0].message.content

        # JSON 파싱 (마크다운 코드블록 제거)
        content = content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            if lines[-1].strip() == "```":
                content = "\n".join(lines[1:-1])
            else:
                content = "\n".join(lines[1:])

        data = json.loads(content)
        rubric_scores = data.get("rubric_scores", [])
        overall_feedback = data.get("feedback", "")

        # 루브릭 점수를 채점 기준 항목과 매칭
        graded = []
        for c in criteria:
            found = next((r for r in rubric_scores if r.get("item") == c.item), None)
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
                    "reason": "평가 항목을 찾을 수 없습니다"
                })

        return graded, overall_feedback

    except json.JSONDecodeError as e:
        return [
            {
                "item": c.item,
                "max_score": c.score,
                "score": 0,
                "reason": f"AI 응답 파싱 오류: {str(e)}"
            }
            for c in criteria
        ], f"AI 평가 중 응답 형식 오류: {str(e)}"

    except openai.RateLimitError as e:
        raise APIQuotaError(str(e))

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
