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
key = "AIzaSyAKEaaM7fWIErN3VbikjP_T5m0UfhBy5iE"
st.title("CSV Agent Dashboard")
st.markdown("_Prototype v0.1.0_")
with st.sidebar:
    st.header("Configuration")
    # uploaded_file =r"C:\Users\arunj\Downloads\tradebook-ZM1064-EQ (1).csv"
    url = "https://raw.githubusercontent.com/Rigava/DataRepo/main/yesbank.csv"
    uploaded_file = requests.get(url).content
# df=pd.read_csv(uploaded_file)
df = pd.read_csv(io.StringIO(uploaded_file.decode('utf-8'))) 
st.write(df)
if uploaded_file is not None:
    llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.1,
    google_api_key=key,
    convert_system_message_to_human=True
)
    agent = create_csv_agent(llm,url,verbose=True,allow_dangerous_code=True)
    user_question = st.text_input("Ask a question about your csv: ")
    if user_question is not None and user_question != "":
        with st.spinner(text="In progress..."):
            st_callback = StreamlitCallbackHandler(st.container())
            st.success(agent.run(user_question,callbacks=[st_callback]))                   
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
 

