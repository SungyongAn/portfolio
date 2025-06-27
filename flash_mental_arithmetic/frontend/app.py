import time
import requests
import streamlit as st


# from PIL import Image
if "flash_questions" not in st.session_state:
    st.session_state.flash_questions = []
if "flash_answer" not in st.session_state:
    st.session_state.flash_answer = 0
if "flash_show_answer" not in st.session_state:
    st.session_state.show_flash_answer = False

st.title("フラッシュ暗算")
st.write("")

st.sidebar.write("注意：半角小文字の数字を入力してください。")
num_questions_zero = st.sidebar.text_input("問題数", value="5")
num_digits_zero = st.sidebar.text_input("桁数", value="2")


# フラッシュ暗算
if st.sidebar.button("フラッシュ暗算"):
    try:
        num_questions = int(num_questions_zero)
        num_digits = int(num_digits_zero)
    except ValueError:
        st.sidebar.error("問題数と桁数には整数を入力してください。")
    else:
        st.session_state.flash_questions = []
        st.session_state.flash_answer = 0
        st.session_state.show_flash_answer = False # 正解表示をリセット

    url = "http://backend:8000/page_add"
    response = requests.post(url, json={"num_times": num_questions, "num_range": num_digits})

    if response.status_code == 200:
        data = response.json()
        question_list = data["question_list"]
        answer_zero = data["answer"]
        st.session_state.flash_questions = question_list
        st.session_state.flash_answer = answer_zero
    else:
        st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
        st.json(response.json())

    for i in range(int(num_questions_zero)):
        screen = st.empty()
        if i == 0:
            screen.markdown(
            "<center>"'<p style="font-size: 50px;">START!</p></center>',
            unsafe_allow_html=True,
            )
            time.sleep(1.5)
            screen.markdown(" ")
            time.sleep(0.5)
            screen.markdown(
                "<center>"f'<p style="font-size: 50px;">{question_list[i]}</p></center>',
                unsafe_allow_html=True,
                )
            time.sleep(1.5)
            screen.markdown(" ")
            time.sleep(0.5)

        elif 0 < i < int(num_questions_zero) - 1:
            screen.markdown(
                "<center>"f'<p style="font-size: 60px;">{question_list[i]}</p></center>',
                unsafe_allow_html=True,
                )
            time.sleep(1.5)
            screen.markdown(" ")
            time.sleep(0.5)

        else:
            screen.markdown(
                "<center>"f'<p style="font-size: 50px;">{question_list[i]}</p></center>',
                unsafe_allow_html=True,
                )
            time.sleep(1.5)
            screen.markdown(" ")
            time.sleep(0.5)
            screen.markdown(
                "<center>"'<p style="font-size: 60px;">finish!</p></center>',
                unsafe_allow_html=True,
                )

answer = st.session_state.flash_answer

# 回答入力欄の表示
if st.session_state.flash_questions:
    input_answer = st.sidebar.text_input("回答", value="0")

    # 採点確認
    if st.sidebar.button("採点"):
        if input_answer:
            st.session_state.show_flash_answer = True
            if int(input_answer) == int(answer):
                st.write('<p style="font-size: 20px;">おめでとう 正解です！</p>', unsafe_allow_html=True)
            else:
                st.write('<p style="font-size: 20px;">残念…不正解…</p>', unsafe_allow_html=True)
                st.write(f'<p style="font-size: 20px;">正解は{int(answer)}</p>', unsafe_allow_html=True)
        else:
            st.warning("回答を入力してください。")
