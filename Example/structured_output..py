from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser  # 폴백용 추가
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 1. 출력 스키마 정의
class EmailSummary(BaseModel):
    sender:       str             = Field(description="발신자 이름")
    purpose:      str             = Field(description="이메일 목적 한 문장")
    action_items: list[str]       = Field(description="처리 필요 항목 목록")
    deadline:     Optional[str]   = Field(default=None, description="기한. 없으면 None")
    priority:     int             = Field(description="중요도 1~5", ge=1, le=5)

# 2. LLM에 스키마 등록
structured_llm = llm.with_structured_output(EmailSummary)

# ↓↓↓ 수정: 프롬프트를 별도 변수로 추출 (버그 3 수정 — 폴백에서 재사용) ↓↓↓
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "이메일 분석 전문가입니다. 요청된 필드를 정확하게 추출하세요."),
    ("human", "다음 이메일을 분석해주세요:\n\n{email}"),
])
# ↑↑↑ 수정 끝 ↑↑↑

# 3. 프롬프트 + structured_llm으로 체인 구성
#    (StrOutputParser가 필요 없음! Pydantic이 이미 파서 역할)
chain = prompt_template | structured_llm

# 4. 호출
email_text = """
안녕하세요, 이팀장님.

8/12(수) 오전 10시 MCP 프로젝트 킥오프 미팅 참석 부탁드립니다.
준비 자료: 팀 소개 슬라이드 3~5장
확인 후 회신 부탁드립니다.

홍길동 드림
"""
# 중요한 호출은 try-except로 감싸기
try:
    result = chain.invoke({"email": email_text})
    print(result.model_dump())

except Exception as e:
    print(f"구조화 출력 실패:{e}")
    # ↓↓↓ 수정: prompt_template 재사용 (버그 3 수정), StrOutputParser 임포트 필요 ↓↓↓
    fallback_chain = prompt_template | llm | StrOutputParser()   # prompt_template으로 수정
    raw_text = fallback_chain.invoke({"email": email_text})
    # ↑↑↑ 수정 끝 ↑↑↑
    print ({"raw_output": raw_text, "parse_error": str(e)})


