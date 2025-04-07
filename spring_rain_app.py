# spring_rain_app.py (2025 완성본)
# Streamlit 기반 봄비 점수 분석기 (신모형 + UI + 예시 + 시각화 포함)

import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="봄비 점수 분석기", page_icon="🌱", layout="wide")

st.title("🌧️ 봄비(Spring Rain) 점수 분석기")
st.caption("서울시립대학교 | 이춘우 교수님의 기업가정신 통합모형 기반")

menu = st.sidebar.radio("메뉴", ["분석기", "모형 설명"])

if menu == "모형 설명":
    st.header("📘 기업가정신 통합모형 구조 설명")
    st.markdown("""
    ### 🔄 전체 레이어 구조

    1. **Outcome Layer (성과)**
    2. **Mission Layer (사명)**
    3. **Attitude Layer (태도)**
    4. **Competence Layer (역량)**

    #### ▶️ 점수 전이 구조
    - 각 하위 요소는 자신이 속한 역량 번들 점수에 `1/n`씩 기여
    - 각 역량 번들은 2개의 태도 요소에 0.5씩 전이
    - 각 태도 요소는 사명 레이어에 가중치로 전이
    - 사명 점수 평균 → 최종 Outcome 점수

    ---

    ### 🧬 기업가정신 통합모형 시각 자료
    ![통합모형 이미지](https://raw.githubusercontent.com/itisbreeze/spring-rain-model/main/integrated_model.png)
    """)

if menu == "분석기":
    st.subheader("🤖 AI 기반 인물 분석")

    sample_profiles = {
        "제프 베조스": {
            "도전정신": 0.93,
            "최고·최초·최신·유일 지향": 0.91,
            "Integrity": 0.87,
            "창조적 문제해결": 0.91,
            "독립성 · 자기고용 · 자기세계": 0.89,
            "진취성(선도성)": 0.94,
            "위험감수성": 0.91,
            "혁신성": 0.95
        },
        "김슬아": {
            "도전정신": 0.87,
            "최고·최초·최신·유일 지향": 0.86,
            "Integrity": 0.85,
            "창조적 문제해결": 0.89,
            "독립성 · 자기고용 · 자기세계": 0.84,
            "진취성(선도성)": 0.90,
            "위험감수성": 0.82,
            "혁신성": 0.91
        },
        "정주영": {
            "도전정신": 0.96,
            "최고·최초·최신·유일 지향": 0.94,
            "Integrity": 0.92,
            "창조적 문제해결": 0.90,
            "독립성 · 자기고용 · 자기세계": 0.93,
            "진취성(선도성)": 0.95,
            "위험감수성": 0.92,
            "혁신성": 0.93
        }
    }

    selected_name = st.text_input("인물 이름 입력")

    if selected_name in sample_profiles:
        competence_scores = sample_profiles[selected_name]
        st.success(f"✅ '{selected_name}'의 프로파일을 불러왔습니다.")
    else:
        st.info("✍️ 아래에서 직접 세부 역량을 입력해도 됩니다.")
        competence_details = {
            "도전정신": ["자기효능감, 자신감", "성취 욕구", "헝그리정신, 목표 달성 추구"],
            "최고·최초·최신·유일 지향": ["열망(야망)", "추진력, 실행력", "결단력(의사결정)", "고수익 기대"],
            "Integrity": ["리더십", "사업수완", "경영 관리 역량", "신용, 신뢰", "근면, 검소, 성실성"],
            "창조적 문제해결": ["긍정적, 낙관적", "통찰력, 안목", "아이디어, 상상력, 호기심, 탐구", "인지 능력"],
            "독립성 · 자기고용 · 자기세계": ["자아실현", "자율성 지향", "순응 거부", "역경 극복"],
            "진취성(선도성)": ["열정", "높은 모호성 인내도", "경쟁적 공격성", "선도적"],
            "위험감수성": ["인내심", "위험선호", "CSR/CSV", "책임감"],
            "혁신성": ["기업윤리", "창의성", "변화 및 혁신 적극 수용"]
        }
        competence_scores = {}
        for bundle, traits in competence_details.items():
            st.markdown(f"#### {bundle}")
            scores = [st.slider(f"{trait}", 0.0, 1.0, 0.0, 0.01) for trait in traits]
            competence_scores[bundle] = np.mean(scores)

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
            "혁신 · 변화 · 개선": {"기회추구": 0.25, "공동체발전": 0.25},
            "도전 · 극복": {"공동체발전": 0.5},
            "주도 · 사업화": {"공동체발전": 0.25, "창조적파괴": 0.25},
            "역발상 · 재해석": {"창조적파괴": 0.5},
            "개척 · 탐험 · 모험": {"창조적파괴": 0.25, "미래지향": 0.25},
            "발견 · 발상 · 상상": {"미래지향": 0.5}
        }
        mission = {k: 0.0 for k in ["기회추구", "공동체발전", "창조적파괴", "미래지향"]}
        for att, val in attitude.items():
            for mis, w in att_to_mis.get(att, {}).items():
                mission[mis] += val * w
        mission = {k: min(v, 1.0) for k, v in mission.items()}
        outcome_score = np.mean(list(mission.values()))
        return outcome_score, attitude, mission

    if competence_scores:
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