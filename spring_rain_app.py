import streamlit as st
import numpy as np
import plotly.graph_objects as go
import json
import os

# Streamlit 설정
st.set_page_config(page_title="봄비 점수 분석기", page_icon="🌱", layout="wide")
st.title("🌧️ 봄비(Spring Rain) 점수 분석기")
st.caption("이춘우 교수님의 기업가정신 통합모형 기반")

# 왼쪽 사이드바 탭 메뉴 (모형 설명, 분석기, 샘플 데이터)
menu = st.sidebar.radio("메뉴", ["모형 설명", "분석기", "샘플 데이터"])

##############################
# 모형 설명 탭 (변경 없음)
##############################
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

##############################
# 분석기 탭 (변경 없음)
##############################
elif menu == "분석기":
    st.header("🤖 나의 역량 점수 입력")
    st.markdown("슬라이더를 조정하여 각 하위 역량을 평가한 뒤 '분석 실행'을 누르세요.")
    
    # 역량 번들을 구성하는 세부 항목 구조
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
    
    # 각 역량 번들에 대한 슬라이더 생성
    for bundle, traits in TRAIT_STRUCTURE.items():
        st.markdown("")
        st.markdown(f"### {EMOJIS.get(bundle, '')} {bundle}")
        cols = st.columns(len(traits))
        for i, trait in enumerate(traits):
            user_inputs[f"{bundle}_{trait}"] = cols[i].slider(trait, 0.0, 1.0, 0.5, 0.01)
    
    if st.button("💧 분석 실행"):
        st.success("분석이 시작되었습니다!")
        
        # 역량 번들 점수 계산: 각 항목의 평균값
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
        
        mission_scores = {}
        for att, val in attitude_scores.items():
            for m, w in att_to_mis[att].items():
                mission_scores[m] = mission_scores.get(m, 0) + val * w
        mission_scores = {k: round(min(v, 1.0), 3) for k, v in mission_scores.items()}
        mission_scores = {k: mission_scores[k] for k in ["기회추구", "공동체발전", "창조적파괴", "미래지향"]}
        
        outcome_score = round(min(sum(mission_scores.values()) * 0.25, 1.0), 3)
        
        # 레이더 차트 함수 (분석기 탭에서 사용)
        def radar(title, data, clockwise=True):
            labels = list(data.keys())
            values = list(data.values())
            if clockwise:
                labels = labels[::-1]
                values = values[::-1]
            labels += [labels[0]]
            values += [values[0]]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=values, theta=labels, fill="toself", name=title))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
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
            fill="toself",
            name="역량 프로파일"
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=False,
            margin=dict(l=30, r=30, t=30, b=30),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

