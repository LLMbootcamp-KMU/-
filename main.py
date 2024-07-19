import streamlit as st
import json
import requests

# Streamlit 애플리케이션 제목 설정
st.set_page_config(page_title="사용자 정보 입력", layout="centered")
st.title("사용자 정보 입력")

# CSS 스타일 적용
st.markdown(
    """
    <style>
    .stApp {
        background-color:  #faf9f2; /* 더욱 연한 베이지 색 */
        padding: 20px;
        border-radius: 14px;
    }
    .stTextInput, .stNumberInput, .stTextArea, .stCheckbox {
        background-color: #ffffff;  /* 극히 연한 베이지 색 */
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }
    .stJson {
        background-color: #faf5e6;  /* 더욱 연한 베이지 색 */
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# PC 존재여부 입력
col1, col2 = st.columns(2)

with col1:
    has_pc = st.checkbox("PC 존재여부")

with col2:
    has_kitchen = st.checkbox("취사시설 존재여부")

# 위치 입력
location = st.text_input("숙박업소 위치(시)를 입력하세요", placeholder="ex)속초시")

# 객실 크기 입력
room_size = st.text_input("객실 크기를 입력하세요")

# 기준 인원 입력
capacity = st.number_input("기준 인원을 입력하세요", min_value=1, step=1)

# 추가 요구사항 입력 (한 줄 입력)
requirements = st.text_input(
    "추가 요구사항을 입력하세요", placeholder="ex) 오션뷰의 인테리어가 예쁜 가족여행지"
)

# JSON 데이터 생성
data = {
    "pc": "o" if has_pc else "x",
    "취사여부": "o" if has_kitchen else "x",
    "객실크기": room_size,
    "인원": capacity,
    "위치": location,
    "사용자입력": requirements,
}

# 위치 데이터만 JSON 형식으로 저장
data2 = json.dumps({"위치": location}, ensure_ascii=False)

# JSON 형식으로 출력
st.subheader("입력한 정보 (JSON 형식):")
st.json(data)

st.subheader("위치 정보 (JSON 형식):")
st.json(json.loads(data2))

# Flask 서버로 데이터 전송
if st.button("데이터 전송"):
    response = requests.post(
        "http://127.0.0.1:5000/search_accommodation", json=json.loads(data2)
    )
    if response.status_code == 200:
        st.success(f"서버 응답: {response.json()}")
    elif response.status_code == 404:
        st.warning(f"서버 응답: {response.json().get('message')}")
    else:
        st.error("서버와의 통신에 실패했습니다.")

# Streamlit 애플리케이션 실행
if __name__ == "__main__":
    st.set_option("deprecation.showfileUploaderEncoding", False)
