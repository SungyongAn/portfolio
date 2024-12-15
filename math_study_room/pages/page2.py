import requests
import streamlit as st

if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "residue" not in st.session_state:
    st.session_state.residues = []
if "show_answers" not in st.session_state:
    st.session_state.show_answers = False

# 項目一覧
with st.sidebar:
    st.page_link("app.py", label="ホーム", icon="🏠")
    st.page_link("pages/page1.py", label="整数問題", icon="1️⃣")
    st.write("# 実数問題")
    st.write("問題数:１〜９問、桁数:１〜３桁から選択できます。")
    a = st.slider("問題数", min_value=1, max_value=9, value=1, step=1)
    b = st.slider("桁数", min_value=1, max_value=3, value=1, step=1)
    st.write("桁数1:1.9 ~ 0.1、桁数2:1.9 ~ 0.01、桁数3:1.9 ~0.001")
    addition = st.button(" ＋ (足し算)")
    subtract = st.button(" ー (引き算)")
    multiply = st.button(" × (掛け算)")
    divide = st.button(" ÷ (割り算)")
    st.write("※小数点3位までに割り切れない場合は、小数点4位を四捨五入する。")


# 足し算
if addition:
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
            url = "http://127.0.0.1:8000/page_addition"
            response = requests.post(url, json={"num_range": num_digits, "identification_code": 2})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{question_list[0]} + {question_list[1]} = "
                if question not in st.session_state.questions:
                    st.session_state.questions.append(question)
                    st.session_state.answers.append(answer)
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break

# 引き算
if subtract:
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
            url = "http://127.0.0.1:8000/page_subtract"
            response = requests.post(url, json={"num_range": num_digits, "identification_code": 2})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{question_list[0]} - {question_list[1]} ="
                if question not in st.session_state.questions:
                    st.session_state.questions.append(question)
                    st.session_state.answers.append(answer)
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break

# 掛け算
if multiply:
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
            url = "http://127.0.0.1:8000/page_multiply"
            response = requests.post(url, json={"num_range": num_digits, "identification_code": 2})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{question_list[0]} × {question_list[1]} ="
                if question not in st.session_state.questions:
                    st.session_state.questions.append(question)
                    st.session_state.answers.append(answer)
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break

# 割り算
if divide:
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
        url = "http://127.0.0.1:8000/page_divide"
        response = requests.post(url, json={"num_range": num_digits})
        if response.status_code == 200:
            data = response.json()
            question_list = data["question_list"]
            answer = data["answer"]
            question = f"{question_list[0]} ÷ {question_list[1]} ="
            if question not in st.session_state.questions:
                st.session_state.questions.append(question)
                st.session_state.answers.append(answer)
        else:
            st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
            st.json(response.json())
            break


# 各計算問題の出力
if st.session_state.questions:
    answer_list = []
    st.write("### 問題一覧")
    if int(b) == 1:
        col1, col2 = st.columns([1,3.4])
    elif int(b) == 2:
        col1, col2 = st.columns([1,2.8])
    elif int(b) == 3:
        col1, col2 = st.columns([1,2.3])

    for idx, question in enumerate(st.session_state.questions, 1):
        with col1:
            st.write(f'<p style="font-size: 25px; text-align: left;">問{idx}) {question} </p>', unsafe_allow_html=True)
        with col2:
            p_answer = st.text_input(label="", value=0, placeholder=f"{idx}", label_visibility="collapsed")
        answer_list.append(p_answer)

    if st.button("正解表示"):
        st.session_state.show_answers = True

    if st.session_state.show_answers:
        st.write("### 正解一覧")
        st.write("数字は半角数字で入力してください。")
        for idx, answer in enumerate(st.session_state.answers, 1):
            st.write(f'<p style="font-size: 20px;">問{idx}）{answer}</p>', unsafe_allow_html=True)
            list_idx = idx - 1
            if answer_list[list_idx] == str(answer):
                st.write("○")
            else:
                st.write("×")

