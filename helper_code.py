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

# Function to chunk data
def chunk_data(data, chunk_size=30):
    chunks = []
    for i in range(0, len(data), chunk_size):
        chunks.append(data[i:i + chunk_size])
    return chunks

# Function to create FAISS vector database
def create_vdb():
    loader = CSVLoader(file_path='amazon_data.csv', source_column="question")
    data = loader.load()
    chunked_data = chunk_data(data)
    
    print("Creating FAISS vector database...")
    for idx, chunk in enumerate(chunked_data):
        vdb = FAISS.from_documents(chunk, embedding=embed)
        vdb.save_local(f"amazon_vdb_chunk_{idx}")
    print("Done creating FAISS vector database.")

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

if __name__ == "__main__":
    
    #create_vdb()
    
    query = "How to use a coupon?"
    print(get_answer(query))
