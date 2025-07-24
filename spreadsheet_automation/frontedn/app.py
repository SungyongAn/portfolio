import streamlit as st
import requests
from datetime import date

# 初期化
# 詳細入力欄の表示フラグ
if "detailed_input_flag" not in st.session_state:
    st.session_state.detailed_input_flag = False

# アカウント情報の確認時に一緒に送る作業内容
if "work_flag" not in st.session_state:
    st.session_state.work_flag = None

# アカウント情報確認後、作業詳細入力時に表示するユーザー名
if "user_name_for_display" not in st.session_state:
    st.session_state.user_name_for_display = ""

# アカウント情報確認後、作業詳細入力時に表示するメールアドレス
if "mail_address_for_display" not in st.session_state:
    st.session_state.mail_address_for_display = ""

# backendから返ってきたresponse_contentの保管先
if "response_content" not in st.session_state:
    st.session_state.response_content = ""


st.title("実務日報(スプレットシート版)")

# サイドバー入力
with st.sidebar:
    st.text_input("Googleアドレス", value="google accountに紐づけられるようにする。", key="account_date")
    st.markdown('<p style="color:red;">*必須の質問です</p>', unsafe_allow_html=True)

    mail_address = st.text_input("メールアドレス")
    user_name = st.text_input("氏名")
    work_flag = st.radio("作業内容", ["A", "B", "C", "D", "E", "F"])

    if st.button("送信"):
        url = "http://127.0.0.1:8000/page_check_account"
        # backendに渡す情報をまとめる：dict
        payload = {
            "mail_address": mail_address,
            "user_name": user_name,
            "work_flag": work_flag
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                st.session_state.response_content = data["response_content"]
                st.session_state.mail_address_for_display = data["mail_address"]
                st.session_state.user_name_for_display = data["user_name"]
                st.session_state.work_flag = work_flag
                st.session_state.detailed_input_flag = True
            else:
                st.error(f"{response.status_code} エラーが発生しました。")
                st.json(response.json())
        except Exception as e:
            st.error(f"通信エラーが発生しました: {e}")

# 詳細入力
if st.session_state.detailed_input_flag:
    st.markdown(f"### {st.session_state.response_content}")
    st.write(f"{st.session_state.user_name_for_display}さん、お疲れ様です。前回の作業履歴は以下の内容になります。")

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"メールアドレス: {st.session_state.mail_address_for_display}")
    with col2:
        st.write(f"氏名: {st.session_state.user_name_for_display}")

    # 作業日入力
    today_date = st.date_input("今日の日付", value=date.today(), format="YYYY/MM/DD")

    # 作業詳細（work_flagに応じて変化）
    detailed_options = {
        "A": ["A1", "A2", "A3", "A4", "A5"],
        "B": ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"],
        "C": ["C1", "C2", "C3", "C4", "C5"]
    }

    # 作業項目の代入先
    work_type = None
    if st.session_state.work_flag in detailed_options:
        work_type = st.radio("作業詳細", detailed_options[st.session_state.work_flag], horizontal=True)
    else:
        work_type = st.session_state.work_flag  # 詳細指定がない場合はそのまま

    # 作業時間
    st.write("作業時間")
    col1, col2, _ = st.columns([1, 1, 5])
    with col1:
        time_worked = st.text_input("作業時間", label_visibility="collapsed")
    with col2:
        st.write("分")

    if st.button("作業日報の送信"):
        try:
            payload = {
                "today_date": str(today_date),
                "user_name": st.session_state.user_name_for_display,
                "work_type": str(work_type),
                "time_worked": int(time_worked)
            }
        except ValueError:
            st.error("作業時間は整数で入力してください。")
        else:
            url = "http://127.0.0.1:8000/page_write_to_test0001"
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.response_content = data["response_content"]
                    st.success(st.session_state.response_content)
                else:
                    st.error(f"{response.status_code} エラーが発生しました。")
                    st.json(response.json())
            except Exception as e:
                st.error(f"通信エラーが発生しました: {e}")
