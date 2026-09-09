#목표: 논문 요약 프롬프트를 작성해보자

#Role(R): 너는 논문 요약 도우미야
#Context(C): 논문 본문
#Instruction(I): 논문 내용을 한국어로 요약해줘.
#Format(F): 주제, 해결해야 할 문제, 해결 방법

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

paper = """



"""

# v1 — 최소 동작: 일단 요약이 되는지 확인
v1 = llm.invoke([SystemMessage(content="당신은 논문 요약 전문가입니다."), HumanMessage(content=f"논문 요약:\n{paper}")])
print("=== v1 ==="); print(v1.content)

# v2 — 형식, 구조 추가:
v2 = llm.invoke(
    f"아래 형식으로 이메일 요약:\n"
    f"- 주제:\n"
    f"- 해결해야 할 문제:\n"
    f"- 해결 방법:\n"
    f"\n논문:\n{paper}"
)
print("=== v2 ==="); print(v2.content)

# v3 — 역할 + 독자 + 제약: 누가 읽는지, 어떤 판단을 내려야 하는지 명시
v3 = llm.invoke(
    f"이 논문 내용을 구현하는 프로젝트를 하는 한국인 대학생의 관점에서 요약해.\n"
    f"- 주제:\n"
    f"- 해결해야 할 문제:\n"
    f"- 해결 방법:\n"
    f"- 구현 방법:\n"
    f"\n논문:\n{paper}"
)
print("=== v3 ==="); print(v3.content)

#v4: 예시 케이스 처리 (논문 요약본 예시를 활용)
v4 = llm.invoke(
    f"논문 요약 예시를 아래에 제시할테니 이런 느낌으로 요약해줘"
    f"- 주제: 순환 신경망(RNN)이나 합성곱(CNN) 구조를 완전히 배제하고, 오직 어텐션(Attention) 메커니즘에만 기반하여 시퀀스 변환(Sequence Transduction) 작업을 수행하는 새로운 신경망 아키텍처인 트랜스포머(Transformer)의 제어 및 성능 입증\n"
    f"""- 해결해야 할 문제: 기존 RNN/CNN 기반 모델의 한계: 기존의 최신 모델들은 인코더와 디코더를 포함하는 복잡한 순환 또는 합성곱 신경망에 의존했음.
        시퀀스를 순차적으로(Sequential) 처리해야 하는 순환 구조 특성상 학습 시 병렬화(Parallelization)가 불가능하여 연산 속도가 저하됨.
        문장의 길이가 길어질수록 장기 의존성(Long-range dependency)을 학습하기 어렵고, 메모리 제약 및 학습 시간이 과도하게 소요됨.\n"""
    f"- 해결 방법: 순환/합성곱의 전면 배제 및 셀프 어텐션 도입: 순환 연산과 합성곱 구조를 완전히 제거하고, 입력 시퀀스의 모든 위치 간 관계를 한 번에 계산하는 셀프 어텐션(Self-Attention) 구조만을 활용함. 이를 통해 연산의 병렬화를 극대화하고, 시퀀스 내의 멀리 떨어진 단어 간의 관계도 효율적으로 학습할 수 있도록 함.\n"
    f"""- 구현 방법: 인코더-디코더 구조 (Encoder-Decoder Architecture): 스택 구조의 인코더와 디코더를 각각 구성함. 인코더는 입력 시퀀스를 받아 연속 표현으로 변환하고, 디코더는 이를 바탕으로 출력 시퀀스를 순차적으로 생성함.
        멀티 헤드 어텐션 (Multi-Head Attention): 단일 어텐션 대신 여러 개의 '헤드'를 두어 서로 다른 표현 subspace에서 동시에 정보를 주목(Attention)할 수 있게 구현함.
        스케일드 닷-프로덕트 어텐션 (Scaled Dot-Product Attention): Query, Key, Value 벡터 간의 내적을 이용해 유사도를 계산하며, 차원이 커질수록 기울기 소실 문제가 발생하는 것을 막기 위해 Key 벡터의 차원 크기로 스케일링(나누기)을 수행함.
        포지셔널 인코딩 (Positional Encoding): 순환 구조가 없어 단어의 순서 정보를 알 수 없는 한계를 극복하기 위해, 입력 엠베딩 벡터에 단어의 상대적/절대적 위치 정보를 담은 포지셔널 인코딩 값을 더해줌.\n"""
    f"\n논문:\n{paper}"
)
print("=== v4 ==="); print(v4.content)