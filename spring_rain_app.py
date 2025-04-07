# spring_rain_app.py (최종 완성본)
# 분석기 Tab과 모형 설명 Tab 완전 분리, 전체 코드 구성

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from typing import Dict

st.set_page_config(page_title="봄비 점수 분석기", page_icon="🌱", layout="wide")

st.title("🌧️ 봄비(Spring Rain) 점수 분석기")
st.caption("서울시립대학교 | 이춘우 교수님의 기업가정신 통합모형 기반")

menu = st.sidebar.radio("메뉴", ["분석기", "모형 설명"])

if menu == "모형 설명":
    st.header("📘 기업가정신 통합모형 구조 설명")
    st.markdown("""
    ### 🌟 Outcome Layer (2가지)
    - 부의 증대 (Wealth Creation)
    - 가치 창출 (Value Creation)

    ### 🎯 Mission Layer (4가지)
    - 기회추구 (Opportunity Seeking)
    - 공동체 발전 (Community Development)
    - 창조적 파괴 (Creative Destruction)
    - 미래지향 (Future Orientation)

    ### 🌀 Attitude Layer (8가지)
    - 창조 · 발명 · 개발
    - 조합 · 중개
    - 혁신 · 변화 · 개선
    - 도전 · 극복
    - 주도 · 사업화
    - 역발상 · 재해석
    - 개척 · 탐험 · 모험
    - 발견 · 발상 · 상상

    ### 🧬 Competence Layer (8가지)
    - 💪 도전정신: 자기효능감 (self-efficacy), 자신감 (self confidence), 성취 욕구 (N-Achievement), 헝그리정신, 목표 달성 추구
    - 💡 최고·최초·최신·유일 지향: 열망(야망), 추진력, 실행력, 결단력(의사결정), 고수익 기대
    - 🧭 Integrity: 리더십, 사업수완, 경영 관리 역량, 신용, 신뢰, 근면, 검소, 성실성
    - 🔍 창조적 문제해결: 긍정적, 낙관적, 통찰력, 안목, 아이디어, 상상력, 호기심, 탐구, 인지 능력 (지적 능력)
    - 🌱 독립성·자기고용: 자아실현 (self actualization), 자율성 지향, 순응 거부, 역경 극복
    - 🚀 진취성(선도성): 열정, 높은 모호성 인내도, 경쟁적 공격성, 선도적
    - 🛡 위험감수성: 인내심, 위험선호, CSR/CSV, 책임감(책임의식)
    - 🔄 혁신성: 기업윤리, 창의성, 변화 및 혁신 적극 수용

    ---

    ### 💡 점수 전이 구조 요약
    각 레이어는 하위 레벨의 점수를 기반으로 상위 레벨 점수를 산출합니다:

    - **Competence → Attitude**: 하나의 역량 번들이 두 개의 태도 항목에 각각 0.5의 가중치로 분배됩니다.
    - **Attitude → Mission**: 각 태도 항목은 미션 항목에 사전에 정의된 가중치 비율(0.25 또는 0.5)로 영향을 미칩니다.
    - **Mission → Outcome**: 4개 미션 항목의 평균값이 Outcome 점수로 환산됩니다.

    → 전체적으로는 계층 간 유기적인 흐름을 통해 '행동'에서 '의미'로, 다시 '성과'로 이행되는 구조를 수치화합니다.

    ---

    ### 🖼️ 통합모형 시각 자료
    ![통합모형 이미지](https://raw.githubusercontent.com/ellie0129/spring-rain-app/main/assets/1ce34f642e1b80808f4edd8cc64b1a95.png)
    """)

