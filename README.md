# 🎙️ AI Voice & PDF Study Assistant (LangChain + Groq)

An **AI-powered study assistant** built with **Streamlit, LangChain, Groq LLMs, and Google Speech APIs**.

This system helps students study smarter by allowing them to:

* 📝 Type notes
* 🎤 Speak notes (Speech-to-Text using Google Speech Recognition)
* 📄 Upload PDFs

The AI can then:

* 📌 Summarize notes
* ❓ Generate quiz questions with answers
* 📝 Create flashcards
* ⏰ Build a personalized study schedule
* 🔊 Read summaries aloud (Text-to-Speech using gTTS)

This project is ideal for **students, self-learners, and exam preparation**.

---

## 🚀 Features

### 🔹 Multiple Input Modes

* Text input (typed notes)
* Voice input via microphone (Google Speech Recognition API)
* PDF upload and text extraction

### 🔹 AI-Powered Learning Tools

* Notes summarization (easy bullet points)
* Quiz generation (with answers)
* Flashcard creation (Q&A format)
* Personalized study schedule based on available hours

### 🔹 Voice Support

* Speech-to-Text using **Google Speech Recognition API**
* Text-to-Speech using **gTTS (Google Text-to-Speech)**

### 🔹 Fast AI Responses

* Uses **Groq LLM API** for text-based AI tasks

---

## 🧠 System Architecture (Important Clarification)

This project uses **multiple AI services**, each for a specific role:

* **Groq LLM**
  Used ONLY for **text generation tasks**:

  * Summarization
  * Quiz generation
  * Flashcards
  * Study schedules

* **Google Speech Recognition API**
  Used for converting **spoken voice into text** (Speech-to-Text)

* **gTTS (Google Text-to-Speech)**
  Used for converting **AI-generated text into audio**

➡️ **Groq is NOT used for voice processing**.

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **LLM Framework**: LangChain
* **LLM Provider**: Groq (Text generation only)
* **Speech-to-Text**: Google Speech Recognition API
* **Text-to-Speech**: gTTS (Google Text-to-Speech)
* **PDF Processing**: PyPDF2
* **Environment Management**: python-dotenv

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/ai-voice-pdf-study-assistant.git
cd ai-voice-pdf-study-assistant
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install streamlit langchain-groq SpeechRecognition gTTS pyaudio python-dotenv PyPDF2
```

> ⚠️ **Windows Users**
> If `pyaudio` fails to install:

```bash
pip install pipwin
pipwin install pyaudio
```

---

## 🔑 API Key Setup

### Groq API Key (Required)

1. Create a free account on **Groq**
2. Generate an API key
3. Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ Google Speech Recognition works via the `SpeechRecognition` library and does NOT require a separate API key for basic usage.

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open in your browser:

```
http://localhost:8501
```

---

## 📖 How to Use

1. Select an **input method**:

   * 📝 Type Notes
   * 🎤 Speak Notes
   * 📄 Upload PDF

2. Provide your study material

3. Select **study hours** using the slider

4. Click **Generate Study Help**

5. View generated results:

   * Summary
   * Quiz Questions
   * Flashcards
   * Study Schedule

6. (Optional) Click **🔊 Read Aloud Summary** to hear the summary

---

## 🧠 Supported Groq Models

You can change the model inside the code:

```python
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)
```

Other supported models:

* `llama3-8b-8192`
* `llama3-70b-8192`
* `gemma-7b-it`
* `mixtral-8x7b-32768`

---

## 📂 Project Structure

```
├── app.py              # Main Streamlit application
├── .env                # Environment variables (DO NOT push to GitHub)
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
```

---

## 🎯 Use Cases

* Exam preparation
* Quick revision from PDFs
* Voice-based learning
* Automatic quiz & flashcard generation
* Daily study planning

---

## 🔒 Security Notes

* ❌ Do NOT upload `.env` file to GitHub
* ✅ Add `.env` to `.gitignore`

---

## 🌟 Future Improvements

* User login system
* Chat history per user
* Export summaries to PDF
* Multilingual support
* Mobile-friendly UI

---

## 🤝 Contributing

Contributions are welcome:

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgements

* Streamlit
* LangChain
* Groq LLMs
* Google Speech Recognition API
* Google Text-to-Speec
