
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys
sys.path.append("modules")
from bombi_score_module import compute_bombi_score, TRAIT_STRUCTURE

# 앱 설정
st.set_page_config(page_title="봄비 점수 분석기 (모듈형)", page_icon="🌧️", layout="wide")
st.title("🌱 봄비(Spring Rain) 점수 분석기 (모듈형)")
st.caption("이춘우 교수님의 기업가정신 통합모형 기반 · 모듈 분리 구조")

# 메뉴
menu = st.sidebar.radio("탭을 선택하세요", ["분석기", "모형 설명"])

if menu == "모형 설명":
    st.header("📘 기업가정신 통합모형 구조 설명")
    st.markdown("""
    이 앱은 이춘우 교수님의 통합모형에 따라 구성된 분석 도구입니다.  
    총 4개 레이어가 존재하며, 점수는 아래 흐름을 통해 전이됩니다.

    **[하위 항목] → Competence → Attitude → Mission → Outcome (봄비 점수)**

    ✅ Outcome은 단일 지표: **'부의 증대 & 가치창출'**  
    ✅ Mission 평균의 0.25배로 계산됨  
    ✅ 최종 점수는 100점 환산하여 표기됨

    모형 이미지:
    """)
    st.image("https://raw.githubusercontent.com/ellie0129/spring-rain-app/main/assets/1ce34f642e1b80808f4edd8cc64b1a95.png", use_container_width=True)

else:
    st.header("🤖 인물 점수 분석기")
    st.markdown("분석할 인물 이름을 입력하세요 (예: **제프 베조스**, **김슬아**, **정주영**)")

    selected_name = st.text_input("이름 입력")

    # 샘플 입력
    sample_profiles = {
        "제프 베조스": {
            "자기효능감 (self-efficacy), 자신감 (self confidence)": 0.95,
            "성취 욕구 (N-Achievement)": 0.9,
            "헝그리정신, 목표 달성 추구": 0.9,
            "열망(야망)": 1.0,
            "추진력, 실행력": 0.95,
            "결단력(의사결정)": 0.9,
            "고수익 기대": 1.0,
            "리더십": 0.9,
            "사업수완": 0.95,
            "경영 관리 역량": 0.95,
            "신용, 신뢰": 0.85,
            "근면, 검소, 성실성": 0.85,
            "긍정적, 낙관적": 0.85,
            "통찰력, 안목": 0.9,
            "아이디어, 상상력, 호기심, 탐구": 0.95,
            "인지 능력 (지적 능력)": 1.0,
            "자아실현 (self actualization)": 0.85,
            "자율성 지향": 0.9,
            "순응 거부": 0.85,
            "역경 극복": 0.9,
            "열정": 0.95,
            "높은 모호성 인내도": 0.9,
            "경쟁적 공격성": 1.0,
            "선도적": 0.95,
            "인내심": 0.85,
            "위험선호": 0.9,
            "CSR/CSV": 0.75,
            "책임감(책임의식)": 0.85,
            "기업윤리": 0.8,
            "창의성": 0.95,
            "변화 및 혁신 적극 수용": 1.0
        },
        "김슬아": {
            "자기효능감 (self-efficacy), 자신감 (self confidence)": 0.9,
            "성취 욕구 (N-Achievement)": 0.85,
            "헝그리정신, 목표 달성 추구": 0.85,
            "열망(야망)": 0.85,
            "추진력, 실행력": 0.85,
            "결단력(의사결정)": 0.9,
            "고수익 기대": 0.85,
            "리더십": 0.85,
            "사업수완": 0.85,
            "경영 관리 역량": 0.85,
            "신용, 신뢰": 0.85,
            "근면, 검소, 성실성": 0.85,
            "긍정적, 낙관적": 0.9,
            "통찰력, 안목": 0.9,
            "아이디어, 상상력, 호기심, 탐구": 0.85,
            "인지 능력 (지적 능력)": 0.9,
            "자아실현 (self actualization)": 0.85,
            "자율성 지향": 0.85,
            "순응 거부": 0.8,
            "역경 극복": 0.85,
            "열정": 0.9,
            "높은 모호성 인내도": 0.9,
            "경쟁적 공격성": 0.9,
            "선도적": 0.9,
            "인내심": 0.8,
            "위험선호": 0.8,
            "CSR/CSV": 0.8,
            "책임감(책임의식)": 0.9,
            "기업윤리": 0.9,
            "창의성": 0.9,
            "변화 및 혁신 적극 수용": 0.95
        },
        "정주영": {
            "자기효능감 (self-efficacy), 자신감 (self confidence)": 0.95,
            "성취 욕구 (N-Achievement)": 1.0,
            "헝그리정신, 목표 달성 추구": 1.0,
            "열망(야망)": 0.95,
            "추진력, 실행력": 1.0,
            "결단력(의사결정)": 0.95,
            "고수익 기대": 1.0,
            "리더십": 0.9,
            "사업수완": 0.95,
            "경영 관리 역량": 0.95,
            "신용, 신뢰": 0.9,
            "근면, 검소, 성실성": 1.0,
            "긍정적, 낙관적": 0.85,
            "통찰력, 안목": 0.85,
            "아이디어, 상상력, 호기심, 탐구": 0.75,
            "인지 능력 (지적 능력)": 0.85,
            "자아실현 (self actualization)": 0.95,
            "자율성 지향": 1.0,
            "순응 거부": 0.95,
            "역경 극복": 1.0,
            "열정": 1.0,
            "높은 모호성 인내도": 0.95,
            "경쟁적 공격성": 0.95,
            "선도적": 1.0,
            "인내심": 0.9,
            "위험선호": 0.9,
            "CSR/CSV": 0.75,
            "책임감(책임의식)": 0.95,
            "기업윤리": 0.9,
            "창의성": 0.85,
            "변화 및 혁신 적극 수용": 0.9
        }
    }

    if selected_name == "이춘우":
        st.success(f"✅ '{selected_name}'의 프로파일을 불러왔습니다.")
        st.write("**이춘우 교수님은 의심할 여지 없이 완벽한 기업가이십니다!**")
        trait_inputs = {item: 1.0 for bundle in TRAIT_STRUCTURE.values() for item in bundle}
    elif selected_name in sample_profiles:
        st.success(f"✅ '{selected_name}'의 프로파일을 불러왔습니다.")
        trait_inputs = sample_profiles[selected_name]
        if selected_name == "김슬아":
            st.info("**김슬아**는 신선배송 유통 스타트업을 창업하여 혁신성과 실행력을 기반으로 높은 '창조적 문제해결'과 '최고·최초·최신 지향' 점수를 획득했습니다.")
        elif selected_name == "정주영":
            st.info("**정주영**은 극복력, 진취성, 추진력에서 독보적 점수를 보입니다. 특히 '역경 극복', '목표 달성 추구', '자율성 지향' 항목에서 최고 수준입니다.")
        elif selected_name == "제프 베조스":
            st.info("**제프 베조스**는 '경쟁적 공격성', '아이디어', '결단력'이 돋보입니다. 미래를 내다보는 인지 능력과 사업수완도 우수하게 평가됐습니다.")
    else:
        st.info("직접 하위 항목의 점수를 입력할 수 있습니다.")
        trait_inputs = {}
        for bundle, traits in TRAIT_STRUCTURE.items():
            st.markdown(f"#### 🧩 {bundle}")
            cols = st.columns(len(traits))
            for i, trait in enumerate(traits):
                val = cols[i].slider(f"{trait}", 0.0, 1.0, 0.5, 0.01)
                trait_inputs[trait] = val

    if st.button("💧 분석 시작"):
        comp, att, mis, outcome = compute_bombi_score(trait_inputs)

        
