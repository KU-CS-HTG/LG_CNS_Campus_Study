from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일의 내용을 환경변수로 등록

api_key = os.getenv("OPENAI_API_KEY")

# ✅ 키 앞 7자만 출력 (전체 키 출력 절대 금지!)
print(f"키 앞 7자:{api_key[:7]}")
# 출력 예시: 키 앞 7자: sk-proj

# 키가 없으면 에러 메시지 안내
if not api_key:
    print("⚠️ OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")