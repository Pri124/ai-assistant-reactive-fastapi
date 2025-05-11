import streamlit as st
import requests
import time
from datetime import datetime
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
import shutil


st.set_page_config(page_title="AI Chatbot Agents", layout="wide")


if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "avatar" not in st.session_state:
    st.session_state.avatar = "🤖"


st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

        /* Theme-based styling */
        .stApp {{
            background: { 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)' if st.session_state.theme == 'dark' else 'linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%)' };
            color: { '#e0e0e0' if st.session_state.theme == 'dark' else '#1a1a2e' };
            font-family: 'Orbitron', sans-serif;
        }}

        /* Title */
        .title {{
            font-size: 3.5rem;
            color: { '#00d4ff' if st.session_state.theme == 'dark' else '#3b82f6' };
            text-align: center;
            text-shadow: 0 0 10px { '#00d4ff' if st.session_state.theme == 'dark' else '#3b82f6' };
            animation: glow 2s ease-in-out infinite alternate;
        }}

        /* Subtitle */
        .subtitle {{
            font-size: 1.5rem;
            color: { '#b0c4de' if st.session_state.theme == 'dark' else '#4b5563' };
            text-align: center;
            margin-bottom: 30px;
        }}

        /* Input Fields */
        .stTextArea textarea, .stSelectbox select, .stTextInput input {{
            background: { 'rgba(255, 255, 255, 0.1)' if st.session_state.theme == 'dark' else 'rgba(0, 0, 0, 0.05)' };
            border: 2px solid { '#00d4ff' if st.session_state.theme == 'dark' else '#3b82f6' };
            border-radius: 10px;
            color: { '#e0e0e0' if st.session_state.theme == 'dark' else '#1a1a2e' };
            padding: 15px;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 0 10px { 'rgba(0, 212, 255, 0.3)' if st.session_state.theme == 'dark' else 'rgba(59, 130, 246, 0.3)' };
        }}

        .stTextArea textarea:focus, .stSelectbox select:focus, .stTextInput input:focus {{
            border-color: { '#ff00ff' if st.session_state.theme == 'dark' else '#ec4899' };
            box-shadow: 0 0 15px { 'rgba(255, 0, 255, 0.5)' if st.session_state.theme == 'dark' else 'rgba(236, 72, 153, 0.5)' };
        }}

        /* Buttons */
        .stButton button {{
            background: linear-gradient(45deg, { '#00d4ff, #ff00ff' if st.session_state.theme == 'dark' else '#3b82f6, #ec4899' });
            border: none;
            border-radius: 25px;
            padding: 12px 30px;
            font-size: 1.2rem;
            color: #fff;
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 0 15px { 'rgba(0, 212, 255, 0.5)' if st.session_state.theme == 'dark' else 'rgba(59, 130, 246, 0.5)' };
            width: 100%;
            animation: bounce 0.5s ease-in-out infinite alternate;
        }}

        .stButton button:hover {{
            transform: scale(1.05);
            box-shadow: 0 0 25px { 'rgba(255, 0, 255, 0.7)' if st.session_state.theme == 'dark' else 'rgba(236, 72, 153, 0.7)' };
        }}

        /* Checkbox and Radio */
        .stCheckbox input, .stRadio input {{
            accent-color: { '#00d4ff' if st.session_state.theme == 'dark' else '#3b82f6' };
            transform: scale(1.5);
        }}

        /* Sidebar */
        .stSidebar {{
            background: { 'rgba(255, 255, 255, 0.05)' if st.session_state.theme == 'dark' else 'rgba(0, 0, 0, 0.05)' };
            border-right: 1px solid { '#00d4ff' if st.session_state.theme == 'dark' else '#3b82f6' };
            box-shadow: 0 0 10px { 'rgba(0, 212, 255, 0.2)' if st.session_state.theme == 'dark' else 'rgba(59, 130, 246, 0.2)' };
        }}

        /* Response Container */
        .response-container {{
            background: { 'linear-gradient(45deg, rgba(0, 212, 255, 0.1), rgba(255, 0, 255, 0.1))' if st.session_state.theme == 'dark' else 'linear-gradient(45deg, rgba(59, 130, 246, 0.1), rgba(236, 72, 153, 0.1))' };
            border: 2px solid { '#00d4ff' if st.session_state.theme == 'dark' else '#3b82f6' };
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 0 20px { 'rgba(0, 212, 255, 0.3)' if st.session_state.theme == 'dark' else 'rgba(59, 130, 246, 0.3)' };
            animation: fadeIn 1s ease-in;
            position: relative;
            overflow: hidden;
        }}

        .response-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
            opacity: 0.3;
            z-index: -1;
        }}

        /* Feedback Buttons */
        .feedback-button {{
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            margin: 0 10px;
            transition: transform 0.3s ease;
        }}

        .feedback-button:hover {{
            transform: scale(1.2);
        }}

        /* Typing Indicator */
        .typing-indicator {{
            display: flex;
            justify-content: center;
            margin: 10px 0;
        }}

        .typing-indicator span {{
            height: 12px;
            width: 12px;
            background-color: { '#00d4ff' if st.session_state.theme == 'dark' else '#3b82f6' };
            border-radius: 50%;
            display: inline-block;
            margin: 0 6px;
            animation: typing 1s infinite;
        }}

        .typing-indicator span:nth-child(2) {{ animation-delay: 0.2s; }}
        .typing-indicator span:nth-child(3) {{ animation-delay: 0.4s; }}

        /* Animations */
        @keyframes glow {{
            from {{ text-shadow: 0 0 10px { '#00d4ff' if st.session_state.theme == 'dark' else '#3b82f6' }; }}
            to {{ text-shadow: 0 0 20px { '#ff00ff' if st.session_state.theme == 'dark' else '#ec4899' }; }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes bounce {{
            from {{ transform: translateY(0); }}
            to {{ transform: translateY(-5px); }}
        }}

        @keyframes typing {{
            0% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-12px); }}
            100% {{ transform: translateY(0); }}
        }}

        /* Footer */
        .footer {{
            text-align: center;
            color: { '#b0c4de' if st.session_state.theme == 'dark' else '#4b5563' };
            margin-top: 50px;
            font-size: 0.9rem;
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            .title {{ font-size: 2.5rem; }}
            .stTextArea textarea, .stSelectbox select, .stTextInput input {{
                font-size: 1rem;
                padding: 10px;
            }}
            .stButton button {{
                padding: 10px 20px;
                font-size: 1rem;
            }}
        }}
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="title">AI Chatbot Agents</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Experience the Future of AI Interaction!</div>', unsafe_allow_html=True)


