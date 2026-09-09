from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

email = """
안녕하세요, 홍길동 부장님.

다음 주 월요일(8/10) 오후 2시에 AI 프로젝트
진행 상황 공유 미팅을 요청드립니다.
가능하시면 답변 부탁드립니다.

IT팀 박철수 드림
"""

# v1 — 최소 동작: 일단 요약이 되는지 확인
v1 = llm.invoke(f"이메일 요약:\n{email}")
print("=== v1 ==="); print(v1.content)
# 예상 출력: "이 이메일은 8/10 2시 미팅을 요청하는 내용입니다."
# 문제: 너무 길고, 임원이 판단하기 어려운 형식

# v2 — 형식 지정: 원하는 필드 구조 추가
v2 = llm.invoke(
    f"아래 형식으로 이메일 요약:\n"
    f"- 발신자:\n"
    f"- 핵심 요청:\n"
    f"- 시급성:\n"
    f"\n이메일:\n{email}"
)
print("=== v2 ==="); print(v2.content)
# 예상 출력: "발신자: 박철수 / 핵심 요청: 미팅 요청 / 시급성: 보통"
# 개선: 포맷 생김. 문제: 시급성 판단 기준 없어 AI마다 다르게 판단

# v3 — 역할 + 독자 + 제약: 누가 읽는지, 어떤 판단을 내려야 하는지 명시
v3 = llm.invoke(
    f"바쁜 임원 보고 관점으로 이메일을 요약해.\n"
    f"형식:\n"
    f"- 이름:\n"
    f"- 핵심 요청 (20자 이내):\n"
    f"- 필요 조치 (즉시처리/검토필요/참고):\n"
    f"- 기한:\n"
    f"\n이메일:\n{email}"
)
print("=== v3 ==="); print(v3.content)
# 예상 출력:
# 이름: 박철수
# 핵심 요청: 8/10 AI미팅 참석요청 (14자)
# 필요 조치: 검토필요
# 기한: 8/10 이전 답변 필요