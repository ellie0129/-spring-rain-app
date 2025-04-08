import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 정확한 모듈 경로 사용
from modules.bombi_score_module import TRAIT_STRUCTURE, calculate_competence_scores, compute_layers
from modules.radar_chart import draw_all_radars, draw_outcome_layer

# Streamlit 기본 설정
st.set_page_config(page_title="🌧️ 봄비 점수 분석기", page_icon="🌱", layout="wide")
st.title("🌧️ 봄비(Spring Rain) 점수 분석기")
st.caption("이춘우 교수님의 기업가정신 통합모형 기반")

menu = st.sidebar.radio("메뉴", ["분석기", "모형 설명"])

# ───────────────────────────────────────────────────────────
# 📘 모형 설명 탭
# ───────────────────────────────────────────────────────────
if menu == "모형 설명":
    st.header("📘 기업가정신 통합모형 구조 설명")
    st.markdown("""
    ### 🔄 전체 레이어 구조
    - **Outcome Layer**: 부의 증대 & 가치 창출
    - **Mission Layer**: 기회추구, 공동체발전, 창조적파괴, 미래지향
    - **Attitude Layer**: 8가지 행동양식
    - **Competence Layer**: 8가지 역량 번들

    점수는 아래로부터 위로 전이됩니다:  
    `Competence → Attitude → Mission → Outcome`
    """)
    st.image("https://raw.githubusercontent.com/ellie0129/spring-rain-app/main/assets/1ce34f642e1b80808f4edd8cc64b1a95.png", use_container_width=True)

# ───────────────────────────────────────────────────────────
# 🤖 분석기 탭
# ───────────────────────────────────────────────────────────
else:
    st.header("🤖 인물 분석")
    
    # 샘플 인물 프로필
    sample_profiles = {
        "제프 베조스": {
            "도전정신": 0.9, "최고·최초·최신·유일 지향": 1.0, "Integrity": 0.9, "창조적 문제해결": 0.85,
            "독립성 · 자기고용 · 자기세계": 0.8, "진취성(선도성)": 0.95, "위험감수성": 0.9, "혁신성": 0.95
        },
        "김슬아": {
            "도전정신": 0.85, "최고·최초·최신·유일 지향": 0.9, "Integrity": 0.85, "창조적 문제해결": 0.9,
            "독립성 · 자기고용 · 자기세계": 0.85, "진취성(선도성)": 0.9, "위험감수성": 0.85, "혁신성": 0.9
        },
        "정주영": {
            "도전정신": 1.0, "최고·최초·최신·유일 지향": 0.95, "Integrity": 0.9, "창조적 문제해결": 0.8,
            "독립성 · 자기고용 · 자기세계": 1.0, "진취성(선도성)": 0.9, "위험감수성": 1.0, "혁신성": 0.85
        },
        "이춘우": {
            "도전정신": 1.0, "최고·최초·최신·유일 지향": 1.0, "Integrity": 1.0, "창조적 문제해결": 1.0,
            "독립성 · 자기고용 · 자기세계": 1.0, "진취성(선도성)": 1.0, "위험감수성": 1.0, "혁신성": 1.0
        }
    }

    # 사용자 입력
    selected_name = st.text_input("분석할 인물 이름을 입력하세요:", value="제프 베조스")

    # 이스터에그
    if selected_name == "이춘우":
        st.success("이춘우 교수님은 완벽한 기업가이십니다! 🎓")

    # 사전 정의된 인물이면 불러오기
    if selected_name in sample_profiles:
        competence_scores = sample_profiles[selected_name]
        st.success(f"'{selected_name}'의 역량 프로파일을 불러왔습니다.")
    else:
        st.info("아래 슬라이더를 사용해 역량 점수를 직접 입력하세요.")
        competence_scores = {}
        for bundle, traits in TRAIT_STRUCTURE.items():
            cols = st.columns(len(traits))
            values = []
            for i, trait in enumerate(traits):
                values.append(cols[i].slider(f"{bundle} - {trait}", 0.0, 1.0, 0.5, 0.01))
            competence_scores[bundle] = np.mean(values)

    # 분석 버튼
    if st.button("📈 분석하기"):
        # 계산 수행
        competence_scores = calculate_competence_scores(competence_scores)
        comp, att, mis, outcome = compute_layers(competence_scores)

        # 출력
        st.subheader("📌 분석 결과")
        st.write("**🧩 Competence 점수:**", comp)
        st.write("**🌪️ Attitude 점수:**", att)
        st.write("**🎯 Mission 점수:**", mis)
        st.success(f"🌧️ **최종 봄비 점수**: {outcome * 100:.2f}점")

        # 시각화
        fig_comp, fig_att, fig_mis = draw_all_radars(comp, att, mis)
        st.plotly_chart(fig_comp, use_container_width=True)
        st.plotly_chart(fig_att, use_container_width=True)
        st.plotly_chart(fig_mis, use_container_width=True)

        fig_outcome = draw_outcome_layer(comp, att, mis)
        st.plotly_chart(fig_outcome, use_container_width=True)
