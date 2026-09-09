from typing import TypedDict

class ChatState(TypedDict):        # 딕셔너리의 "모양"을 선언 - 이런 key들을 쓸 거라고 미리 정의
    question:    str
    answer:      str
    tokens_used: int

# 생성·사용은 그냥 딕셔너리와 동일
state: ChatState = {"question": "안녕?", "answer": "", "tokens_used": 0}
state["answer"] = "안녕하세요!"     # 에디터가 키 이름을 자동 완성해줌

state["tokens"] = 10               # 오타! 실행은 되지만 에디터가 경고 표시
print(type(state))                 # <class 'dict'> — 런타임엔 그냥 dict, 검증 없음