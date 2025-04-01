import os
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()


# Load and process the student handbook PDF
def load_student_handbook(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    
    return chunks

# Create vector store from document chunks
def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(chunks, embeddings)
    
    return vector_store

# Define the student handbook chatbot prompt
STUDENT_HANDBOOK_QA_TEMPLATE = """
You are an AI assistant with access to a Student Handbook. Your role is to answer student queries accurately and concisely, relying only on the information in the handbook. You provide guidance on policies, academic requirements, campus regulations, qualifications, skills, and other relevant topics covered in the handbook.

Relevant information from the Student Handbook:
{context}

Current conversation:
{chat_history}

Student's question:
{question}

Response Guidelines:
1. Accuracy First - Your response must be based only on the information available in the Student Handbook. Do not generate or infer details beyond what is provided.

2. Transparency - If the handbook does not contain the requested information, clearly state that the information is unavailable.

3. Concise & Professional Tone - Keep your responses clear, professional, and easy to understand. Avoid unnecessary elaboration.

4. Reference Handbook Sections - Where applicable, reference specific sections or pages in the handbook to help students find more details.

Always ensure that your answers align strictly with the handbook content and remain informative, relevant, and helpful."""

# Initialize the student handbook chatbot
def create_student_handbook_chatbot(vector_store):
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    qa_prompt = PromptTemplate.from_template(STUDENT_HANDBOOK_QA_TEMPLATE)
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.environ["GEMINI_API_KEY"],
        temperature=0.2
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

# Global variables to store chatbot instances and conversations
chatbots = {}
conversations = {}

# Initialize the chatbot
def initialize_chatbot():
    print("RAG Chatbot Initializing...")
    
    # Replace with your PDF path
    pdf_path = "chatbot/IITM BS Degree Programme - Student Handbook.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} not found.")
        return None
    
    print("Processing Student Handbook...")
    chunks = load_student_handbook(pdf_path)
    print(f"Student Handbook processed into {len(chunks)} chunks.")
    
    print("Creating vector database...")
    vector_store = create_vector_store(chunks)
    
    print("Initializing chatbot...")
    chatbot = create_student_handbook_chatbot(vector_store)
    
    return chatbot

# Initialize the global chatbot on startup
global_chatbot = initialize_chatbot()

# API Resources
class ChatResource(Resource):
    def post(self):
        if global_chatbot is None:
            return {"error": "Chatbot initialization failed"}, 500
        
        data = request.get_json()
        query = data.get('message', '')
        conversation_id = data.get('conversationId')
        
        if not conversation_id:
            # Create a new conversation
            conversation_id = str(uuid.uuid4())
            conversations[conversation_id] = {
                "id": conversation_id,
                "title": f"Conversation {len(conversations) + 1}",
                "messages": []
            }
            chatbots[conversation_id] = create_student_handbook_chatbot(global_chatbot.retriever.vectorstore)
        
        # Get or create the conversation chatbot
        if conversation_id not in chatbots:
            chatbots[conversation_id] = create_student_handbook_chatbot(global_chatbot.retriever.vectorstore)
        
        # Add user message to conversation history
        user_message = {
            "id": str(uuid.uuid4()),
            "type": "user",
            "text": query,
            "timestamp": ""  # You can add timestamp if needed
        }
        conversations[conversation_id]["messages"].append(user_message)
        
        try:
            # Get response from chatbot
            response = chatbots[conversation_id]({"question": query})
            answer = response['answer']
            
            # Add AI response to conversation history
            ai_message = {
                "id": str(uuid.uuid4()),
                "type": "ai",
                "text": answer,
                "timestamp": ""  # You can add timestamp if needed
            }
            conversations[conversation_id]["messages"].append(ai_message)
            
            return {
                "answer": answer,
                "conversationId": conversation_id,
                "message": ai_message
            }
        except Exception as e:
            print(f"Error: {e}")
            return {"error": str(e)}, 500

class ConversationsResource(Resource):
    def get(self):
        return {"conversations": list(conversations.values())}

class ConversationResource(Resource):
    def get(self, conversation_id):
        if conversation_id in conversations:
            return conversations[conversation_id]
        return {"error": "Conversation not found"}, 404
    
    def post(self):
        # Create a new conversation
        conversation_id = str(uuid.uuid4())
        conversation = {
            "id": conversation_id,
            "title": f"New Conversation {len(conversations) + 1}",
            "messages": []
        }
        conversations[conversation_id] = conversation
        return conversation

    def delete(self, conversation_id):
        if conversation_id in conversations:
            del conversations[conversation_id]
            return {"message": "Conversation deleted successfully"}
        return {"error": "Conversation not found"}, 404
