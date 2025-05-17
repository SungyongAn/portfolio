from fractions import Fraction
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
if "divide_flag" not in st.session_state:
    st.session_state.divide_flag = False

# 項目一覧
with st.sidebar:
    st.page_link("app.py", label="ホーム", icon="🏠")
    st.page_link("pages/page2.py", label="実数問題", icon="2️⃣")
    st.write("# 整数問題")
    st.write("問題数:１〜10問、桁数:１〜３桁から選択できます。")
    num_questions_zero = st.slider("問題数", min_value=1, max_value=10, value=1, step=1)
    num_digits_zero = st.slider("桁数", min_value=1, max_value=3, value=1, step=1)
    addition = st.button(" ＋ (足し算)")
    subtract = st.button(" ー (引き算)")
    multiply = st.button(" × (掛け算)")
    divide = st.button(" ÷ (割り算)")
    kinds = st.radio(
        "割り算の回答形式",
        ["余り", "分数"],
        captions=["回答例)1余り3", "回答例) 1 1/3"],
    )

# 足し算
if addition:
    st.session_state.divide_flag = False
    try:
        num_questions = int(num_questions_zero)
        num_digits = int(num_digits_zero)
    except ValueError:
        st.sidebar.error("問題数と桁数には整数を入力してください。")
    else:
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.show_answers = False

        while len(st.session_state.questions) < num_questions:
            url = "http://127.0.0.1:8000/page_addition_integer"
            response = requests.post(url, json={"num_range_integer": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{int(question_list[0])} + {int(question_list[1])} = "
                if question not in st.session_state.questions:
                    st.session_state.questions.append(question)
                    st.session_state.answers.append(int(answer))
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break

# 引き算
if subtract:
    st.session_state.divide_flag = False
    try:
        num_questions = int(num_questions_zero)
        num_digits = int(num_digits_zero)
    except ValueError:
        st.sidebar.error("問題数と桁数には整数を入力してください。")
    else:
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.show_answers = False

        while len(st.session_state.questions) < num_questions:
            url = "http://127.0.0.1:8000/page_subtract"
            response = requests.post(url, json={"num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{int(question_list[0])} - {int(question_list[1])} ="
                if question not in st.session_state.questions:
                    st.session_state.questions.append(question)
                    st.session_state.answers.append(int(answer))
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break


# 掛け算
if multiply:
    st.session_state.divide_flag = False
    try:
        num_questions = int(num_questions_zero)
        num_digits = int(num_digits_zero)
    except ValueError:
        st.sidebar.error("問題数と桁数には整数を入力してください。")
    else:
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.show_answers = False

        while len(st.session_state.questions) < num_questions:
            url = "http://127.0.0.1:8000/page_multiply"
            response = requests.post(url, json={"num_range": num_digits, "identification_code": 1})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer = data["answer"]
                question = f"{int(question_list[0])} × {int(question_list[1])} ="
                if question not in st.session_state.questions:
                    st.session_state.questions.append(question)
                    st.session_state.answers.append(int(answer))
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break

# 割り算
if divide:
    st.session_state.divide_flag = True
    if kinds == "余り":
        try:
            num_questions = int(num_questions_zero)
            num_digits = int(num_digits_zero)
        except ValueError:
            st.sidebar.error("問題数と桁数には整数を入力してください。")
        else:
            st.session_state.questions = []
            st.session_state.answers = []
            st.session_state.residues = []
            st.session_state.show_answers = False

        while len(st.session_state.questions) < num_questions:
            url = "http://127.0.0.1:8000/page_divide_residue"
            response = requests.post(url, json={"num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer_zero = data["answer"]
                residue = data["residue"]
                question = f"{int(question_list[0])} ÷ {int(question_list[1])} ="
                answer = [answer_zero, residue]
                if question not in st.session_state.questions:
                    st.session_state.questions.append(question)
                    st.session_state.answers.append(answer)
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break

    elif kinds == "分数":
        try:
            num_questions = int(num_questions_zero)
            num_digits = int(num_digits_zero)
        except ValueError:
            st.sidebar.error("問題数と桁数には整数を入力してください。")
        else:
            st.session_state.questions = []
            st.session_state.answers = []
            st.session_state.residues = []
            st.session_state.show_answers = False
        for _ in range(num_questions):
            url = "http://127.0.0.1:8000/page_divide_residue"
            response = requests.post(url, json={"num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer_zero = data["answer"]
                residue = data["residue"]
                question = f"{int(question_list[0])} ÷ {int(question_list[1])} ="
                answer_two = str(Fraction(int(residue), int(question_list[1])))
                answer = []
                answer.append(answer_zero)
                answer.append(answer_two)
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

    # 割り算以外の出力
    if st.session_state.divide_flag == False:
        answer_list = []
        st.write("### 問題一覧")
        if num_digits_zero == 1:
            col1, col2 = st.columns([1, 4.2])
        elif num_digits_zero == 2:
            col1, col2 = st.columns([1, 3.4])
        elif num_digits_zero == 3:
            col1, col2 = st.columns([1, 2.7])

        for idx, question in enumerate(st.session_state.questions, 1):
            with col1:
                st.write(
                    f'<p style="font-size: 25px; text-align: left;">問{idx})  {question} </p>', unsafe_allow_html=True,
                )
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
            st.write(f'<p style="font-size: 20px;">{num_questions_zero}問中 {st.session_state.num_correct}問正解</P>', unsafe_allow_html=True)

        if st.button("間違えた問題の正解表示"):
            if len(st.session_state.incorrect_list) < 1:
                st.write('<p style="font-size: 20px;">おめでとう 満点です！</p>', unsafe_allow_html=True)
            else:
                for i in range(len(st.session_state.incorrect_list)):
                    st.write(f'<p style="font-size: 20px;">問{st.session_state.incorrect_list[i][0]}） {st.session_state.incorrect_list[i][1]}</p>', unsafe_allow_html=True)

    # 割り算の出力
    elif st.session_state.divide_flag == True:
        answer_list = []
        st.write("### 問題一覧")

        if kinds == "余り":
            if num_digits == 1:
                col1, col2, col3, col4 = st.columns([12, 14, 4, 14])
            elif num_digits == 2:
                col1, col2, col3, col4 = st.columns([12, 14, 4, 14])
            elif num_digits == 3:
                col1, col2, col3, col4 = st.columns([12, 14, 4, 14])

            for idx, question in enumerate(st.session_state.questions, 1):
                with col1:
                    st.write(
                        f'<p style="font-size: 25px; text-align: left;">問{idx})  {question} </p>',
                        unsafe_allow_html=True,
                    )
                with col2:
                    p_answer_1 = st.text_input(
                        label="", value=0, autocomplete=f"整数{idx}", label_visibility="collapsed",
                    )
                with col3:
                    st.write('<p style="font-size: 25px; text-align: center;"> 余り </p>', unsafe_allow_html=True)
                with col4:
                    p_answer_2 = st.text_input(
                        label="", value=0, autocomplete=f"余り {idx}", label_visibility="collapsed",
                    )
                answer_zero = [p_answer_1, p_answer_2]
                answer_list.append(answer_zero)
        elif kinds == "分数":
            col1, col2, col3, col4, col5 = st.columns([10, 8, 8, 2, 8])

            for idx, question in enumerate(st.session_state.questions, 1):
                with col1:
                    st.write(
                        f'<p style="font-size: 25px; text-align: left;">問{idx}){question} </p>',
                        unsafe_allow_html=True,
                    )
                with col2:
                    p_answer_1 = st.text_input(
                        label="", value=0, autocomplete=f"整数 {idx}", label_visibility="collapsed",
                    )
                with col3:
                    p_answer_2 = st.text_input(
                        label="", value=0, autocomplete=f"分子 {idx}", label_visibility="collapsed",
                    )
                with col4:
                    st.write('<p style="font-size: 25px; text-align: center;"> / </p>', unsafe_allow_html=True)
                with col5:
                    p_answer_3 = st.text_input(
                        label="", value=0, autocomplete=f"分母 {idx}", label_visibility="collapsed",
                    )
                answer_zero = [p_answer_1, p_answer_2, p_answer_3]
                answer_list.append(answer_zero)

        if st.button("採点"):
            st.session_state.show_answers = True

        if st.session_state.show_answers and kinds == "余り":
            for idx, answer in enumerate(st.session_state.answers, 1):
                list_idx = idx - 1
                if int(answer_list[list_idx][0]) == int(answer[0]) and int(answer_list[list_idx][1]) == int(answer[1]):
                    st.session_state.num_correct += 1
                else:
                    incorrect_list_zero = []
                    incorrect_list_zero.append(idx)
                    incorrect_list_zero.append(answer)
                    st.session_state.incorrect_list.append(incorrect_list_zero)
            st.write(f'<p style="font-size: 20px;">{num_questions_zero}問中 {st.session_state.num_correct}問正解</P>', unsafe_allow_html=True)

        if st.session_state.show_answers and kinds == "分数":
            for idx, answer in enumerate(st.session_state.answers, 1):
                list_idx = idx - 1
                if int(answer_list[list_idx][0]) == int(answer[0]) and int(answer_list[list_idx][1]) == int(answer[1][0]) and int(answer_list[list_idx][2]) == int(answer[1][2]):
                    st.session_state.num_correct += 1
                else:
                    incorrect_list_zero = []
                    incorrect_list_zero.append(idx)
                    incorrect_list_zero.append(answer)
                    st.session_state.incorrect_list.append(incorrect_list_zero)
            st.write(f'<p style="font-size: 20px;">{num_questions_zero}問中 {st.session_state.num_correct}問正解</P>', unsafe_allow_html=True)

        if st.button("間違えた問題の正解表示"):
            if len(st.session_state.incorrect_list) < 1:
                st.write('<p style="font-size: 20px;">おめでとう 満点です！</p>', unsafe_allow_html=True)
            else:
                if kinds == "余り":
                    for i in range(len(st.session_state.incorrect_list)):
                        st.write(
                            f'<p style="font-size: 20px;">問{st.session_state.incorrect_list[i][0]}){int(st.session_state.incorrect_list[i][1][0])} 余り{int(st.session_state.incorrect_list[i][1][1])}</p>',
                            unsafe_allow_html=True,
                        )
                elif kinds == "分数":
                    for i in range(len(st.session_state.incorrect_list)):
                        st.write(
                            f'<p style="font-size: 20px;">問{st.session_state.incorrect_list[i][0]}){int(st.session_state.incorrect_list[i][1][0])} {st.session_state.incorrect_list[i][1][1]}</p>',
                            unsafe_allow_html=True,
                        )
