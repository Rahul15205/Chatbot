# 🤖 TalentScout Hiring Assistant

## 📋 Project Overview

An intelligent AI-powered chatbot designed to streamline the initial screening process for technology recruitment. The chatbot:

- **Greets candidates** warmly and explains the screening process
- **Collects essential information** (name, email, phone, experience, position, location, tech stack)
- **Generates technical questions** based on the candidate's declared tech stack
- **Maintains conversation context** for seamless interactions
- **Ends gracefully** with a professional farewell and next steps

Built with **Streamlit** and powered by **Groq's LLM**, this application provides a seamless candidate experience while efficiently gathering information for recruiters.

## 🚀 Installation Instructions

### Prerequisites
- Python 3.8 or higher
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Step-by-Step Setup

1. **Clone and Navigate**
   ```bash
   git clone <repository-url>
   cd Chatbot
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Key**
   - Get free API key from [console.groq.com](https://console.groq.com)
   - Create `.env` file in project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run Application**
   ```bash
   streamlit run app.py
   ```

6. **Access Application**
   Open browser to `http://localhost:8501`

### Streamlit Cloud Deployment
1. Push code to GitHub repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository and set main file to `app.py`
4. Add Groq API key in secrets section
5. Deploy!

## 📖 Usage Guide

### For Candidates
1. **Start Conversation** - Open the app and begin chatting
2. **Provide Information** - Share your name, experience, and tech stack
3. **Answer Questions** - Respond to technical questions tailored to your skills
4. **Complete Screening** - Say "goodbye" to finish and see collected data

### For Recruiters
1. **Review Information** - Check sidebar for collected candidate details
2. **View Tech Stack** - See candidate's technical skills
3. **Access Questions** - Review generated technical questions
4. **Monitor Progress** - Track conversation completion percentage

## 🛠️ Technical Details

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.8+
- **AI Model**: Groq LLM (llama3-8b-8192)
- **Styling**: Custom CSS for modern UI

### Key Libraries
```
streamlit==1.28.1
groq==0.4.2
python-dotenv==1.0.0
pandas>=2.0.0
numpy>=1.24.0
requests==2.31.0
```

### Architecture
- **Session Management**: Streamlit session state for conversation persistence
- **API Integration**: Groq client for LLM interactions
- **Data Processing**: JSON handling for structured information extraction
- **UI Components**: Custom chat interface with message bubbles

### Data Flow
```
User Input → Validation → Groq API → Response Processing → Information Extraction → UI Update
```

## 🎯 Prompt Design

### System Prompts Strategy

The application uses carefully crafted prompts to ensure consistent behavior:

1. **Main Conversation Prompt**
   ```python
   """
   You are TalentScout's AI Hiring Assistant, a friendly and professional chatbot.
   
   Responsibilities:
   1. Greet candidates warmly and explain purpose
   2. Collect essential candidate information
   3. Generate relevant technical questions
   4. Maintain professional conversation
   5. End gracefully when candidate says goodbye
   
   Guidelines:
   - Be professional but friendly
   - Ask one question at a time
   - Generate 3-5 technical questions per technology
   - Keep responses concise but informative
   - Always maintain conversation context
   """
   ```

2. **Information Extraction Prompt**
   ```python
   """
   Extract the following information if mentioned:
   - Full Name, Email, Phone, Experience, Position, Location, Tech Stack
   
   Return in JSON format. Use null if information not available.
   """
   ```

3. **Technical Questions Prompt**
   ```python
   """
   Generate 3-5 relevant technical questions for each technology mentioned.
   Format as JSON array with 'technology' and 'questions' fields.
   Make questions appropriate for specified experience level.
   """
   ```

### Prompt Optimization
- **Context Preservation**: Maintain conversation history for coherent responses
- **Role Definition**: Clear system role to guide model behavior
- **Format Specification**: Structured output formats for data extraction
- **Error Handling**: Fallback responses for unexpected inputs

## 🔧 Challenges & Solutions

### Challenge 1: API Integration Issues
**Problem**: OpenAI API quota limitations and billing requirements
**Solution**: Switched to Groq API (free tier) with llama3-8b-8192 model

### Challenge 2: UI Styling Problems
**Problem**: "Big white line" issue with Streamlit chat input
**Solution**: Custom CSS targeting `.stChatInput` with proper styling rules

### Challenge 3: Data Extraction Reliability
**Problem**: Inconsistent information extraction from conversation
**Solution**: Combined AI extraction with structured prompts and JSON formatting

### Challenge 4: Conversation Flow
**Problem**: Maintaining context across multiple messages
**Solution**: Session state management with conversation history preservation

### Challenge 5: Deployment Complexity
**Problem**: Complex cloud deployment setup
**Solution**: Streamlit Cloud integration with simple GitHub deployment

### Challenge 6: Error Handling
**Problem**: API failures and unexpected inputs
**Solution**: Try-catch blocks with graceful fallback messages

## 📊 Features Summary

✅ **Core Requirements Met**
- Greeting and information gathering
- Tech stack declaration and technical questions
- Context handling and graceful exit
- Professional UI with Streamlit

✅ **Bonus Features**
- Modern UI with custom styling
- JSON data export at conversation end
- Real-time information extraction
- Responsive design and animations

✅ **Technical Excellence**
- Clean, modular code structure
- Comprehensive error handling
- Free AI integration (Groq)
- Easy deployment to Streamlit Cloud

---

**🎉 Ready for Production!** This chatbot successfully demonstrates LLM integration, prompt engineering, and modern web development skills. 