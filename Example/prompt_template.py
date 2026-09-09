from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 템플릿 정의 — {중괄호}가 변수 자리 (단일 중괄호 사용!)
chat_template = ChatPromptTemplate.from_messages([
    ("system", "당신은{industry} 산업 전문 분석가입니다.{tone} 어조로 한국어로 답하세요."),
    ("human", "{task}에 대해{format}으로 분석해주세요."),
])

# 변수를 채워서 호출
chain = chat_template | llm   # 내일 LCEL에서 자세히 배울 연결 방식!
                               # chat_template 출력이 llm 입력으로 자동 전달

# 같은 템플릿으로 산업만 바꿔서 3번 호출 — 코드 중복 없음
industries = [
    {"industry": "금융업", "tone": "보수적이고 신중한"},
    {"industry": "유통업", "tone": "실용적인"},
    {"industry": "헬스케어", "tone": "규정 중심적인"},
]

for config in industries:
    result = chain.invoke({
        **config,               # 산업·어조 자동 언패킹 (딕셔너리 병합)
        "task": "ERP 도입 리스크",
        "format": "번호 목록 3가지",
    })
    print(f"\n==={config['industry']} ===")
    print(result.content)