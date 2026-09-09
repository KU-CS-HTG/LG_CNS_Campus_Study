# shot_comparison.py
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()                                           # .env에서 API 키 로드
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)   # temperature=0: 재현 가능한 결과

inquiry = "지난달 주문한 노트북이 아직 안 왔어요."

# Zero-shot — 예시 없이 AI가 훈련된 지식으로 판단
zero = llm.invoke(
    f"고객 문의를 분류해. 분류: [배송문의, 환불, 제품불량, 기타]\n"
    f"문의: '{inquiry}'\n"
    f"분류 결과만 출력:"
)
print("Zero-shot:", zero.content)
# 예상 출력: "배송문의"

# Few-shot — 예시 3개로 패턴을 명확히 제시
few = llm.invoke(
    f"고객 문의를 분류해. 분류: [배송문의, 환불, 제품불량, 기타]\n\n"
    f"예시:\n"
    f"'주문 2주 됐는데 배송 안 됐어요.' → 배송문의\n"     # 예시: 배송 지연
    f"'화면에 금이 가 있어요.' → 제품불량\n"              # 예시: 물리적 파손
    f"'환불하고 싶어요.' → 환불\n\n"                      # 예시: 환불 요청
    f"분류할 문의: '{inquiry}'\n"
    f"분류 결과만 출력:"
)
print("Few-shot:", few.content)
# 예상 출력: "배송문의"  (동일 결과이지만 복잡한 케이스에서 차이 발생)