# pydantic_basics.py
from pydantic import BaseModel, Field
from typing import Literal, Optional

class TaskClassification(BaseModel):
    """업무 분류 모델 — AI가 이 필드들을 채웁니다"""

    category: Literal["기술지원", "구매요청", "일정조율", "기타"] = Field(
        description="업무 유형 4가지 중 하나. 반드시 이 4가지 중에서 선택."
    )
    priority: int = Field(
        description="우선순위 1(낮음)~5(높음)",
        ge=1,   # greater than or equal: 1 이상
        le=5,   # less than or equal: 5 이하
    )
    summary: str = Field(
        description="핵심 요약 20자 이내",
        max_length=20,
    )
    urgent: bool = Field(
        description="24시간 이내 처리가 필요하면 True"
    )
    assignee: Optional[str] = Field(
        default=None,
        description="담당 부서명. 불명확하면 None"
    )

# ✅ 올바른 데이터 생성
task = TaskClassification(
    category="기술지원",
    priority=4,
    summary="VPN 연결 불가",
    urgent=True,
    assignee="LG CNS"
)
print(task.category)      # "기술지원"
print(task.priority)      # 4
print(task.model_dump())  # dict 변환 (JSON 전송용)
# 예상: {'category': '기술지원', 'priority': 4, 'summary': 'VPN 연결 불가', 'urgent': True, 'assignee': LG CNS}

# ❌ 잘못된 타입 → 즉시 ValidationError
try:
    bad_task = TaskClassification(
        category="없는카테고리",   # Literal에 없는 값
        priority=10,              # 5 초과 → ge/le 위반
        summary="a" * 30,         # max_length 초과
        urgent="maybe",           # bool이 아닌 값
    )
except Exception as e:
    print("검증 오류:", e)
    # 예상: pydantic_core._pydantic_core.ValidationError: 4 validation errors for TaskClassification
    #        category: Input should be '기술지원' or '구매요청' or '일정조율' or '기타' ...