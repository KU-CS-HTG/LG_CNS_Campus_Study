from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.tools import tool as _tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_tavily import TavilySearch as _TS

load_dotenv()   
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

@_tool
def web_search(query: str, max_results: int = 10) -> str:
    """
    웹을 실시간으로 검색해 최신 정보를 가져옵니다.
    사용 시점: 기존 모델이 학습하지 않은 정보가 입력으로 들어왔을 때
    Args:
        query: 검색어 (한국어/영어 모두 가능)
        max_results: 반환할 결과 수 (10)
    """
    results = _TS(max_results=max_results).invoke(query)["results"]
    # if results:
    #     r0 = results[0]
    #     print(f"  title  : {r0.get('title', 'N/A')}")
    #     print(f"  url    : {r0.get('url', 'N/A')}")
    #     print(f"  content: {r0.get('content', '')[:150]}...")
    #     print(f"  score  : {r0.get('score', 'N/A')}")
    # print()
    return "\n---\n".join(
        f"제목: {d.get('title','N/A')}\nURL: {d.get('url','')}\n내용: {d.get('content','')}"
        for d in results
    )

#llm에 web search 기능 업데이트
llm_with_tavily = llm.bind_tools([web_search])

youtuber_categories = [    #Context
    # 1. 게임 
    {"input": "풍월량", "output": "게임"},
    {"input": "김성회의 G식백과", "output": "게임"},
    {"input": "한동숙", "output": "게임"},
    
    # 2. 요리
    {"input": "쯔양", "output": "요리"},
    {"input": "승우아빠", "output": "요리"},
    {"input": "백종원", "output": "요리"},
    
    # 3. 패션
    {"input": "이사배", "output": "뷰티"},
    {"input": "Pony Syndrome", "output": "뷰티"},
    {"input": "혜인", "output": "뷰티"},
    
    # 4. 지식
    {"input": "슈카월드", "output": "지식"},
    {"input": "지식해적단", "output": "지식"},
    {"input": "안될과학", "output": "지식"},
    
    # 5. 일상 
    {"input": "밍모", "output": "일상"},
    {"input": "슛뚜", "output": "일상"},
    {"input": "Casey Neistat", "output": "일상"},
    
    # 6. 테크
    {"input": "잇섭", "output": "테크"},
    {"input": "테크몽", "output": "테크"},
    {"input": "MKbHD", "output": "테크"},
    
    # 7. 음악 
    {"input": "J.Fla", "output": "음악"},
    {"input": "라온", "output": "음악"},
    {"input": "Boyce Avenue", "output": "음악"},
    
    # 8. 운동
    {"input": "김계란", "output": "운동"},
    {"input": "지기TV", "output": "운동"},
    {"input": "Chloe Ting", "output": "운동"},
    
    # 9. 여행 
    {"input": "빠니보틀", "output": "여행"},
    {"input": "곽튜브", "output": "여행"},
    {"input": "원지의 하루", "output": "여행"},

    # 10. 코미디 
    {"input": "꼰대희", "output": "코미디"},
    {"input": "너튜브", "output": "코미디"},
    {"input": "흔한남매", "output": "코미디"}
]

youtube_classification_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"), ("ai", "{output}")
])

few_shot_template = FewShotChatMessagePromptTemplate(
    examples=youtuber_categories,
    example_prompt=youtube_classification_prompt,
)

final_template = ChatPromptTemplate.from_messages([
    ("system", """당신은 유튜버 분류 전문가입니다. 유튜버 입력이 들어오면 아래 형식에 맞춰 정확히 출력하세요.
    분류 결과: [게임, 뷰티, 요리, 지식, 일상, 테크, 음악, 운동, 여행, 코미디 중 하나만 작성]
    이유: [선택한 카테고리로 분류한 이유를 간결하게 작성]"""),   
    #Role, Format, Instruction
    few_shot_template,
    ("human", "{query}"),
])

# LCEL(LangChain Expression Language)을 이용한 체인 구성
chain = final_template | llm_with_tavily

# 유튜버 입력받기
print("유튜버를 입력하세요: ", end='')
query_text = input()

# 최종 invoke 전에 입력 가공하기
messages = [HumanMessage(content=query_text)]
ai_msg = llm_with_tavily.invoke(messages)
messages.append(ai_msg)
for tc in ai_msg.tool_calls:
    result = web_search.invoke(tc["args"])   # 실제 함수 호출
    # print(f"  결과: {result}")
    messages.append(ToolMessage(
        content=str(result),
        tool_call_id=tc["id"],   # AI의 요청 ID와 반드시 연결!
    ))
    # print(tc)

result = chain.invoke(messages)
print(f"입력: {query_text}")
print(f"분류 결과: {result.content}")

