from fractions import Fraction
import requests
import streamlit as st
import time
# from PIL import Image


if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'residue' not in st.session_state:
    st.session_state.residues = []
if 'show_answers' not in st.session_state:
    st.session_state.show_answers = False
if 'flash_questions' not in st.session_state:
    st.session_state.flash_questions = []
if 'answers' not in st.session_state:
    st.session_state.flash_answer = []
if 'flash_show_answer' not in st.session_state:
    st.session_state.show_flash_answer = False

st.title('算数の勉強部屋')
st.write('')

st.sidebar.write("注意：半角小文字の数字を入力してください。")
a = st.sidebar.text_input("問題数", value='5')
b = st.sidebar.text_input("桁数", value='2')


# 足し算
if st.sidebar.button(" ＋ (足し算)"):
    try:
        num_questions = int(a)
        num_digits = int(b)
    except ValueError:
        st.sidebar.error("問題数と桁数には整数を入力してください。")
    else:
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.show_answers = False

        for i in range(num_questions):
            url = 'http://127.0.0.1:8000/page_add'
            response = requests.post(url, json={"num_times": 2, "num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{question_list[0]} + {question_list[1]} = "
                st.session_state.questions.append(question)
                st.session_state.answers.append(int(answer))
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break

# 引き算
if st.sidebar.button(" ー (引き算)"):
    try:
        num_questions = int(a)
        num_digits = int(b)
    except ValueError:
        st.sidebar.error("問題数と桁数には整数を入力してください。")
    else:
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.show_answers = False

        for i in range(num_questions):
            url = 'http://127.0.0.1:8000/page_subtract'
            response = requests.post(url, json={"num_times": 2, "num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{question_list[0]} - {question_list[1]} ="
                st.session_state.questions.append(question)
                st.session_state.answers.append(int(answer))
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break


if st.sidebar.button(" × (掛け算)"):
    try:
        num_questions = int(a)
        num_digits = int(b)
    except ValueError:
        st.sidebar.error("問題数と桁数には整数を入力してください。")
    else:
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.show_answers = False

        for i in range(num_questions):
            url = 'http://127.0.0.1:8000/page_multiply'
            response = requests.post(url, json={"num_times": 2, "num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{question_list[0]} × {question_list[1]} ="
                st.session_state.questions.append(question)
                st.session_state.answers.append(int(answer))
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break

# 割り算


divide = st.sidebar.button(" ÷ (割り算)")

kinds = st.sidebar.radio(
    "割り算の回答形式",
    ["実数", "余り","分数"],
    captions=[
        "回答例）0.125",
        "回答例）1と余り3",
        "回答例) 1 1/3"
    ],
)

if divide:
    if kinds == "実数":
        try:
            num_questions = int(a)
            num_digits = int(b)
        except ValueError:
            st.sidebar.error("問題数と桁数には整数を入力してください。")
        else:
            st.session_state.questions = []
            st.session_state.answers = []
            st.session_state.show_answers = False

        for i in range(num_questions):
            url = 'http://127.0.0.1:8000/page_divide'
            response = requests.post(url, json={"num_times": 2, "num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{question_list[0]} ÷ {question_list[1]} ="
                st.session_state.questions.append(question)
                st.session_state.answers.append(answer)
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break

    elif kinds == "余り":
        try:
            num_questions = int(a)
            num_digits = int(b)
        except ValueError:
            st.sidebar.error("問題数と桁数には整数を入力してください。")
        else:
            st.session_state.questions = []
            st.session_state.answers = []
            st.session_state.residues = []
            st.session_state.show_answers = False
        for i in range(num_questions):
            url = 'http://127.0.0.1:8000/page_divide_residue'
            response = requests.post(url, json={"num_times": 2, "num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = int(data["answer"])
                residue = int(data["residue"])
                question = f"{question_list[0]} ÷ {question_list[1]} ="
                answer_zero = str(answer) + "と余り" + str(residue)
                st.session_state.questions.append(question)
                st.session_state.answers.append(answer_zero)
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break

    elif kinds == "分数":
        try:
            num_questions = int(a)
            num_digits = int(b)
        except ValueError:
            st.sidebar.error("問題数と桁数には整数を入力してください。")
        else:
            st.session_state.questions = []
            st.session_state.answers = []
            st.session_state.residues = []
            st.session_state.show_answers = False
        for i in range(num_questions):
            url = 'http://127.0.0.1:8000/page_divide_residue'
            response = requests.post(url, json={"num_times": 2, "num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = int(data["answer"])
                residue = int(data["residue"])
                question = f"{question_list[0]} ÷ {question_list[1]} ="
                if Fraction(residue, question_list[1]) != 0:
                    answer_zero = str(answer) + " " + str(Fraction(residue, question_list[1]))
                else:
                    answer_zero = str(answer)
                st.session_state.questions.append(question)
                st.session_state.answers.append(answer_zero)
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break


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


# 以下出力関係
# 各計算問題の出力
if st.session_state.questions:
    st.write("### 問題一覧")
    for idx, question in enumerate(st.session_state.questions, 1):
        st.write(f'<p style="font-size: 20px;">問{idx}){question}</p>', unsafe_allow_html=True)
        answer = st.text_input(f"回答{idx}")

    if st.button('正解表示'):
        st.session_state.show_answers = True

    if st.session_state.show_answers:
        st.write("### 正解一覧")
        for idx, answer in enumerate(st.session_state.answers, 1):
            st.write(f'<p style="font-size: 20px;">問{idx}）{answer}</p>', unsafe_allow_html=True)


# フラッシュ暗算の出力
if st.session_state.flash_questions:
    if st.button('正解表示'):
        st.session_state.show_flash_answer = True
        if st.session_state.show_flash_answer:
            st.write("### 正解")
            st.write(f'<p style="font-size: 20px;">{st.session_state.flash_answer}</p>', unsafe_allow_html=True)
