# https://github.com/amjadraza/streamlit-agent/blob/main/streamlit_agent/chat_pandas_df.py
# https://blog.streamlit.io/chat-with-pandas-dataframes-using-llms/
# https://github.com/majinmarco/LLMs/blob/main/PANDAS_Agent/data_qa.py
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from langchain_google_genai import ChatGoogleGenerativeAI 
import streamlit as st
import pandas as pd
import os

file_formats = {
    "csv": pd.read_csv,
    "xls": pd.read_excel,
    "xlsx": pd.read_excel,
    "xlsm": pd.read_excel,
    "xlsb": pd.read_excel,
}

key = "AIzaSyAKEaaM7fWIErN3VbikjP_T5m0UfhBy5iE"
# api_key = st.sidebar.text_input("LLM API Key", type="password")

def clear_submit():
    """
    Clear the Submit Button State
    Returns:

    """
    st.session_state["submit"] = False


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


st.set_page_config(page_title="Chat with files", page_icon="🚀 ")
st.title("🗣️ Chat with CSV files")

uploaded_file = st.file_uploader(
    "Upload a Data file",
    type=list(file_formats.keys()),
    help="Various File formats are Support",
    on_change=clear_submit,
)

if not uploaded_file:
    st.warning(
        "This app uses LangChain's `PythonAstREPLTool` which is vulnerable to arbitrary code execution. Please use caution in deploying and sharing this app."
    )

if uploaded_file:
    df = load_data(uploaded_file)
    with st.expander("🔍 Data Preview"):
        st.dataframe(df)


if "messages" not in st.session_state or st.sidebar.button("Clear conversation history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What is this data about?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not key:
        st.info("Please add your LLM API key to continue.")
        st.stop()

   
    llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.1,
    google_api_key=key,
    convert_system_message_to_human=True
)

    pandas_df_agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        handle_parsing_errors=True,allow_dangerous_code=True,
    )
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = pandas_df_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
