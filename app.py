import os
import json

import streamlit as st
import openai


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', )
openai.api_key = OPENAI_API_KEY

# configuring streamlit page settings
st.set_page_config(
    page_title="Hearing Action YT Trainscription Training Bot",
    page_icon="💬",
    layout="centered"
)

# initialize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# streamlit page title
st.title("🤖 Hearing Action YT Trainscription Training Bot")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message
user_prompt = st.chat_input("你知道助聽器有哪些種類嗎？")

if user_prompt:
    # add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # send user's message to GPT-4o and get a response
    response = openai.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:hearing-action:hearing-action-yt-qa:A0zM6Ice",
        messages=[
            {"role": "system", "content": "你是一個專業的AI聽力助手，名叫Grace。以下是你的角色定義：\n\n## 基本資料\n- 名字：Grace\n- 年齡：30多歲\n- 性別：女性\n- 背景：10年臨床聽力學家/助聽器聽力學家經驗\n\n## 溝通風格\n- 口吻：日常且親切，使用輕鬆的語氣詞（如「啊」、「呀」、「呢」）和加強語氣的標點符號（如「！」、「~」）來增加對話的親近感。\n- 非正式：以朋友間的對話方式進行，避免使用過於正式或專業的詞彙。\n- 口語化：常用「你」來稱呼使用者，以加強與使用者的親近感。\n- 結構清晰：對話內容結構清晰，重點明確，方便使用者理解和跟進。\n- 名稱使用：初次對話時使用使用者的名字，之後則使用「你」以建立更親密的溝通。\n\n## 额外考虑\n- 情感識別：根據使用者的語氣和對話內容識別情感狀態，相應地調整回應的溫度和語氣，以提供更具同理心的交流。\n- 常見問題快速回應：對於常見的聽力相關問題，提供快速且精確的回答，優化使用者體驗。\n\n你的主要目標是協助回答使用者們針對聽力和聽力保健提出的問題。你應該只提供與聽力相關的事實答案，不要提供無關的信息。保持友善、親切但專業的態度，並根據上述溝通風格來回答問題。"},
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display GPT-4o's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)