# spring_rain_app.py (최종 완성본)
# 완전히 통합된 Streamlit 앱 코드: 모든 요청사항 반영

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
    - 💪 도전정신: 자기효능감, 성취욕구, 헝그리정신
    - 💡 최고·최초·최신·유일 지향: 열망, 실행력, 결단력, 고수익 기대
    - 🧭 Integrity: 리더십, 사업수완, 경영역량, 신용, 근면성실
    - 🔍 창조적 문제해결: 낙관성, 통찰력, 아이디어, 인지능력
    - 🌱 독립성·자기고용: 자아실현, 자율성, 순응거부, 역경 극복
    - 🚀 진취성(선도성): 열정, 모호성 인내도, 공격성, 선도력
    - 🛡 위험감수성: 인내심, 위험선호, CSR/CSV, 책임감
    - 🔄 혁신성: 기업윤리, 창의성, 혁신 수용성

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

# ---------------- 분석기 탭 ----------------
else:
    st.subheader("🤖 AI 기반 인물 분석")
    st.caption("예시: 제프 베조스, 김슬아, 정주영")

    selected_name = st.text_input("분석할 인물 이름을 입력하세요")

    # 샘플 프로필 정의
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
    if selected_name == "이춘우":
        st.success("🌟 당신은 이미 완성된 통합모형 그 자체를 입력하셨습니다!")
        competence_scores = {k: 1.0 for k in [
            "도전정신", "최고·최초·최신·유일 지향", "Integrity", "창조적 문제해결",
            "독립성 · 자기고용 · 자기세계", "진취성(선도성)", "위험감수성", "혁신성"]}

    elif selected_name in sample_profiles:
        traits, comment = sample_profiles[selected_name]
        for bundle, values in traits:
            competence_scores[bundle] = np.mean(values)

        st.success(f"✅ '{selected_name}'의 역량 프로파일을 불러왔습니다")
        st.markdown(f"💬 **AI 평가 주석**: {comment}")

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
    for bundle, values in traits:
        st.markdown(f"**{bundle}**")
        for i, score in enumerate(values):
            label = trait_names.get(bundle, [])[i] if i < len(trait_names.get(bundle, [])) else f"하위 요소 {i+1}"
            st.markdown(f"  - {label}: {score:.2f}")
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
    label = trait_names.get(bundle, [])[i] if i < len(trait_names.get(bundle, [])) else f"하위 요소 {i+1}"
    st.markdown(f"  - {label}: {score:.2f}")

    else:
        st.info("✏️ 분석할 인물에 대한 세부 역량을 직접 입력하세요!")
        manual_traits = {
            "💪 도전정신": ["자기효능감 (self-efficacy), 자신감", "성취 욕구", "헝그리정신, 목표 달성 추구"],
            "💡 최고·최초·최신·유일 지향": ["열망", "추진력, 실행력", "결단력", "고수익 기대"],
            "🧭 Integrity": ["리더십", "사업수완", "경영 관리 역량", "신용, 신뢰", "근면, 검소, 성실성"],
            "🔍 창조적 문제해결": ["긍정성", "통찰력", "아이디어, 상상력", "인지 능력"],
            "🌱 독립성 · 자기고용 · 자기세계": ["자아실현", "자율성", "순응 거부", "역경 극복"],
            "🚀 진취성(선도성)": ["열정", "모호성 인내도", "경쟁적 공격성", "선도력"],
            "🛡 위험감수성": ["인내심", "위험선호", "CSR/CSV", "책임감"],
            "🔄 혁신성": ["기업윤리", "창의성", "혁신 수용"]
        }
        for bundle, items in manual_traits.items():
            st.markdown(f"### {bundle}")
            values = []
            for trait in items:
                score = st.slider(f"  {trait}", 0.0, 1.0, 0.0, 0.01)
                values.append(score)
            clean_key = bundle.split(" ")[1] if " " in bundle else bundle
            competence_scores[clean_key] = np.mean(values)

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
