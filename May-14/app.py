import streamlit as st
import pymupdf 
from dotenv import load_dotenv
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.schema import Document


#api configuration
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



#function to extract text from pdf
def extract_text_from_pdf(pdf_docs):
    all_text = ""  
    for pdf in pdf_docs:
        doc = pymupdf.open(stream=pdf.read(), filetype="pdf")
        for page in doc:
            all_text += page.get_text()
        doc.close()
    return all_text

#Chcunking text
def get_text_chunks(text):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

#embedding in chromadb
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    client = chromadb.PersistentClient(path="chroma_db")  # Save DB locally at 'chroma_db'
    collection = client.get_or_create_collection(name="pdf_texts")

    for i, text in enumerate(text_chunks):
        vector = embeddings.embed_query(text)
        collection.add(
            documents=[text],
            ids=[f"doc_{i}"],
            embeddings=[vector]
        )

#conversatiom
def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Load existing ChromaDB persistent collection
    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_collection(name="pdf_texts")
    
    question_embedding = embeddings.embed_query(user_question)
    
    # Perform similarity search (Chroma natively supports similarity search using embeddings)
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3, 
        include=["documents"]
    )
    
    # Convert retrieved text chunks into Document objects
    raw_docs = results["documents"][0] if results["documents"] else []
    docs = [Document(page_content=doc, metadata={}) for doc in raw_docs]
    

    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )
    
    print(response)
    st.write("Reply: ", response["output_text"])


#main program
def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with PDF using Gemini💁")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = extract_text_from_pdf(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")



if __name__ == "__main__":
    main()
