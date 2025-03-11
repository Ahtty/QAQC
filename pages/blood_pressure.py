import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.title("🩺 혈압 상세 정보")


    # ✅ `session_state`에서 데이터 불러오기
    if "patient_data" not in st.session_state:
        st.warning("⚠️ 먼저 메인 페이지에서 건강 정보를 입력하세요.")
        st.stop()  # 데이터가 없으면 실행 중지

    patient_data = pd.DataFrame([{k: float(v) if isinstance(v, (int, float)) else v for k, v in st.session_state["patient_data"].items()}])

    systolic = patient_data['systolic'].iloc[0]
    relaxation = patient_data['relaxation'].iloc[0]
    metric_value = (systolic, relaxation)
    fig = px.bar(
        x=["수축기", "이완기"],
        y=[metric_value[0], metric_value[1]],
        text=[metric_value[0], metric_value[1]],
        title="혈압 비교 (mmHg)"
    )
    fig.add_hline(y=120, line_dash="dash", line_color="red", annotation_text="정상 수축기 혈압")
    fig.add_hline(y=80, line_dash="dash", line_color="blue", annotation_text="정상 이완기 혈압")
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
