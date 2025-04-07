import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Streamlit 설정
st.set_page_config(page_title="봄비 점수 분석기", page_icon="🌱", layout="wide")

# 페이지 제목
st.title("🌧️ 봄비(Spring Rain) 점수 분석기")
st.caption("이춘우 교수님의 기업가정신 통합모형 기반")

# 탭 메뉴
menu = st.sidebar.radio("메뉴", ["분석기", "모형 설명"])

# "모형 설명" 탭 내용
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
    st.image("https://raw.githubusercontent.com/ellie0129/spring-rain-app/main/assets/1ce34f642e1b80808f4edd8cc64b1a95.png", use_container_width=True, cache_key=None)

    st.markdown("---")

    st.markdown("""
    ### 📋 각 레이어별 구성 요소 상세

    #### 🧩 Outcome Layer (성과)
    - **부의 증대 (Wealth Creation)**
    - **가치 창출 (Value Creation)**

    #### 🎯 Mission Layer (사명)
    - **기회추구 (실패위험)**
    - **공동체발전 (상호이익)**
    - **창조적파괴 (새로운질서)**
    - **미래지향 (불확실성)**

    #### 🌀 Attitude Layer (직무 수행 태도)
    - 🧑‍🎨 창조 · 발명 · 개발  
    - 🔄 조합(결합·융합) · 중개  
    - 💡 혁신 · 변화 · 개선  
    - 🚀 도전 · 극복  
    - 💼 주도(자수성가) · 사업화  
    - 🔍 역발상 · 재해석  
    - 🌍 개척 · 탐험 · 모험  
    - 🌱 발견 · 발상 · 상상

    #### 🧬 Competence Layer (역량 번들)
    - 💪 **[도전정신]**: 자기효능감, 자신감, 헝그리정신  
    - 💰 **[고수익 기대]**: 열망(야망), 추진력, 의사결정  
    - 🧠 **[창의성]**: 리더십, 관리역량, 경쟁적 공격성  
    - 💡 **[아이디어 · 상상력]**: 인지능력, 성취욕구, 목표 달성 추구  
    - 🌍 **[독립성 · 자기고용 · 자기세계]**: 부지런함(성실성), 순응 거부  
    - 🚀 **[진취성]**: 열정, 자율지향, 선도적  
    - 🛠️ **[위험감수성]**: 인내심, 위험선호, CSR/CSV, 책임감  
    - 🔄 **[혁신성]**: 기업윤리, 창의성, 변화 및 혁신 적극 수용
    """)

