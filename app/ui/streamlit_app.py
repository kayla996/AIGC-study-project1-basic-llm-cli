import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/rag/chat"

st.set_page_config(page_title="Enterprise RAG Assistant", layout="wide")

st.title("Enterprise RAG Assistant")
st.caption("Ask questions based on your local knowledge base.")

question = st.text_input("Question", placeholder="Ask something about the documents...")

top_k = st.slider("Top K", min_value=1, max_value=5, value=3)

if st.button("Ask") and question.strip():
    with st.spinner("Retrieving and generating answer..."):
        response = requests.post(
            API_URL,
            json={"question": question, "top_k": top_k},
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        # st.write(data)

    st.subheader("Answer")
    st.write(data["answer"])

    st.subheader("Sources")
    for i, source in enumerate(data["source"], start=1):
        with st.expander(f"Source {i} | score={source['score']:.4f} | {source['source_id']}"):
            st.write(source["text"])