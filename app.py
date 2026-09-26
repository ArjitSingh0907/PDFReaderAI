import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

from htmlTemplates import css, bot_template, user_template

# Force reload the .env file to ensure the API key is read into memory
load_dotenv(override=True)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"  # free, fast, local — no API needed
    )
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_qa_chain():
    # Pass the API key explicitly to the chat model
    llm = ChatGoogleGenerativeAI(
    model="gemini-pro",  # change from gemini-1.5-flash to gemini-pro
    temperature=0,
    google_api_key=GOOGLE_API_KEY,
    convert_system_message_to_human=True  # add this too
    )
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an assistant for question-answering tasks. "
            "Use the following retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know. "
            "Keep the answer concise.\n\n"
            "Context:\n{context}"
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    return prompt | llm | StrOutputParser()


def handle_userinput(user_question):
    # 1. Retrieve relevant chunks from FAISS
    docs = st.session_state.retriever.invoke(user_question)
    context = format_docs(docs)

    # 2. Invoke the chain with question, history, and context
    answer = st.session_state.conversation.invoke({
        "input": user_question,
        "chat_history": st.session_state.chat_history,
        "context": context
    })

    # 3. Save to chat history
    st.session_state.chat_history.append(HumanMessage(content=user_question))
    st.session_state.chat_history.append(AIMessage(content=answer))

    # 4. Render styled chat boxes
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            st.write(
                user_template.replace("{{MSG}}", message.content),
                unsafe_allow_html=True
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", message.content),
                unsafe_allow_html=True
            )


def main():
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    # Diagnostic check for API key
    if not GOOGLE_API_KEY:
        st.error("GOOGLE_API_KEY is missing or empty. Please check your .env file and restart the server.")
        return

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "retriever" not in st.session_state:
        st.session_state.retriever = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        if st.session_state.conversation and st.session_state.retriever:
            handle_userinput(user_question)
        else:
            st.warning("Please upload and process your PDFs first.")

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'",
            accept_multiple_files=True
        )
        if st.button("Process"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF file.")
            else:
                with st.spinner("Processing documents..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vectorstore(text_chunks)

                    st.session_state.retriever = vectorstore.as_retriever()
                    st.session_state.conversation = get_qa_chain()
                    st.success("Documents processed successfully! You can now ask questions.")


if __name__ == '__main__':
    main()