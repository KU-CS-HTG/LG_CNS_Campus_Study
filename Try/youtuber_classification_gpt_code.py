from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.tools import tool as _tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_tavily import TavilySearch as _TS

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

@_tool
def web_search(query: str, max_results: int = 10) -> str:
    """
    웹을 실시간으로 검색해 최신 정보를 가져옵니다.
    """
    results = _TS(max_results=max_results).invoke(query)["results"]

    return "\n---\n".join(
        f"제목: {d.get('title', 'N/A')}\n"
        f"URL: {d.get('url', '')}\n"
        f"내용: {d.get('content', '')}"
        for d in results
    )

# Tool 연결
llm_with_tavily = llm.bind_tools([web_search])

# =========================
# Few-shot 예시
# =========================
youtuber_categories = [

    {
        "input": "풍월량",
        "output": "분류 결과: 게임\n이유: 다양한 게임을 플레이하고 게임 관련 콘텐츠를 주로 제작하는 유튜버입니다."
    },

    {
        "input": "김성회의 G식백과",
        "output": "분류 결과: 게임\n이유: 게임 산업과 게임에 대한 정보를 전달하는 콘텐츠를 주로 제작합니다."
    },

    {
        "input": "쯔양",
        "output": "분류 결과: 요리\n이유: 음식 먹방과 음식 관련 콘텐츠를 주로 제작하는 유튜버입니다."
    },

    {
        "input": "백종원",
        "output": "분류 결과: 요리\n이유: 음식과 요리 방법을 소개하는 콘텐츠를 주로 제작합니다."
    },

    {
        "input": "이사배",
        "output": "분류 결과: 뷰티\n이유: 메이크업과 뷰티 관련 콘텐츠를 중심으로 활동하는 유튜버입니다."
    },

    {
        "input": "슈카월드",
        "output": "분류 결과: 지식\n이유: 경제와 사회 이슈 등을 쉽게 설명하는 지식 콘텐츠를 제작합니다."
    },

    {
        "input": "잇섭",
        "output": "분류 결과: 테크\n이유: 스마트폰, 컴퓨터 등 IT 제품을 리뷰하고 관련 정보를 전달합니다."
    },

    {
        "input": "빠니보틀",
        "output": "분류 결과: 여행\n이유: 국내외 여행을 다니며 여행 경험과 문화를 소개하는 콘텐츠를 제작합니다."
    }
]

youtube_classification_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])

few_shot_template = FewShotChatMessagePromptTemplate(
    examples=youtuber_categories,
    example_prompt=youtube_classification_prompt,
)

# =========================
# 최종 Prompt
# =========================

final_template = ChatPromptTemplate.from_messages([
    (
        "system",
        """
당신은 유튜버 분류 전문가입니다.

입력된 유튜버를 다음 10개 카테고리 중 정확히 하나로 분류하세요.

가능한 카테고리:
게임, 뷰티, 요리, 지식, 일상, 테크, 음악, 운동, 여행, 코미디

유튜버에 대한 정보가 부족하거나 확실하지 않은 경우 웹 검색 도구를 사용하여 정보를 확인하세요.

반드시 다음 형식으로 답변하세요.

분류 결과: [카테고리]
이유: [해당 카테고리로 분류한 이유를 한 문장으로 간결하게 설명]
"""
    ),
    few_shot_template,
    ("human", "{query}")
])

# =========================
# 사용자 입력
# =========================

print("유튜버를 입력하세요: ", end="")
query_text = input()

# =========================
# 1차 Prompt 생성
# =========================

messages = final_template.format_messages(
    query=query_text
)

# =========================
# 2차: LLM 호출
# =========================

ai_msg = llm_with_tavily.invoke(messages)
# Tool 호출이 필요한 경우
if ai_msg.tool_calls:

    messages.append(ai_msg)

    for tc in ai_msg.tool_calls:

        result = web_search.invoke(tc["args"])

        messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tc["id"]
            )
        )
    # 검색 결과를 반영하여 최종 답변 생성
    result = llm.invoke(messages)
else:
    # 검색이 필요 없다고 판단한 경우
    result = ai_msg
print(f"입력: {query_text}")
print(result.content)