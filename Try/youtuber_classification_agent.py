from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()   
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

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
    {"input": "원지자의 하루", "output": "여행"}
]

youtube_classification_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"), ("ai", "{output}")
])

few_shot_template = FewShotChatMessagePromptTemplate(
    examples=youtuber_categories,
    example_prompt=youtube_classification_prompt,
)

final_template = ChatPromptTemplate.from_messages([
    ("system", "당신은 유튜버 분류 전문가입니다. 유튜버 입력이 들어오면 [게임, 뷰티, 요리, 지식, 일상, 테크, 음악, 운동, 여행] 중 하나로 분류하세요. "),   
    #Role, Format, Instruction
    few_shot_template,
    ("human", "{query}"),
])

# 1. LCEL(LangChain Expression Language)을 이용한 체인 구성
chain = final_template | llm

# 2. 유튜버 입력받기
print("유튜버를 입력하세요: ", end='')
query_text = input()

# 3. 실행 및 결과 출력
result = chain.invoke({"query": query_text})
print(f"입력: {query_text}")
print(f"분류 결과: {result.content}")

