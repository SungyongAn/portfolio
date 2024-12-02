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
