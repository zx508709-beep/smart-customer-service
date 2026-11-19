import streamlit as st

from qwen_answer import answer_question
from vector_retrieve import SOURCE, load_retriever, search_policy


st.set_page_config(page_title="售后智能客服")
st.title("售后智能客服")
st.caption("演示项目 · 支持查询售后政策，无法查询真实订单或物流。")


@st.cache_resource
def get_retriever():
    return load_retriever()


if "messages" not in st.session_state:
    st.session_state.messages = []


def show_message(role, text, source=None):
    with st.chat_message(role):
        st.write(text)
        if source:
            st.caption(f"本次检索到的资料：{source}")


for message in st.session_state.messages:
    show_message(*message)

question = st.chat_input("例如：商家寄错货，退货邮费谁出？")
if question and question.strip():
    question = question.strip()
    user_message = ("user", question)
    st.session_state.messages.append(user_message)
    show_message(*user_message)

    with st.spinner("正在检索政策并生成回答……"):
        policy = search_policy(question, get_retriever())
        answer = answer_question(question, policy)

    source = f"{SOURCE} / {policy.splitlines()[0]}"
    assistant_message = ("assistant", answer, source)
    st.session_state.messages.append(assistant_message)
    show_message(*assistant_message)