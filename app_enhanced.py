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

def validate_security_query(query):
    """Validate if the query is related to network security topics"""
    security_keywords = ['encryption', 'firewall', 'vpn', 'ssl', 'tls', 'authentication', 
                        'authorization', 'cryptography', 'hash', 'security', 'attack']
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in security_keywords)


def format_quiz_results(quiz_data, user_answers):
    """Format quiz results with score calculation"""
    total_questions = len(quiz_data)
    correct_answers = 0
    
    for i, question in enumerate(quiz_data):
        if user_answers.get(i) == question.get('correct_answer'):
            correct_answers += 1
    
    score_percentage = (correct_answers / total_questions) * 100
    
    return {
        'total': total_questions,
        'correct': correct_answers,
        'score': score_percentage,
        'passed': score_percentage >= 70
    }

def log_user_interaction(user_id, query, response, timestamp):
    """Log user interactions for analytics and monitoring"""
    interaction_data = {
        'user_id': user_id,
        'query': query,
        'response_length': len(response),
        'timestamp': timestamp,
        'session_active': True
    }
    return interaction_data


def sanitize_user_input(user_input):
    """Sanitize and validate user input before processing"""
    if not user_input or not isinstance(user_input, str):
        return ""
    
    # Remove leading/trailing whitespace
    sanitized = user_input.strip()
    
    # Remove potentially harmful characters
    dangerous_chars = ['<', '>', '{', '}', ';', '|']
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    # Limit input length
    max_length = 500
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized

