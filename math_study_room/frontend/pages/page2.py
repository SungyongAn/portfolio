import requests
import streamlit as st

if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "residue" not in st.session_state:
    st.session_state.residues = []
if "incorrect_list" not in st.session_state:
    st.session_state.incorrect_list = []
if "num_correct" not in st.session_state:
    st.session_state.num_correct = 0
if "show_answers" not in st.session_state:
    st.session_state.show_answers = False

# 項目一覧
with st.sidebar:
    st.page_link("app.py", label="ホーム", icon="🏠")
    st.page_link("pages/page1.py", label="整数問題", icon="1️⃣")
    st.write("# 実数問題")
    st.write("問題数:１〜10問、桁数:１〜３桁から選択できます。")
    num_questions_zero = st.slider("問題数", min_value=1, max_value=10, value=1, step=1)
    b = st.radio(
        "問題の桁数",
        ["1桁、1桁", "2桁、1桁", "2桁、2桁", "3桁、2桁", "3桁、3桁"],
    )
    st.write("桁数1  \n 1.9 ~ 0.1  \n 桁数2  \n 1.9 ~ 0.01  \n 桁数3  \n 1.9 ~0.001")

    addition = st.button(" ＋ (足し算)")
    subtract = st.button(" ー (引き算)")
    multiply = st.button(" × (掛け算)")
    divide = st.button(" ÷ (割り算)")
    st.write("※小数点3位までに割り切れない場合は、小数点4位を四捨五入する。")


# 出題される数字の桁数をcalculation.pyに渡すデータに変換
if b == "1桁、1桁":
    num_digits_list_zero = [1, 1]
elif b == "2桁、1桁":
    num_digits_list_zero = [2, 1]
elif b == "2桁、2桁":
    num_digits_list_zero = [2, 2]
elif b == "3桁、2桁":
    num_digits_list_zero = [3, 2]
elif b == "3桁、3桁":
    num_digits_list_zero = [3, 3]


# 足し算
if addition:
    try:
        num_questions = int(num_questions_zero)
        num_digits_list = num_digits_list_zero
    except ValueError:
        st.sidebar.error("問題数と桁数には整数を入力してください。")
    else:
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.show_answers = False

        while len(st.session_state.questions) < num_questions:
            url = "http://127.0.0.1:8000/page_addition"
            response = requests.post(url, json={"num_range": num_digits_list_zero, "identification_code": 2})
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
        num_questions = int(num_questions_zero)
        num_digits_list = num_digits_list_zero
    except ValueError:
        st.sidebar.error("問題数と桁数には整数を入力してください。")
    else:
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.show_answers = False

        while len(st.session_state.questions) < num_questions:
            url = "http://127.0.0.1:8000/page_subtract"
            response = requests.post(url, json={"num_range": num_digits_list_zero, "identification_code": 2})
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
        num_questions = int(num_questions_zero)
        num_digits_list = num_digits_list_zero
    except ValueError:
        st.sidebar.error("問題数と桁数には整数を入力してください。")
    else:
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.show_answers = False

        while len(st.session_state.questions) < num_questions:
            url = "http://127.0.0.1:8000/page_multiply"
            response = requests.post(url, json={"num_range": num_digits_list_zero, "identification_code": 2})
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
        num_questions = int(num_questions_zero)
        num_digits_list = num_digits_list_zero
    except ValueError:
        st.sidebar.error("問題数と桁数には整数を入力してください。")
    else:
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.show_answers = False

    while len(st.session_state.questions) < num_questions:
        url = "http://127.0.0.1:8000/page_divide"
        response = requests.post(url, json={"num_range": num_digits_list_zero})
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
    st.session_state.incorrect_list = []
    st.session_state.num_correct = 0
    answer_list = []
    st.write("### 問題一覧")
    if b == "1桁、1桁":
        col1, col2, col3, col4 = st.columns([12, 14, 4, 14])
    elif b == "2桁、1桁":
        col1, col2, col3, col4 = st.columns([12, 14, 4, 14])
    elif b == "2桁、2桁":
        col1, col2, col3, col4 = st.columns([12, 14, 4, 14])
    elif b == "3桁、2桁":
        col1, col2, col3, col4 = st.columns([12, 14, 4, 14])
    elif b == "3桁、3桁":
        col1, col2, col3, col4 = st.columns([12, 14, 4, 14])

    for idx, question in enumerate(st.session_state.questions, 1):
        with col1:
            st.write(f'<p style="font-size: 25px; text-align: left;">問{idx}) {question} </p>', unsafe_allow_html=True)
        with col2:
            p_answer = st.text_input(label="", value=0, placeholder=f"{idx}", label_visibility="collapsed")
        answer_list.append(p_answer)

    if st.button("採点"):
        st.session_state.show_answers = True

    if st.session_state.show_answers:
        for idx, answer in enumerate(st.session_state.answers, 1):
            list_idx = idx - 1
            if str(answer_list[list_idx]) == str(answer):
                st.session_state.num_correct += 1
            else:
                incorrect_list_zero = []
                incorrect_list_zero.append(idx)
                incorrect_list_zero.append(answer)
                st.session_state.incorrect_list.append(incorrect_list_zero)
        st.write(f'<p style="font-size: 20px;">{a}問中 {st.session_state.num_correct}問正解</P>', unsafe_allow_html=True)
        if len(st.session_state.incorrect_list) < 1:
                st.write('<p style="font-size: 20px;">おめでとう 満点です！</p>', unsafe_allow_html=True)
        else:
            st.write("不正解問題の正解")
            for i in range(len(st.session_state.incorrect_list)):
                st.write(f'<p style="font-size: 20px;">問{st.session_state.incorrect_list[i][0]}） {st.session_state.incorrect_list[i][1]}</p>', unsafe_allow_html=True)
