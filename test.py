import streamlit as st

st.sidebar.header('로그인') 

user_id = st.sidebar.text_input('아이디 입력',value='streamlit',max_chars=15) 

user_password = st.sidebar.text_input('패스워드 입력', value='',type='password') 


st.subheader('환영합니다')


새로 고쳤음
또 고침
