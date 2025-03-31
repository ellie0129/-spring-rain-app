import streamlit as st

st.set_page_config(page_title="봄비 점수 분석기", page_icon="🌱")
st.title("🌧️ 봄비(Spring Rain) 점수 분석기")
st.caption("이춘우 교수님의 기업가정신 통합모형 기반")

st.markdown("---")
st.subheader("1️⃣ 역량 점수 입력")

# 역량 목록
competence_list = [
    "도전정신",
    "고수익 기대",
    "창의성",
    "아이디어 · 상상력",
    "독립성 · 자기고용 · 자기세계",
    "진취성",
    "위험감수성",
    "혁신성"
]

# 점수 입력받기 (0~1)
competence_scores = {}
for comp in competence_list:
    competence_scores[comp] = st.slider(f"{comp}", 0.0, 1.0, 0.5, 0.01)

# 계산 함수
def compute_spring_rain_score(scores):
    comp_to_att = {
        "도전정신": ["창조 · 발명 · 개발", "조합 · 중개"],
        "고수익 기대": ["조합 · 중개", "혁신 · 변화 · 개선"],
        "창의성": ["혁신 · 변화 · 개선", "도전 · 극복"],
        "아이디어 · 상상력": ["도전 · 극복", "주도 · 사업화"],
        "독립성 · 자기고용 · 자기세계": ["주도 · 사업화", "역발상 · 재해석"],
        "진취성": ["역발상 · 재해석", "개척 · 탐험 · 모험"],
        "위험감수성": ["개척 · 탐험 · 모험", "발견 · 발상 · 상상"],
        "혁신성": ["발견 · 발상 · 상상", "창조 · 발명 · 개발"]
    }
    att_scores = {k: 0.0 for k in [
        "창조 · 발명 · 개발", "조합 · 중개", "혁신 · 변화 · 개선", "도전 · 극복",
        "주도 · 사업화", "역발상 · 재해석", "개척 · 탐험 · 모험", "발견 · 발상 · 상상"]}
    for comp, val in scores.items():
        for att in comp_to_att[comp]:
            att_scores[att] += val * 0.5
    att_scores = {k: min(v, 1.0) for k, v in att_scores.items()}

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
    mis_scores = {k: 0.0 for k in ["기회추구", "공동체발전", "창조적파괴", "미래지향"]}
    for att, val in att_scores.items():
        for mis, w in att_to_mis[att].items():
            mis_scores[mis] += val * w
    mis_scores = {k: min(v, 1.0) for k, v in mis_scores.items()}

    outcome = sum(mis_scores.values()) * 0.25
    bombi = outcome * 100
    return att_scores, mis_scores, outcome, bombi

# 실행 버튼
if st.button("💧 봄비 점수 계산하기"):
    att, mis, out, bombi = compute_spring_rain_score(competence_scores)
    st.markdown("---")
    st.subheader("2️⃣ 분석 결과")

    st.write("**🌿 Attitude Layer**")
    for k, v in att.items():
        st.write(f"- {k}: {v:.2f}")

    st.write("**🌏 Mission Layer**")
    for k, v in mis.items():
        st.write(f"- {k}: {v:.2f}")

    st.write("**🌧️ Outcome Layer**")
    st.success(f"통합 성과 점수: {out:.2f} → 봄비 점수: {bombi:.2f}점")
