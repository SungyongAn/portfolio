import streamlit as st
import requests

# 作業日報詳細入力の表示フラグ
detailed_input_flag = False

st.title("実務日報")

with st.sidebar:
    account_date = st.text_input("", value="google accountに紐づけられるようにする。")
    st.write('<p style="color:red;">*必須の質問です</p>', unsafe_allow_html=True)

    mail_address = st.text_input("メールアドレス", key="メールアドレス入力欄")

    user_name = st.text_input("氏名", key="氏名")

    today_date = st.date_input("今日の日付", key="今日の日付", format="YYYY/MM/DD")

    work_type = st.radio("作業内容", ["A", "B", "C", "D", "E", "F"], key="実務")

    # open_input_field = st.button("詳細入力画面の表示")

    send_info = st.button("送信")

# if open_input_field:

#     if work_type == "A":
#         work_flag_zero = "A"
#         col1, col2, col3 = st.columns([1, 1, 1])
#         with col1:
#             time_worked_zero = st.text_input("作業時間（分）", value="半角数字で入力してください。")
#         with col2:
#             st.empty()
#         with col3:
#             st.empty()

#     elif work_type == "B":
#         st.write("作成中")
            
#     elif work_type == "C":
#         st.write("作成中")
            
#     elif work_type == "D":
#         st.write("作成中")
            
#     elif work_type == "E":
#         st.write("作成中")
            
#     elif work_type == "F":
#         st.write("作成中")

if send_info:
    try:
        # 入力をdatetimeオブジェクトに変換
        mail_address = str(mail_address)
        user_name = str(user_name)
        work_flag = str(work_type)
    except ValueError:
        st.error("入力内容に誤りがあります。")
    else:
        url = "http://127.0.0.1:8000/page_check_account"
        response = requests.post(url, json={"mail_address": mail_address, "user_name": user_name, "work_flag": work_flag})
        if response.status_code == 200:
            data = response.json()
            response_content = data["response_content"]
            mail_address_for_display = data["mail_address"]
            user_name_for_display = data["user_name"]
            # previous_content = data["previous_content"]
            detailed_input_flag = True
        else:
            st.error(f"{response.status_code}エラーが発生しました。詳細は以下を参照ください")
            st.json(response.json())

if detailed_input_flag == True:
    st.write(f"{response_content}")
    st.write(f"{user_name_for_display}さん、お疲れ様です。前回の作業履歴は以下の内容になります。")
    st.write()
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write(f"{mail_address_for_display}")
    with col2:
        st.write(f"{user_name_for_display}")
    if work_flag == "A":
        st.radio("作業詳細", ["A1", "A2", "A3", "A4", "A5"], horizontal=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.text_input("作業時間")
        with col2:
            st.write("分")
