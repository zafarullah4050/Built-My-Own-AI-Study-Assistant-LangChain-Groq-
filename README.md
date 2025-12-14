# 🎙️ AI Voice & PDF Study Assistant (LangChain + Groq)

An **AI-powered study assistant** built with **Streamlit, LangChain, and Groq LLMs**.
It helps students study smarter by allowing them to:

* 📝 Type notes
* 🎤 Speak notes (Speech-to-Text)
* 📄 Upload PDFs

The AI can then:

* 📌 Summarize notes
* ❓ Generate quiz questions with answers
* 📝 Create flashcards
* ⏰ Build a personalized study schedule
* 🔊 Read summaries aloud (Text-to-Speech)

This project is ideal for **students, self-learners, and exam preparation**.

---

## 🚀 Features

* **Multiple Input Modes**

  * Text input (notes)
  * Voice input using microphone
  * PDF upload and text extraction

* **AI-Powered Learning Tools**

  * Notes summarization (easy bullet points)
  * Quiz generation (with answers)
  * Flashcard creation (Q&A format)
  * Personalized study schedule based on available hours

* **Voice Support**

  * Speech-to-Text using `SpeechRecognition`
  * Text-to-Speech using `gTTS`

* **Fast & Free LLMs**

  * Uses **Groq API** with models like `llama-3.1-8b-instant`

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **LLM Framework**: LangChain
* **LLM Provider**: Groq
* **Speech-to-Text**: SpeechRecognition (Google API)
* **Text-to-Speech**: gTTS
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

> ⚠️ **Note for Windows Users**
> If `pyaudio` fails to install:

```bash
pip install pipwin
pipwin install pyaudio
```

---

## 🔑 API Key Setup (Groq)

1. Create a free account at **Groq**
2. Generate an API key
3. Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The app will open in your browser:

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

5. View:

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
├── app.py              # Main Streamlit app
├── .env                # Environment variables (not pushed to GitHub)
├── requirements.txt    # Dependencies
├── README.md           # Project documentation
```

---

## 🎯 Use Cases

* Exam preparation
* Quick revision from PDFs
* Voice-based learning
* Creating quizzes & flashcards automatically
* Daily study planning

---

## 🔒 Security Notes

* Do **NOT** upload your `.env` file to GitHub
* Add `.env` to `.gitignore`

---

## 🌟 Future Improvements

* Chat history memory per user
* Export summaries to PDF
* Multilingual support
* Login system
* Mobile-friendly UI

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Commit changes
4. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgements

* Streamlit
* LangChain
* Groq LLMs
* Google Speech Recognition



