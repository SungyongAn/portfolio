import streamlit as st


st.title('算数の勉強部屋')
st.write('')

# st.sidebar.write("注意：半角小文字の数字を入力してください。")
# a = st.sidebar.text_input("問題数", value='1')
# b = st.sidebar.text_input("桁数", value='1')

with st.sidebar:
    st.page_link("app.py", label="ホーム")
    st.page_link("pages/page1.py", label="整数問題へ移動")
    st.page_link("pages/page2.py", label="実数問題へ移動")
