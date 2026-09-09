from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 🔰 기본 미션: 아래 두 줄을 내 서비스에 맞게 수정하세요!
# TODO(🔰-1): AI 역할을 내 서비스에 맞게 수정하세요
#             (힌트: 📖 강의 모듈 1-7 "마이 서비스 조각 예시" 표 참고)
system_prompt = "당신은 게임 전문가입니다. 게임 용어를 활용하여 구체적으로 답하세요."  # ← 내 서비스에 맞게 수정!

# TODO(🔰-2): 내 서비스에 실제로 넣을 텍스트로 수정하세요
user_input = "던그리드에 대해 설명해줘."  # ← 실제 서비스 입력 예시로 수정!

response_my = llm.invoke([
    SystemMessage(content=system_prompt),
    HumanMessage(content=user_input),
])

print("=== 내 서비스 첫 출력 ===")
print(response_my.content)
print(f"\n📊 토큰 사용: {response_my.usage_metadata}")