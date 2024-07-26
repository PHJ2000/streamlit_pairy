import streamlit as st
import pandas as pd

# 예시 데이터프레임 생성
data = {
    "직업군": ["Data Scientist", "Data Engineer", "Machine Learning Engineer", "Data Analyst"],
    "평균연봉": [120000, 110000, 130000, 90000],
    "국가": ["USA", "Canada", "Europe", "Others"],
    "경력 수준": ["엔트리급", "중급", "시니어급", "고위급"]
}

df = pd.DataFrame(data)


# 첫 번째 화면: '연봉 데이터 제공' 탭
if 'page' not in st.session_state:
    st.session_state.page = 0

def next_page():
    st.session_state.page += 1

if st.session_state.page == 0:
    st.title("AI/ML 연봉 데이터")
    if st.button('연봉 데이터 제공'):
        next_page()

# 두 번째 화면: 직업 선택 후 정보 제공
if st.session_state.page == 1:
    st.title("연봉 데이터 제공")
    st.write("원하는 직업군을 선택하세요.")
    job_selected = st.selectbox("직업 선택", df["직업군"])

    # 선택된 직업에 대한 데이터 필터링
    job_data = df[df["직업군"] == job_selected]

    # 데이터 출력
    st.write("### 선택한 직업에 대한 정보")
    st.write(job_data)
