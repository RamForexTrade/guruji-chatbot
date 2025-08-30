#!/usr/bin/env python3
"""
Test script to validate the JAI GURU DEV AI Chatbot components
"""

import os
import sys
from pathlib import Path

def test_document_processor():
    """Test the document processor"""
    print("🧪 Testing Document Processor...")
    
    try:
        from document_processor import DocumentProcessor
        
        # Initialize processor
        processor = DocumentProcessor("Knowledge_Base")
        
        # Load all teachings
        teachings = processor.load_all_teachings()
        
        if not teachings:
            print("❌ No teachings loaded")
            return False
        
        print(f"✅ Loaded {len(teachings)} teachings")
        
        # Test first few teachings
        for i, teaching in enumerate(teachings[:2]):
            print(f"\n📖 Teaching {i+1}:")
            print(f"   Number: {teaching.number}")
            print(f"   Title: {teaching.title}")
            print(f"   Topics: {teaching.topics}")
            print(f"   Keywords: {teaching.keywords}")
            print(f"   Content length: {len(teaching.content)} characters")
        
        # Test metadata search
        print(f"\n🔍 Testing metadata search...")
        love_teachings = processor.search_teachings_by_metadata(
            teachings=teachings,
            query_topics=["love", "relationship"],
            query_emotions=["love"]
        )
        
        print(f"✅ Found {len(love_teachings)} teachings about love")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\n⚙️ Testing Configuration...")
    
    try:
        import yaml
        
        with open("config.yaml", 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"✅ Config loaded successfully")
        print(f"   Default model provider: {config['model_provider']['default']}")
        print(f"   UI title: {config['ui']['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_environment():
    """Test environment setup"""
    print("\n🌍 Testing Environment...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv('OPENAI_API_KEY')
        groq_key = os.getenv('GROQ_API_KEY')
        
        if openai_key:
            print(f"✅ OpenAI API key found (length: {len(openai_key)})")
        else:
            print("⚠️ OpenAI API key not found")
        
        if groq_key:
            print(f"✅ Groq API key found (length: {len(groq_key)})")
        else:
            print("⚠️ Groq API key not found")
        
        return bool(openai_key or groq_key)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🙏 JAI GURU DEV AI Chatbot - Component Tests")
    print("=" * 60)
    
    tests = [
        ("Document Processor", test_document_processor),
        ("Configuration", test_config),
        ("Environment", test_environment)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} Test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\n🚀 To start the chatbot:")
        print("   streamlit run chatbot.py")
    else:
        print(f"❌ {total - passed} tests failed. Please fix the issues before running.")
    
    return passed == total

if __name__ == "__main__":
    # Change to the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    success = main()
    sys.exit(0 if success else 1)
