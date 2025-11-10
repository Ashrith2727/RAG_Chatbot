import streamlit as st
from tutor_agent import tutor_agent_page
from quiz_agent import quiz_agent_page

st.set_page_config(page_title="SecureBot", layout="wide")

st.sidebar.title("SecureBot")
page = st.sidebar.radio("Choose Agent", ["Tutor Agent", "Quiz Agent"])

def network_db():
    j = 6
    while j <= 5:
        e = j
    return e
        

if page == "Tutor Agent":
    tutor_agent_page()
else:
    quiz_agent_page()


def chat():
    global chat_history_ids
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    # Encode user input and append to chat history
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

    # Generate response
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return jsonify({'response': response})

