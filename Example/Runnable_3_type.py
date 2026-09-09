from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import (
    RunnablePassthrough, RunnableLambda,
    RunnableSequence
) #RunnableParallel은 따로 py파일 있음
from operator import itemgetter

load_dotenv()
llm    = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()   # AIMessage → str 변환기

# ① RunnablePassthrough — 문자열 직접 입력 패턴
# chain.invoke("질문") 시 {"question": "질문"} 으로 자동 변환
prompt_q  = ChatPromptTemplate.from_template("이 질문에 간단히 답해줘:{question}")
chain_rpt = {"question": RunnablePassthrough()} | prompt_q | llm | StrOutputParser()
print(chain_rpt.invoke("내일 해는 어디서 뜨지?"))   # 문자열 직접 입력 가능

# ② RunnableLambda — 파이썬 함수를 체인 중간에 삽입
preprocess = RunnableLambda(lambda x: x.strip().upper())   # 전처리: 공백 제거 + 대문자
greeting   = RunnableLambda(lambda name: f"안녕하세요,{name}님!")

chain_rl = preprocess | greeting
print(chain_rl.invoke("  alice  "))   # "안녕하세요, ALICE님!"

# ③ itemgetter — 딕셔너리 State에서 특정 키만 추출 (10월 LangGraph State 패턴 복선)
prompt_ig = ChatPromptTemplate.from_template(
    "{고객번호} 고객님, {창구번호}번 창구로 오십시오."
)
chain_ig = (
    {
        "고객번호": itemgetter("customer_number"),   # dict["customer_number"] 추출
        "창구번호": itemgetter("counter_number"),
    }
    | prompt_ig | llm | StrOutputParser()
)
print(chain_ig.invoke({"customer_number": "132", "counter_number": "4"}))

# ④ RunnableSequence — | 연산자와 완전히 동일 (명시적 표현)
double    = RunnableLambda(lambda x: x + x)
say_hello = RunnableLambda(lambda name: f"Hello,{name}!")
seq       = RunnableSequence(first=double, last=say_hello)
print(seq.invoke("Minjae"))              # "Hello, MinjaeMinjae!"
print((double | say_hello).invoke("Minjae"))  # 동일 출력 — | 방식