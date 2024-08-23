# https://www.youtube.com/watch?v=eOP_i4Qn8m4
import os
import streamlit as st
import pandas as pd
from csv_functions import ask_agent,decode_response,write_answer
import json
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from langchain_google_genai import ChatGoogleGenerativeAI 
key = st.secrets.API_KEY

llm = ChatGoogleGenerativeAI(
model="gemini-pro",
temperature=0.1,
google_api_key=key,
convert_system_message_to_human=True
)

st.set_page_config(page_title="👨‍💻 Talk with your Data")
st.title("👨‍💻 Talk with your Data")
st.write("Please upload your CSV file below.")

def csv_tool(filename :  str):

    df = pd.read_csv(filename)    

    return df

data = st.file_uploader("Upload a CSV" , type="csv")

if data is None:
    st.info(" Upload a file through config", icon="ℹ️")
    st.stop()
df = csv_tool(data)    
with st.expander("🔍 Data Preview"):
    st.dataframe(df)
query = st.text_area("Send a Message")
if st.button("Submit Query", type="primary"):
    # Create an agent from the CSV file. 
    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)

    agent = create_pandas_dataframe_agent(llm, df, verbose=True,allow_dangerous_code=True)
    # Query the agent.
    response = ask_agent(agent=agent, query=query)

    # Decode the response.
    decoded_response = decode_response(response)

    # Write the response to the Streamlit app.
    write_answer(decoded_response)
