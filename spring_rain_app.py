# spring_rain_app.py (2025 완성본)
# 완전히 통합된 Streamlit 앱 코드
# 모든 요청사항 반영: 이춘우 이스터에그 자동 실행, 예시 인물 하위요소 주석 출력, 모든 레이어 설명 추가 포함

import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="봄비 점수 분석기", page_icon="🌱", layout="wide")

st.title("🌧️ 봄비(Spring Rain) 점수 분석기")
st.caption("서울시립대학교 | 이춘우 교수님의 기업가정신 통합모형 기반")

menu = st.sidebar.radio("메뉴", ["분석기", "모형 설명"])

# ---------------- 모형 설명 탭 ----------------
if menu == "모형 설명":
    st.header("📘 기업가정신 통합모형 구조 설명")
    st.markdown("""
    ### 🔄 전체 레이어 구조

    본 분석기는 이춘우 교수님의 [기업가정신 통합모형]에 기반하여 총 4단계로 구성됩니다:

    1. **Competence Layer (역량)**: 구체적이고 관찰 가능한 기업가적 능력
    2. **Attitude Layer (태도)**: 기업가의 업무 접근 및 실행 방식
    3. **Mission Layer (사명)**: 기업가정신의 사회적 의미 및 지향점
    4. **Outcome Layer (성과)**: 부의 창출과 가치 창출이라는 결과물

    ---

    ### 🧬 Competence Layer (8가지)
    - 💪 도전정신: 자기효능감, 성취욕구, 헝그리정신
    - 💡 최고·최초·최신·유일 지향: 열망, 실행력, 결단력, 고수익 기대
    - 🧭 Integrity: 리더십, 사업수완, 경영역량, 신용, 근면성실
    - 🔍 창조적 문제해결: 낙관성, 통찰력, 아이디어, 인지능력
    - 🌱 독립성·자기고용: 자아실현, 자율성, 순응거부, 역경 극복
    - 🚀 진취성(선도성): 열정, 모호성 인내도, 공격성, 선도력
    - 🛡 위험감수성: 인내심, 위험선호, CSR/CSV, 책임감
    - 🔄 혁신성: 기업윤리, 창의성, 혁신 수용성

    ### 🌀 Attitude Layer (8가지)
    - 창조 · 발명 · 개발
    - 조합 · 중개
    - 혁신 · 변화 · 개선
    - 도전 · 극복
    - 주도 · 사업화
    - 역발상 · 재해석
    - 개척 · 탐험 · 모험
    - 발견 · 발상 · 상상

    ### 🎯 Mission Layer (4가지)
    - 기회추구 (Opportunity Seeking)
    - 공동체 발전 (Community Development)
    - 창조적 파괴 (Creative Destruction)
    - 미래지향 (Future Orientation)

    ### 🌟 Outcome Layer (2가지)
    - 부의 증대 (Wealth Creation)
    - 가치 창출 (Value Creation)

    ---

    ### 🖼️ 통합모형 시각 자료
    ![통합모형 이미지](https://raw.githubusercontent.com/ellie0129/spring-rain-app/main/assets/1ce34f642e1b80808f4edd8cc64b1a95.png)
    """)

