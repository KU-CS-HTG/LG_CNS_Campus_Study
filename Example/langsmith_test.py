# langsmith_test.py
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
# load_dotenv()가 LANGCHAIN_TRACING_V2=true를 환경변수로 등록하면,
# 이후 모든 랭체인 호출이 자동으로 LangSmith 서버에 전송됩니다.
# 코드에 LangSmith 관련 import나 설정을 추가할 필요가 없습니다.
# 흐름: .env → load_dotenv() → 환경변수 등록 → 랭체인 내부에서 자동 감지 → LangSmith 전송

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 이 한 줄이 자동으로 LangSmith에 기록됩니다
response = llm.invoke("안녕? 나는 LG CNS AI 캠퍼스 수강생이야. 한 문장으로 응원해줘!")

print(response.content)
# 출력 예시: "LG CNS AI 캠퍼스에서 최고의 AI 개발자로 성장하실 것을 응원합니다! 🎉"