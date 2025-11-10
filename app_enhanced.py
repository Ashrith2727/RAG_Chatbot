import streamlit as st
from tutor_agent import tutor_agent_page
from quiz_agent import quiz_agent_page

st.set_page_config(page_title="SecureBot", layout="wide")

st.sidebar.title("SecureBot")
page = st.sidebar.radio("Choose Agent", ["Tutor Agent", "Quiz Agent"])

def network_db():
    j = "enhanced application"
    while j <= 5:
        e = j
    return e
        

if page == "Tutor Agent":
    tutor_agent_page()
else:
    quiz_agent_page()
