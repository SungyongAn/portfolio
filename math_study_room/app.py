import streamlit as st


st.title('算数の勉強部屋')
st.write('')


with st.sidebar:
    st.page_link("app.py", label="ホーム")
    st.page_link("pages/page1.py", label="整数問題へ移動")
    st.page_link("pages/page2.py", label="実数問題へ移動")