with st.sidebar:
    st.header("Agent Configuration")
    
   
    avatar_options = ["🤖", "🚀", "🧠", "🌟"]
    st.session_state.avatar = st.selectbox("Choose AI Avatar:", avatar_options, index=avatar_options.index(st.session_state.avatar))
    
    
    theme = st.checkbox("Light Theme", value=st.session_state.theme == "light", key="theme_toggle")
    st.session_state.theme = "light" if theme else "dark"
    
   
    system_prompt = st.text_area(
        "System Prompt:",
        height=100,
        placeholder="Define the behavior of your AI agent...",
        key="system_prompt"
    )
    

    MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
    MODEL_NAMES_OPENAI = ["gpt-4o-mini"]
    provider = st.radio("Model Provider:", ("Groq", "OpenAI"), key="provider")
    if provider == "Groq":
        selected_model = st.selectbox("Groq Model:", MODEL_NAMES_GROQ, key="groq_model")
    else:
        selected_model = st.selectbox("OpenAI Model:", MODEL_NAMES_OPENAI, key="openai_model")
    
    
    allow_web_search = st.checkbox("Enable Web Search", key="web_search")

    with st.expander("Conversation History"):
        if st.session_state.conversation_history:
            for i, (query, response) in enumerate(st.session_state.conversation_history):
                st.markdown(f"**Q{i+1}:** {query[:50]}...")
                st.markdown(f"**A{i+1}:** {response[:50] if response else 'Pending'}...")
        else:
            st.write("No history yet.")


st.markdown(f"### Ask Your AI Agent {st.session_state.avatar}")
col1, col2 = st.columns([3, 1])
with col1:
    user_query = st.text_area(
        "Your Query:",
        height=150,
        placeholder="Type your question or task here...",
        key="user_query"
    )
