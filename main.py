import importlib
import pickle
import joblib
from sklearn.utils import resample
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import RandomizedSearchCV
from catboost import CatBoostClassifier
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# `st.set_page_config()` 실행
st.set_page_config(
    page_title="건강 데이터분석 대시보드", 
    page_icon="🏠", 
    layout="wide",
    menu_items={"About": None}  # 기본 메뉴 비활성화
)
# 사이드바 상단의 기본 네비게이션 메뉴 숨기기 (CSS 활용)
hide_menu_style = """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title('🚭환자 금연 확률 예측 모델')

# 사용자가 입력할 수 있는 양식 만들기
st.sidebar.title("환자 정보를 입력해주세요.")
age = st.sidebar.number_input('나이', value=25)
height = st.sidebar.number_input('키(cm)', value=172)
weight = st.sidebar.number_input('몸무게(kg)', value=76)
waist = st.sidebar.number_input('허리 둘레(cm)', value=84.0)
eyesight_left = st.sidebar.number_input('시력(왼쪽)', value=1.0)
eyesight_right = st.sidebar.number_input('시력(오른쪽)', value=1.1)
hearing_left = st.sidebar.number_input('청력(왼쪽)', value=1)
hearing_right = st.sidebar.number_input('청력(오른쪽)', value=1)
systolic = st.sidebar.number_input('혈압(수축기)', value=114)
relaxation = st.sidebar.number_input('혈압(이완기)', value=68)
fastingBloodSugar = st.sidebar.number_input('공복혈당', value=86)
cholesterol = st.sidebar.number_input('콜레스테롤', value=230)
triglyceride = st.sidebar.number_input('중성지방', value=71)
HDL = st.sidebar.number_input('HDL', value=72)
LDL = st.sidebar.number_input('LDL', value=144)
hemoglobin = st.sidebar.number_input('헤모글로빈', value=12)
urineProtein = st.sidebar.number_input('요단백', value=1)
serumCreatinine = st.sidebar.number_input('혈청 크레아티닌', value=0.6)
AST = st.sidebar.number_input('AST', value=26)
ALT = st.sidebar.number_input('ALT', value=11)
Gtp = st.sidebar.number_input('Gtp', value=12)
dentalCaries = st.sidebar.number_input('충치 유무', value=1)


# ✅ "Submit" 버튼을 눌렀을 때 session_state에 값 저장
if st.button("🔍 건강 분석 실행"):
    st.session_state["patient_data"] = {
        "age": age,
        "height(cm)": height,
        "weight(kg)": weight,
        "waist(cm)": waist,
        "eyesight(left)": eyesight_left,
        "eyesight(right)": eyesight_right,
        "hearing(left)": hearing_left, 
        "hearing(right)": hearing_right, 
        "systolic": systolic,
        "relaxation": relaxation, 
        "fasting blood sugar": fastingBloodSugar, 
        "Cholesterol": cholesterol, 
        "triglyceride": triglyceride,
        "HDL": HDL, 
        "LDL": LDL, 
        "hemoglobin": hemoglobin, 
        "Urine protein": urineProtein, 
        "serum creatinine": serumCreatinine, 
        "AST": AST,
        "ALT": ALT, 
        "Gtp": Gtp, 
        "dental caries": dentalCaries
    }
    patient_data = pd.DataFrame([{k: float(v) if isinstance(v, (int, float)) else v for k, v in st.session_state["patient_data"].items()}])
    st.dataframe(patient_data)
    # Feature Engineering
    def feature_engineering(df):
        df['waist_height_ratio'] = df['waist(cm)'] / df['height(cm)']
        df['alt_ast_ratio'] = df['ALT'] / (df['AST'] + 0.001)
        bins = [0, 18.5, 24.9, 29.9, np.inf]
        labels = ['Underweight', 'Normal', 'Overweight', 'Obesity']
        df['BMI_category'] = pd.cut(df['BMI'], bins=bins, labels=labels)
        df = pd.get_dummies(df, columns=['BMI_category'], drop_first=True)
        return df

    # 필요 컬럼 생성
    patient_data['BMI'] = patient_data['weight(kg)']/((patient_data['height(cm)']/100)**2)
    patient_data['triglyceride/HDL'] = patient_data['triglyceride']/patient_data['HDL']
    patient_data['LDL/HDL'] = patient_data['LDL']/patient_data['HDL']
    patient_data['BP Ratio'] = patient_data['systolic']/patient_data['relaxation']
    patient_data = feature_engineering(patient_data)

    st.subheader('예측 결과 확인')

    # 저장된 모델 불러오기 (CatBoost)
    with open('files/catboost_model(final).pkl', 'rb') as f:
        model = pickle.load(f)
    # 사용자가 입력한 값으로 예측
    prediction = model.predict(patient_data)
    # 금연 가능성 확률 추가 (0일 확률)
    prob = model.predict_proba(patient_data)
    patient_data['smoking_prob_0'] = prob[:, 0]

    # 결과 출력
    st.write(f"📌 CatBoost 모델 예측 결과: {prediction}")
    st.write(f"📌 금연 가능성: {patient_data['smoking_prob_0'].iloc[0]*100:.2f} %")
    st.success("✅ 환자 정보가 저장되었습니다! 사이드바에서 '건강 분석' 페이지로 이동하세요.")

    # 금연 확률에 따른 치료 방법 추천
    def recommend_treatment(probability):
        if probability >= 90:
            return (
                "### 🟢 매우 강한 의지 (90~100%)\n"
                "<small>- ✅ **추천 치료 방법**: 행동 요법, 금연 앱 활용</small><br>\n"
                "<small>- 📌 **금연 상담(1:1 또는 그룹)**을 받고, 금연 앱(Smoke Free, QuitNow!)을 활용하세요.</small><br>\n"
                "<small>- 🚭 흡연 유발 환경을 피하고, 자기 동기 강화 기법을 사용하세요.</small>"
            )
        elif probability >= 70:
            return (
                "### 🟡 강한 의지 (70~89%)\n"
                "<small>- ✅ **추천 치료 방법**: 행동 요법 + 니코틴 대체 요법(NRT)</small><br>\n"
                "<small>- 📌 니코틴 패치, 껌, 사탕을 사용하고 금연 상담을 병행하면 효과가 증가합니다.</small><br>\n"
                "<small>- 🚭 스트레스 대처법을 학습하고, 금연 보상 시스템을 활용하세요.</small>"
            )
        elif probability >= 50:
            return (
                "### 🟠 보통 의지 (50~69%)\n"
                "<small>- ✅ **추천 치료 방법**: 니코틴 대체 요법(NRT) + 행동 요법 + 금연 상담</small><br>\n"
                "<small>- 📌 니코틴 패치와 껌을 병행하며, 금연 상담을 통해 동기 부여를 강화하세요.</small><br>\n"
                "<small>- 🚭 필요 시 부프로피온(웰부트린) 같은 약물을 고려할 수 있습니다.</small>"
            )
        elif probability >= 30:
            return (
                "### 🔴 약한 의지 (30~49%)\n"
                "<small>- ✅ **추천 치료 방법**: 처방 약물(바레니클린, 부프로피온) + 행동 요법</small><br>\n"
                "<small>- 📌 바레니클린(챔픽스), 부프로피온(웰부트린) 같은 약물을 복용하며 금연 상담을 받으세요.</small><br>\n"
                "<small>- 🚭 니코틴 패치와 껌을 병행하면 효과가 더욱 증가합니다.</small>"
            )
        else:
            return (
                "### ⚫ 매우 약한 의지 (0~29%)\n"
                "<small>- ✅ **추천 치료 방법**: 처방 약물(바레니클린 + 부프로피온 병합 요법) + 전문 상담</small><br>\n"
                "<small>- 📌 강력한 약물 요법이 필요하며, 병합 치료를 고려하세요.</small><br>\n"
                "<small>- 🚭 금연 클리닉에 등록하고, 집중적인 관리 프로그램에 참여하세요.</small>"
            )    
    st.subheader("🚭 금연 치료 방법 추천")
    st.markdown(recommend_treatment(patient_data['smoking_prob_0'].iloc[0]*100))



# 사이드바에서 페이지 선택
st.sidebar.title("건강 분석")
pages = {
    "BMI": "bmi",
    "Hemoglobin": "hemoglobin",
    "Serum Creatinine, Urine protein, Fasting blood sugar":"serum creatinine_urine protein",
    "Blood Pressure": "blood_pressure",
    "Liver(AST,ALT,Gtp)": "liver(AST, ALT, Gtp)",
    "Cholesterol": "cholesterol etc"

}

selected_page = st.sidebar.radio("이동할 페이지 선택", list(pages.keys()))

# 선택된 페이지 불러오기
module_name = f"pages.{pages[selected_page]}"
try:
    module = importlib.import_module(module_name)
    if hasattr(module, "main"):  # main 함수가 존재하면 실행
        module.main()
    else:
        st.warning(f"⚠️ {module_name} 모듈에 'main' 함수가 없습니다.")
except Exception as e:
    st.error(f"🚨 페이지 로드 중 오류 발생: {e}")