##############################
# 샘플 데이터 탭 (수정됨)
##############################
elif menu == "샘플 데이터":
    st.header("🧪 샘플 인물 데이터 보기")
    
    # JSON 파일 경로 설정 (spring_rain_app.py와 같은 디렉토리)
    json_path = os.path.join(os.path.dirname(__file__), "sample_data.json")
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            sample_data = json.load(f)
        detailed_profiles = sample_data.get("sample_profiles", {})
        sample_comments = sample_data.get("sample_comments", {})
    except Exception as e:
        st.error(f"샘플 데이터 불러오기 실패: {e}")
        detailed_profiles = {}
        sample_comments = {}
    
    if detailed_profiles:
        selected_profile = st.selectbox("샘플 인물을 선택하세요", list(detailed_profiles.keys()))
        
        st.markdown(f"### 🧾 {selected_profile}의 상세 점수 프로파일")
        
        # profile_detail: 하위 요소 포함 세부 데이터
        profile_detail = detailed_profiles[selected_profile]
        
        # computed_competence 계산 (각 역량 번들의 하위 요소 평균)
        computed_competence = {}
        for bundle, subtraits in profile_detail.items():
            if isinstance(subtraits, dict):
                trait_scores = list(subtraits.values())
                avg_score = round(sum(trait_scores) / len(trait_scores), 3) if trait_scores else 0
                computed_competence[bundle] = avg_score
            else:
                computed_competence[bundle] = subtraits
        
        # 계산: Competence → Attitude → Mission → Outcome (분석기와 동일한 매핑)
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
        attitude_scores = {}
        for comp, avg in computed_competence.items():
            if comp in comp_to_att:
                for att in comp_to_att[comp]:
                    attitude_scores[att] = attitude_scores.get(att, 0) + avg * 0.5
        attitude_scores = {k: round(min(v, 1.0), 3) for k, v in attitude_scores.items()}
        
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
        mission_scores = {}
        for att, val in attitude_scores.items():
            for m, w in att_to_mis.get(att, {}).items():
                mission_scores[m] = mission_scores.get(m, 0) + val * w
        mission_scores = {k: round(min(v, 1.0), 3) for k, v in mission_scores.items()}
        mission_scores = {k: mission_scores.get(k, 0) for k in ["기회추구", "공동체발전", "창조적파괴", "미래지향"]}
        
        outcome_score = round(min(sum(mission_scores.values()) * 0.25, 1.0), 3)
        
        # Radar 차트 함수 (샘플 데이터 탭에서 재사용)
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
            st.plotly_chart(fig, use_container_width=True)
        
        # 이모지 매핑 (역량 번들 명 옆에 추가)
        sample_emojis = {
            "도전정신": "🔥",
            "최고·최초·최신·유일 지향": "🏆",
            "Integrity": "🧭",
            "창조적 문제해결": "🧠",
            "독립성 · 자기고용 · 자기세계": "🚀",
            "진취성(선도성)": "🌟",
            "위험감수성": "⚠️",
            "혁신성": "💡"
        }
        
        # ========= 원하는 순서대로 출력 =========
        # 1. 해석 주석
        st.markdown("<h4>🔎 해석 주석</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:16px;'>{sample_comments.get(selected_profile, '해당 인물에 대한 설명이 없습니다.')}</p>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # 2. 레이더 차트 3개 (횡 방향: 3열로 배치)
        st.markdown("<h4>📊 레이더 차트</h4>", unsafe_allow_html=True)
        cols = st.columns(3)
        with cols[0]:
            st.markdown("**🧩 Competence Layer (Aggregated) Radar Chart**")
            radar("🧩 Competence Layer (Aggregated)", computed_competence)
        with cols[1]:
            st.markdown("**🌀 Attitude Layer Radar Chart**")
            radar("🌀 Attitude Layer", attitude_scores)
        with cols[2]:
            st.markdown("**🎯 Mission Layer Radar Chart**")
            radar("🎯 Mission Layer", mission_scores)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # 3. ▶️ 계산된 결과 (순서: 상세 역량 번들 점수, Competence, Attitude, Mission, Outcome)
        st.markdown("#### ▶️ 계산된 결과", unsafe_allow_html=True)
        
        # 3-1. 상세 역량 번들 점수 (토글)
        with st.expander("**▶ 상세 역량 번들 점수 (하위 요소별)**"):
            st.markdown("#### 상세 역량 번들 점수 (하위 요소별)")
            for bundle, subtraits in profile_detail.items():
                emoji = sample_emojis.get(bundle, "")
                st.markdown(f"**{emoji} {bundle}**")
                if isinstance(subtraits, dict):
                    trait_list = []
                    for trait, score in subtraits.items():
                        st.write(f"- {trait}: {score}")
                        trait_list.append(score)
                    avg_score = round(sum(trait_list) / len(trait_list), 3) if trait_list else 0
                    st.write(f"**→ {bundle} 평균 점수: {avg_score}**")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 3-2. Competence Layer (평균 점수)
        with st.expander("**Competence Layer (평균 점수)**"):
            st.write(computed_competence)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 3-3. Attitude Layer
        with st.expander("**Attitude Layer**"):
            st.write(attitude_scores)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 3-4. Mission Layer
        with st.expander("**Mission Layer**"):
            st.write(mission_scores)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 3-5. Outcome (봄비 점수)
        with st.expander("**Outcome (봄비 점수)**"):
            st.success(f"{outcome_score * 100:.2f}점")
        st.markdown("<br><br>", unsafe_allow_html=True)
        
    else:
        st.info("샘플 데이터가 없습니다.")
