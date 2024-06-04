import streamlit as st
import pandas as pd
import numpy as np
from Bedrock import Converse

#st.set_page_config(layout="wide")

with (st.sidebar):
    st.header('Credentials')
    aws_access_key_id = st.text_input('AWS Access Key', value='', type='password')
    aws_secret_access_key = st.text_input('AWS Secret Key', value='', type='password')

st.header("Converse with Bedrock !")

option = st.selectbox(
    "Pick a foundational model on Bedrock to Converse",
    ("Claude-3-Haiku", "Claude-3-Sonnet", "Claude-3-Opus", "Llama3-70B","Mistral-Small"))
system_prompt = "You are a helpful chatbot"
model_id = "anthropic.claude-3-haiku-20240307-v1:0"

if option == "Claude-3-Haiku":
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
elif option == "Claude-3-Sonnet":
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
elif option == "Claude-3-Opus":
    model_id = "anthropic.claude-3-opus-20240229-v1:0"
elif option == "Llama3-70B":
    model_id = "meta.llama3-70b-instruct-v1:0"
elif option == "Mistral-Large":
    model_id = "mistral.mistral-large-2402-v1:0"
elif option == "Mistral-Small":
    model_id = "mistral.mistral-small-2402-v1:0"
elif option == "Titan-Text-Premier":
    model_id = "amazon.titan-text-premier-v1:0"
    system_prompt=''


if "messages" not in st.session_state:
      st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
      st.session_state["br_messages"] = []

for msg in st.session_state.messages:
      st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    if not aws_access_key_id or not aws_secret_access_key:
        st.info("Please add your AWS credentials to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.br_messages.append({"role": "user", "content": [{"text": prompt}]})
    st.chat_message("user").write(prompt)

    converse = Converse(access_key_id=aws_access_key_id, secret_key=aws_secret_access_key)
    response = converse.converse_with_model(model_id=model_id, messages=st.session_state.br_messages, system_text=system_prompt)

    st.chat_message("assistant").write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.br_messages.append({"role": "assistant", "content": [{"text": response}]})