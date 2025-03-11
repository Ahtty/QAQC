import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def main():
    st.title("🩺 혈청 크레아티닌, 요단백, 혈당 상세 정보")


    # ✅ `session_state`에서 데이터 불러오기
    if "patient_data" not in st.session_state:
        st.warning("⚠️ 먼저 메인 페이지에서 건강 정보를 입력하세요.")
        st.stop()  # 데이터가 없으면 실행 중지

    patient_data = pd.DataFrame([{k: float(v) if isinstance(v, (int, float)) else v for k, v in st.session_state["patient_data"].items()}])

        # ✅ 정상 기준 값 설정
    normal_ranges = {
        "혈청 크레아티닌": (44, 106),
        "요단백": (1, 2),
        "혈당": (0, 126)
    }

    # ✅ 환자 입력값
    patient_values = {
        "혈청 크레아티닌": patient_data["serum creatinine"].iloc[0],
        "요단백": patient_data["Urine protein"].iloc[0],
        "혈당": patient_data["fasting blood sugar"].iloc[0]
    }

    # 📊 **그래프 생성**
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="환자 수치",
        x=list(patient_values.keys()),
        y=list(patient_values.values()),
        marker_color="red"
    ))

    fig.add_trace(go.Bar(
        name="정상 기준 (최고치)",
        x=list(normal_ranges.keys()),
        y=[normal_ranges[key][1] for key in normal_ranges],
        marker_color="green",
        opacity=0.6
    ))

    fig.update_layout(
        title="📊 환자 수치 vs 정상 기준",
        yaxis=dict(title="수치"),
        barmode="group"
    )

    st.plotly_chart(fig)

    # 🚨 **건강 안내 메시지 출력**
    warnings = []

    if patient_data["serum creatinine"] < 44:
        warnings.append("🚨 혈청 크레아티닌이 너무 낮습니다. 근육량 감소 또는 신장 문제 가능성이 있습니다.")
    elif patient_data["serum creatinine"] > 106:
        warnings.append("🚨 혈청 크레아티닌이 정상 범위를 초과했습니다. 신장 기능 검사가 필요할 수 있습니다.")

    if patient_data["Urine protein"] not in [1, 2]:
        warnings.append("🚨 요단백 수치가 비정상적입니다. 단백뇨 또는 신장 질환 가능성이 있습니다.")

    if patient_data["fasting blood sugar"] > 126:
        warnings.append("🚨 공복 혈당이 높습니다. 당뇨 가능성을 고려해 보세요.")

    if warnings:
        for warning in warnings:
            st.error(warning)
    else:
        st.success("✅ 모든 수치가 정상 범위 내에 있습니다! 건강을 유지하세요.")


if __name__ == "__main__":
    main()




