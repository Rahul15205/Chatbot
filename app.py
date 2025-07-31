import streamlit as st
import groq
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Groq configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Fallback responses for when API is not available
FALLBACK_RESPONSES = {
    "greeting": "Hello! I'm TalentScout's AI assistant. I'm here to help with your screening process. Please tell me about yourself and your experience.",
    "info_collection": "Thank you for sharing that information. Could you please provide your full name, email address, and phone number?",
    "tech_stack": "Great! Could you tell me about your tech stack and current location?",
    "technical_questions": "I'll generate some technical questions based on your skills. What specific technologies are you most experienced with?",
    "farewell": "Thank you for your time! Your information has been recorded and our team will review your profile."
}

# Page configuration
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/talentscout-chatbot',
        'Report a bug': 'https://github.com/yourusername/talentscout-chatbot/issues',
        'About': '# TalentScout Hiring Assistant\nAn AI-powered recruitment screening chatbot.'
    }
)

# Simplified CSS for better compatibility
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    
    /* Container styling */
    .main .block-container {
        background: transparent !important;
        padding-top: 1rem !important;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.5rem !important;
        color: white !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
    }
    
    .sub-header {
        font-size: 1.2rem !important;
        color: #f8fafc !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    /* Chat container styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
        padding: 10px !important;
        margin: 8px 0 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    
    /* Message bubbles */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        padding: 12px 18px !important;
        border-radius: 18px 18px 4px 18px !important;
        margin: 8px 0 !important;
        text-align: right !important;
        max-width: 75% !important;
        margin-left: auto !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    .bot-message {
        background: #f8fafc !important;
        color: #1e293b !important;
        padding: 12px 18px !important;
        border-radius: 18px 18px 18px 4px !important;
        margin: 8px 0 !important;
        text-align: left !important;
        max-width: 75% !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Status indicator */
    .status-indicator {
        display: inline-block !important;
        width: 8px !important;
        height: 8px !important;
        border-radius: 50% !important;
        margin-right: 8px !important;
        background-color: #10b981 !important;
        animation: pulse 2s infinite !important;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Progress bar */
    .progress-container {
        width: 100%;
        background-color: #e2e8f0;
        border-radius: 8px;
        padding: 2px;
        margin: 10px 0;
    }
    
    .progress-bar {
        height: 6px;
        background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
        border-radius: 6px;
        transition: width 0.3s ease;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Simplified chat input styling */
    .stChatInput {
        margin-top: 20px !important;
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    
    .stChatInput input {
        border: none !important;
        background: transparent !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        color: #1e293b !important;
    }
    
    .stChatInput input:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    .stChatInput input::placeholder {
        color: #64748b !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(15, 23, 42, 0.8) !important;
    }
    
    /* Text colors for better contrast */
    .stText, .stMarkdown {
        color: #f8fafc !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header { font-size: 2rem; }
        .user-message, .bot-message { max-width: 85%; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'candidate_info' not in st.session_state:
    st.session_state.candidate_info = {}
if 'conversation_ended' not in st.session_state:
    st.session_state.conversation_ended = False
if 'tech_stack' not in st.session_state:
    st.session_state.tech_stack = []
if 'technical_questions' not in st.session_state:
    st.session_state.technical_questions = []

def get_ai_response(messages, system_prompt):
    """Get response from Groq API"""
    try:
        # Initialize Groq client with proper error handling
        if not GROQ_API_KEY:
            return "Error: GROQ_API_KEY not configured"
        
        client = groq.Groq(api_key=GROQ_API_KEY)
        
        # Prepare messages with system prompt
        api_messages = [{"role": "system", "content": system_prompt}]
        api_messages.extend(messages)
        
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=api_messages,
            max_tokens=500,
            temperature=0.7
        )
        
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
        else:
            return "I apologize, but I received an empty response. Please try again."
            
    except Exception as e:
        error_msg = str(e)
        if "proxies" in error_msg:
            return "I apologize, but there's a configuration issue with the API client. Please check your deployment settings."
        elif "api_key" in error_msg.lower():
            return "I apologize, but there's an issue with the API key configuration. Please check your Streamlit secrets."
        else:
            return f"I apologize, but I'm experiencing technical difficulties. Please try again later. Error: {error_msg}"

def extract_candidate_info(message):
    """Extract candidate information from the conversation"""
    system_prompt = """
    You are an AI assistant helping to extract candidate information from conversations.
    Extract the following information if mentioned:
    - Full Name
    - Email Address
    - Phone Number
    - Years of Experience
    - Desired Position(s)
    - Current Location
    - Tech Stack
    
    Return the information in JSON format. If information is not available, use null.
    """
    
    try:
        if not GROQ_API_KEY:
            return {}
            
        client = groq.Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=300,
            temperature=0.3
        )
        
        if response.choices and len(response.choices) > 0:
            return json.loads(response.choices[0].message.content)
        else:
            return {}
    except Exception as e:
        st.error(f"Error extracting candidate info: {str(e)}")
        return {}

def generate_technical_questions(tech_stack):
    """Generate technical questions based on tech stack"""
    if not tech_stack:
        return []
    
    system_prompt = f"""
    You are a technical interviewer. Based on the following tech stack: {', '.join(tech_stack)}
    Generate 3-5 relevant technical questions for each technology mentioned.
    Format the response as a JSON array with objects containing 'technology' and 'questions' fields.
    Make questions appropriate for the specified experience level.
    """
    
    try:
        if not GROQ_API_KEY:
            return []
            
        client = groq.Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Generate technical questions for this tech stack."}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        if response.choices and len(response.choices) > 0:
            return json.loads(response.choices[0].message.content)
        else:
            return []
    except Exception as e:
        st.error(f"Error generating technical questions: {str(e)}")
        return []

def check_conversation_end(message):
    """Check if the conversation should end"""
    end_keywords = ['goodbye', 'bye', 'end', 'finish', 'complete', 'done', 'exit', 'quit']
    return any(keyword in message.lower() for keyword in end_keywords)

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 TalentScout Hiring Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your AI-powered recruitment screening partner (Powered by Groq)</p>', unsafe_allow_html=True)
    
    # Status indicator
    if GROQ_API_KEY:
        st.markdown('<div style="text-align: center; margin: 10px 0;"><span class="status-indicator"></span>AI Assistant Online</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align: center; margin: 10px 0; color: #ef4444;">⚠️ AI Assistant Offline</div>', unsafe_allow_html=True)
    
    # Check if API key is set
    if not GROQ_API_KEY:
        st.error("⚠️ GROQ_API_KEY not found in .env file. Please add your Groq API key.")
        st.info("Get your free API key from: https://console.groq.com/")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Candidate Information")
        if st.session_state.candidate_info:
            for key, value in st.session_state.candidate_info.items():
                if value:
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        if st.session_state.tech_stack:
            st.header("🛠️ Tech Stack")
            for tech in st.session_state.tech_stack:
                st.write(f"• {tech}")
        
        if st.session_state.technical_questions:
            st.header("❓ Technical Questions")
            for q_set in st.session_state.technical_questions:
                if isinstance(q_set, dict) and 'technology' in q_set:
                    st.write(f"**{q_set['technology']}:**")
                    for i, question in enumerate(q_set.get('questions', []), 1):
                        st.write(f"{i}. {question}")
        
        # Progress bar
        if st.session_state.messages:
            progress = min(len(st.session_state.messages) / 10 * 100, 100)
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress}%;"></div>
            </div>
            <p style="text-align: center; font-size: 12px; color: #64748b;">
                Conversation Progress: {int(progress)}%
            </p>
            """, unsafe_allow_html=True)
        
        # Reset button
        if st.button("🔄 Reset Conversation"):
            st.session_state.messages = []
            st.session_state.candidate_info = {}
            st.session_state.conversation_ended = False
            st.session_state.tech_stack = []
            st.session_state.technical_questions = []
            st.rerun()
    
    # Chat interface
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display messages
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: #64748b;">
            <h3>👋 Welcome to TalentScout!</h3>
            <p>Start your screening process by introducing yourself.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    if not st.session_state.conversation_ended:
        user_input = st.chat_input("Type your message here...")
        
        if user_input:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Check for conversation end
            if check_conversation_end(user_input):
                st.session_state.conversation_ended = True
                farewell_message = """
                Thank you for your time! Your information has been recorded and our team will review your profile.
                
                **Next Steps:**
                - You will receive a confirmation email within 24 hours
                - Our technical team will review your responses
                - We'll schedule a follow-up interview if your profile matches our requirements
                
                Have a great day! 👋
                """
                st.session_state.messages.append({"role": "assistant", "content": farewell_message})
                st.rerun()
            
            # Generate AI response
            system_prompt = """
            You are TalentScout's AI Hiring Assistant, a friendly and professional chatbot designed to screen candidates for technology positions.
            
            Your responsibilities:
            1. Greet candidates warmly and explain your purpose
            2. Collect essential candidate information (name, email, phone, experience, desired position, location, tech stack)
            3. Generate relevant technical questions based on their tech stack
            4. Maintain a professional, helpful, and engaging conversation
            5. End the conversation gracefully when the candidate says goodbye or similar
            
            Guidelines:
            - Be professional but friendly
            - Ask one question at a time to avoid overwhelming the candidate
            - If tech stack is mentioned, generate 3-5 technical questions for each technology
            - Keep responses concise but informative
            - Always maintain context of the conversation
            """
            
            ai_response = get_ai_response(st.session_state.messages, system_prompt)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            # Extract candidate information
            candidate_info = extract_candidate_info(user_input)
            if candidate_info:
                st.session_state.candidate_info.update(candidate_info)
            
            # Extract tech stack and generate questions
            if 'tech_stack' in candidate_info and candidate_info['tech_stack']:
                if isinstance(candidate_info['tech_stack'], list):
                    st.session_state.tech_stack = candidate_info['tech_stack']
                else:
                    st.session_state.tech_stack = [candidate_info['tech_stack']]
                
                if st.session_state.tech_stack and not st.session_state.technical_questions:
                    questions = generate_technical_questions(st.session_state.tech_stack)
                    if questions:
                        st.session_state.technical_questions = questions
            
            st.rerun()
    else:
        st.info("💬 Conversation ended. Click 'Reset Conversation' in the sidebar to start a new session.")
        
        # Show collected data in a more visible way
        if st.session_state.candidate_info or st.session_state.tech_stack or st.session_state.technical_questions:
            st.markdown("### 📊 Collected Information Summary")
            
            # Create a structured display of collected data
            collected_data = {
                "Candidate Information": st.session_state.candidate_info,
                "Tech Stack": st.session_state.tech_stack,
                "Technical Questions": st.session_state.technical_questions,
                "Conversation Summary": {
                    "Total Messages": len(st.session_state.messages),
                    "Ended At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            
            # Display as JSON in a code block
            st.json(collected_data)
            
            # Also show in expandable sections
            with st.expander("📋 View Raw JSON Data"):
                st.code(json.dumps(collected_data, indent=2), language="json")
    
    # Information box
    with st.expander("ℹ️ About TalentScout Hiring Assistant"):
        st.markdown("""
        **Welcome to TalentScout's AI-powered hiring assistant!**
        
        This intelligent chatbot is designed to:
        - 🤝 Provide a warm welcome and explain the screening process
        - 📝 Collect essential candidate information efficiently
        - 🛠️ Assess technical skills through relevant questions
        - 📊 Maintain conversation context for seamless interactions
        - 🎯 Generate personalized technical questions based on your tech stack
        
        **How it works:**
        1. Start by introducing yourself and sharing your experience
        2. Provide your contact information and desired position
        3. Share your tech stack and current location
        4. Answer technical questions tailored to your skills
        5. Complete the screening process
        
        Your information is handled securely and in compliance with data privacy standards.
        
        **Powered by Groq AI** - Fast, free, and reliable AI processing.
        """)

if __name__ == "__main__":
    main() 