from clarifai.rag import RAG
import streamlit as st
import os
import tempfile

st.set_page_config(layout="wide")
query_params = st.experimental_get_query_params()
clarifai_pat = query_params.get("pat", [])[0]

st.title("Chat with your file, Clarifai RAG example")

import os 
os.environ["CLARIFAI_PAT"] = st.secrets["CLARIFAI_PAT"]
workflow="https://clarifai.com/mogith-p-n/rag_app_1706193548/workflows/rag-wf-1706193548"

if "triggered" not in st.session_state:
            st.session_state.triggered = ""
if "messages" not in st.session_state:
            st.session_state.messages = []

with st.sidebar:
    st.markdown("**upload your files here**")
    uploaded_files = st.file_uploader(
                "_", accept_multiple_files=True, label_visibility="hidden")
    workflow="https://clarifai.com/mogith-p-n/rag_app_1706193548/workflows/rag-wf-1706193548"
    if uploaded_files and st.session_state.triggered == "":
        rag_object_from_url = RAG(workflow_url = workflow)
        temp_dir = tempfile.TemporaryDirectory()
        for file in uploaded_files:
                    temp_filepath = os.path.join(temp_dir.name, file.name)
                    with open(temp_filepath, "wb") as f:
                        f.write(file.getvalue())
                    rag_object_from_url.upload(file_path = temp_filepath)
                    st.write("Files uploaded successfully")
        st.session_state.triggered = "done"

for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

if prompt := st.chat_input("Chat with your Files?"):
        
        rag_object_from_url = RAG(workflow_url = workflow)      
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response = rag_object_from_url.chat(messages=[{"role":"human", "content": prompt}])
            print(response)
            message_placeholder.markdown(response[0]['content'])
        st.session_state.messages.append({"role": "assistant", "content": response[0]['content']})
