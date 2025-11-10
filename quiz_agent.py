import streamlit as st
from rag_pipeline import get_relevant_docs
from chat_utils import local_llm_generate
from logger_utils import create_log_entry
import random


def quiz_agent_page():
    st.title("Quiz Agent")
    st.write("Generate random quiz questions from your network security knowledge base.")

    topic = st.text_input("Enter a topic for your quiz (optional - leave blank for random questions from all PDFs):", placeholder="e.g., AES, Cryptography, Firewalls...")

    if st.button("Generate Quiz"):
        st.info("Generating quiz questions from knowledge base...")

        if topic.strip():
            docs = get_relevant_docs(topic)
            user_query = f"Generate quiz on topic: {topic}"
        else:
            general_topics = ["encryption", "network security", "cryptography", "authentication", "firewall"]
            random_topic = random.choice(general_topics)
            docs = get_relevant_docs(random_topic)
            user_query = "Generate random quiz from all PDFs"
        
        if not docs:
            st.warning("No relevant documents found in the database. Please ensure PDFs are ingested.")
            return
        
        quiz_context = " ".join([doc.page_content for doc in docs])
        
        prompt = f"""
You are a professional Quiz Generator AI specializing in network security.
Based on the following study material, generate a 10-question quiz with mixed question types.

Question Types to Include:
- 2-3 True/False questions
- 3-4 Single Correct Answer (MCQ with 4 options)
- 2-3 Multiple Correct Answers (select all that apply)
- 2 Open-Ended Questions (no options, requires written answer)

Ensure questions are conceptually relevant, moderately challenging, and well-formatted.

Study Material:
{quiz_context[:3000]}

Format output exactly like this:

Q1. [TRUE/FALSE] <question text>
Answer: True/False

Q2. [SINGLE CORRECT] <question text>
A) <option 1>
B) <option 2>
C) <option 3>
D) <option 4>
Correct Answer: <letter>

Q3. [MULTIPLE CORRECT] <question text>
A) <option 1>
B) <option 2>
C) <option 3>
D) <option 4>
Correct Answers: <letters separated by comma, e.g., A, C>

Q4. [OPEN ENDED] <question text>
Sample Answer: <brief expected answer>

Generate all 10 questions following these formats strictly. Mix the question types randomly.
"""

        quiz_output = local_llm_generate(prompt)
        
        create_log_entry(user_query, docs, quiz_output, agent_type="quiz_generator")

        st.subheader("Generated Quiz")
        st.text_area("Quiz Output", quiz_output, height=400)
        
        sources = list(set([doc.metadata.get("source", "Unknown") for doc in docs]))
        st.info(f"Questions generated from: {', '.join(sources)}")


if __name__ == "__main__":
    quiz_agent_page()
