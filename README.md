# Streamlit Pairy

## 프로젝트 개요
**Streamlit Pairy**는 Streamlit을 활용한 급여 데이터 분석 및 예측 웹 애플리케이션입니다. 이 프로젝트는 사용자가 급여 데이터를 시각화하고 분석할 수 있도록 지원하며, 머신러닝 모델을 활용하여 급여 예측을 수행할 수 있도록 설계되었습니다.

## 주요 기능
- **데이터 시각화**: 급여 데이터의 다양한 요소를 그래프 및 표 형태로 시각화
- **머신러닝 기반 급여 예측**: Logistic Regression을 활용하여 급여 수준을 예측
- **사용자 친화적인 대시보드**: Streamlit을 사용하여 직관적인 UI 제공
- **경험 수준 변환**: 급여 데이터의 경험 수준을 한글로 변환하여 가독성 향상
- **한글 폰트 지원**: `malgun.ttf` 폰트를 적용하여 한글이 깨지지 않도록 처리

## 프로젝트 구조
```
streamlit_pairy/
│── Salary_info.py  # 급여 데이터 분석 관련 코드
│── end_point_to_streamlit.py  # API 연동 관련 코드
│── finall.py  # 메인 Streamlit 실행 파일
│── job_visa.py  # 비자 및 직업 관련 분석
│── streamlit.py  # Streamlit 기반 웹 애플리케이션 실행 코드
│── test.py  # 테스트 코드
│── p_salary_data_total.csv  # 급여 데이터 파일
│── salary_data_total.csv  # 전체 급여 데이터 파일
│── requirements.txt  # 필요 라이브러리 목록
│── README.md  # 프로젝트 설명 파일
└── malgun.ttf  # 한글 폰트 파일
```

## 실행 방법
1. 필수 라이브러리 설치:
   ```bash
   pip install -r requirements.txt
   ```
2. Streamlit 애플리케이션 실행:
   ```bash
   streamlit run streamlit.py
   ```

## 필요 라이브러리
본 프로젝트는 다음과 같은 Python 라이브러리를 사용합니다:
- `streamlit`
- `pandas`
- `matplotlib`
- `scikit-learn`

## 데이터 설명
프로젝트는 `p_salary_data_total.csv` 및 `salary_data_total.csv` 파일을 활용하여 분석을 수행합니다. 주요 컬럼은 다음과 같습니다:
- **work_year**: 연도
- **job_title**: 직업명
- **salary_in_usd**: 연봉 (USD 기준)
- **experience_level**: 경험 수준 (엔트리급, 중급, 시니어급, 고위급 등)

## 기여 방법
1. 본 레포지토리를 포크합니다.
2. 새로운 브랜치를 생성합니다.
3. 변경 사항을 커밋하고 푸시합니다.
4. Pull Request를 생성하여 기여합니다.

## 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다.

