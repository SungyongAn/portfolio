from fractions import Fraction
import requests
import streamlit as st


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

# st.sidebar.write("注意：半角小文字の数字を入力してください。")
# a = st.sidebar.text_input("問題数", value='1')
# b = st.sidebar.text_input("桁数", value='1')


st.sidebar.write("問題数:１〜９問、桁数:１〜３桁から選択できます。")
a = st.sidebar.slider("問題数", min_value=1, max_value=9, value=1, step=1)
b = st.sidebar.slider("桁数", min_value=1, max_value=3, value=1, step=1)

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

        while len(st.session_state.questions) < num_questions:
            url = 'http://127.0.0.1:8000/page_add'
            response = requests.post(url, json={"num_times": 2, "num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{question_list[0]} + {question_list[1]} = "
                if question not in st.session_state.questions:
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

        while len(st.session_state.questions) < num_questions:
            url = 'http://127.0.0.1:8000/page_subtract'
            response = requests.post(url, json={"num_times": 2, "num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{question_list[0]} - {question_list[1]} ="
                if question not in st.session_state.questions:
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

        while len(st.session_state.questions) < num_questions:
            url = 'http://127.0.0.1:8000/page_multiply'
            response = requests.post(url, json={"num_times": 2, "num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{question_list[0]} × {question_list[1]} ="
                if question not in st.session_state.questions:
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

        while len(st.session_state.questions) < num_questions:
            url = 'http://127.0.0.1:8000/page_divide'
            response = requests.post(url, json={"num_times": 2, "num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{question_list[0]} ÷ {question_list[1]} ="
                if question not in st.session_state.questions:
                    st.session_state.questions.append(question)
                    st.session_state.answers.append(int(answer))
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


# 各計算問題の出力
if st.session_state.questions:
    answer_list = []
    st.write("### 問題一覧")
    if int(b) == 1:
        col1, col2 = st.columns([1,4.7])
    elif int(b) == 2:
        col1, col2 = st.columns([1,3.7])
    elif int(b) == 3:
        col1, col2 = st.columns([1,3])

    for idx, question in enumerate(st.session_state.questions, 1):
        with col1:
            st.write(f'<p style="font-size: 25px; text-align: right;">問{idx})  {question} </p>', unsafe_allow_html=True)
        with col2:
            p_answer = st.text_input(label="", value=0, placeholder=f"{idx}", label_visibility="collapsed")
        answer_list.append(p_answer)


    if st.button('正解表示'):
        st.session_state.show_answers = True

    if st.session_state.show_answers:
        st.write("### 正解一覧")
        for idx, answer in enumerate(st.session_state.answers, 1):
            st.write(f'<p style="font-size: 20px;">問{idx}）{answer}</p>', unsafe_allow_html=True)
            list_idx = idx - 1
            if int(answer_list[list_idx]) == int(answer):
                st.write("○")
            else:
                st.write("×")

