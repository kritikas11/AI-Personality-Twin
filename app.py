"""
Main Streamlit Application
AI Personality Twin - Interactive personality analysis
"""
import streamlit as st
from PIL import Image
import io
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from backend.nlp.pipeline import NLPPipeline
from backend.vision.emotion_detector import EmotionDetector
from backend.avatar.generator import AvatarGenerator
from backend.db.database import Database
from backend.utils.helpers import (
    validate_name,
    validate_text_input,
    format_confidence,
    calculate_profile_score,
    get_color_from_trait,
    format_timestamp
)

# Page config
st.set_page_config(
    page_title="AI Personality Twin",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .trait-card {
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        background-color: #f8f9fa;
        margin: 0.5rem 0;
    }
    .metric-card {
        text-align: center;
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .avatar-container {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def init_components():
    """Initialize application components"""
    return {
        'nlp': NLPPipeline(),
        'emotion': EmotionDetector(),
        'avatar': AvatarGenerator(),
        'db': Database()
    }

components = init_components()

# Header
st.markdown("""
<div class="main-header">
    <h1>🎭 AI Personality Twin</h1>
    <p>Discover your unique personality through AI analysis</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 About")
    st.write("""
    This app analyzes your personality using:
    - **NLP** for text analysis
    - **Computer Vision** for emotion detection
    - **AI** to generate your personality profile
    """)
    
    st.header("📊 Statistics")
    stats = components['db'].get_stats()
    st.metric("Total Profiles", stats['total_profiles'])
    
    if st.button("🗑️ Clear History"):
        st.session_state.clear()
        st.success("History cleared!")

# Main content
tab1, tab2, tab3 = st.tabs(["🆕 Create Profile", "📜 View History", "ℹ️ How It Works"])

with tab1:
    st.header("Create Your Personality Twin")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Name input
        name = st.text_input(
            "👤 Your Name",
            placeholder="Enter your name...",
            max_chars=50
        )
        
        # Text input
        text_input = st.text_area(
            "✍️ Tell us about yourself",
            placeholder="Describe your interests, hobbies, personality, goals... (minimum 10 characters)",
            height=200,
            max_chars=5000
        )
        
        st.caption(f"Characters: {len(text_input)}/5000")
    
    with col2:
        # Image upload
        st.subheader("📸 Upload Photo (Optional)")
        uploaded_image = st.file_uploader(
            "Upload a selfie for emotion detection",
            type=['jpg', 'jpeg', 'png'],
            help="Optional: Upload a photo to detect your emotion"
        )
        
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Analyze button
    st.markdown("---")
    
    if st.button("🚀 Analyze My Personality", type="primary", use_container_width=True):
        # Validate inputs
        name_valid, name_error = validate_name(name)
        text_valid, text_error = validate_text_input(text_input)
        
        if not name_valid:
            st.error(f"❌ {name_error}")
        elif not text_valid:
            st.error(f"❌ {text_error}")
        else:
            with st.spinner("🔮 Analyzing your personality..."):
                # Process text
                nlp_results = components['nlp'].process(text_input)
                
                if not nlp_results['success']:
                    st.error(f"❌ {nlp_results.get('error', 'Analysis failed')}")
                else:
                    # Process image if uploaded
                    emotion_result = None
                    if uploaded_image:
                        image_bytes = uploaded_image.getvalue()
                        emotion_result = components['emotion'].detect_from_bytes(image_bytes)
                    
                    # Use neutral emotion if no image
                    if not emotion_result or not emotion_result.get('success'):
                        emotion_result = {
                            'dominant_emotion': 'neutral',
                            'emoji': '😐',
                            'confidence': 0
                        }
                    
                    # Generate avatar
                    avatar_url = components['avatar'].generate_avatar_url(
                        name=name,
                        traits=nlp_results['traits'],
                        emotion=emotion_result['dominant_emotion']
                    )
                    
                    # Calculate profile score
                    profile_score = calculate_profile_score(
                        nlp_results['polarity'],
                        len(nlp_results['traits']),
                        len(text_input)
                    )
                    
                    # Save to database
                    profile_id = components['db'].save_profile(
                        name=name,
                        text_input=text_input,
                        personality_traits=nlp_results['traits'],
                        emotion=emotion_result['dominant_emotion'],
                        sentiment_score=nlp_results['polarity'],
                        avatar_url=avatar_url
                    )
                    
                    # Display results
                    st.success("✅ Analysis Complete!")
                    
                    st.markdown("---")
                    
                    # Top section: Avatar and Summary
                    col_left, col_right = st.columns([1, 2])
                    
                    with col_left:
                        st.markdown(f"""
                        <div class="avatar-container">
                            <img src="{avatar_url}" width="200" />
                            <h3>{name}</h3>
                            <p>{emotion_result['emoji']} {emotion_result['dominant_emotion'].title()}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_right:
                        st.subheader("📊 Personality Overview")
                        
                        # Metrics
                        met1, met2, met3 = st.columns(3)
                        with met1:
                            st.metric("Profile Score", f"{profile_score}/100")
                        with met2:
                            sentiment_emoji = "😊" if nlp_results['sentiment'] == "Positive" else "😐" if nlp_results['sentiment'] == "Neutral" else "😔"
                            st.metric("Sentiment", f"{sentiment_emoji} {nlp_results['sentiment']}")
                        with met3:
                            st.metric("Traits Found", len(nlp_results['traits']))
                        
                        st.write(f"**Summary:** {nlp_results['summary']}")
                    
                    st.markdown("---")
                    
                    # Personality Traits
                    st.subheader("🎯 Your Personality Traits")
                    
                    trait_descriptions = components['nlp'].get_trait_descriptions()
                    trait_emojis = components['nlp'].get_trait_emojis()
                    
                    for trait, score in nlp_results['traits'].items():
                        col_trait, col_bar = st.columns([3, 1])
                        with col_trait:
                            st.markdown(f"""
                            <div class="trait-card">
                                <h4>{trait_emojis.get(trait, '⭐')} {trait}</h4>
                                <p>{trait_descriptions.get(trait, '')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_bar:
                            st.metric("Confidence", format_confidence(score))
                            st.progress(score / 100)
                    
                    # Additional insights
                    st.markdown("---")
                    st.subheader("💡 Additional Insights")
                    
                    col_ins1, col_ins2 = st.columns(2)
                    with col_ins1:
                        st.info(f"""
                        **Emotional Tone:** {nlp_results['sentiment']}  
                        **Polarity Score:** {nlp_results['polarity']}  
                        **Subjectivity:** {nlp_results['subjectivity']}
                        """)
                    
                    with col_ins2:
                        if emotion_result.get('all_emotions'):
                            st.info(f"""
                            **Detected Emotion:** {emotion_result['dominant_emotion'].title()}  
                            **Confidence:** {emotion_result.get('confidence', 0)}%  
                            {components['emotion'].get_emotion_description(emotion_result['dominant_emotion'])}
                            """)
                    
                    # Save to session
                    if 'profiles' not in st.session_state:
                        st.session_state.profiles = []
                    
                    st.session_state.profiles.append({
                        'id': profile_id,
                        'name': name,
                        'avatar_url': avatar_url,
                        'traits': nlp_results['traits'],
                        'score': profile_score
                    })

with tab2:
    st.header("📜 Profile History")
    
    profiles = components['db'].get_all_profiles(limit=20)
    
    if not profiles:
        st.info("No profiles yet. Create your first personality twin!")
    else:
        for profile in profiles:
            with st.expander(f"👤 {profile['name']} - {format_timestamp(profile['created_at'])}"):
                col_a, col_b = st.columns([1, 3])
                
                with col_a:
                    st.image(profile['avatar_url'], width=150)
                    st.caption(f"Emotion: {profile['emotion']}")
                
                with col_b:
                    st.write(f"**Text:** {profile['text_input'][:200]}...")
                    st.write(f"**Sentiment Score:** {profile['sentiment_score']}")
                    
                    st.write("**Traits:**")
                    for trait, score in profile['personality_traits'].items():
                        st.write(f"- {trait}: {format_confidence(score)}")

with tab3:
    st.header("ℹ️ How It Works")
    
    st.markdown("""
    ### 🧠 The AI Personality Twin Process
    
    #### 1️⃣ **Text Analysis (NLP)**
    - Analyzes your text using Natural Language Processing
    - Extracts personality traits based on keyword matching
    - Determines sentiment (Positive, Neutral, Negative)
    - Calculates confidence scores for each trait
    
    #### 2️⃣ **Emotion Detection (Computer Vision)**
    - Optional: Upload a photo for facial emotion analysis
    - Uses DeepFace library to detect emotions
    - Identifies: Happy, Sad, Angry, Surprise, Fear, Neutral
    
    #### 3️⃣ **Avatar Generation**
    - Creates a unique avatar using DiceBear API
    - Avatar style matches your personality traits
    - No API keys required - completely free!
    
    #### 4️⃣ **Profile Creation**
    - Combines text and image analysis
    - Generates comprehensive personality report
    - Saves profile to database for future reference
    
    ### 🎯 Personality Traits Detected
    
    - **Creative** 🎨: Imaginative and artistic
    - **Optimistic** 🌟: Positive and hopeful
    - **Friendly** 🤝: Social and approachable
    - **Analytical** 🧠: Logical and systematic
    - **Adventurous** 🗺️: Bold and exploratory
    - **Calm** 🧘: Peaceful and composed
    - **Energetic** ⚡: Active and enthusiastic
    - **Empathetic** ❤️: Understanding and caring
    
    ### 🔒 Privacy
    - All data is stored locally in SQLite database
    - No external API keys required
    - Your photos are processed locally
    - No data is sent to third parties
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Made with ❤️ using Streamlit | AI Personality Twin v1.0</p>
</div>
""", unsafe_allow_html=True)