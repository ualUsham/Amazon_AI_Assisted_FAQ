import streamlit as st
from PIL import Image
from helper_code import get_answer
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
