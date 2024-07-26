import streamlit as st
import pandas as pd
# import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import urllib.request
import json
import ssl
import os

# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')


# Streamlit 앱 내용
st.title('한글 테스트')
st.write('이 문장은 한글로 작성되었습니다.')

# 데이터 로드
salary_data_path = 'p_salary_data_total.csv'
salary_data_total_path = 'salary_data_total.csv'
 
salary_data = pd.read_csv(salary_data_path)
salary_data_total = pd.read_csv(salary_data_total_path)
 
# 경험 수준 한글 변환
experience_level_map = {
    'EN': '엔트리급',
    'MI': '중급',
    'SE': '시니어급',
    'EX': '고위급'
}
 
salary_data['experience_level'] = salary_data['experience_level'].map(experience_level_map)
salary_data_total['experience_level'] = salary_data_total['experience_level'].map(experience_level_map)
 
# 데이터프레임 생성
df = pd.concat([salary_data[['work_year', 'job_title', 'salary_in_usd', 'experience_level']], 
                salary_data_total[['work_year', 'job_title', 'salary_in_usd', 'experience_level']]])
df_grouped = df.groupby(['job_title', 'experience_level']).agg({'salary_in_usd': 'mean'}).reset_index()
df_grouped.columns = ['직업군', '경력 수준', '평균연봉']
 
# 평균연봉을 정수로 변환
df_grouped['평균연봉'] = df_grouped['평균연봉'].round().astype(int)
 
# 국가 데이터 추가
df_grouped['국가'] = 'USA'
 
# 비자 데이터 로드
visa_data_path = 'visa_data.csv'
 
# 앱의 제목 만들기
st.title(':rainbow[파린이 유랑단]:heart_eyes:')

# Function to get prevailing wage based on SOC title
def get_prevailing_wage(soc_title):
    if soc_title in salary_data['job_title'].values:
        return int(salary_data[salary_data['job_title'] == soc_title]['salary'].mean())
    else:
        return 50000  # Default value if SOC title is not found
    
def get_wage_range(soc_title):
    if soc_title in salary_data['job_title'].values:
        min_wage = int(salary_data[salary_data['job_title'] == soc_title]['salary'].min())
        max_wage = int(salary_data[salary_data['job_title'] == soc_title]['salary'].max())
        return min_wage, max_wage
    else:
        return 0, 300000  # Default range if SOC title is not found

# 세션 상태를 사용하여 상태 관리
if 'page' not in st.session_state:
    st.session_state.page = 'main'
 
# 페이지 전환 함수
def go_to_page(page):
    st.session_state.page = page
 
# 메인 페이지
if st.session_state.page == 'main':
    st.markdown("""
<div style="font-size:30px;"><직업별 연봉 예측 및 비자 발급 여부 예측></div>
<br>
<div style="font-size:20px;">직업을 선택하면 대략적인 연봉을 예측하는 프로그램입니다.</div>
                """, unsafe_allow_html=True)
    if st.button('직업 정보 제공'):
        go_to_page('page1')
    st.markdown('<div style="font-size:20px;">직업을 선택하면 대략적인 비자 발급 여부를 예측하는 프로그램입니다.</div>', unsafe_allow_html=True)
    if st.button('비자 정보 예측'):
        go_to_page('page2')

    st.image('newplot.png')
    st.image('0.png')
    st.image('00.png')
    st.image('1.png')
    st.image('2.png')
    st.image('3.png')
    st.image('4.png')
    st.image('5.png')
    st.image('6.png')
    st.image('7.png')
 
