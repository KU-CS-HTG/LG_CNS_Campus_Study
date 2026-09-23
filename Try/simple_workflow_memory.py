#messages.append 부분을 memory를 활용하여 바꾸기
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from datetime import datetime
from langchain_tavily import TavilySearch as _TS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

@tool
def web_search(query: str, max_results: int = 5) -> str:
    """
    웹을 실시간으로 검색해 최신 정보를 가져옵니다.
    사용 시점: 기존 모델이 학습하지 않은 정보가 입력으로 들어왔을 때
    Args:
        query: 검색어 (한국어/영어 모두 가능)
        max_results: 반환할 결과 수 (기본 5, 최대 20)
    """
    results = _TS(max_results=max_results).invoke(query)["results"]
    return "\n---\n".join(
        f"제목: {d.get('title','N/A')}\nURL: {d.get('url','')}\n내용: {d.get('content','')}"
        for d in results
    )

import json as _j
# print("📋 web_search 도구 스키마:")
# print(_j.dumps(web_search.args_schema.model_json_schema(), ensure_ascii=False, indent=2))

@tool
def get_employee_info(employee_id: str) -> dict:
    """
    직원 정보를 DB에서 조회합니다.

    사용 시점: 특정 직원의 이름, 부서, 직급 정보가 필요할 때.
    주의: 직원 ID는 반드시 'EMP' + 3자리 숫자 형식 (예: EMP001)

    Args:
        employee_id: 직원 고유 ID (형식: EMP + 3자리 숫자)
    Returns:
        직원 정보 dict: name, dept, level 키 포함
    """
    db = {
        "EMP001": {"name": "김철수", "dept": "AI개발팀",  "level": "팀장"},
        "EMP002": {"name": "이영희", "dept": "기획팀",    "level": "PM"},
        "EMP003": {"name": "박민준", "dept": "데이터팀",  "level": "시니어"},
    }
    return db.get(employee_id, {"error": f"직원 없음: {employee_id}"})

# AI에게 전달되는 스키마 확인 — Day 3 타입 힌트 → Pydantic 스키마 변환
import json as _json
schema = get_employee_info.args_schema.model_json_schema()
# print("📋 AI가 받는 도구 스키마:")
# print(_json.dumps(schema, ensure_ascii=False, indent=2))

@tool
def calculate(expression: str) -> str:
    """
    수학 계산을 수행합니다.
    사용 시점: 사칙연산 등 숫자 계산이 필요할 때.
    expression: 계산 가능한 수식 (예: '1234 * 567', '100 / 4')
    """
    # ⚠️ 교육용 코드: eval()은 프로덕션에서 사용 금지 (보안 취약점)
    try: return str(eval(expression))
    except Exception as e: return f"계산 오류: {str(e)}"

@tool
def current_date() -> str:
    """
    현재 날짜를 조회합니다.

    사용 시점: 오늘 날짜·현재 시각이 필요할 때.
    예시 질문: '오늘 몇 월이야?', '지금 몇 년도야?', '이번 달이 뭐야?'

    Returns:
        str: YYYY-MM-DD 형식의 현재 날짜
    """
    return datetime.now().strftime("%Y-%m-%d")


def simple_workflow(llm, question: str, tools: list) -> str:
    """
    질문과 도구 목록을 받아 도구 호출이 완료될 때까지 반복 실행합니다.
    """
    tool_list = {t.name: t for t in tools}           # TODO ① — 이름→함수 dict
    llm_wt = llm.bind_tools(tools)
    messages = [HumanMessage(content=question)]
    # print(messages)

    print(f"Q: {question}")
    ai_msg = llm_wt.invoke(messages)
    messages.append(ai_msg)
    # print(messages)

    while ai_msg.tool_calls:                  # TODO ② — ai_msg.tool_calls 조건
        for tc in ai_msg.tool_calls:
            # print(tc)
            tname = tc["name"]
            # print(f"  → 도구: {tname} | args: {tc['args']}")
            tool_exec = tool_list[tname]    # TODO ③ — tool_list에서 함수 꺼내기
            tool_result = tool_exec.invoke(tc)
            messages.append(tool_result)
            # print(messages)
        ai_msg = llm_wt.invoke(messages)
        # print(ai_msg)
        messages.append(ai_msg)

    return ai_msg.content

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ── 테스트 ─────────────────────────────────────────────────────────────
tools_basic = [get_employee_info, calculate, current_date, web_search]

r1 = simple_workflow(llm, "EMP002 직원 정보 알려줘", tools_basic)
print(f"A: {r1}\n")

SYSTEM_CONTENT = "너는 내 비서야. 짧고 구조적으로 대답해줘."

prompt_with_history = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_CONTENT),
    MessagesPlaceholder("chat_history"),   # ← 이전 대화 목록 삽입 위치
    ("human", "{input}")
])
chain_with_history = prompt_with_history | llm_wt | StrOutputParser()


# r2 = simple_workflow(llm, "1234 * 567은?", tools_basic)
# print(f"A: {r2}\n")

# r3 = simple_workflow(llm, "오늘 날짜는?", tools_basic)
# print(f"A: {r3}\n")

# r4 = simple_workflow(llm, "현재 환율은?", tools_basic)
# print(f"A: {r4}")
