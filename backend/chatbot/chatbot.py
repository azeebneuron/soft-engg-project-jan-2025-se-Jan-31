import os
import pdfplumber
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Extract text and tables from the student handbook PDF
def load_student_handbook(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()  # Returns a list of Document objects
    
    # Extract tables using pdfplumber and append them as Document objects
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                # Convert each table to plain text format, handling None values
                table_text = "\n".join(["\t".join(map(str, [cell if cell is not None else "" for cell in row])) for row in table])
                documents.append(Document(page_content=table_text, metadata={"source": f"Page {page_number + 1}"}))
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,  # Smaller chunks for detailed indexing
        chunk_overlap=100
    )
    
    # Split documents into smaller chunks while preserving metadata
    chunks = text_splitter.split_documents(documents)
    
    return chunks

# Create vector store from document chunks
def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(chunks, embeddings)
    
    return vector_store

# Define the improved chatbot prompt template
STUDENT_HANDBOOK_QA_TEMPLATE = """
You are an AI assistant with access to a Student Handbook. Your role is to answer student queries accurately and concisely, relying only on the information in the handbook. You can also interpret data from tables in the handbook to answer questions.

Relevant information from the Student Handbook:
{context}

Current conversation:
{chat_history}

Student's question:
{question}

Response Guidelines:
1. Accuracy First - Your response must be based only on the information available in the Student Handbook. Do not generate or infer details beyond what is provided.

2. Transparency - If the handbook does not contain the requested information, clearly state that the information is unavailable.

3. Data Interpretation - If the question pertains to a table, extract relevant data and provide a clear interpretation.

4. Concise & Professional Tone - Keep your responses clear, professional, and easy to understand. Avoid unnecessary elaboration.

5. Reference Handbook Sections - Where applicable, reference specific sections or pages in the handbook to help students find more details.

Always ensure that your answers align strictly with the handbook content and remain informative, relevant, and helpful."""

# Initialize the student_handbook chatbot
def create_student_handbook_chatbot(vector_store):
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    qa_prompt = PromptTemplate.from_template(STUDENT_HANDBOOK_QA_TEMPLATE)
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
        temperature=0.2  # Lower temperature for factual responses
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

# Main function to run the student_handbook chatbot
def main():
    print("RAG Chatbot Initializing...")
    
    pdf_path = "IITM BS Degree Programme - Student Handbook.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} not found.")
        return 
    
    print("Processing Student Handbook...")
    try:
        chunks = load_student_handbook(pdf_path)
        print(f"Student Handbook processed into {len(chunks)} chunks.")
        
        print("Creating vector database...")
        vector_store = create_vector_store(chunks)
        
        print("Initializing chatbot...")
        chatbot = create_student_handbook_chatbot(vector_store)
        
        print("\nStudent Handbook Chatbot Ready! Ask questions about the student handbook (type 'exit' to end)")
        
        while True:
            query = input("\nQuestion: ")
            
            if query.lower() == "exit":
                break
                
            try:
                response = chatbot({"question": query})
                print(f"\nAnswer: {response['answer']}")
            except Exception as e:
                print(f"Error during query processing: {e}")
                
    except Exception as e:
        print(f"Error initializing chatbot: {e}")

if __name__ == "__main__":
    main()
