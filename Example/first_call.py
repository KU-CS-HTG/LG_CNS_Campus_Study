# first_call.py — v2: System + Human 메시지 분리
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 메시지 리스트로 호출 — System이 AI의 역할을 정의
response = llm.invoke([
    SystemMessage(content="당신은 IT 기업 분석 전문가입니다. 한국어로 간결하게 답하세요."),
    HumanMessage(content="LG CNS의 주요 사업을 3줄로 요약해줘"),
])

print(response.content)
# 출력 예시:
# LG CNS는 IT 서비스, 클라우드, 스마트물류 분야를 주력 사업으로 합니다.
# ERP, MES 등 엔터프라이즈 솔루션과 AI/데이터 분석 서비스를 제공합니다.
# 공공·금융·제조 분야 디지털 전환(DX) 프로젝트를 주도합니다.