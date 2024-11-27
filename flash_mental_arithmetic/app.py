from fractions import Fraction
import requests
import streamlit as st
import time
# from PIL import Image


if 'flash_questions' not in st.session_state:
    st.session_state.flash_questions = []
if 'answers' not in st.session_state:
    st.session_state.flash_answer = []
if 'flash_show_answer' not in st.session_state:
    st.session_state.show_flash_answer = False

st.title('フラッシュ暗算')
st.write('')

st.sidebar.write("注意：半角小文字の数字を入力してください。")
a = st.sidebar.text_input("問題数", value='5')
b = st.sidebar.text_input("桁数", value='2')


# フラッシュ暗算
if st.sidebar.button("フラッシュ暗算"):
    try:
        num_questions = int(a)
        num_digits = int(b)
    except ValueError:
        st.sidebar.error("問題数と桁数には整数を入力してください。")
    else:
        st.session_state.flash_questions = []
        st.session_state.start = ""
        st.session_state.flash_show_answer = False

    url = 'http://127.0.0.1:8000/page_add'
    response = requests.post(url, json={"num_times": num_questions, "num_range": num_digits})
    if response.status_code == 200:
        data = response.json()
        question_list = data["question_list"]
        answer = int(data["answer"])
        st.session_state.flash_questions = question_list
        st.session_state.flash_answer = answer
        screen = st.empty()
        for i in range(int(a)):
            if i == 0:
                screen.markdown("<center>"'<p style="font-size: 50px;">START!</p>'"</center>", unsafe_allow_html=True)
                time.sleep(1.5)
                screen.markdown(" ")
                time.sleep(0.5)
                screen.markdown("<center>"f'<p style="font-size: 50px;">{question_list[i]}</p>'"</center>", unsafe_allow_html=True)
                time.sleep(1.5)
                screen.markdown(" ")
                time.sleep(0.5)
            elif i == int(a) - 1:
                screen.markdown("<center>"f'<p style="font-size: 50px;">{question_list[i]}</p>'"</center>", unsafe_allow_html=True)
                time.sleep(1.5)
                screen.markdown(" ")
                time.sleep(0.5)
                screen.markdown("<center>"'<p style="font-size: 60px;">finish!</p>'"</center>", unsafe_allow_html=True)
            else:
                screen.markdown("<center>"f'<p style="font-size: 60px;">{question_list[i]}</p>'"</center>", unsafe_allow_html=True)
                time.sleep(1.5)
                screen.markdown(" ")
                time.sleep(0.5)
    else:
        st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
        st.json(response.json())


# フラッシュ暗算の出力
if st.session_state.flash_questions:
    answer = st.text_input("回答", value='0')
    if st.button('正解表示'):
        st.session_state.show_flash_answer = True
        if st.session_state.show_flash_answer:
            st.write(f'<p style="font-size: 20px;">{st.session_state.flash_answer}</p>', unsafe_allow_html=True)
            if st.session_state.flash_answer == int(answer):
                st.write("○")
            else:
                st.write("×")