from collections import OrderedDict


from collections import OrderedDict

def radar(title, data):
    if title == "🌀 Attitude Layer":
        attitude_order = [
            "창조 · 발명 · 개발",
            "조합(결합/융합) · 중개",
            "혁신 · 변화 · 개선",
            "도전 · 극복",
            "주도(자수성가) · 사업화",
            "역발상 · 재해석",
            "개척 · 탐험 · 모험",
            "발견 · 발상 · 상상"
        ]
        data = OrderedDict((k, data[k]) for k in attitude_order if k in data)
    
    fig = go.Figure()  # 들여쓰기 위치 조정
    labels = list(data.keys())
    values = list(data.values())
    labels += [labels[0]]
    values += [values[0]]
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        name=title,
        direction='clockwise'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False
    )
    st.markdown(f"#### {title}")
    st.plotly_chart(fig, use_container_width=True)


            fig = go.Figure()
            labels = list(data.keys())
            values = list(data.values())
            labels += [labels[0]]
            values += [values[0]]
            fig.add_trace(go.Scatterpolar(r=values, theta=labels, fill='toself', name=title))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=False
            )
            st.markdown(f"#### {title}")
            st.plotly_chart(fig, use_container_width=True)

        radar("🕸️ Competence Layer", comp)
        radar("🌀 Attitude Layer", att)
        radar("🎯 Mission Layer", mis)

        st.subheader("📊 레이어별 점수표")
        st.write("**Competence Layer**")
        st.dataframe({k: [f"{v:.2f}"] for k, v in comp.items()})
        st.write("**Attitude Layer**")
        st.dataframe({k: [f"{v:.2f}"] for k, v in att.items()})
        st.write("**Mission Layer**")
        st.dataframe({k: [f"{v:.2f}"] for k, v in mis.items()})

        st.subheader("🌧️ 최종 봄비 점수")
        st.success(f"☔ {outcome * 100:.2f}점 (부의 증대 & 가치창출)")
