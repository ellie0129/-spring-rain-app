
import numpy as np

# 정해진 역량 번들과 하위 항목 구조
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

def compute_bombi_score(trait_scores_by_item):
    """
    trait_scores_by_item: dict - {하위 항목명: 점수}
    return: comp, att, mis, outcome
    """

    # 0단계: 세부 항목 평균으로 Competence 점수 계산
    comp = {}
    for bundle, items in TRAIT_STRUCTURE.items():
        values = []
        for item in items:
            if item in trait_scores_by_item:
                values.append(trait_scores_by_item[item])
        if values:
            comp[bundle] = np.mean(values)
        else:
            comp[bundle] = 0.0

    # 1단계: Competence → Attitude
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

    # 2단계: Attitude → Mission
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

    # 3단계: Outcome 점수 = Mission 평균 × 0.25
    outcome = round(min(np.mean(list(mis.values())) * 0.25, 1.0), 3)

    return comp, att, mis, outcome
