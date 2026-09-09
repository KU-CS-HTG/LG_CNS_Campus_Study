# rcif_comparison.py
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage  # 역할별 메시지 타입

load_dotenv()                                           # .env에서 API 키 로드
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)   # temperature=0: 일관된 출력

meeting_text = """
박팀장: 신제품 출시를 8월 15일로 확정하자고 제안합니다.
김팀장: 동의합니다. 마케팅은 SNS 먼저 시작하고요.
이팀장: AI 추천 기능은 9월 적용하겠습니다. 개발 일정 필요해요.
"""

# ❌ RCIF 없음 — AI가 정리 형식을 임의로 선택
bad = llm.invoke(f"회의록 정리해줘:\n{meeting_text}")
print("=== RCIF 없음 ===")
print(bad.content)
# 예상 출력: "신제품 출시는 8월 15일로 결정되었습니다. 마케팅팀은..."
# (형식 없음, 길이 불규칙, 요청한 구조 없음)

# ✅ RCIF 적용 — 역할·배경·지시·형식을 명확히 전달
good = llm.invoke([
    SystemMessage(content="[R] 당신은 비즈니스 커뮤니케이션 전문가입니다."),
    # SystemMessage: AI의 전반적 역할과 행동 원칙 설정
    HumanMessage(content=f"""[C] 킥오프 회의 기록입니다.
{meeting_text}

[I] 아래 형식으로 정리해주세요.
[F]
1. 핵심 결정 사항 (번호 목록)
2. 액션 아이템 표: 담당자 | 내용 | 기한
3. 다음 회의 안건"""),
    # HumanMessage: 실제 사용자 입력 (배경 + 지시 + 형식)
])
print("\n=== RCIF 적용 ===")
print(good.content)
# 예상 출력:
# 1. 핵심 결정 사항
#    1) 신제품 출시일 8월 15일 확정
#    2) 마케팅: SNS 채널 우선 시작
# 2. 액션 아이템
#    | 담당자 | 내용               | 기한 |
#    | 이팀장 | 개발 일정 공유     | 미정 |
# 3. 다음 회의 안건
#    - AI 추천 기능 개발 일정 확인