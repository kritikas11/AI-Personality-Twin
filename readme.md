# 🎭 AI Personality Twin

An AI-powered application that generates personality profiles by analyzing user-written descriptions and optional facial emotions from uploaded images.

Built using **Python, Streamlit, NLP (TextBlob), DeepFace, OpenCV, and SQLite**.

## 🚀 Live Demo

**Streamlit App:** *https://ai-personality-twin.streamlit.app/*

---

## ✨ Features

- Personality trait extraction using NLP
- Sentiment analysis from user descriptions
- Facial emotion detection using DeepFace
- Automatic avatar generation using DiceBear
- Interactive Streamlit dashboard
- SQLite database for storing profile history
- No paid APIs required

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | Streamlit |
| NLP | TextBlob |
| Computer Vision | OpenCV, DeepFace |
| Database | SQLite |
| Avatar Generation | DiceBear |
| Language | Python |

---

## 📂 Project Structure

```text
AI-Personality-Twin/
│
├── backend/
│   ├── nlp/
│   ├── vision/
│   ├── avatar/
│   └── database/
│
├── app.py
├── run.py
├── requirements.txt
├── packages.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/kritikas11/AI-Personality-Twin.git
cd AI-Personality-Twin
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 🎯 Example

### User Input

```text
I love creating art and designing new things.
I enjoy meeting new people and exploring new places.
```

### Output

```text
Creative      : 85%
Optimistic    : 78%
Friendly      : 65%
Adventurous   : 72%
```

If an image is uploaded, the application also predicts the dominant facial emotion.

---

## 🔍 How It Works

1. User enters a text description.
2. TextBlob performs sentiment analysis.
3. Keyword-based NLP identifies personality traits.
4. DeepFace analyzes uploaded images (optional).
5. DiceBear generates a matching avatar.
6. Results are displayed through Streamlit and stored in SQLite.

---

## 📌 Future Improvements

- More advanced personality modelling
- PDF report export
- Multi-language support
- Improved emotion recognition
- LLM-based personality summaries

---

## 👩‍💻 Author

**Kritika Singh**

GitHub: https://github.com/kritikas11
