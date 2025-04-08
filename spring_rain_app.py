import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Streamlit 설정
st.set_page_config(page_title="봄비 점수 분석기", page_icon="🌱", layout="wide")

# 탭 메뉴
menu = st.sidebar.radio("메뉴", ["모형 설명", "분석기", "샘플 데이터"])

# ---------------------------------------------
# 📘 모형 설명 탭 (수정 금지)
# ---------------------------------------------
if menu == "모형 설명":
    st.header("📘 기업가정신 통합모형 구조 설명")
    st.markdown("""
    ### 🔄 전체 레이어 구조

    이 앱은 이춘우 교수님의 [기업가정신 통합모형]에 따라 총 4개의 레이어로 구성되어 있습니다:

    1. **Outcome Layer (성과)**: 최종 성취 - `부의 증대`, `가치 창출`
    2. **Mission Layer (사명)**: 사업의 지향점 - `기회추구`, `공동체발전`, `창조적파괴`, `미래지향`
    3. **Attitude Layer (행동양식)**: 기업가의 태도와 접근 방식 (총 8개)
    4. **Competence Layer (역량 번들)**: 세부 역량 요소들로 구성된 기본기 (총 8개)

    각 레이어는 아래로부터 위로 점수가 **전이(transfer)** 되어 올라갑니다.

    ---    

    ### 🧬 점수 전이 흐름 요약

    - **역량(Competence)** → 태도(Attitude)로: 각 역량 번들이 2개 태도에 0.5점씩 기여
    - **태도(Attitude)** → 사명(Mission)으로: 각 태도가 관련된 사명에 0.25~0.5점 비중으로 연결
    - **사명(Mission)** → 성과(Outcome)로: 각 사명이 `부의 증대` & `가치 창출`에 각각 0.25점 기여

    이 구조를 통해 최종 **Outcome Layer**에서 1점(100점 만점) 기준으로 `봄비 점수`가 계산됩니다.

    ---    

    ### 🧭 시각적 구조 요약

    아래는 전체 통합모형의 계층적 흐름입니다:

    ``Competence`` → ``Attitude`` → ``Mission`` → ``Outcome``

    또는 쉽게 표현하면:

    > 부지런함/창의성/도전정신 → 행동양식들 → 사회/시장 사명 → 가치/부 창출

    ---    

    ### 🖼️ 모형 도식 이미지

    📌 *이 모형은 실제 논문(이춘우, 2019 및 2020)에서 발췌한 이미지로 시각화한 것입니다.*
    """)
    st.image("https://raw.githubusercontent.com/ellie0129/spring-rain-app/main/assets/1ce34f642e1b80808f4edd8cc64b1a95.png", use_container_width=True)
    st.markdown("---")

# ---------------------------------------------
# 🤖 분석기 탭 (슬라이더 수동 입력)
# ---------------------------------------------