with col2:

    st.markdown("**Voice Input**")
    st.write("Record audio using an external app and upload the file (WAV or MP3).")
    audio_file = st.file_uploader("Upload Audio Query:", type=["wav", "mp3"], key="audio_upload")
    if audio_file:
        try:
            
            if not shutil.which("ffmpeg"):
                st.error("FFmpeg is not installed or not in PATH. Please install FFmpeg and add it to your system PATH.")
                st.markdown("[Download FFmpeg](https://ffmpeg.org/download.html) or [Windows Builds](https://www.gyan.dev/ffmpeg/builds/)")
            else:
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_input:
                    temp_input.write(audio_file.read())
                    temp_input_path = temp_input.name
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
                    temp_wav_path = temp_wav.name
                
                
                audio = AudioSegment.from_file(temp_input_path)
                audio.export(temp_wav_path, format="wav")
                
               
                recognizer = sr.Recognizer()
                with sr.AudioFile(temp_wav_path) as source:
                    audio_data = recognizer.record(source)
                    transcribed_text = recognizer.recognize_google(audio_data)
                    st.text_area("Transcribed Query:", value=transcribed_text, height=50, key="transcribed_query")
                    user_query = transcribed_text  
                
                
                os.unlink(temp_input_path)
                os.unlink(temp_wav_path)
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Please try a clearer recording.")
        except sr.RequestError as e:
            st.error(f"Speech recognition error: {str(e)}. Check your internet connection.")
        except Exception as e:
            st.error(f"Error processing audio: {str(e)}. Ensure FFmpeg is installed and the audio file is valid.")


col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Ask Agent!", key="ask_button"):
        if user_query.strip():
            
            st.session_state.conversation_history.append((user_query, ""))
            
            
            st.markdown('<div class="typing-indicator"><span></span><span></span><span></span></div>', unsafe_allow_html=True)
            time.sleep(1.5) 
            
           
            API_URL = "http://127.0.0.1:9999/chat"
            payload = {
                "model_name": selected_model,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_web_search
            }
            
            with st.spinner("Processing your query..."):
                try:
                    response = requests.post(API_URL, json=payload)
                    if response.status_code == 200:
                        response_data = response.json()
                        st.markdown('<div class="response-container">', unsafe_allow_html=True)
                        st.markdown(f"### {st.session_state.avatar} Agent Response")
                        
                        if "error" in response_data:
                            st.error(response_data["error"])
                        else:
                           
                            st.markdown(f"""
                                <div style='padding: 10px; border-left: 4px solid {"#ff00ff" if st.session_state.theme == "dark" else "#ec4899"};'>
                                    <strong>Answer:</strong> {response_data}<br>
                                    {"<strong>Source:</strong> Web Search (Dynamic)" if allow_web_search else ""}
                                </div>
                            """, unsafe_allow_html=True)
                            
                            
                            st.session_state.conversation_history[-1] = (user_query, str(response_data))
                            
                            #
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("👍", key=f"thumbs_up_{len(st.session_state.conversation_history)}", help="Rate as helpful"):
                                    st.success("Thanks for your feedback!")
                            with col2:
                                if st.button("👎", key=f"thumbs_down_{len(st.session_state.conversation_history)}", help="Rate as unhelpful"):
                                    st.warning("Sorry, we'll improve!")
                            
                            
                            st.markdown("**Suggested Follow-ups:**")
                            quick_replies = ["Can you elaborate?", "Give me more details", "Try a different approach"]
                            for reply in quick_replies:
                                if st.button(reply, key=f"quick_reply_{reply}_{len(st.session_state.conversation_history)}"):
                                    st.text_area("Your Query:", value=reply, height=50, key=f"quick_reply_input_{reply}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.balloons()  
                    else:
                        st.error(f"API Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Error connecting to API: {str(e)}")
        else:
            st.warning("Please enter a query!")


current_time = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
st.markdown(f'<div class="footer">Powered by Priyanshu Patil | Built with Streamlit | Current Time: {current_time}</div>', unsafe_allow_html=True)