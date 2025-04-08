
import plotly.graph_objects as go
from collections import OrderedDict

def draw_radar(title, data):
    """
    주어진 데이터에 맞춰 레이더 차트를 시계방향으로 그려주는 함수
    """
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

    fig = go.Figure()
    labels = list(data.keys())
    values = list(data.values())
    labels += [labels[0]]  # 원형으로 되돌리기 위해 첫 번째 값 추가
    values += [values[0]]  # 마찬가지로 첫 번째 값 추가
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        name=title,
        direction='clockwise'  # 시계방향으로 설정
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False
    )
    return fig

def draw_all_radars(competence_data, attitude_data, mission_data):
    """
    Competence, Attitude, Mission Layer에 대해 각각 레이더 차트를 그려주는 함수
    """
    # Competence Layer
    fig_comp = draw_radar("🕸️ Competence Layer", competence_data)
    
    # Attitude Layer
    fig_att = draw_radar("🌀 Attitude Layer", attitude_data)
    
    # Mission Layer
    fig_mis = draw_radar("🎯 Mission Layer", mission_data)
    
    return fig_comp, fig_att, fig_mis

def draw_outcome_layer(competence_data, attitude_data, mission_data):
    """
    Outcome Layer는 Mission, Attitude, Competence 레이더 차트를 하나로 포개는 함수
    """
    fig = go.Figure()

    # 각 레이더 차트 추가
    fig.add_trace(go.Scatterpolar(r=list(mission_data.values()) + [mission_data.get(list(mission_data.keys())[0])],
                                 theta=list(mission_data.keys()) + [list(mission_data.keys())[0]],
                                 fill='toself', name="🎯 Mission Layer", direction='clockwise'))

    fig.add_trace(go.Scatterpolar(r=list(attitude_data.values()) + [attitude_data.get(list(attitude_data.keys())[0])],
                                 theta=list(attitude_data.keys()) + [list(attitude_data.keys())[0]],
                                 fill='toself', name="🌀 Attitude Layer", opacity=0.5, direction='clockwise'))

    fig.add_trace(go.Scatterpolar(r=list(competence_data.values()) + [competence_data.get(list(competence_data.keys())[0])],
                                 theta=list(competence_data.keys()) + [list(competence_data.keys())[0]],
                                 fill='toself', name="🕸️ Competence Layer", opacity=0.3, direction='clockwise'))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True
    )
    return fig
