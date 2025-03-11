import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def main():
    st.title("🩺 헤모글로빈 상세 정보")
    # ✅ `session_state`에서 데이터 불러오기
    if "patient_data" not in st.session_state:
        st.warning("⚠️ 먼저 메인 페이지에서 건강 정보를 입력하세요.")
        st.stop()  # 데이터가 없으면 실행 중지

    patient_data = pd.DataFrame([{k: float(v) if isinstance(v, (int, float)) else v for k, v in st.session_state["patient_data"].items()}])



    # ✅ 헤모글로빈 정상 기준 값 정의 (일반 기준 적용)
    hemoglobin_ranges = {
        "심각 (낮음)": (0, 7, "red"),
        "경고 (낮음)": (7, 13.5, "orange"),
        "정상": (13.5, 17.5, "green"),
        "경고 (높음)": (17.5, 20, "orange"),
        "심각 (높음)": (20, 25, "red")
    }


    # ✅ 환자의 헤모글로빈 수치 가져오기
    patient_hemoglobin = patient_data['hemoglobin'].iloc[0]

    # 📊 **헤모글로빈 수치 그래프**
    fig_hb = go.Figure()

    for category, (hb_min, hb_max, color) in hemoglobin_ranges.items():
        fig_hb.add_trace(go.Scatter(
            x=[hb_min, hb_max], y=[1, 1], 
            fill='toself', mode='lines',
            line=dict(color=color, width=4),
            name=f"{category} ({hb_min} ~ {hb_max} g/dL)"
        ))

    fig_hb.add_trace(go.Scatter(
        x=[patient_hemoglobin], y=[1.1], 
        mode="markers+text",
        marker=dict(color="red", size=12, symbol="arrow-bar-up"),
        text=[f"🔴 {patient_hemoglobin:.1f} g/dL"],
        textposition="top center",
        name="환자 헤모글로빈"
    ))

    fig_hb.update_layout(
        title="📊 헤모글로빈 정상 범위 및 환자 수치",
        xaxis=dict(title="헤모글로빈 (g/dL)", range=[5, 25]),
        yaxis=dict(showticklabels=False),  
        showlegend=True
    )

    st.plotly_chart(fig_hb)

    # ✅ 건강 상태 문구 추가
    status_message = "✅ 정상 범위 내에 있습니다. 건강을 유지하세요!"
    for category, (hb_min, hb_max, _) in hemoglobin_ranges.items():
        if hb_min <= patient_hemoglobin < hb_max:
            if "경고" in category:
                status_message = "⚠️ 헤모글로빈 수치가 경계선에 있습니다. 주의가 필요합니다."
                st.warning(status_message)
            elif "심각" in category:
                status_message = "🚨 헤모글로빈 수치가 위험 수준입니다. 즉시 의료진과 상담하세요!"
                st.error(status_message)
            else:
                st.success(status_message)
            break

if __name__ == "__main__":
    main()
