import streamlit as st
import pandas as pd
import requests
import io
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from langchain_google_genai import ChatGoogleGenerativeAI 
st.set_page_config(page_title="Langchain Dashboard", page_icon=":bar_chart:", layout="wide")
key = st.secrets.API_KEY
st.title("CSV Agent Dashboard")
st.markdown("_Prototype v0.1.0_")
with st.sidebar:
     st.header("Add your file")
     uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

with st.sidebar:
    st.header("Disclaimer")
    st.warning(
        "This app uses LangChain's `PythonAstREPLTool` which is vulnerable to arbitrary code execution. Please use caution in deploying and sharing this app."
    )

if not uploaded_file:
    uploaded_file = "https://raw.githubusercontent.com/Rigava/DataRepo/main/yesbank.csv"
    content = requests.get(uploaded_file).content
    df = pd.read_csv(io.StringIO(content.decode('utf-8'))) 
if uploaded_file:
        df = pd.read_csv(uploaded_file)
        with st.expander("🔍 Data Preview"):
            st.dataframe(df)

if uploaded_file is not None:
    llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=key
)
    agent = create_csv_agent(llm,uploaded_file,verbose=True,allow_dangerous_code=True)
    user_question = st.text_input("Ask a question about your csv: ")
    if user_question is not None and user_question != "":
        with st.spinner(text="In progress..."):
            st_callback = StreamlitCallbackHandler(st.container())
            st.success(agent.run(user_question,callbacks=[st_callback]))        
