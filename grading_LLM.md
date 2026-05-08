# 채점 모델 라인업

## 현재 사용 중인 모델 (`llm_service.py` > `AVAILABLE_MODELS`)

### OpenAI

| 라벨 | 모델 ID | 특징 |
|------|---------|------|
| gpt-4o-mini | `openai/gpt-4o-mini` | 빠르고 저렴, 간단한 채점 |
| gpt-4o | `openai/gpt-4o` | 고성능, 비용 높음 |
| gpt-4.1-mini | `openai/gpt-4.1-mini` | 최신 경량 모델 |

### Fireworks (외부 오픈소스)

| 라벨 | 모델 ID | 풀네임 | 추론 여부 | 특징 |
|------|---------|--------|-----------|------|
| deepseek-v3.2 | `fireworks/accounts/fireworks/models/deepseek-v3p2` | DeepSeek V3.2 | ❌ 일반 LLM | 코딩 강점, 안정적 |
| kimi-k2.6 | `fireworks/accounts/fireworks/models/kimi-k2p6` | Kimi K2.6 | ❌ 일반 LLM | MoE 구조, 1028B 파라미터 |
| qwen3.6-plus | `fireworks/accounts/fireworks/models/qwen3p6-plus` | Qwen3.6 Plus | ❌ 일반 LLM | Alibaba 최신 모델, 강력한 성능 |

---

## 제거된 모델

| 라벨 | 이유 |
|------|------|
| `deepseek-v4(추론)` / `deepseek-v4-pro` | 추론 모델 → 채점에 불필요, qwen3.6-plus로 교체 |
| `kimi-k2-instruct` | 모델 ID 오류 → kimi-k2p6으로 교체 |
| `qwen3.5-35b-a3b` | 모델 ID 오류 → qwen3p6-plus로 교체 |

---

## 채점 모델 선택 기준

- **추론(Thinking) 모델** → 채점에 비추천 (느리고 비싸고, JSON 파싱 오류 가능)
- **일반 LLM** → 채점 권장 (빠르고, JSON 포맷 응답 안정적)
- **한국어 과제 채점** → Qwen 계열이 유리
- **코딩 과제** → DeepSeek 계열이 유리
