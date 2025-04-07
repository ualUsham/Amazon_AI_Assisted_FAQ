# Import necessary modules
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import streamlit as st
from PIL import Image
import traceback
import os

# ========== API Key Handling ==========
if "google_api_key" not in st.session_state:
    st.session_state.google_api_key = st.secrets.get("GOOGLE_API_KEY", "")

# ========== Embeddings ==========
embed = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=st.session_state.google_api_key
)

# ========== Cache FAISS Vector Store ==========
@st.cache_resource
def load_vector_store(index_path):
    if os.path.exists(index_path):
        return FAISS.load_local(index_path, embeddings=embed, allow_dangerous_deserialization=True)
    return None

# ========== Answer Retrieval ==========
def get_answer(query):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=st.session_state.google_api_key)

    system_prompt = (
    "You are an assistant that answers user questions using the provided context. "
    "Respond concisely in less than 10 sentences. If possible, provide stepwise instructions. "
    "If the answer is not found in context, say so.\n\nContext:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

for i in range(4):
    index_path = f"amazon_vdb_chunk_{i}"
    vdb = load_vector_store(index_path)
    if vdb is None:
        continue

    retriever = vdb.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={'score_threshold': 0.2}
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, question_answer_chain)

    result = chain.invoke({"input": query})
    
    # Debug: Inspect the result
    st.write("DEBUG: Chain output:", result)
    
    # Check if the key 'result' exists in the output
    return result["answer"]

# If no valid answer is found
return "Please go to the Amazon website for more details because your question is not a part of Amazon FAQ."


# ========== Streamlit UI Starts Here ==========

# Image
image = Image.open("amazon.jpeg")
st.image(image, width=750)

# Title
st.markdown(
    "<h1 style='text-align: center;'>Amazon <span style='color:#f7a805;'>AI-Assisted</span> FAQ</h1>",
    unsafe_allow_html=True
)

# Input
st.markdown(
    "<h4 style='color:#ff4b4b;font-family:Source Sans Pro; font-weight:bold'>Query :</h4>",
    unsafe_allow_html=True
)
question = st.text_input(label="Question", placeholder="Ask a question.....How to apply coupons?", label_visibility="collapsed")

# Answer display function
def ans_template(answer):
    st.markdown(
        "<h4 style='color:#00A300;font-family:Source Sans Pro; font-weight:bold'>Answer :</h4>",
        unsafe_allow_html=True
    )
    st.write(answer)
    st.write("\n\n\n")
    st.write("**Disclaimer**: This information is based on the FAQ provided by the [Amazon website Help Centre](https://www.amazon.in/gp/help/customer/display.html).")
    st.write("Please cross-check with the [Amazon website](https://www.amazon.in) in case any confusion arises.")

# Answer logic
if question:
    try:
        answer = get_answer(question)
        ans_template(answer)
    except Exception:
        st.markdown(
            "<h4 style='color:#f7a805;font-family:Source Sans Pro; font-weight:bold'>API Required !!</h4>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#2f2e2a;font-family:Arial; font-size:18px; font-weight:bold' >Run this App in just 3 steps : </p>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:18px'>1. Click here: <a href='https://aistudio.google.com/app/u/1/apikey' target='_blank'>Create Google API key</a></p>",
            unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px'>2. Create API key of your Google account. </p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:18px'>3. Copy & Paste your API key below. </p>", unsafe_allow_html=True)

        user_api = st.text_input(label="user_api", placeholder="Your API key ...", label_visibility="collapsed")
        if user_api:
            st.session_state.google_api_key = user_api
            try:
                answer = get_answer(question)
                ans_template(answer)
            except Exception:
                st.markdown(
                    "<p style='color:red; font-family:Arial; font-size:18px; font-weight:bold'>Enter a Valid API key !!</p>",
                    unsafe_allow_html=True
                )
                st.code(traceback.format_exc())
