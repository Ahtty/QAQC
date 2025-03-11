import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def main():
    st.title("🩺 BMI 상세 정보")

    # ✅ `session_state`에서 데이터 불러오기
    if "patient_data" not in st.session_state:
        st.warning("⚠️ 먼저 메인 페이지에서 건강 정보를 입력하세요.")
        st.stop()  # 데이터가 없으면 실행 중지

    patient_data = pd.DataFrame([{k: float(v) if isinstance(v, (int, float)) else v for k, v in st.session_state["patient_data"].items()}])
    # BMI 컬럼 생성
    patient_data['BMI'] = patient_data['weight(kg)']/((patient_data['height(cm)']/100)**2)

    # ✅ BMI 기준 값 정의
    bmi_categories = {
        "저체중": (0, 18.5, "blue"),
        "정상": (18.5, 24.9, "green"),
        "과체중": (25, 29.9, "yellow"),
        "비만": (30, 34.9, "orange"),
        "고도비만": (35, 50, "red")
    }

    # ✅ 허리둘레 기준 값 정의 (남성/여성 구분)
    waist_categories = {
        "정상": (0, 90, "green"),
        "주의 단계": (90, 100, "yellow"),
        "비만 위험": (100, 110, "orange"),
        "고도비만 위험": (110, 200, "red")
    }

    # ✅ 환자의 BMI & 허리둘레 값 가져오기
    patient_bmi = patient_data['BMI'].iloc[0]
    patient_waist = patient_data['waist(cm)'].iloc[0]

    # 📊 **BMI 카테고리 그래프**
    fig_bmi = go.Figure()

    for category, (bmi_min, bmi_max, color) in bmi_categories.items():
        fig_bmi.add_trace(go.Scatter(
            x=[bmi_min, bmi_max], y=[1, 1], 
            fill='toself', mode='lines',
            line=dict(color=color, width=4),
            name=f"{category} ({bmi_min} ~ {bmi_max})"
        ))

    fig_bmi.add_trace(go.Scatter(
        x=[patient_bmi], y=[1.1], 
        mode="markers+text",
        marker=dict(color="red", size=12, symbol="arrow-bar-up"),
        text=[f"🔴 {patient_bmi:.1f}"],
        textposition="top center",
        name="환자 BMI"
    ))

    fig_bmi.update_layout(
        title="📊 BMI 정상 범위 및 환자 BMI 위치",
        xaxis=dict(title="BMI 값", range=[10, 40]),
        yaxis=dict(showticklabels=False),  
        showlegend=True
    )

    st.plotly_chart(fig_bmi)

    # 📊 **허리둘레 그래프**
    fig_waist = go.Figure()

    for category, (waist_min, waist_max, color) in waist_categories.items():
        fig_waist.add_trace(go.Scatter(
            x=[waist_min, waist_max], y=[1, 1], 
            fill='toself', mode='lines',
            line=dict(color=color, width=4),
            name=f"{category} ({waist_min} ~ {waist_max} cm)"
        ))

    fig_waist.add_trace(go.Scatter(
        x=[patient_waist], y=[1.1], 
        mode="markers+text",
        marker=dict(color="red", size=12, symbol="arrow-bar-up"),
        text=[f"🔴 {patient_waist:.1f} cm"],
        textposition="top center",
        name="환자 허리둘레"
    ))

    fig_waist.update_layout(
        title="📊 허리둘레 정상 범위 및 환자 허리둘레 위치",
        xaxis=dict(title="허리둘레 (cm)", range=[60, 140]),
        yaxis=dict(showticklabels=False),  
        showlegend=True
    )

    st.plotly_chart(fig_waist)

    # ✅ 건강 경고 문구 추가
    for category, (bmi_min, bmi_max, _) in bmi_categories.items():
        if bmi_min <= patient_bmi < bmi_max:
            st.write(f"### ✅ 현재 상태: **{category}** (BMI {bmi_min} ~ {bmi_max})")
            if category == "저체중":
                st.warning("⚠️ 저체중입니다. 영양 섭취를 늘리는 것이 좋습니다.")
            elif category == "과체중":
                st.warning("⚠️ 과체중입니다. 운동과 식단 조절을 고려하세요.")
            elif category == "비만" or category == "고도비만":
                st.warning("⚠️ 비만 단계입니다. 건강 관리를 위해 전문가와 상담하세요.")
            else:
                st.success("✅ 정상 범위에 있습니다. 건강을 유지하세요!")
            break  

    # ✅ 허리둘레 건강 문구 추가
    for category, (waist_min, waist_max, _) in waist_categories.items():
        if waist_min <= patient_waist < waist_max:
            st.write(f"### ✅ 허리둘레 상태: **{category}** ({waist_min} ~ {waist_max} cm)")
            if category == "주의 단계":
                st.warning("⚠️ 허리둘레가 증가하고 있습니다. 건강한 생활습관을 유지하세요.")
            elif category == "비만 위험":
                st.warning("⚠️ 비만 위험이 있습니다. 적극적인 운동과 식단 조절이 필요합니다.")
            elif category == "고도비만 위험":
                st.warning("⚠️ 고도비만 위험이 높습니다. 즉시 건강 관리를 시작하세요.")
            else:
                st.success("✅ 정상 범위에 있습니다. 건강을 유지하세요!")
            break  

if __name__ == "__main__":
    main()