else:
    st.subheader("🤖 AI 기반 인물 분석")

    # 예시 인물 프로파일 데이터
    sample_profiles = {
        "제프 베조스": {
            "도전정신": 0.9,
            "고수익 기대": 1.0,
            "창의성": 0.85,
            "아이디어 · 상상력": 0.8,
            "독립성 · 자기고용 · 자기세계": 0.75,
            "진취성": 0.95,
            "위험감수성": 1.0,
            "혁신성": 0.9
        },
        "정주영": {
            "도전정신": 1.0,
            "고수익 기대": 0.95,
            "창의성": 0.8,
            "아이디어 · 상상력": 0.75,
            "독립성 · 자기고용 · 자기세계": 0.9,
            "진취성": 0.85,
            "위험감수성": 1.0,
            "혁신성": 0.8
        },
        "정슬아": {
            "도전정신": 0.85,
            "고수익 기대": 0.75,
            "창의성": 0.8,
            "아이디어 · 상상력": 0.9,
            "독립성 · 자기고용 · 자기세계": 0.8,
            "진취성": 0.85,
            "위험감수성": 0.9,
            "혁신성": 0.95
        }
    }

    st.markdown("AI가 분석할 인물의 이름을 입력하세요 (예: **제프 베조스**, **정슬아**, **정주영**)")
    selected_name = st.text_input("인물 이름 입력")

    if selected_name == "이춘우":
        st.success(f"✅ '{selected_name}'의 프로파일을 불러왔습니다.")
        competence_scores = sample_profiles[selected_name]
        st.write("**이춘우 교수님은 의심할 여지 없이 완벽한 기업가이십니다!**")
    elif selected_name in sample_profiles:
        st.success(f"✅ '{selected_name}'의 프로파일을 불러왔습니다.")
        competence_scores = sample_profiles[selected_name]
    else:
        st.info("아래에서 직접 세부 역량을 입력해도 됩니다.")
        st.subheader("1️⃣ 세부 역량 입력")
        competence_details = {
            "도전정신": ["자기효능감", "자신감", "헝그리정신"],
            "고수익 기대": ["열망(야망)", "추진력", "의사결정"],
            "창의성": ["리더십", "관리역량", "경쟁적 공격성"],
            "아이디어 · 상상력": ["인지능력(지적 능력)", "성취욕구", "목표 달성 추구"],
            "독립성 · 자기고용 · 자기세계": ["부지런함(성실성)", "순응 거부"],
            "진취성": ["열정", "자율 지향", "선도적"],
            "위험감수성": ["인내심", "위험선호", "CSR/CSV", "책임감(책임의식)"],
            "혁신성": ["기업윤리", "창의성", "변화 및 혁신 적극 수용"]
        }
        competence_scores = {}
        for bundle, traits in competence_details.items():
            st.markdown(f"<h5 style='margin-bottom:5px;'>{bundle}</h5>", unsafe_allow_html=True)
            values = []
            for trait in traits:
                score = st.slider(f"  {trait}", 0.0, 1.0, 0.5, 0.01)
                values.append(score)
            competence_scores[bundle] = np.mean(values)

    # 인물별 뛰어난 역량 번들 설명 추가
    st.markdown("---")
    if selected_name == "제프 베조스":
        st.subheader("📋 제프 베조스: Amazon 창업자")
        st.markdown("""
        **주요 역량 번들**:
        - **위험감수성**: 제프 베조스는 **위험을 감수하고 새로운 시장을 창출**하는 데 두각을 나타냈습니다. **Amazon** 창립 초기, 많은 전문가들이 성공을 의심했지만, 그는 **전자상거래**라는 혁신적인 사업 모델에 투자하고, **급격한 확장**을 추진했습니다.
        - **뛰어난 이유**: 제프 베조스는 **혁신과 변화를 추구하는 사고**를 바탕으로 **모든 사업의 불확실성과 위험을 기회로 바꾼** 인물입니다. 또한, **장기적 비전**과 **고수익을 위한 결단력** 덕분에, **Amazon**을 세계 최대의 온라인 마켓으로 성장시켰습니다.
        """)

    elif selected_name == "정주영":
        st.subheader("📋 정주영: 현대그룹 창업자")
        st.markdown("""
        **주요 역량 번들**:
        - **도전성**: 정주영은 **자기효능감**과 **성취욕구**를 통해, **현대자동차**를 세계적 브랜드로 성장시키는 과정에서 **끊임없는 도전과 노력**을 보여주었습니다. 
        - **뛰어난 이유**: 정주영은 **사업 초기에 큰 어려움을 겪었지만**, **도전정신**을 통해 **국내외 시장에서 두각을 나타내며 성공적인 기업을 만들었습니다**. 그의 **도전성**과 **끊임없는 자기 혁신**은 기업가정신의 대표적인 모델로 평가받고 있습니다.
        """)

    elif selected_name == "정슬아":
        st.subheader("📋 정슬아: 쿠팡 창업자")
        st.markdown("""
        **주요 역량 번들**:
        - **창조적 문제해결**: 김슬아는 **쿠팡의 창의적인 문제 해결** 방식을 통해 **새로운 비즈니스 모델을 창출**하고 **고객 중심의 혁신적인 서비스**를 제공했습니다.
        - **뛰어난 이유**: 김슬아는 **기술적 혁신과 실용적 문제 해결 능력**을 바탕으로 **매일경제신문**에서 **쿠팡의 성장을 이끈 인물**로, **서비스 개선**을 통해 **고객 만족도를 극대화**한 경험이 돋보입니다. **위험 감수와 결단력**이 뛰어난 기업가입니다.
        """)

    # 봄비 점수 계산 함수 및 레이더 차트는 이전과 동일
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

        st.markdown("---")
        st.subheader("📊 역량 번들 점수 레이더 차트")
        radar_labels = list(competence_scores.keys())
        radar_values = list(competence_scores.values())
        radar_values.append(radar_values[0])
        radar_labels.append(radar_labels[0])

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=radar_values,
            theta=radar_labels,
            fill='toself',
            name='역량 프로파일'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=False,
            margin=dict(l=30, r=30, t=30, b=30),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
