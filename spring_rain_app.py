# spring_rain_app.py (정리본)
# 완전히 리터치된 Streamlit 앱: 중복 제거 및 구조 정비

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

from typing import Dict

# 샘플 데이터 및 trait_names 딕셔너리 등 전처리 부분 삽입
competence_scores = {}
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

with st.expander("📊 하위 요소별 점수 보기"):
    for bundle, values in trait_names.items():
        st.markdown(f"**{bundle}**")
        for i, trait in enumerate(values):
            score = competence_scores.get(bundle, 0) / len(values) if bundle in competence_scores else 0
            st.markdown(f"  - {trait}: {score:.2f}")
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

    # 1. Attitude Layer 계산
    attitude_scores = {}
    for comp, score in competence_scores.items():
        for att in comp_to_att[comp]:
            attitude_scores[att] = attitude_scores.get(att, 0) + score * 0.5

    # 2. Mission Layer 계산
    mission_scores = {}
    for att, score in attitude_scores.items():
        for mission in att_to_mission[att]:
            mission_scores[mission] = mission_scores.get(mission, 0) + score * 0.5

    # 3. Outcome Layer 계산
    outcome_scores = {}
    for mission, score in mission_scores.items():
        for outcome in mission_to_outcome[mission]:
            outcome_scores[outcome] = outcome_scores.get(outcome, 0) + score * 0.5

    return outcome_scores, attitude_scores, mission_scores

# 분석 결과 시각화
if competence_scores:
    outcome, attitude, mission = compute_bombi_score(competence_scores)

    st.header("📈 분석 결과 요약")
    st.subheader("Outcome Layer")
    for k, v in outcome.items():
        st.markdown(f"- 🌟 {k}: {v:.2f}")

    st.subheader("Mission Layer")
    for k, v in mission.items():
        st.markdown(f"- 🎯 {k}: {v:.2f}")

    st.subheader("Attitude Layer")
    for k, v in attitude.items():
        st.markdown(f"- 🌀 {k}: {v:.2f}")

    # Radar Chart
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
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
