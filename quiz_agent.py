import streamlit as st
from rag_pipeline import get_relevant_docs
from chat_utils import local_llm_generate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from logger_utils import create_log_entry


def quiz_agent_page():
    st.title("Quiz Agent")
    st.write("Generate interactive quizzes from PDFs or your RAG knowledge base.")

    option = st.radio("Choose your input method:", ["Upload PDF", "Enter Topic"])

    quiz_context = ""
    docs_for_logging = []

    if option == "Upload PDF":
        uploaded_file = st.file_uploader("Upload a PDF to create a quiz", type="pdf")
        if uploaded_file:
            with open("temp_quiz.pdf", "wb") as f:
                f.write(uploaded_file.read())

            st.info("Processing your PDF...")
            loader = PyPDFLoader("temp_quiz.pdf")
            docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(docs)

            quiz_context = " ".join([chunk.page_content for chunk in chunks])
            docs_for_logging = chunks
            st.success("PDF successfully processed and ready for quiz generation!")

    elif option == "Enter Topic":
        topic = st.text_input("Enter a topic for your quiz (e.g., AES, DES, PRNG, ...):")
        if topic:
            st.info("Fetching related content from RAG knowledge base...")
            docs = get_relevant_docs(topic)
            quiz_context = " ".join([doc.page_content for doc in docs]) if docs else ""
            docs_for_logging = docs
            if quiz_context:
                st.success("Retrieved relevant context for quiz generation!")
            else:
                st.warning("No relevant documents found in the database.")

    if st.button("Generate Quiz"):
        if not quiz_context.strip():
            st.warning("Please upload a PDF or enter a topic first!")
            return

        st.info("Generating quiz questions using your local Ollama model...")

        user_query = f"Generate quiz from: {option}"
        
        prompt = f"""
        You are a professional Quiz Generator AI.
        Based on the following study material or topic, generate a 5-question multiple-choice quiz.

        Each question must have 4 options (A, B, C, D) and a correct answer clearly indicated.
        Ensure the questions are conceptually relevant, moderately challenging, and well-formatted.

        Content/Topic:
        {quiz_context}

        Format output exactly like this:
        Q1. <question text>
        A) <option 1>
        B) <option 2>
        C) <option 3>
        D) <option 4>
        Correct Answer: <letter>

        Generate all 5 questions in this format only.
        """

        quiz_output = local_llm_generate(prompt)
        
        if docs_for_logging:
            create_log_entry(user_query, docs_for_logging, quiz_output, agent_type="quiz_generator")

        st.subheader("Generated Quiz")
        st.text_area("Quiz Output", quiz_output, height=400)


if __name__ == "__main__":
    quiz_agent_page()
