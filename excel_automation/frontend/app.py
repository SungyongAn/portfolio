import streamlit as st
import requests

st.title("実務日報")

with st.sidebar:
    account_date = st.text_input("", value="google accountに紐づけられるようにする。")
    st.write('<p style="color:red;">*必須の質問です</p>', unsafe_allow_html=True)

    mail_address = st.text_input("メールアドレス", key="メールアドレス入力欄")

    user_name = st.text_input("氏名", key="氏名")

    today_date = st.date_input("今日の日付", key="今日の日付", format="YYYY/MM/DD")

    work_type = st.radio("作業内容", ["A", "B", "C", "D", "E", "F"], key="実務")

    open_input_field = st.button("詳細入力画面の表示")

    send_info = st.button("送信")

if open_input_field:

    if work_type == "A":
        sheet_flag_zero = "A"
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            time_worked_zero = st.text_input("作業時間（分）", value="半角数字で入力してください。")
        with col2:
            st.empty()
        with col3:
            st.empty()

    elif work_type == "B":
        st.write("作成中")
            
    elif work_type == "C":
        st.write("作成中")
            
    elif work_type == "D":
        st.write("作成中")
            
    elif work_type == "E":
        st.write("作成中")
            
    elif work_type == "F":
        st.write("作成中")

if send_info:
    try:
        # 入力をdatetimeオブジェクトに変換
        time_worked = int(time_worked_zero)
        sheet_flag = str(sheet_flag_zero)
    except ValueError:
        st.error("半角数字で入力してください。")
    else:
        url = "http://127.0.0.1:8000/write_to_excel"
        response = requests.post(url, json={"mail_address": mail_address, "user_name" = user_name, "time_worked": time_worked, "sheet_flag": sheet_flag})
#         if response.status_code == 200:
#             data = response.json()
#             question_list = data["question_list"]
#             answer = data["answer"]
#             question = f"{int(question_list[0])} + {int(question_list[1])} = "
#             if question not in st.session_state.questions:
#                 st.session_state.questions.append(question)
#                 st.session_state.answers.append(int(answer))
#         else:
#             st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
#             st.json(response.json())
#             break
