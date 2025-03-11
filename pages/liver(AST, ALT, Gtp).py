import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.title("🩺 간 수치(AST, ALT, Gtp) 상세 정보")


    # ✅ `session_state`에서 데이터 불러오기
    if "patient_data" not in st.session_state:
        st.warning("⚠️ 먼저 메인 페이지에서 건강 정보를 입력하세요.")
        st.stop()  # 데이터가 없으면 실행 중지

    patient_data = pd.DataFrame([{k: float(v) if isinstance(v, (int, float)) else v for k, v in st.session_state["patient_data"].items()}])


    ast = patient_data['AST'].iloc[0]
    alt = patient_data['ALT'].iloc[0]
    gtp = patient_data['Gtp'].iloc[0]
    fig = px.bar(
        x=["AST", "ALT", "r-Gtp"],
        y=[ast, alt, gtp],
        text=[ast, alt, gtp],
        title="간수치 비교 (IU/L)")
    fig.add_hline(y=40, line_dash="dash", line_color="red", annotation_text="정상 AST/ALT 수치")
    fig.add_hline(y=71, line_dash="dash", line_color="blue", annotation_text="정상 r-Gtp 상한")
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig)
    
    if ast > 40 or alt > 40:
        st.warning("⚠️ 이 환자는 급성간염, 심근경색, 근질환, 악성종양, 폐쇄황달, 알코올간염 등의 위험이 있습니다.")
    if gtp > 71:
        st.warning("⚠️ 이 환자는 만성간염 활동형, 간경변 활동형, 폐쇄황달, 알코올성 간장애, 요독증 등의 위험이 있습니다.")
    else:
        st.success("✅ 간 수치가 정상 범위에 있습니다. 건강을 유지하세요!")

if __name__ == "__main__":
    main()
