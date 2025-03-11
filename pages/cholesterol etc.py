import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def main():
    st.title("🩺 콜레스테롤 상세 정보")

     # ✅ `session_state`에서 데이터 불러오기
    if "patient_data" not in st.session_state:
        st.warning("⚠️ 먼저 메인 페이지에서 건강 정보를 입력하세요.")
        st.stop()  # 데이터가 없으면 실행 중지

    patient_data = pd.DataFrame([{k: float(v) if isinstance(v, (int, float)) else v for k, v in st.session_state["patient_data"].items()}])


    # ✅ 콜레스테롤 정상 기준 값 정의
    normal_values = {
        "Cholesterol": 200,
        "LDL": 100,
        "HDL": 60,  # HDL은 높을수록 좋음
        "triglyceride": 150
    }


    # ✅ 환자의 혈액 검사 수치 가져오기
    patient_values = {
        "Cholesterol": patient_data['Cholesterol'].iloc[0],
        "LDL": patient_data['LDL'].iloc[0],
        "HDL": patient_data['HDL'].iloc[0],
        "triglyceride": patient_data['triglyceride'].iloc[0]
    }

    # 📊 **정상 범위 vs 환자 수치 비교 그래프**
    fig = go.Figure()

    # 환자 수치 막대 그래프
    fig.add_trace(go.Bar(
        name='환자 수치',
        x=list(patient_values.keys()),
        y=list(patient_values.values()),
        marker_color='red'
    ))

    # 정상 기준 막대 그래프
    fig.add_trace(go.Bar(
        name='정상 기준',
        x=list(normal_values.keys()),
        y=list(normal_values.values()),
        marker_color='green'
    ))

    fig.update_layout(
        title='📊 환자 혈액 수치 vs 정상 기준',
        yaxis=dict(title="수치"),
        barmode='group'
    )

    st.plotly_chart(fig)

    # ✅ 건강 상태 및 경고 문구 추가
    for category, value in patient_values.items():
        normal_limit = normal_values[category]

        if category == "HDL":  # HDL은 높을수록 좋음
            if value < 40:
                st.error(f"🚨 {category}: {value} (위험 수준) - 낮은 HDL 수치는 심혈관 질환 위험을 증가시킬 수 있습니다.")
            elif value < normal_limit:
                st.warning(f"⚠️ {category}: {value} (경고 수준) - HDL은 좋은 콜레스테롤이며, 높을수록 건강에 좋습니다.")
            else:
                st.success(f"✅ {category}: {value} (정상) - 건강한 수준의 HDL 수치를 유지하고 있습니다.")
        else:  # 나머지는 낮을수록 좋음
            if value >= 240:
                st.error(f"🚨 {category}: {value} (위험 수준) - 심장병, 동맥경화 등의 위험이 높아질 수 있습니다.")
            elif value >= normal_limit:
                st.warning(f"⚠️ {category}: {value} (경고 수준) - 주의가 필요하며, 식이 조절과 운동이 권장됩니다.")
            else:
                st.success(f"✅ {category}: {value} (정상) - 적절한 수치를 유지하고 있습니다.")


if __name__ == "__main__":
    main()
