# https://www.youtube.com/watch?v=eOP_i4Qn8m4
import os
import streamlit as st
import pandas as pd
from csv_functions import ask_agent,decode_response,write_answer,clear_submit
import json
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from langchain_google_genai import ChatGoogleGenerativeAI 
key = "AIzaSyAKEaaM7fWIErN3VbikjP_T5m0UfhBy5iE"

llm = ChatGoogleGenerativeAI(
model="gemini-pro",
temperature=0.1,
google_api_key=key,
convert_system_message_to_human=True
)

st.set_page_config(page_title="👨‍💻 Josh@i Excel tool",layout="wide")
st.title("👨‍💻 Talk with your Data")
st.write("Please upload your CSV/XLS file below.")

file_formats = {
    "csv": pd.read_csv,
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
    "xlsm": pd.read_excel,
    "xlsb": pd.read_excel,
}
@st.cache_data(ttl="2h")
def load_data(uploaded_file):
    try:
        ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
    except:
        ext = uploaded_file.split(".")[-1]
    if ext in file_formats:
        return file_formats[ext](uploaded_file)
    else:
        st.error(f"Unsupported file format: {ext}")
        return None    

# def csv_tool(filename :  str):

#     df = pd.read_csv(filename)    

#     return df

data = st.file_uploader(
    "Upload a Data file",
    type=list(file_formats.keys()),
    help="Various File formats are Support",
    on_change=clear_submit,
)

if data is None:
    st.info(" Upload a file through config", icon="ℹ️")
    st.warning(
        "This app uses LangChain's `PythonAstREPLTool` which is vulnerable to arbitrary code execution. Please use caution in deploying and sharing this app."
    )
    st.stop()
    
df = load_data(data)    
with st.expander("🔍 Data Preview"):
    st.dataframe(df)
query = st.text_area("Send a Message")
if st.button("Submit Query", type="primary"):
    # Create an agent from the CSV file. 
    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)

    agent = create_pandas_dataframe_agent(llm, df, verbose=True,handle_parsing_errors=True,allow_dangerous_code=True)
    # Query the agent.
    response = ask_agent(agent=agent, query=query)

    # Decode the response.
    decoded_response = decode_response(response)

    # Write the response to the Streamlit app.
    write_answer(decoded_response)
