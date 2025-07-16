import streamlit as st
import requests

# 初期化
if "detailed_input_flag" not in st.session_state:
    st.session_state.detailed_input_flag = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "response_content" not in st.session_state:
    st.session_state.response_content = ""

# UI: サイドバー入力
st.title("実務日報")
with st.sidebar:
    account_date = st.text_input("Googleアドレス", value="google accountに紐づけられるようにする。")
    st.markdown('<p style="color:red;">*必須の質問です</p>', unsafe_allow_html=True)

    mail_address = st.text_input("メールアドレス")
    user_name = st.text_input("氏名")
    work_type = st.radio("作業内容", ["A", "B", "C", "D", "E", "F"])
    send_info = st.button("送信")

# API①: アカウントチェック
if send_info:
    try:
        url = "http://127.0.0.1:8000/page_check_account"
        response = requests.post(url, json={
            "mail_address": mail_address,
            "user_name": user_name,
            "work_flag": work_type
        })
        if response.status_code == 200:
            data = response.json()
            st.session_state.response_content = data["response_content"]
            st.session_state.mail_address = data["mail_address"]
            st.session_state.user_name = data["user_name"]
            st.session_state.work_flag = work_type
            st.session_state.detailed_input_flag = True
            st.session_state.submitted = False  # 念のためリセット
        else:
            st.error(f"{response.status_code} エラーが発生しました。")
            st.json(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"通信エラーが発生しました: {e}")

# UI: アカウントチェック後の詳細入力（ただし送信済みでない場合のみ）
if st.session_state.detailed_input_flag and not st.session_state.submitted:
    st.write(st.session_state.response_content)
    st.write(f"{st.session_state.user_name}さん、お疲れ様です。前回の作業履歴は以下の内容になります。")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.write(f"{st.session_state.mail_address}")
    with col2:
        st.write(f"{st.session_state.user_name}")

    today_date = st.date_input("今日の日付", format="YYYY/MM/DD")

    if st.session_state.work_flag == "A":
        work_detail = st.radio("作業詳細", ["A1", "A2", "A3", "A4", "A5"], horizontal=True)
    elif st.session_state.work_flag == "B":
        work_detail = st.radio("作業詳細", ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"], horizontal=True)
    elif st.session_state.work_flag == "C":
        work_detail = st.radio("作業詳細", ["C1", "C2", "C3", "C4", "C5"], horizontal=True)
    else:
        work_detail = st.session_state.work_flag  # D～Fのとき

    st.write("作業時間")
    col1, col2, _ = st.columns([1, 1, 5])
    with col1:
        time_worked = st.text_input("作業時間（分）", label_visibility="collapsed")
    with col2:
        st.write("分")

    if st.button("作業日報の送信"):
        try:
            url = "http://127.0.0.1:8000/page_write_to_excel"
            response = requests.post(url, json={
                "today_date": str(today_date),
                "user_name": st.session_state.user_name,
                "work_type": str(work_detail),
                "time_worked": int(time_worked)
            })
            if response.status_code == 200:
                data = response.json()
                st.session_state.response_content = data["response_content"]
                st.session_state.submitted = True  # ✅ 作業日報送信済みフラグON
            else:
                st.error(f"{response.status_code} エラーが発生しました。")
                st.json(response.json())
        except Exception as e:
            st.error(f"通信エラーが発生しました: {e}")

# ✅ 作業日報送信後は response_content のみ表示（他は非表示）
if st.session_state.submitted:
    st.success(st.session_state.response_content)
