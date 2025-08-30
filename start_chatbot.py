#!/usr/bin/env python3
"""
Enhanced launcher script for JAI GURU DEV AI Chatbot
Handles dependency conflicts and provides fallback installation.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_and_install_streamlit():
    """Check if Streamlit is available, install if not"""
    try:
        import streamlit
        return True
    except ImportError:
        print("📦 Streamlit not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
            print("✅ Streamlit installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Streamlit: {e}")
            return False

def check_core_dependencies():
    """Check if core dependencies are available"""
    missing = []
    
    dependencies = {
        'langchain': 'langchain',
        'openai': 'openai>=1.10.0',
        'chromadb': 'chromadb',
        'yaml': 'pyyaml',
        'dotenv': 'python-dotenv'
    }
    
    for module, package in dependencies.items():
        try:
            if module == 'dotenv':
                from dotenv import load_dotenv
            elif module == 'yaml':
                import yaml
            else:
                __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"📦 Missing dependencies: {', '.join(missing)}")
        print("🔧 Installing missing packages...")
        
        for package in missing:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"⚠️ Failed to install {package}")
        
        return len(missing) == 0  # Return True if all were installed
    
    return True

def main():
    """Main launcher function"""
    print("🙏 Starting JAI GURU DEV AI Chatbot...")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check Streamlit
    if not check_and_install_streamlit():
        print("❌ Cannot proceed without Streamlit. Please install manually:")
        print("   pip install streamlit")
        return
    
    # Check core dependencies
    if not check_core_dependencies():
        print("⚠️ Some dependencies are missing. The chatbot may not work properly.")
        print("💡 Try running the full setup: python setup.py")
        
        response = input("🤔 Do you want to continue anyway? (y/n): ").lower().strip()
        if response != 'y':
            print("🛑 Setup cancelled. Run 'python setup.py' to fix dependencies.")
            return
    
    # Check for config file
    if not Path("config.yaml").exists():
        print("❌ config.yaml not found. Please ensure all files are in place.")
        return
    
    # Check for knowledge base
    if not Path("Knowledge_Base").exists():
        print("❌ Knowledge_Base folder not found. Please ensure the folder exists with .md files.")
        return
    
    # Start the Streamlit app
    print("\n🚀 Launching JAI GURU DEV AI Chatbot...")
    print("📝 Note: The first run will take longer as it builds the vector database.")
    print("🌐 The chatbot will open in your web browser automatically.")
    print("🛑 To stop the chatbot, press Ctrl+C in this terminal.\n")
    
    try:
        # Try to run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "chatbot.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--theme.base", "light",
            "--theme.primaryColor", "#FF8C00"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting chatbot: {e}")
        print("\n💡 Troubleshooting steps:")
        print("1. Run: python setup.py")
        print("2. Check that all dependencies are installed")
        print("3. Try: streamlit run chatbot.py")
    except KeyboardInterrupt:
        print("\n🙏 JAI GURU DEV AI Chatbot stopped. Jai Guru Dev!")
    except FileNotFoundError:
        print("\n❌ Streamlit command not found.")
        print("💡 Try installing Streamlit: pip install streamlit")
        print("💡 Then run: streamlit run chatbot.py")

if __name__ == "__main__":
    main()
