from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()
llm    = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()   # AIMessage → str 변환기

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 요약 전문가입니다."),
    ("human", "다음 텍스트를{length}줄로 요약해:\n\n{text}")
])

# 파이프로 연결 — 이게 전부입니다!
chain = prompt | llm | parser
texts = [
    "회의 내용 A: AI 프로젝트 일정 조율 논의",
    "회의 내용 B: 예산 확정 및 팀 구성 완료",
    "회의 내용 C: 다음 달 데모 발표 준비",
]

results = chain.batch([
    {"length": "2", "text": texts[0]},
    {"length": "3", "text": texts[1]},
    {"length": "1", "text": texts[2]},
])

# 예상 출력: 3개 str로 이루어진 list
for i, r in enumerate(results):
    print(f"=== 텍스트{i+1} 요약 ===")
    print(r)
    # 예상: "1. AI 프로젝트 ...\n2. 일정 ..."