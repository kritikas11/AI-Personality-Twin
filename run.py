"""
Run Script for AI Personality Twin
Easy startup script with environment checks
"""
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Error: Python 3.9 or higher is required")
        print(f"   Your version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required = [
        'streamlit',
        'textblob',
        'opencv-python',
        'deepface',
        'PIL'
    ]
    
    missing = []
    for package in required:
        try:
            if package == 'PIL':
                __import__('PIL')
            elif package == 'opencv-python':
                __import__('cv2')
            else:
                __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} is NOT installed")
    
    return missing

def install_dependencies():
    """Install missing dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable,
            '-m',
            'pip',
            'install',
            '-r',
            'requirements.txt'
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    print("\n📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('brown', quiet=True)
        nltk.download('punkt', quiet=True)
        print("✅ NLTK data downloaded")
        return True
    except Exception as e:
        print(f"⚠️ Warning: Could not download NLTK data: {e}")
        return False

def run_app():
    """Run the Streamlit application"""
    print("\n🚀 Starting AI Personality Twin...")
    print("=" * 50)
    try:
        subprocess.run([
            sys.executable,
            '-m',
            'streamlit',
            'run',
            'app.py'
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error running application: {e}")

def main():
    """Main execution function"""
    print("=" * 50)
    print("🎭 AI PERSONALITY TWIN - SETUP & RUN")
    print("=" * 50)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠️ Missing packages: {', '.join(missing)}")
        response = input("\nInstall missing dependencies? (y/n): ")
        if response.lower() == 'y':
            if not install_dependencies():
                sys.exit(1)
        else:
            print("❌ Cannot run without dependencies")
            sys.exit(1)
    
    # Download NLTK data
    download_nltk_data()
    
    # Create necessary directories
    print("\n📁 Setting up directories...")
    Path("backend/db").mkdir(parents=True, exist_ok=True)
    Path("storage/images").mkdir(parents=True, exist_ok=True)
    Path("storage/temp").mkdir(parents=True, exist_ok=True)
    print("✅ Directories ready")
    
    # Run the application
    run_app()

if __name__ == "__main__":
    main()