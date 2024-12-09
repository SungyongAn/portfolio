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
if 'divide_flag' not in st.session_state:
    st.session_state.divide_flag = False

# st.sidebar.write("注意：半角小文字の数字を入力してください。")
# a = st.sidebar.text_input("問題数", value='1')
# b = st.sidebar.text_input("桁数", value='1')


st.sidebar.write("# 整数問題")
st.sidebar.page_link("pages/page2.py", label="実数問題へ移動")
st.sidebar.write("問題数:１〜９問、桁数:１〜３桁から選択できます。")
a = st.sidebar.slider("問題数", min_value=1, max_value=9, value=1, step=1)
b = st.sidebar.slider("桁数", min_value=1, max_value=3, value=1, step=1)


# 足し算
if st.sidebar.button(" ＋ (足し算)"):
    st.session_state.divide_flag = False
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
            url = 'http://127.0.0.1:8000/page_addition'
            response = requests.post(url, json={"num_range": num_digits, "identification_code": 1})
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
if st.sidebar.button(" ー (引き算)"):
    st.session_state.divide_flag = False
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
            response = requests.post(url, json={"num_range": num_digits, "identification_code": 1})
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
if st.sidebar.button(" × (掛け算)"):
    st.session_state.divide_flag = False
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
divide = st.sidebar.button(" ÷ (割り算)")

kinds = st.sidebar.radio(
    "割り算の回答形式",
    ["余り", "分数"],
    captions=[
        "回答例）1余り3",
        "回答例) 1 1/3"
    ],
)

if divide:
    st.session_state.divide_flag = True
    if kinds == "余り":
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
        
        while len(st.session_state.questions) < num_questions:
            url = 'http://127.0.0.1:8000/page_divide_residue'
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
            response = requests.post(url, json={"num_range": num_digits})
            if response.status_code == 200:
                data = response.json()
                question_list = data["question_list"]
                answer_zero = data["answer"]
                residue = data["residue"]
                question = f"{int(question_list[0])} ÷ {int(question_list[1])} ="
                answer_two = Fraction(int(residue), int(question_list[1]))
                answer = []
                answer.append(answer_zero)
                answer.append(residue)
                answer.append(question_list[1])
                answer.append(answer_two)
                st.session_state.questions.append(question)
                st.session_state.answers.append(answer)
            else:
                st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
                st.json(response.json())
                break


# 各計算問題の出力
if st.session_state.questions:
    if st.session_state.divide_flag == False:
        answer_list = []
        st.write("### 問題一覧")
        if int(b) == 1:
            col1, col2 = st.columns([1, 4.7])
        elif int(b) == 2:
            col1, col2 = st.columns([1, 3.7])
        elif int(b) == 3:
            col1, col2 = st.columns([1, 3])

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
                if str(answer_list[list_idx]) == str(answer):
                    st.write("○")
                else:
                    st.write("×")

    elif st.session_state.divide_flag == True:
        answer_list = []
        st.write("### 問題一覧")

        if kinds == "余り":
            col1, col2, col3, col4 = st.columns([12, 14, 4, 14])

            for idx, question in enumerate(st.session_state.questions, 1):
                with col1:
                    st.write(f'<p style="font-size: 25px; text-align: left;">問{idx})  {question} </p>', unsafe_allow_html=True)
                with col2:
                    p_answer_1 = st.text_input(label="", value=0, autocomplete="整数"f'{idx}', label_visibility="collapsed")
                with col3:
                    st.write(f'<p style="font-size: 25px; text-align: center;"> 余り </p>', unsafe_allow_html=True)
                with col4:
                    p_answer_2 = st.text_input(label="", value=0, autocomplete="余り"f'{idx}', label_visibility="collapsed")
                answer_zero = [p_answer_1, p_answer_2]
                answer_list.append(answer_zero)

            if st.button('正解表示'):
                st.session_state.show_answers = True

            if st.session_state.show_answers:
                st.write("### 正解一覧")
                for idx, answer in enumerate(st.session_state.answers, 1):
                    st.write(f'<p style="font-size: 20px;">問{idx}）{int(answer[0])} 余り{int(answer[1])}</p>', unsafe_allow_html=True)
                    list_idx = idx - 1
                    if int(answer_list[list_idx][0]) == int(answer[0]) and int(answer_list[list_idx][1]) == int(answer[1]):
                        st.write("○")
                    else:
                        st.write("×")

        elif kinds == "分数":
            col1, col2, col3, col4, col5 = st.columns([10, 9, 9, 2, 9])

            for idx, question in enumerate(st.session_state.questions, 1):
                with col1:
                    st.write(f'<p style="font-size: 25px; text-align: left;">問{idx}) {question} </p>', unsafe_allow_html=True)
                with col2:
                    p_answer_1 = st.text_input(label="", value=0, autocomplete="整数"f'{idx}', label_visibility="collapsed")
                with col3:
                    p_answer_2 = st.text_input(label="", value=0, autocomplete="分子"f'{idx}', label_visibility="collapsed")
                with col4:
                    st.write('<p style="font-size: 25px; text-align: center;"> / </p>', unsafe_allow_html=True)
                with col5:
                    p_answer_3 = st.text_input(label="", value=0, autocomplete="分母"f'{idx}', label_visibility="collapsed")
                answer_zero = [p_answer_1, p_answer_2, p_answer_3]
                answer_list.append(answer_zero)

            if st.button('正解表示'):
                st.session_state.show_answers = True

            if st.session_state.show_answers:
                st.write("### 正解一覧")
                for idx, answer in enumerate(st.session_state.answers, 1):
                    st.write(f'<p style="font-size: 20px;">問{idx}）{int(answer[0])}  {answer[3]}</p>', unsafe_allow_html=True)
                    list_idx = idx - 1
                    if int(answer_list[list_idx][0]) == int(answer[0]) and int(answer_list[list_idx][1]) == int(answer[1]) and int(answer_list[list_idx][2]) == int(answer[2]):
                        st.write("○")
                    else:
                        st.write("×")

