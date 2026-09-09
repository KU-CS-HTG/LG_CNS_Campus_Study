#목표: 경제/시사 유튜버(슈카월드, 지식한방, 크랩 등)들은 다양한 곳에서 정보를 찾고, 
# 그 내용들을 각자의 개성을 살려서 재미있게 전달하는데, 
# 에이전트를 활용해서 나도 그들처럼 뉴스를 재미있게 전달해보고 싶다
# 일단 '여의도 불꽃놀이'를 주제로 영상을 만든다고 생각해보자

#gpt-4o-mini 모델은 2023년도 정보까지밖에 없으니까 RCIF에서 C에 해당하는 내용을 내가 좀 더 넣어줘야 할 것 같은데 그것마저도 아직 배우지 않은 것을 이용해서 AI를 활용하고 싶음
#Role(R): 너는 유튜브 영상 대본 제작 도우미야. / 너는 유튜브에 사용할 이미지 제작 도우미야. 
#Context(C): 여의도 불꽃놀이 관련 각종 정보들
#Instruction(I): 여의도 불꽃놀이를 하게 된 계기를 정리해줘. 여의도 불꽃놀이 명당에 대해 정리해줘. 여의도 불꽃놀이 안전사고에 대해 정리해줘. 
#Format(F): 형식 지정할 때 실제 슈카월드 대본 같은 것들도 활용하면 좋을듯

#Zero-shot과 Few shot: 일단 만들어보라고 한다 - 마음에 안 드는 부분을 shot을 추가하며 수정하면 됨

#프롬프트 개선 가이드(shot을 추가하는 순서)
#v1 → 최소 동작 확인
#v2 → 형식·구조 추가
#v3 → 역할·독자·제약 추가
#v4 → 예시 케이스 처리

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

firework_wiki = """


"""

#v1: 대본 작성이 되는지 확인
v1 = llm.invoke([SystemMessage(content="당신은 유튜브 대본 작성 전문가입니다."), HumanMessage(content=f"위키 내용을 기반으로 대본 작성:\n{firework_wiki}")])
print("=== v1 ==="); print(v1.content)

#v2: 형식, 구조 추가
v2 = llm.invoke(
    f"아래 형식으로 대본 작성:\n"
    f"- 사람들의 흥미를 끌 만한 도입부:\n"
    f"- 2026년 불꽃놀이 내용을 반영한 핵심 내용:\n"
    f"- 불꽃놀이 행사에 대한 다양한 평가와 전망:\n"
    f"\n위키 내용을 기반으로 대본 작성:\n{firework_wiki}"
)
print("=== v2 ==="); print(v2.content)

# v3 — 역할 + 독자 + 제약: 누가 읽는지, 어떤 판단을 내려야 하는지 명시
v3 = llm.invoke(
    f"위키 내용을 기반으로 유튜브 대본을 작성하고 실제로 녹음하는 유튜버의 관점에서 아래 형식에 맞추어 요약해.\n"
    f"- 사람들의 흥미를 끌 만한 도입부:\n"
    f"- 2026년 불꽃놀이 내용을 반영한 핵심 내용:\n"
    f"- 불꽃놀이 행사에 대한 다양한 평가와 전망:\n"
    f"\n위키 내용을 기반으로 대본 작성:\n{firework_wiki}"
)
print("=== v3 ==="); print(v3.content)

