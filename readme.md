🎭 AI Personality Twin
An AI-powered application that creates fun personality profiles by analyzing text and facial emotions. Built with Python, Streamlit, NLP, and Computer Vision.

✨ Features
Text Analysis: Extract personality traits from user descriptions using NLP
Emotion Detection: Optional facial emotion recognition from uploaded photos
Avatar Generation: Unique DiceBear avatars based on personality traits
Interactive Dashboard: Beautiful Streamlit UI with charts and visualizations
Profile History: SQLite database to store and view past profiles
No API Keys Required: Completely free to use, no external API dependencies
🛠️ Tech Stack
Frontend: Streamlit
NLP: TextBlob
Computer Vision: OpenCV + DeepFace
Avatar: DiceBear (free, no API key needed)
Database: SQLite
Language: Python 3.9+

🚀 Installation & Setup
Prerequisites
Python 3.9 or higher
pip (Python package manager)
Step 1: Clone the Repository
bash
git clone <your-repo-url>
cd ai-twin-env
Step 2: Create Virtual Environment
bash
# Windows
python -m venv venv
venv\Scripts\activate

📖 How to Use
Enter Your Name: Provide your name in the input field
Describe Yourself: Write about your interests, personality, hobbies (minimum 10 characters)
Upload Photo (Optional): Upload a selfie for emotion detection
Click Analyze: Hit the "Analyze My Personality" button
View Results: See your personality traits, avatar, and insights!
🎯 Personality Traits Detected
The app can identify these personality traits:

🎨 Creative: Imaginative and artistic
🌟 Optimistic: Positive and hopeful
🤝 Friendly: Social and approachable
🧠 Analytical: Logical and systematic
🗺️ Adventurous: Bold and exploratory
🧘 Calm: Peaceful and composed
⚡ Energetic: Active and enthusiastic
❤️ Empathetic: Understanding and caring
🔍 How It Works
1. Text Analysis (NLP)
Uses TextBlob for sentiment analysis
Keyword matching to identify personality traits
Calculates confidence scores (0-100%) for each trait
2. Emotion Detection (Computer Vision)
DeepFace library analyzes facial expressions
Detects: Happy, Sad, Angry, Surprise, Fear, Neutral, Disgust
Works with uploaded photos (JPG, PNG)
3. Avatar Generation
Creates unique avatars using DiceBear API
Avatar style matches dominant personality trait
Multiple styles: Avataaars, Bottts, Big Smile, Personas, etc.
4. Data Storage
SQLite database stores all profiles
View history of past analyses
No external database required
🧪 Example Usage
Input Text:

I love creating art and designing new things. I'm always optimistic 
about the future and enjoy meeting new people. In my free time, I like 
to explore new places and try adventurous activities.
Expected Output:

Traits: Creative (85%), Optimistic (78%), Adventurous (72%), Friendly (65%)
Sentiment: Positive
Avatar: Creative-style DiceBear avatar
Emotion: Happy (if photo uploaded with smile)
🛡️ Privacy & Security
All data stored locally in SQLite database
No external API keys required (except DiceBear URLs, which are public)
Photos processed locally, not sent to external servers
No user tracking or analytics
🐛 Troubleshooting
Common Issues
1. ModuleNotFoundError: No module named 'textblob'

bash
pip install textblob
python -m textblob.download_corpora
2. DeepFace installation issues

bash
pip install tf-keras tensorflow deepface
3. OpenCV import error

bash
pip install opencv-python-headless
4. Streamlit not found

bash
pip install streamlit --upgrade
🔧 Configuration
Changing Avatar Styles
Edit backend/avatar/generator.py:

python
STYLE_MAPPING = {
    'creative': 'avataaars',  # Change to any DiceBear style
    'optimistic': 'bottts',
    # Add more mappings
}
Adjusting Trait Keywords
Edit backend/nlp/models.py:

python
TRAIT_KEYWORDS = {
    'Creative': ['create', 'imagine', ...],  # Add more keywords
}
📊 Database Schema
sql
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    text_input TEXT,
    personality_traits TEXT,  -- JSON
    emotion TEXT,
    sentiment_score REAL,
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
🚀 Future Enhancements
 Add more personality trait categories
 Implement trait comparison between users
 Export profiles as PDF/Image
 Multi-language support
 Advanced emotion detection (age, gender)
 Personality trait recommendations
 Social sharing features
📝 License
This project is open-source and available under the MIT License.

🙏 Acknowledgments
Streamlit - Amazing web framework
TextBlob - Simple NLP library
DeepFace - Facial analysis framework
DiceBear - Free avatar generation API
OpenCV - Computer vision library