# 페이지 1
elif st.session_state.page == 'page1':
    st.title("AI/ML 연봉 데이터 제공")
    st.write("###### 원하는 직업군을 최대 5개까지 선택하세요.")
    job_selected = st.multiselect("직업 선택", df_grouped["직업군"].unique(), default=df_grouped["직업군"].unique()[:5])
    experience_selected = st.selectbox("경력 수준 선택", ['엔트리급', '중급', '시니어급', '고위급'])
    # 선택된 직업과 경력 수준에 대한 데이터 필터링
    job_data = df_grouped[(df_grouped["직업군"].isin(job_selected)) & (df_grouped["경력 수준"] == experience_selected)]
 
    # 데이터 출력
    st.write("### 선택한 직업에 대한 정보")
    st.write(job_data)
 
    # 시각화 1: 연봉 분포
    st.write("### 연봉 분포")
    fig, ax = plt.subplots()
    for job in job_selected:
        ax.hist(df[df["job_title"] == job]["salary_in_usd"], bins=20, alpha=0.5, label=job)
    ax.set_title("연봉 분포")
    ax.set_xlabel("연봉")
    ax.set_ylabel("빈도")
    ax.legend()
    st.pyplot(fig)
 
    # 시각화 2: 경력 수준별 평균 연봉
    st.write("### 경력 수준별 평균 연봉")
    fig, ax = plt.subplots()
    for job in job_selected:
        experience_data = df_grouped[(df_grouped["직업군"] == job)].sort_values(by="경력 수준")
        ax.bar(experience_data["경력 수준"], experience_data["평균연봉"], alpha=0.5, label=job)
    ax.set_title("경력 수준별 평균 연봉")
    ax.set_xlabel("경력 수준")
    ax.set_ylabel("평균 연봉")
    ax.legend()
    st.pyplot(fig)
 
    # 시각화 3: 연도별 평균 연봉 변화
    st.write("### 연도별 평균 연봉 변화")
    fig, ax = plt.subplots()
    for job in job_selected:
        yearly_data = df[df["job_title"] == job].groupby('work_year').agg({'salary_in_usd': 'mean'}).reset_index()
        ax.plot(yearly_data['work_year'], yearly_data['salary_in_usd'], marker='o', linestyle='-', label=job)
    ax.set_title("연도별 평균 연봉 변화")
    ax.set_xlabel("연도")
    ax.set_ylabel("평균 연봉")
    ax.legend()
    st.pyplot(fig)
 
    if st.button('뒤로'):
        go_to_page('main')
 
# 페이지 2
elif st.session_state.page == 'page2':
    import urllib.request
    import json
    import ssl
    import os
 
    def allowSelfSignedHttps(allowed):
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context
 
    allowSelfSignedHttps(True)
 
    # Streamlit 애플리케이션 시작
    st.title("Azure Machine Learning Model Scoring")
 
    # 사용자 입력 받기
    soc_title = st.selectbox("Select SOC Title:", salary_data['job_title'].unique())
    initial_wage = get_prevailing_wage(soc_title)
    min_wage, max_wage = get_wage_range(soc_title)
    prevailing_wage = st.slider("Enter Prevailing Wage:", min_value=min_wage, max_value=max_wage, value=initial_wage, step=1000)
    
    # 버튼 클릭시 API 호출
    if st.button("Submit"):
        data = {
            "Inputs": {
                "input1": [
                    {
                        "YEAR": 2017,
                        "SOC_Title": soc_title,
                        "PREVAILING_WAGE": prevailing_wage,
                        "CASE_STATUS": True
                    }
                ]
            },
            "GlobalParameters": {}
        }
 
        body = str.encode(json.dumps(data))
 
        url = 'http://0ae0793a-4ce8-471d-a04d-9b5f40fa5be8.koreacentral.azurecontainer.io/score'
        api_key = 'RcUGcMhwTf6HgiafewHBiZMVRvoa3LzS'  # Replace with your API key
 
        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}
 
        req = urllib.request.Request(url, body, headers)
 
        try:
            response = urllib.request.urlopen(req)
            result = response.read().decode("utf8")
            result_json = json.loads(result)
 
            # 예측 결과 출력
            scored_labels = result_json.get("Results", {}).get("WebServiceOutput0", [{}])[0].get("Scored Labels", "N/A")
            scored_probabilities = result_json.get("Results", {}).get("WebServiceOutput0", [{}])[0].get("Scored Probabilities", "N/A")
 
            st.success(f"CASE_STATUS: {scored_labels}")
            st.success(f"CASE_STATUS Probabilities: {scored_probabilities}")
        except urllib.error.HTTPError as error:
            st.error("The request failed with status code: " + str(error.code))
            st.error(error.read().decode("utf8", 'ignore'))
 
    if st.button('뒤로'):
        go_to_page('main')
