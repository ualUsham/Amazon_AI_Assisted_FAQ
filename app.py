# Import necessary modules
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

# API key
# from dotenv import load_dotenv
# import os
# load_dotenv()
# google_api_key = os.getenv("GOOGLE_API_KEY")
google_api_key = st.secrets["GOOGLE_API_KEY"]


# Create an embedding object
embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Function to get answers using FAISS
def get_answer(query):
    # Call LLM model
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=google_api_key)
    except:
        return st.write("Enter a Valid API key")
    
    system_prompt = (
        "Use the context to answer the question. "
        "If you know the answer, keep the answer concise (maximum 10 sentences)."
        "Give the answer in stepwise if possible."
        "Context: {context}"
    )

    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    for i in range(4):
        # Load the FAISS vector database
        vdb = FAISS.load_local(f"amazon_vdb_chunk_{i}", embeddings=embed, allow_dangerous_deserialization=True)
        retriever = vdb.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={'score_threshold': 0.3}
        )

        # Create the chain with the retriever and stuff documents chain
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        chain = create_retrieval_chain(retriever, question_answer_chain)
        
        # Invoke the chain with the input query
        result = chain.invoke({"input": query})
        
        # Check the result for the context and answer
        if result.get("context"):
            return result["answer"]

    return "Please go to the Amazon website for more details because your question is not a part of Amazon FAQ."

#Streamlit code starts here.........................................


from PIL import Image
#f7a805 #yellow
#2f2e2a #black
#ff4b4b #red
#00A300 #green
#image
image = Image.open("amazon.jpeg")
st.image(image, width=750) 

#title
st.markdown(
    "<h1 style='text-align: center;'>Amazon <span style='color:#f7a805;'>AI-Assisted</span> FAQ</h1>", 
    unsafe_allow_html=True
)

#input
st.markdown(
    "<h4 style='color:#ff4b4b;font-family:Source Sans Pro; font-weight:bold'>Query :</h4>", 
    unsafe_allow_html=True)
question=st.text_input(label="Question",placeholder="Write a question.....How to apply coupons?", label_visibility="collapsed")

#answer template function
def ans_template():
    st.markdown(
    "<h4 style='color:#00A300;font-family:Source Sans Pro; font-weight:bold'>Answer :</h4>", 
    unsafe_allow_html=True)
    st.write(answer)
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("**Disclaimer**: This information is based on the FAQ provided by the [Amazon website Help Centre](https://www.amazon.in/gp/help/customer/display.html).")
    st.write("Please cross-check with the [Amazon website](https://www.amazon.in) in case any confusion arises.")
#answer
if question:
    try:
        answer = get_answer(question)
        ans_template()
    except:
        st.markdown(
            "<h4 style='color:#f7a805;font-family:Source Sans Pro; font-weight:bold'>API Required !!</h4>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#2f2e2a;font-family:Arial; font-size:18px; font-weight:bold' >Run this App in just 3 steps : </p>", unsafe_allow_html=True)
        st.markdown(
    "       <p style='font-size:18px'>1. Click here: <a href='https://aistudio.google.com/app/u/1/apikey' target='_blank'>Create Google API key</a></p>", 
            unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:18px'>2. Create API key of your Google account. </p>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:18px'>3. Copy & Paste your API key below. </p>", unsafe_allow_html=True)
        user_api=st.text_input(label="user_api", placeholder="Your API key ...",label_visibility="collapsed")
        if user_api:
            google_api_key=user_api
            answer = get_answer(question)
            ans_template()
        

    