elif menu == "분석기":
    st.header("🤖 나의 역량 점수 입력")
    st.markdown("슬라이더를 조정하여 각 하위 역량을 평가한 뒤 '분석 실행'을 누르세요.")

    TRAIT_STRUCTURE = {
        "도전정신": [
            "자기효능감 (self-efficacy), 자신감 (self confidence)",
            "성취 욕구 (N-Achievement)",
            "헝그리정신, 목표 달성 추구"
        ],
        "최고·최초·최신·유일 지향": [
            "열망(야망)",
            "추진력, 실행력",
            "결단력(의사결정)",
            "고수익 기대"
        ],
        "Integrity": [
            "리더십",
            "사업수완",
            "경영 관리 역량",
            "신용, 신뢰",
            "근면, 검소, 성실성"
        ],
        "창조적 문제해결": [
            "긍정적, 낙관적",
            "통찰력, 안목",
            "아이디어, 상상력, 호기심, 탐구",
            "인지 능력 (지적 능력)"
        ],
        "독립성 · 자기고용 · 자기세계": [
            "자아실현 (self actualization)",
            "자율성 지향",
            "순응 거부",
            "역경 극복"
        ],
        "진취성(선도성)": [
            "열정",
            "높은 모호성 인내도",
            "경쟁적 공격성",
            "선도적"
        ],
        "위험감수성": [
            "인내심",
            "위험선호",
            "CSR/CSV",
            "책임감(책임의식)"
        ],
        "혁신성": [
            "기업윤리",
            "창의성",
            "변화 및 혁신 적극 수용"
        ]
    }

    EMOJIS = {
        "도전정신": "🔥",
        "최고·최초·최신·유일 지향": "🏆",
        "Integrity": "🧭",
        "창조적 문제해결": "🧠",
        "독립성 · 자기고용 · 자기세계": "🚀",
        "진취성(선도성)": "🌟",
        "위험감수성": "⚠️",
        "혁신성": "💡"
    }

    user_inputs = {}
    st.markdown("---")

    for bundle, traits in TRAIT_STRUCTURE.items():
        st.markdown(" ")
        st.markdown(f"### {EMOJIS.get(bundle, '')} {bundle}")
        cols = st.columns(len(traits))
        for i, trait in enumerate(traits):
            user_inputs[f"{bundle}_{trait}"] = cols[i].slider(trait, 0.0, 1.0, 0.5, 0.01)

    if st.button("💧 분석 실행"):
        st.success("분석이 시작되었습니다!")
        st.markdown("⚙️ 분석 결과가 여기에 표시될 수 있도록 기능 연동을 준비해주세요.")
        # 역량 번들 점수 계산
        competence_scores = {}
        for bundle, traits in TRAIT_STRUCTURE.items():
            trait_values = [user_inputs[f"{bundle}_{trait}"] for trait in traits]
            competence_scores[bundle] = round(sum(trait_values) / len(trait_values), 3)

        # Competence → Attitude 매핑
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

        # Attitude 계산
        attitude_scores = {}
        for c, val in competence_scores.items():
            for a in comp_to_att[c]:
                attitude_scores[a] = attitude_scores.get(a, 0) + val * 0.5
        attitude_scores = {k: round(min(v, 1.0), 3) for k, v in attitude_scores.items()}

        # Attitude → Mission 매핑
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

        # Mission 계산
        mission_scores = {}
        for a, val in attitude_scores.items():
            for m, w in att_to_mis[a].items():
                mission_scores[m] = mission_scores.get(m, 0) + val * w
        mission_scores = {k: round(min(v, 1.0), 3) for k, v in mission_scores.items()}

        # Outcome 계산
        outcome_score = round(min(sum(mission_scores.values()) * 0.25, 1.0), 3)

        # 레이더 차트 함수
        def radar(title, data, clockwise=True):
            labels = list(data.keys())
            values = list(data.values())
            if clockwise:
                labels = labels[::-1]
                values = values[::-1]
            labels += [labels[0]]
            values += [values[0]]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=values, theta=labels, fill='toself', name=title))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=False
            )
            st.markdown(f"#### {title}")
            st.plotly_chart(fig, use_container_width=True)

        # 출력
        st.markdown("## 📊 분석 결과")
        radar("🧩 Competence Layer", competence_scores, clockwise=True)
        radar("🌀 Attitude Layer", attitude_scores, clockwise=False)
        radar("🎯 Mission Layer", mission_scores, clockwise=True)

        st.markdown("### 🌧️ Outcome Score (봄비 점수)")
        st.success(f"최종 봄비 점수: {outcome_score * 100:.2f}점")

elif menu == "샘플 데이터":
    st.header("🧪 샘플 인물 데이터 보기")

    sample_profiles = {
        "제프 베조스": {
            "도전정신": 0.9, "고수익 기대": 1.0, "창의성": 0.85, "아이디어 · 상상력": 0.7,
            "독립성 · 자기고용 · 자기세계": 0.8, "진취성": 0.95, "위험감수성": 0.9, "혁신성": 0.9
        },
        "김슬아": {
            "도전정신": 0.85, "고수익 기대": 0.75, "창의성": 0.8, "아이디어 · 상상력": 0.9,
            "독립성 · 자기고용 · 자기세계": 0.85, "진취성": 0.9, "위험감수성": 0.75, "혁신성": 0.8
        },
        "정주영": {
            "도전정신": 1.0, "고수익 기대": 0.95, "창의성": 0.8, "아이디어 · 상상력": 0.6,
            "독립성 · 자기고용 · 자기세계": 1.0, "진취성": 0.9, "위험감수성": 1.0, "혁신성": 0.75
        }
    }

    sample_comments = {
        "제프 베조스": "🧠 강한 실행력과 고수익 지향, 기술 기반 혁신을 바탕으로 세계 전자상거래를 재편한 인물입니다.",
        "김슬아": "🌸 일상생활에서의 불편함을 발견하고, 탁월한 창의력과 실행력을 통해 독보적인 물류 모델을 만든 인물입니다.",
        "정주영": "🏗️ 무에서 유를 창조한 기업가로, 진취성·독립성·도전정신이 매우 두드러지는 대표적인 한국형 기업가입니다."
    }

    for name in sample_profiles.keys():
        if st.button(f"🔍 {name} 샘플 데이터 보기"):
            st.markdown(f"### 🧾 {name}의 점수 프로파일")
            st.write(sample_profiles[name])
            st.markdown(f"**해석 주석**: {sample_comments[name]}")
