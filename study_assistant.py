# Install dependencies:
# pip install streamlit langchain-groq SpeechRecognition gTTS pyaudio python-dotenv PyPDF2

import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
import speech_recognition as sr
from gtts import gTTS
import os
from dotenv import load_dotenv
import PyPDF2

# 🔑 Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY missing! Add it in .env file.")
    st.stop()

# --- LLM Setup (Groq models: llama3-8b-8192, llama3-70b-8192, gemma-7b-it, mixtral-8x7b-32768) ---
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"   # ✅ Supported model
)

# --- Memory for chat history ---
memory = ConversationBufferMemory(return_messages=True)

st.title("🎙️ AI Voice & PDF Study Assistant (LangChain + Groq)")
st.write("Upload, speak, or type notes. AI will summarize, quiz, and even create flashcards with memory!")

# ---- Speech to Text ----
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("❌ Sorry, I couldn't understand.")
        return ""
    except sr.RequestError:
        st.error("❌ Speech Recognition service error.")
        return ""

# ---- Text to Speech ----
def text_to_speech(text, filename="output.mp3"):
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename

# ---- PDF Reader ----
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# ---- Input Options ----
st.subheader("Choose Input Method")
input_mode = st.radio("Select:", ["📝 Type Notes", "🎤 Speak Notes", "📄 Upload PDF"])

notes = ""
if input_mode == "📝 Type Notes":
    notes = st.text_area("Paste your study notes here:", height=200)

elif input_mode == "🎤 Speak Notes":
    if st.button("🎙️ Start Recording"):
        notes = speech_to_text()

elif input_mode == "📄 Upload PDF":
    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    if uploaded_file is not None:
        notes = extract_text_from_pdf(uploaded_file)
        st.success("✅ PDF uploaded and text extracted!")

study_hours = st.slider("⏳ How many hours to study today?", 1, 12, 3)

# ---- Generate Study Help ----
if st.button("Generate Study Help"):
    if notes.strip() == "":
        st.warning("Please provide some notes or upload a PDF!")
    else:
        # --- Prompts with LangChain ---
        summary_prompt = ChatPromptTemplate.from_template(
            "Summarize the following notes in 5-6 easy bullet points:\n\n{notes}"
        )
        quiz_prompt = ChatPromptTemplate.from_template(
            "Create 5 quiz questions (with answers) from the following notes:\n\n{notes}"
        )
        flash_prompt = ChatPromptTemplate.from_template(
            "Convert these notes into 5 flashcards (Q&A format):\n\n{notes}"
        )
        schedule_prompt = ChatPromptTemplate.from_template(
            "Create a {hours}-hour study plan using these notes. Divide into sessions with breaks:\n\n{notes}"
        )

        # --- Generate outputs ---
        summary = llm.invoke(summary_prompt.format(notes=notes))
        quiz = llm.invoke(quiz_prompt.format(notes=notes))
        flashcards = llm.invoke(flash_prompt.format(notes=notes))
        schedule = llm.invoke(schedule_prompt.format(notes=notes, hours=study_hours))

        # --- Display results ---
        st.subheader("📌 Summary")
        summary_text = summary.content
        st.write(summary_text)

        st.subheader("❓ Quiz Questions")
        quiz_text = quiz.content
        st.write(quiz_text)

        st.subheader("📝 Flashcards")
        flash_text = flashcards.content
        st.write(flash_text)

        st.subheader("⏰ Study Schedule")
        sched_text = schedule.content
        st.write(sched_text)

        # --- Voice Output ---
        if st.button("🔊 Read Aloud Summary"):
            filename = text_to_speech(summary_text)
            audio_file = open(filename, "rb")
            st.audio(audio_file, format="audio/mp3")
