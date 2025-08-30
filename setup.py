#!/usr/bin/env python3
"""
Enhanced setup script for JAI GURU DEV AI Chatbot
Handles dependency conflicts and provides multiple installation options.
"""

import os
import sys
import subprocess
from pathlib import Path
import yaml
from dotenv import load_dotenv

def install_requirements_with_fallback():
    """Install requirements with fallback options for dependency conflicts"""
    print("🔧 Installing required packages...")
    
    # Try method 1: Install with updated requirements
    try:
        print("📦 Attempting installation with specific versions...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Method 1 failed: {e}")
    
    # Try method 2: Install with simple requirements (let pip resolve)
    try:
        print("📦 Attempting installation with flexible versions...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_simple.txt"])
        print("✅ Requirements installed successfully with flexible versions!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Method 2 failed: {e}")
    
    # Try method 3: Install packages individually
    try:
        print("📦 Installing packages individually...")
        essential_packages = [
            "streamlit",
            "langchain", 
            "langchain-openai",
            "langchain-community",
            "chromadb",
            "python-dotenv",
            "pyyaml",
            "openai>=1.10.0",
            "pandas",
            "numpy"
        ]
        
        for package in essential_packages:
            print(f"   Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                    capture_output=True, text=True)
            except subprocess.CalledProcessError:
                print(f"   ⚠️ Failed to install {package}, continuing...")
        
        print("✅ Essential packages installed!")
        return True
        
    except Exception as e:
        print(f"❌ All installation methods failed: {e}")
        return False

def install_groq_separately():
    """Install Groq separately as it might have conflicts"""
    try:
        print("📦 Installing Groq API client...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "groq"])
        return True
    except subprocess.CalledProcessError:
        print("⚠️ Groq installation failed - you'll only be able to use OpenAI models")
        return False

def verify_installation():
    """Verify that core packages are installed"""
    print("🔍 Verifying installation...")
    
    required_packages = [
        'streamlit',
        'langchain', 
        'openai',
        'chromadb',
        'yaml',
        'pandas',
        'numpy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'yaml':
                import yaml
            else:
                __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ All core packages verified!")
    return True

def verify_environment():
    """Verify environment variables"""
    print("🔍 Verifying environment setup...")
    
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    groq_key = os.getenv('GROQ_API_KEY')
    
    if not openai_key:
        print("⚠️  Warning: OPENAI_API_KEY not found in environment")
    else:
        print("✅ OpenAI API key found")
    
    if not groq_key:
        print("⚠️  Warning: GROQ_API_KEY not found in environment")
    else:
        print("✅ Groq API key found")
    
    if not openai_key and not groq_key:
        print("❌ No API keys found! Please check your .env file")
        return False
    
    return True

def verify_knowledge_base():
    """Verify knowledge base files"""
    print("📚 Verifying knowledge base...")
    
    kb_path = Path("Knowledge_Base")
    if not kb_path.exists():
        print(f"❌ Knowledge base directory not found: {kb_path}")
        return False
    
    md_files = list(kb_path.glob("*.md"))
    if not md_files:
        print("❌ No markdown files found in Knowledge_Base directory")
        return False
    
    print(f"✅ Found {len(md_files)} markdown files:")
    for file in md_files:
        print(f"   - {file.name}")
    
    return True

def test_document_processor():
    """Test the document processor"""
    print("🧪 Testing document processor...")
    
    try:
        from document_processor import DocumentProcessor
        
        processor = DocumentProcessor("Knowledge_Base")
        teachings = processor.load_all_teachings()
        
        if teachings:
            print(f"✅ Successfully loaded {len(teachings)} teachings")
            print(f"   First teaching: #{teachings[0].number} - {teachings[0].title}")
            return True
        else:
            print("❌ No teachings loaded")
            return False
            
    except Exception as e:
        print(f"❌ Error testing document processor: {e}")
        return False

def test_config():
    """Test configuration file"""
    print("⚙️  Testing configuration...")
    
    try:
        with open("config.yaml", 'r') as f:
            config = yaml.safe_load(f)
        
        required_sections = ['model_provider', 'rag', 'embeddings', 'ui', 'chatbot']
        for section in required_sections:
            if section not in config:
                print(f"❌ Missing configuration section: {section}")
                return False
        
        print("✅ Configuration file is valid")
        return True
        
    except FileNotFoundError:
        print("❌ config.yaml file not found")
        return False
    except yaml.YAMLError as e:
        print(f"❌ Error parsing config.yaml: {e}")
        return False

def main():
    """Main setup function"""
    print("🙏 JAI GURU DEV AI Chatbot - Enhanced Setup Script")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Installation steps
    print(f"\n📦 Step 1: Installing Dependencies")
    if not install_requirements_with_fallback():
        print("❌ Failed to install core dependencies")
        print("💡 Try running manually: pip install streamlit langchain langchain-openai chromadb python-dotenv pyyaml openai")
        return False
    
    # Install Groq separately
    print(f"\n📦 Step 2: Installing Groq (optional)")
    install_groq_separately()
    
    # Verification steps
    verification_steps = [
        ("Verify Installation", verify_installation),
        ("Verify Environment", verify_environment),
        ("Verify Knowledge Base", verify_knowledge_base),
        ("Test Configuration", test_config),
        ("Test Document Processor", test_document_processor)
    ]
    
    all_passed = True
    for step_name, step_func in verification_steps:
        print(f"\n🔍 {step_name}...")
        if not step_func():
            all_passed = False
            print(f"❌ {step_name} failed!")
        else:
            print(f"✅ {step_name} completed!")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 Setup completed successfully!")
        print("\n🚀 To start the chatbot, run:")
        print("   python start_chatbot.py")
        print("   OR")
        print("   streamlit run chatbot.py")
        print("\n💡 Note: First run will take 1-2 minutes to build the vector database")
    else:
        print("❌ Setup encountered some issues.")
        print("💡 The chatbot may still work if core dependencies are installed.")
        print("💡 Try running: python start_chatbot.py")
    
    return all_passed

if __name__ == "__main__":
    main()
