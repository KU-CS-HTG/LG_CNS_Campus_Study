# ⭐ 병렬 처리 — 요약과 분류를 동시에!
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel

load_dotenv()
llm    = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()   # AIMessage → str 변환기

prompt_summary = ChatPromptTemplate.from_messages([
    ("system", "요약 전문가입니다."),
    ("human", "다음 텍스트를 2줄로 요약:\n{text}"),
])

prompt_classify = ChatPromptTemplate.from_messages([
    ("system", "분류 전문가입니다."),
    ("human", "다음 텍스트의 주제를 [업무/개인/기술/기타] 중 하나로 분류:\n{text}"),
])

summary_chain    = prompt_summary  | llm | parser
classify_chain   = prompt_classify | llm | parser

parallel = RunnableParallel(
    summary  = summary_chain,
    category = classify_chain,
)

result = parallel.invoke({"text": "AI 프로젝트 킥오프 회의에서 팀 구성과 일정을 확정했습니다."})
print(result["summary"])    # 예상: "AI 프로젝트 킥오프에서 팀과 일정을 확정했다."
print(result["category"])   # 예상: "업무"
# LangSmith에서 두 호출이 동시에 실행된 것을 확인!