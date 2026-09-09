from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

examples = [
    {"input": "배송 2주 됐는데 안 왔어요", "output": "배송문의"},
    {"input": "화면이 깨졌어요", "output": "제품불량"},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"), ("ai", "{output}")
])

few_shot_template = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
)

final_template = ChatPromptTemplate.from_messages([
    ("system", "고객 문의를 분류합니다: [배송문의, 환불, 제품불량, 기타]"),
    few_shot_template,
    ("human", "{query}"),
])

# 1. LCEL(LangChain Expression Language)을 이용한 체인 구성
chain = final_template | llm

# 2. 테스트할 고객 문의 입력
query_text = "어제 주문했는데 언제 오나요?"

# 3. 실행 및 결과 출력
result = chain.invoke({"query": query_text})
print(f"입력: {query_text}")
print(f"분류 결과: {result.content}")