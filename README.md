# Amazon AI-Assisted FAQ Chatbot

This repository contains the code for an AI-powered FAQ chatbot designed for Amazon customers. It uses **Retrieval-Augmented Generation (RAG)** techniques to assist users with queries based on Amazon FAQs.

---

## 🌐 Access the App
👉 **To use the app, go to the link:** [Amazon AI-Assisted FAQ Chatbot](https://amazon-ai-assisted-faq.streamlit.app/)  

---

## 🚀 Implementation Instructions

Follow these steps to run the project locally:

### Requirements  
Install the necessary dependencies:  
```cmd
pip install -r requirements.txt

###**Suggested to use a virtual environment**

📂 Code Files
streamlit_code.py: Contains the code for the Streamlit-based UI.
helper_code.py: Implements RAG using LLM, LangChain, embeddings, and the vector database.
app.py: Combines the functionalities to run and deploy the complete project.

🛠 Tools Used
LLM: Google’s “Gemini-1.5-Flash”
Embeddings: HuggingFace Instructor Embeddings
Vector Database & Retrieval: FAISS
Integration: LangChain
UI & Deployment: Streamlit
