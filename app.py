# Import necessary modules
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Call LLM model
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key="AIzaSyCxpS4DpYHn8vmDVk04uYDeyIODFpz07hU")

# Create an embedding object
embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Function to get answers using FAISS
def get_answer(query):
    
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

import streamlit as st
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
    "<h5 style='color:#ff4b4b;font-family:Times New Roman; font-weight:bold'>Query:</h5>", 
    unsafe_allow_html=True)
question=st.text_input(label="Question",placeholder="Write a question.....How to apply coupons?", label_visibility="collapsed")


#answer
if question:
    answer = get_answer(question)
    st.markdown(
    "<h5 style='color:#00A300;font-family:Times New Roman; font-weight:bold'>Answer:</h5>", 
    unsafe_allow_html=True)
    st.write(answer)
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("**Disclaimer**: This information is based on the FAQ provided by the [Amazon website Help Centre](https://www.amazon.in/gp/help/customer/display.html).")
    st.write("Please cross-check with the [Amazon website](https://www.amazon.in) in case any confusion arises.")
