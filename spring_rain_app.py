# spring_rain_app.py - 최종 완성본
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 🌱 Streamlit 기본 설정
st.set_page_config(page_title="🌧️ 봄비 점수 분석기", page_icon="🌱", layout="wide")
st.title("🌧️ 봄비(Spring Rain) 점수 분석기")
st.caption("이춘우 교수님의 기업가정신 통합모형 기반")

menu = st.sidebar.radio("메뉴", ["분석기", "모형 설명"])

# ──────────────────────────────────────────────
# 📘 모형 설명 탭
# ──────────────────────────────────────────────
if menu == "모형 설명":
    st.header("📘 기업가정신 통합모형 구조 설명")
    st.markdown("""
    - Competence Layer (8개 역량 번들)
    - Attitude Layer (8개 행동양식)
    - Mission Layer (4개 사명)
    - Outcome Layer (최종 점수)

    점수 흐름:
    Competence → Attitude → Mission → Outcome

    Outcome은 Mission 점수 평균의 0.25배로 계산되어 최종 봄비 점수가 됩니다.
    """)
    st.image("https://raw.githubusercontent.com/ellie0129/spring-rain-app/main/assets/1ce34f642e1b80808f4edd8cc64b1a95.png", use_container_width=True)

# ──────────────────────────────────────────────
# 🤖 분석기 탭
# ──────────────────────────────────────────────
else:
    st.header("🤖 인물 분석기")

    # ✅ 세부 항목 구조
    TRAIT_STRUCTURE = {
        "도전정신": ["자기효능감 (self-efficacy), 자신감 (self confidence)", "성취 욕구 (N-Achievement)", "헝그리정신, 목표 달성 추구"],
        "최고·최초·최신·유일 지향": ["열망(야망)", "추진력, 실행력", "결단력(의사결정)", "고수익 기대"],
        "Integrity": ["리더십", "사업수완", "경영 관리 역량", "신용, 신뢰", "근면, 검소, 성실성"],
        "창조적 문제해결": ["긍정적, 낙관적", "통찰력, 안목", "아이디어, 상상력, 호기심, 탐구", "인지 능력 (지적 능력)"],
        "독립성 · 자기고용 · 자기세계": ["자아실현 (self actualization)", "자율성 지향", "순응 거부", "역경 극복"],
        "진취성(선도성)": ["열정", "높은 모호성 인내도", "경쟁적 공격성", "선도적"],
        "위험감수성": ["인내심", "위험선호", "CSR/CSV", "책임감(책임의식)"],
        "혁신성": ["기업윤리", "창의성", "변화 및 혁신 적극 수용"]
    }

    def calculate_competence_scores(user_input):
        comp = {}
        trait_details = {}
        for bundle, traits in TRAIT_STRUCTURE.items():
            scores = [user_input.get(f"{bundle}_{trait}", 0) for trait in traits]
            comp[bundle] = round(np.mean(scores), 3)
            trait_details[bundle] = {trait: round(user_input.get(f"{bundle}_{trait}", 0), 2) for trait in traits}
        return comp, trait_details

    def compute_layers(comp):
        comp = {k: min(v, 1.0) for k, v in comp.items()}
        comp_to_att = {
            "도전정신": ["창조 · 발명 · 개발", "조합(결합/융합) · 중개"],
            "최고·최초·최신·유일 지향": ["조합(결합/융합) · 중개", "혁신 · 변화 · 개선"],
            "Integrity": ["혁신 · 변화 · 개선", "도전 · 극복"],
            "창조적 문제해결": ["도전 · 극복", "주도(자수성가) · 사업화"],
            "독립성 · 자기고용 · 자기세계": ["주도(자수성가) · 사업화", "역발상 · 재해석"],
            "진취성(선도성)": ["역발상 · 재해석", "개척 · 탐험 · 모험"],
            "위험감수성": ["개척 · 탐험 · 모험", "발견 · 발상 · 상상"],
            "혁신성": ["발견 · 발상 · 상상", "창조 · 발명 · 개발"]
        }
        att = {}
        for c, val in comp.items():
            for a in comp_to_att[c]:
                att[a] = att.get(a, 0) + val * 0.5
        att = {k: min(v, 1.0) for k, v in att.items()}

        att_to_mis = {
            "창조 · 발명 · 개발": {"기회추구": 0.25, "미래지향": 0.25},
            "조합(결합/융합) · 중개": {"기회추구": 0.5},
            "혁신 · 변화 · 개선": {"기회추구": 0.25, "공동체발전": 0.25},
            "도전 · 극복": {"공동체발전": 0.5},
            "주도(자수성가) · 사업화": {"공동체발전": 0.25, "창조적파괴": 0.25},
            "역발상 · 재해석": {"창조적파괴": 0.5},
            "개척 · 탐험 · 모험": {"창조적파괴": 0.25, "미래지향": 0.25},
            "발견 · 발상 · 상상": {"미래지향": 0.5}
        }
        mis = {}
        for a, val in att.items():
            for m, w in att_to_mis[a].items():
                mis[m] = mis.get(m, 0) + val * w
        mis = {k: min(v, 1.0) for k, v in mis.items()}
        outcome = round(min(sum(mis.values()) * 0.25, 1.0), 3)
        return att, mis, outcome

    def draw_radar_chart(title, scores, clockwise_order):
        labels = clockwise_order
        values = [scores.get(label, 0) for label in labels]
        labels += [labels[0]]
        values += [values[0]]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=values, theta=labels, fill='toself', name=title))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False)
        st.markdown(f"### {title}")
        st.plotly_chart(fig, use_container_width=True)

    # 샘플 데이터 정의
    sample_profiles = {
        "제프 베조스": {
            "도전정신": 0.95, "최고·최초·최신·유일 지향": 1.0, "Integrity": 0.92, "창조적 문제해결": 0.88,
            "독립성 · 자기고용 · 자기세계": 0.85, "진취성(선도성)": 0.95, "위험감수성": 0.93, "혁신성": 0.96
        },
        "김슬아": {
            "도전정신": 0.87, "최고·최초·최신·유일 지향": 0.88, "Integrity": 0.85, "창조적 문제해결": 0.91,
            "독립성 · 자기고용 · 자기세계": 0.84, "진취성(선도성)": 0.89, "위험감수성": 0.86, "혁신성": 0.89
        },
        "정주영": {
            "도전정신": 1.0, "최고·최초·최신·유일 지향": 0.95, "Integrity": 0.9, "창조적 문제해결": 0.85,
            "독립성 · 자기고용 · 자기세계": 1.0, "진취성(선도성)": 0.9, "위험감수성": 1.0, "혁신성": 0.85
        }
    }

    st.markdown("샘플 인물 이름 입력 (예: 제프 베조스, 김슬아, 정주영)")
    selected_name = st.text_input("인물 이름:")

    user_inputs = {}
    if selected_name in sample_profiles:
        st.success(f"✅ '{selected_name}'의 데이터를 불러왔습니다.")
        user_inputs = {f"{bundle}_{trait}": sample_profiles[selected_name][bundle]
                       for bundle, traits in TRAIT_STRUCTURE.items()
                       for trait in traits}
    else:
        st.info("슬라이더를 사용해 직접 값을 입력할 수 있습니다.")
        for bundle, traits in TRAIT_STRUCTURE.items():
            st.markdown(f"**{bundle}**")
            cols = st.columns(len(traits))
            for i, trait in enumerate(traits):
                key = f"{bundle}_{trait}"
                user_inputs[key] = cols[i].slider(trait, 0.0, 1.0, 0.5, 0.01)

    if st.button("🌧️ 분석 시작"):
        comp_scores, trait_details = calculate_competence_scores(user_inputs)
        att_scores, mis_scores, outcome = compute_layers(comp_scores)

        st.metric("💧 최종 봄비 점수", f"{outcome * 100:.2f}점")

        st.subheader("🧩 Competence Layer - 세부 항목 점수")
        for bundle, traits in trait_details.items():
            cols = st.columns(len(traits))
            for i, (trait, score) in enumerate(traits.items()):
                cols[i].markdown(f"`{trait}`: **{score:.2f}**")

        # 시계방향 순서 지정
        comp_order = list(TRAIT_STRUCTURE.keys())
        att_order = ["창조 · 발명 · 개발", "조합(결합/융합) · 중개", "혁신 · 변화 · 개선", "도전 · 극복",
                     "주도(자수성가) · 사업화", "역발상 · 재해석", "개척 · 탐험 · 모험", "발견 · 발상 · 상상"]
        mis_order = ["기회추구", "공동체발전", "창조적파괴", "미래지향"]

        draw_radar_chart("🧩 Competence Layer", comp_scores, comp_order)
        draw_radar_chart("🌀 Attitude Layer", att_scores, att_order)
        draw_radar_chart("🎯 Mission Layer", mis_scores, mis_order)