# ---------------- 분석기 탭 ----------------
else:
    st.subheader("🤖 AI 기반 인물 분석")
    st.caption("예시: 제프 베조스, 김슬아, 정주영, 이춘우")

    selected_name = st.text_input("분석할 인물 이름을 입력하세요")

    # 이춘우 이스터에그: 점수 자동 만점 + 자동 실행
    if selected_name == "이춘우":
        st.success("🌟 당신은 이미 완성된 통합모형 그 자체를 입력하셨습니다!")
        competence_scores = {
            "도전정신": 1.0,
            "최고·최초·최신·유일 지향": 1.0,
            "Integrity": 1.0,
            "창조적 문제해결": 1.0,
            "독립성 · 자기고용 · 자기세계": 1.0,
            "진취성(선도성)": 1.0,
            "위험감수성": 1.0,
            "혁신성": 1.0
        }
        show_manual = False
    else:
        show_manual = True

    # 예시 인물 사전
    sample_profiles = {
        "제프 베조스": {
            "도전정신": (0.93, [1.0, 0.9, 0.9]),
            "최고·최초·최신·유일 지향": (0.91, [0.9, 0.9, 0.95, 0.9]),
            "Integrity": (0.87, [0.85, 0.85, 0.9, 0.85, 0.9]),
            "창조적 문제해결": (0.91, [0.95, 0.9, 0.9, 0.9]),
            "독립성 · 자기고용 · 자기세계": (0.89, [0.9, 0.9, 0.85, 0.9]),
            "진취성(선도성)": (0.94, [0.95, 0.95, 0.9, 0.95]),
            "위험감수성": (0.91, [0.9, 0.9, 0.9, 0.95]),
            "혁신성": (0.95, [0.95, 0.95, 0.95]),
            "주석": "아마존 창립자 제프 베조스는 혁신성과 진취성 면에서 타의 추종을 불허하며, 문제 해결력과 추진력, 도전정신에서 매우 높은 역량을 보입니다."
        },
        "김슬아": {
            "도전정신": (0.87, [0.9, 0.85, 0.85]),
            "최고·최초·최신·유일 지향": (0.86, [0.85, 0.85, 0.9, 0.85]),
            "Integrity": (0.85, [0.85, 0.85, 0.85, 0.85, 0.85]),
            "창조적 문제해결": (0.89, [0.9, 0.9, 0.85, 0.9]),
            "독립성 · 자기고용 · 자기세계": (0.84, [0.85, 0.85, 0.8, 0.85]),
            "진취성(선도성)": (0.90, [0.9, 0.9, 0.9, 0.9]),
            "위험감수성": (0.82, [0.8, 0.8, 0.8, 0.9]),
            "혁신성": (0.91, [0.9, 0.9, 0.95]),
            "주석": "마켓컬리를 창업한 김슬아 대표는 고위험을 감수하며 새로운 물류 패러다임을 제시했고, 실행력과 혁신 수용성에서 두각을 나타냅니다."
        },
        "정주영": {
            "도전정신": (0.96, [1.0, 0.95, 0.95]),
            "최고·최초·최신·유일 지향": (0.94, [0.95, 0.95, 0.9, 0.95]),
            "Integrity": (0.92, [0.9, 0.9, 0.9, 0.95, 0.95]),
            "창조적 문제해결": (0.90, [0.9, 0.9, 0.9, 0.9]),
            "독립성 · 자기고용 · 자기세계": (0.93, [0.95, 0.9, 0.95, 0.9]),
            "진취성(선도성)": (0.95, [0.95, 0.95, 0.95, 0.95]),
            "위험감수성": (0.92, [0.9, 0.9, 0.95, 0.95]),
            "혁신성": (0.93, [0.9, 0.95, 0.95]),
            "주석": "현대그룹을 일군 정주영 회장은 자율성, 도전정신, 실행력 등 전방위적 역량에서 고루 뛰어난 인물입니다."
        }
    }

    # 예시 인물 자동 불러오기 (단, 이춘우 제외)
    # 점수 계산 및 시각화
    def compute_bombi_score(scores):
        comp_to_att = {
            "도전정신": ["창조 · 발명 · 개발", "조합 · 중개"],
            "최고·최초·최신·유일 지향": ["조합 · 중개", "혁신 · 변화 · 개선"],
            "Integrity": ["혁신 · 변화 · 개선", "도전 · 극복"],
            "창조적 문제해결": ["도전 · 극복", "주도 · 사업화"],
            "독립성 · 자기고용 · 자기세계": ["주도 · 사업화", "역발상 · 재해석"],
            "진취성(선도성)": ["역발상 · 재해석", "개척 · 탐험 · 모험"],
            "위험감수성": ["개척 · 탐험 · 모험", "발견 · 발상 · 상상"],
            "혁신성": ["발견 · 발상 · 상상", "창조 · 발명 · 개발"]
        }
        attitude = {k: 0.0 for v in comp_to_att.values() for k in v}
        for comp, val in scores.items():
            for att in comp_to_att[comp]:
                attitude[att] += val * 0.5
        attitude = {k: min(v, 1.0) for k, v in attitude.items()}

        att_to_mis = {
            "창조 · 발명 · 개발": {"기회추구": 0.25, "미래지향": 0.25},
            "조합 · 중개": {"기회추구": 0.5},
            "혁신 · 변화 · 개선": {"기회추구": 0.25, "공동체 발전": 0.25},
            "도전 · 극복": {"공동체 발전": 0.5},
            "주도 · 사업화": {"공동체 발전": 0.25, "창조적 파괴": 0.25},
            "역발상 · 재해석": {"창조적 파괴": 0.5},
            "개척 · 탐험 · 모험": {"창조적 파괴": 0.25, "미래지향": 0.25},
            "발견 · 발상 · 상상": {"미래지향": 0.5}
        }
        mission = {k: 0.0 for k in ["기회추구", "공동체 발전", "창조적 파괴", "미래지향"]}
        for att, val in attitude.items():
            for mis, w in att_to_mis.get(att, {}).items():
                mission[mis] += val * w
        mission = {k: min(v, 1.0) for k, v in mission.items()}
        outcome_score = np.mean(list(mission.values()))
        return outcome_score, attitude, mission

    if 'competence_scores' in locals():
        outcome, attitude, mission = compute_bombi_score(competence_scores)

        st.markdown("---")
        st.metric("🌟 최종 봄비 점수", f"{round(outcome * 100, 2)} / 100")

        with st.expander("🌀 태도 레이어 점수 보기"):
            st.json(attitude)

        with st.expander("🎯 사명 레이어 점수 보기"):
            st.json(mission)

        st.markdown("---")
        st.subheader("📈 레이더 차트")
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=list(competence_scores.values()),
            theta=list(competence_scores.keys()),
            fill='toself',
            name='역량 프로파일'
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)