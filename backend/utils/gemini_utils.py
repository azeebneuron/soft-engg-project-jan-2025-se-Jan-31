import os
import google.generativeai as genai

def initialize_gemini():
    """Initialize the Gemini API."""
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    
    # Directly use gemini-2.0-flash model
    return "gemini-2.0-flash"


def create_lecture_context(lecture_title, transcript):
    """Create a context for the Gemini model with lecture information."""
    context = f"""
    You are a Virtual Teaching Assistant for the lecture: "{lecture_title}".
    
    The lecture transcript is as follows:
    
    {transcript}
    
    Your role is to help students understand the lecture content. For questions directly related to the lecture, 
    provide clear explanations based on the lecture material. 
    
    For general subject questions not directly answered in the lecture:
    1. Guide students to think through the problem step by step 
    2. Provide hints rather than direct solutions
    3. Ask leading questions to help students discover the answer themselves
    4. Relate the question back to lecture concepts when possible
    
    Always be encouraging, supportive, and focus on helping students develop their understanding.
    """
    return context.strip()

def get_gemini_response(model_name, prompt, context=None):
    """Get a response from the Gemini model."""
    model = genai.GenerativeModel(model_name)
    
    try:
        if context:
            chat = model.start_chat(history=[{"role": "user", "parts": [context]}])
            response = chat.send_message(prompt)
        else:
            response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        print(f"Error getting Gemini response: {e}")
        return f"I'm having trouble connecting to my knowledge base. Please try again later. (Error: {str(e)})"