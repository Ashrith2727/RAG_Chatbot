import streamlit as st

from chat_utils import (
    load_chat_history,
    save_chat_history,
    delete_chat,
    get_bot_response,
)

def init_tutor_state():
    key = "tutor_chats"
    if key not in st.session_state:
        st.session_state[key] = load_chat_history(key)
    if "selected_chat_tutor" not in st.session_state:
        st.session_state["selected_chat_tutor"] = 0
    if len(st.session_state[key]) == 0:
        st.session_state[key].append({"messages": []})
    return key


def tutor_agent_page():
    st.subheader("Tutor Agent - Networksecurity Learning Assistant")

    chat_key = init_tutor_state()

    with st.sidebar:
        st.markdown("### Tutor Chats")
        if st.button("+ New Chat", key="new_tutor_chat"):
            st.session_state[chat_key].append({"messages": []})
            st.session_state["selected_chat_tutor"] = len(st.session_state[chat_key]) - 1
            save_chat_history(st.session_state[chat_key], chat_key)

        for i, chat in enumerate(st.session_state[chat_key]):
            cols = st.columns([3, 1])
            with cols[0]:
                if st.button(f"Chat {i + 1}", key=f"tutor_chat_{i}"):
                    st.session_state["selected_chat_tutor"] = i
            with cols[1]:
                if st.button("🗑️", key=f"tutor_del_{i}"):
                    st.session_state[chat_key] = delete_chat(i, st.session_state[chat_key], chat_key)
                    st.session_state["selected_chat_tutor"] = 0
                    st.success(f"Deleted Chat {i+1}")
                    st.rerun()

    current_chat = st.session_state[chat_key][st.session_state["selected_chat_tutor"]]

    chat_container = st.container()
    with chat_container:
        if not current_chat["messages"]:
            st.info("Start chatting with the Tutor Agent")
        for msg in current_chat["messages"]:
            st.markdown(f"**You:** {msg['user']}")
            st.markdown(f"**Tutor:** {msg['bot']}")
            st.divider()

    with st.form(key="tutor_form", clear_on_submit=True):
        query = st.text_input(
            "Message Tutor Agent...",
            key="tutor_input_box",
            placeholder="Ask your networksecurity questions here...",
        )
        send = st.form_submit_button("Send")

    if send and query.strip():
        current_chat["messages"].append({"user": query, "bot": "Generating response..."})
        save_chat_history(st.session_state[chat_key], chat_key)
        st.rerun()

    if current_chat["messages"]:
        last_msg = current_chat["messages"][-1]
        if last_msg["bot"] == "Generating response...":
            user_query = last_msg["user"]
            with st.spinner("Generating response..."):
                try:
                    bot_response = get_bot_response(user_query, current_chat)

                    current_chat["messages"][-1]["bot"] = bot_response
                    save_chat_history(st.session_state[chat_key], chat_key)
                except Exception as e:
                    current_chat["messages"][-1]["bot"] = f"Error: {e}"
                    save_chat_history(st.session_state[chat_key], chat_key)
            st.rerun()
