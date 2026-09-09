# ⭐ pydantic_advanced.py — 커스텀 검증자
from pydantic import BaseModel, Field, field_validator, model_validator

class SmartTaskClassification(BaseModel):
    category: str = Field(description="업무 유형")
    priority: int = Field(description="우선순위 1~5", ge=1, le=5)
    summary:  str = Field(description="20자 이내 요약")

    @field_validator('summary')
    @classmethod
    def summary_must_be_concise(cls, v: str) -> str:
        """요약 앞뒤 공백 제거 후 길이 재확인"""
        v = v.strip()
        if len(v) > 20:
            raise ValueError(f"요약은 20자 이내여야 합니다 (현재:{len(v)}자)")
        return v

    @model_validator(mode='after')
    def urgent_category_check(self):
        """우선순위 5(긴급)는 '기타' 카테고리로 분류 불가"""
        if self.priority == 5 and self.category == "기타":
            raise ValueError("우선순위 5(긴급)는 '기타' 카테고리로 분류할 수 없습니다")
        return self

# 테스트
try:
    t = SmartTaskClassification(category="기타", priority=5, summary="긴급 처리")
except Exception as e:
    print(e)  # 예상: "우선순위 5(긴급)는 '기타' 카테고리로 분류할 수 없습니다"