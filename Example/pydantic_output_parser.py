# pydantic_output_parser.py
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class EmailSummaryParser(BaseModel):
    person:  str = Field(description="메일을 보낸 사람의 이름")
    subject: str = Field(description="메일 제목")
    summary: str = Field(description="본문을 3문장 이내로 요약")
    date:    str = Field(description="본문에 언급된 미팅 날짜와 시간")

# 1단계: 파서 생성 → 형식 지시문 자동 생성
parser              = PydanticOutputParser(pydantic_object=EmailSummaryParser)
format_instructions = parser.get_format_instructions()
# get_format_instructions()가 스키마를 보고
# 'JSON으로 이렇게 출력해라'는 지시문을 자동 생성해줌

# 2단계: 프롬프트에 {format} 자리를 만들고 지시문을 미리 고정
prompt = ChatPromptTemplate.from_messages([
    ("system", "이메일에서 핵심 정보를 추출해. 모르면 빈 문자열로 두고 추측하지 마."),
    ("human", "아래 형식만 지켜 JSON으로 출력해.\n{format}\n\n이메일:\n{email_raw}"),
]).partial(format=format_instructions)   # {format}을 지시문으로 미리 고정

# 3단계: 체인 — parser가 JSON 문자열을 Pydantic 객체로 변환
chain  = prompt | llm | parser
result = chain.invoke({"email_raw": "안녕하세요, 홍길동 팀장님. 8/12 오전 10시 킥오프 미팅 참석 부탁드립니다."})

print(type(result))    # <class 'EmailSummaryParser'>
print(result.person)   # 홍길동
print(result.date)     # 8월 12일 오전 10시