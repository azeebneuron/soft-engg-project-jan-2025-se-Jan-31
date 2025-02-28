import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load and process the resume PDF
def load_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Smaller chunks for resume
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documents)
    
    return chunks

# Create vector store from document chunks
def create_vector_store(chunks):
    # Using Sentence Transformers for embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(chunks, embeddings)
    
    return vector_store

# Define the resume chatbot prompt
RESUME_QA_TEMPLATE = """
You are an AI assistant that has access to a resume. You will answer questions about the person's qualifications, experience, skills, education, and other information contained in their resume.

Relevant information from the resume:
{context}

Current conversation:
{chat_history}

Question: {question}

Your response should:
1. Be concise and accurate, based only on the information in the resume
2. Not make up or infer information that isn't explicitly stated in the resume
3. If asked about something not in the resume, honestly state that the information isn't available
4. Format your response in a professional manner

Respond based solely on the information provided in the resume sections above.
"""

# Initialize the resume chatbot
def create_resume_chatbot(vector_store):
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    qa_prompt = PromptTemplate.from_template(RESUME_QA_TEMPLATE)
    
    # Use Gemini for the language model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.environ["GOOGLE_API_KEY"],
        temperature=0.2  # Lower temperature for more factual responses
    )
    
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": qa_prompt}
    )
    
    return qa_chain

# Main function to run the resume chatbot
def main():
    print("Resume RAG Chatbot Initializing...")
    
    # Get resume path from user
    # Replace this with your resume path
    pdf_path = "RahulSinghResume.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} not found.")
        return
    
    print("Processing resume...")
    chunks = load_resume(pdf_path)
    print(f"Resume processed into {len(chunks)} chunks.")
    
    print("Creating vector database...")
    vector_store = create_vector_store(chunks)
    
    print("Initializing chatbot...")
    chatbot = create_resume_chatbot(vector_store)
    
    print("\nResume Chatbot Ready! Ask questions about the resume (type 'exit' to end)")
    
    while True:
        query = input("\nQuestion: ")
        
        if query.lower() == "exit":
            break
            
        try:
            response = chatbot({"question": query})
            print(f"\nAnswer: {response['answer']}")
        except Exception as e:
            print(f"Error: {e}")
            print("Please make sure your Google API key is set correctly in the .env file.")

if __name__ == "__main__":
    main()