trait_names = {
    "도전정신": ["자기효능감 (self-efficacy), 자신감 (self confidence)", "성취 욕구 (N-Achievement)", "헝그리정신, 목표 달성 추구"],
    "최고·최초·최신·유일 지향": ["열망(야망)", "추진력, 실행력", "결단력(의사결정)", "고수익 기대"],
    "Integrity": ["리더십", "사업수완", "경영 관리 역량", "신용, 신뢰", "근면, 검소, 성실성"],
    "창조적 문제해결": ["긍정적, 낙관적", "통찰력, 안목", "아이디어, 상상력, 호기심, 탐구", "인지 능력 (지적 능력)"],
    "독립성 · 자기고용 · 자기세계": ["자아실현 (self actualization)", "자율성 지향", "순응 거부", "역경 극복"],
    "진취성(선도성)": ["열정", "높은 모호성 인내도", "경쟁적 공격성", "선도적"],
    "위험감수성": ["인내심", "위험선호", "CSR/CSV", "책임감(책임의식)"],
    "혁신성": ["기업윤리", "창의성", "변화 및 혁신 적극 수용"]
}

if menu == "분석기":
    st.subheader("🎛️ 직접 조작: 나만의 점수 만들기")
st.markdown("<br>", unsafe_allow_html=True)
    custom_scores = {}
    with st.expander("🧬 각 하위 요소별로 점수를 직접 설정해보세요 (0.0 ~ 1.0)"):
        for bundle, traits in trait_names.items():
            scores = []
            st.markdown(f"**{bundle}**")
            for trait in traits:
                val = st.slider(f"{trait}", 0.0, 1.0, 0.0, 0.01, key=f"{bundle}-{trait}")
                scores.append(val)
            if scores:
                custom_scores[bundle] = np.mean(scores)

    selected_name = st.text_input("다음의 이름을 입력하여 예시 분석 결과를 확인할 수 있습니다: 제프 베조스, 김슬아, 정주영")

    sample_profiles = {
        "제프 베조스": ([
            ("도전정신", [1.0, 0.9, 0.9]),
            ("최고·최초·최신·유일 지향", [0.9, 0.9, 0.95, 0.9]),
            ("Integrity", [0.85, 0.85, 0.9, 0.85, 0.9]),
            ("창조적 문제해결", [0.95, 0.9, 0.9, 0.9]),
            ("독립성 · 자기고용 · 자기세계", [0.9, 0.9, 0.85, 0.9]),
            ("진취성(선도성)", [0.95, 0.95, 0.9, 0.95]),
            ("위험감수성", [0.9, 0.9, 0.9, 0.95]),
            ("혁신성", [0.95, 0.95, 0.95])
        ], "아마존 창립자 제프 베조스는 혁신성과 진취성 면에서 타의 추종을 불허하며, 문제 해결력과 추진력, 도전정신에서 매우 높은 역량을 보입니다."),

        "김슬아": ([
            ("도전정신", [0.9, 0.85, 0.85]),
            ("최고·최초·최신·유일 지향", [0.85, 0.85, 0.9, 0.85]),
            ("Integrity", [0.85, 0.85, 0.85, 0.85, 0.85]),
            ("창조적 문제해결", [0.9, 0.9, 0.85, 0.9]),
            ("독립성 · 자기고용 · 자기세계", [0.85, 0.85, 0.8, 0.85]),
            ("진취성(선도성)", [0.9, 0.9, 0.9, 0.9]),
            ("위험감수성", [0.8, 0.8, 0.8, 0.9]),
            ("혁신성", [0.9, 0.9, 0.95])
        ], "마켓컬리를 창업한 김슬아 대표는 고위험을 감수하며 새로운 물류 패러다임을 제시했고, 실행력과 혁신 수용성에서 두각을 나타냅니다."),

        "정주영": ([
            ("도전정신", [1.0, 0.95, 0.95]),
            ("최고·최초·최신·유일 지향", [0.95, 0.95, 0.9, 0.95]),
            ("Integrity", [0.9, 0.9, 0.9, 0.95, 0.95]),
            ("창조적 문제해결", [0.9, 0.9, 0.9, 0.9]),
            ("독립성 · 자기고용 · 자기세계", [0.95, 0.9, 0.95, 0.9]),
            ("진취성(선도성)", [0.95, 0.95, 0.95, 0.95]),
            ("위험감수성", [0.9, 0.9, 0.95, 0.95]),
            ("혁신성", [0.9, 0.95, 0.95])
        ], "현대그룹을 일군 정주영 회장은 자율성, 도전정신, 실행력 등 전방위적 역량에서 고루 뛰어난 인물입니다.")
    }

    competence_scores = {}
    traits = []
    if selected_name == "이춘우":
        competence_scores = {k: 1.0 for k in trait_names.keys()}
        st.success("🌟 당신은 이미 완성된 통합모형 그 자체를 입력하셨습니다!")
    elif selected_name in sample_profiles:
        traits, comment = sample_profiles[selected_name]
        for bundle, values in traits:
            competence_scores[bundle] = np.mean(values)
        st.success(f"✅ '{selected_name}'의 역량 프로파일을 불러왔습니다")
        st.markdown(f"💬 **AI 평가 주석**: {comment}")
    elif custom_scores:
        competence_scores = custom_scores
        st.success("🧪 직접 설정한 점수로 분석을 진행합니다!")

    def compute_bombi_score(competence_scores):
        comp_to_att = {
            "도전정신": ["도전 · 극복", "주도 · 사업화"],
            "최고·최초·최신·유일 지향": ["창조 · 발명 · 개발", "혁신 · 변화 · 개선"],
            "Integrity": ["조합 · 중개", "발견 · 발상 · 상상"],
            "창조적 문제해결": ["역발상 · 재해석", "개척 · 탐험 · 모험"],
            "독립성 · 자기고용 · 자기세계": ["발견 · 발상 · 상상", "도전 · 극복"],
            "진취성(선도성)": ["개척 · 탐험 · 모험", "주도 · 사업화"],
            "위험감수성": ["조합 · 중개", "혁신 · 변화 · 개선"],
            "혁신성": ["창조 · 발명 · 개발", "역발상 · 재해석"]
        }
        att_to_mission = {
            "창조 · 발명 · 개발": ["미래지향"],
            "조합 · 중개": ["기회추구"],
            "혁신 · 변화 · 개선": ["창조적 파괴"],
            "도전 · 극복": ["기회추구"],
            "주도 · 사업화": ["기회추구"],
            "역발상 · 재해석": ["창조적 파괴"],
            "개척 · 탐험 · 모험": ["미래지향"],
            "발견 · 발상 · 상상": ["공동체 발전"]
        }
        mission_to_outcome = {
            "기회추구": ["부의 증대"],
            "공동체 발전": ["가치 창출"],
            "창조적 파괴": ["부의 증대"],
            "미래지향": ["가치 창출"]
        }
        attitude_scores = {}
        for comp, score in competence_scores.items():
            for att in comp_to_att[comp]:
                attitude_scores[att] = attitude_scores.get(att, 0) + score * 0.5
        mission_scores = {}
        for att, score in attitude_scores.items():
            for mission in att_to_mission[att]:
                mission_scores[mission] = mission_scores.get(mission, 0) + score * 0.5
        outcome_scores = {}
        for mission, score in mission_scores.items():
            for outcome in mission_to_outcome[mission]:
                outcome_scores[outcome] = outcome_scores.get(outcome, 0) + score * 0.5
        return outcome_scores, attitude_scores, mission_scores

    if competence_scores:
        outcome, attitude, mission = compute_bombi_score(competence_scores)

        if traits:
            st.subheader("🧩 Competence Layer - 하위 요소별 점수")
            for bundle, values in traits:
                st.markdown(f"**{bundle}**")
                for i, score in enumerate(values):
                    label = trait_names.get(bundle, [])[i] if i < len(trait_names.get(bundle, [])) else f"하위 요소 {i+1}"
                    st.markdown(f"  - {label}: {score:.2f}")

        st.subheader("🕸️ Competence Layer (Radar Chart)")
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=list(competence_scores.values()),
            theta=list(competence_scores.keys()),
            fill='toself',
            name='봄비 점수'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1]),
                angularaxis=dict(direction='clockwise')
            ),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("🌀 **Attitude Layer**")
        for k, v in attitude.items():
            st.markdown(f"- {k}: {v:.2f}")

        st.markdown("🎯 **Mission Layer**")
        for k, v in mission.items():
            st.markdown(f"- {k}: {v:.2f}")

        st.markdown("🌟 **Outcome Layer**")
        for k, v in outcome.items():
            st.markdown(f"- {k}: {v:.2f}")

        
