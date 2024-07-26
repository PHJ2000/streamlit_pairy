import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# 데이터 로드
path = 'C:/Users/USER/Desktop/project/parini/visa_data.csv'

data = pd.read_csv(path)

# 필요한 컬럼 선택 및 전처리
data = data[['SOC_NAME', 'CASE_STATUS']].dropna()

# CASE_STATUS를 이진 변수로 변환
data['CASE_STATUS'] = data['CASE_STATUS'].apply(lambda x: 1 if x == 'CERTIFIED' else 0)

# 특징과 타겟 변수 분리
X = data[['SOC_NAME']]
y = data['CASE_STATUS']

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 원-핫 인코더 설정
encoder = OneHotEncoder()

# 로지스틱 회귀 모델 설정
model = LogisticRegression()

# 전처리와 모델을 포함한 파이프라인 설정
pipeline = Pipeline([
    ('encoder', encoder),
    ('model', model)
])

# 모델 학습
pipeline.fit(X_train, y_train)

# 모델 저장
joblib.dump(pipeline, 'visa_predictor.pkl')


import streamlit as st
import joblib

# SOC_NAME 리스트 추출
soc_names = data['SOC_NAME'].unique()

# 저장된 모델 로드
pipeline = joblib.load('visa_predictor.pkl')

# 비자 발급 예측 함수
def analyze_job(soc_name):
    # 입력 데이터를 변환 및 예측 수행
    prediction = pipeline.predict([[soc_name]])
    return 'CERTIFIED' if prediction[0] == 1 else 'DENIED'

# Streamlit UI 구성
st.title('비자 발급 여부 예측')
st.write('직업을 입력하여 H1B의 발급 여부를 알 수 있는 프로그램입니다.')

# 사용자로부터 키워드 입력 받기
keyword = st.text_input('직업 키워드를 입력해주세요:')

# 키워드에 따른 SOC_NAME 필터링
filtered_soc_names = [name for name in soc_names if keyword.lower() in name.lower()]

# 필터링된 SOC_NAME을 드롭다운 메뉴로 제공
soc_name_input = st.selectbox('해당하는 직업을 선택해 주세요:', filtered_soc_names)

# 사용자가 SOC_NAME을 선택하면 예측 결과 출력
if soc_name_input:
    result = analyze_job(soc_name_input)
    st.write(f'예측된 비자 발급 결과입니다: {result}')