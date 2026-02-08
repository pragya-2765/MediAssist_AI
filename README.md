# 🩺 MediAssist AI

MediAssist AI is a full-stack, AI-powered healthcare assistant that allows users to submit symptoms and receive **AI-generated health insights and recommendations** using **Google Gemini Flash**.

⚠️ **Disclaimer:**  
This project is **non-diagnostic** and intended strictly for **educational and demonstration purposes only**. It does **not** replace professional medical advice, diagnosis, or treatment.

---

## ✨ Key Features

- 👤 User management system
- 📝 Symptom submission with severity levels
- 🤖 AI-powered symptom analysis using Google Gemini
- 🗄️ SQLite database with relational tables
- 🔁 Full CRUD APIs
- 🚀 RESTful backend using FastAPI
- 🌐 Simple frontend interface
- 🔐 Secure handling of API keys via environment variables

---

## 🛠️ Technology Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Google Gemini (Flash)
- Uvicorn

### Frontend
- HTML
- CSS
- JavaScript

---

## 📁 Project Structure

MediAssist_AI/
│
├── backend/
│ ├── app/
│ │ ├── main.py
│ │ ├── database.py
│ │ ├── models.py
│ │ ├── schemas.py
│ │ ├── crud.py
│ │ ├── routes/
│ │ │ ├── users.py
│ │ │ ├── symptoms.py
│ │ │ └── ai_analysis.py
│ │ ├── ai/
│ │ │ └── gemini.py
│ │ └── utils/
│ │ └── logger.py
│ │
│ ├── run.py
│ └── requirements.txt
│
├── frontend/
│ └── (frontend files)
│
├── .gitignore
├── LICENSE
└── README.md

---

## ⚙️ Setup Instructions

1️⃣ Clone the Repository
git clone https://github.com/pragya-2765/MediAssist_AI.git
cd MediAssist_AI

2️⃣ Create a Virtual Environment (Recommended)
python -m venv venv
Windows: venv\Scripts\activate

3️⃣ Install Backend Dependencies
cd backend
pip install -r requirements.txt

4️⃣ Configure Environment Variables
Create a .env file inside the backend directory:

GEMINI_API_KEY=your_gemini_api_key_here

🚫 Do NOT upload .env to GitHub

5️⃣ Run the Backend Server
python run.py
Server will start at:
http://127.0.0.1:8000

---

## 📌 API Documentation

After starting the server, open:

Swagger UI:

http://127.0.0.1:8000/docs

---

## 🔒 Security Practices

• API keys are stored securely using environment variables

• .env and database files are excluded via .gitignore

• No sensitive data is committed to the repository

---

## 🚫 Medical Disclaimer

MediAssist AI does not provide medical diagnoses.
All AI-generated outputs are informational only and must not be used as a substitute for professional medical advice.

---

## 📜 License

This project is licensed under the MIT License and is intended for academic and learning purposes.

---

## 👩‍💻 Author

**Pragya Srivastava** 
