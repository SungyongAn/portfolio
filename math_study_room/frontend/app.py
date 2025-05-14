import streamlit as st

st.title("算数の勉強部屋")
st.write("")

# 項目一覧
with st.sidebar:
    st.page_link("app.py", label="ホーム", icon="🏠")
    st.page_link("pages/page1.py", label="整数問題", icon="1️⃣")
    st.page_link("pages/page2.py", label="実数問題", icon="2️⃣")
