# 🙏 JAI GURU DEV AI Chatbot

A spiritual guidance chatbot powered by Sri Sri Ravi Shankar's teachings, built using RAG (Retrieval Augmented Generation) technology with Streamlit UI.

## ✨ Features

- **Intelligent Retrieval**: Advanced RAG system that finds the most relevant teachings based on your questions and context
- **Context-Aware**: Gathers user context (emotional state, life situation, guidance type) for personalized responses
- **Multiple AI Models**: Configurable support for OpenAI GPT and Groq Llama models
- **Beautiful UI**: Saffron-themed Streamlit interface inspired by spiritual aesthetics
- **Comprehensive Knowledge Base**: Contains structured teachings with metadata (topics, keywords, emotional states, etc.)
- **Source Attribution**: Shows which specific teachings were used to generate responses

## 📁 Project Structure

```
Guruji_Chatbot/
├── .env                    # API keys
├── config.yaml            # Configuration file
├── requirements.txt       # Python dependencies
├── setup.py               # Setup and testing script
├── chatbot.py             # Main Streamlit application
├── rag_system.py          # RAG system with LangChain
├── document_processor.py  # Markdown file processor
├── Knowledge_Base/        # Teaching files
│   ├── ssrs_teachings_batch1.md
│   ├── ssrs_teachings_batch3.md
│   ├── ssrs_teachings_batch4.md
│   └── ssrs_teachings_batch5.md
└── chroma_db/             # Vector database (created automatically)
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- OpenAI API key and/or Groq API key

### 2. Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/RamForexTrade/guruji-chatbot.git
   cd guruji-chatbot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key and/or Groq API key

4. **Run setup script** to verify everything is working:
   ```bash
   python setup.py
   ```

5. **Start the chatbot**:
   ```bash
   streamlit run chatbot.py
   ```

### 3. First Run

1. The application will automatically initialize the vector database on first run
2. Select your preferred AI model provider (OpenAI or Groq) in the sidebar
3. Answer the initial context questions to personalize your experience
4. Start asking questions about life, spirituality, relationships, and more!

## ⚙️ Configuration

### Model Provider Selection

Edit `config.yaml` to change default settings:

```yaml
model_provider:
  default: "openai"  # or "groq"
  
  openai:
    model: "gpt-4o-mini"
    temperature: 0.7
    max_tokens: 1500
    
  groq:
    model: "llama3-8b-8192"
    temperature: 0.7
    max_tokens: 1500
```

### RAG Settings

```yaml
rag:
  chunk_size: 1000
  chunk_overlap: 200
  top_k_results: 5
  similarity_threshold: 0.7
```

## 📚 Knowledge Base Structure

Each teaching in the markdown files follows this structure:

```markdown
## Teaching #XXX: [Title]
**Date:** [Date if available]
**Location:** [Location if mentioned]
**Topics:** [main themes - comma separated]
**Keywords:** [specific words for exact matching - comma separated]
**Problem Categories:** [user problems this addresses - comma separated]
**Emotional States:** [emotions this helps with - comma separated]
**Life Situations:** [when to apply - comma separated]

### Content:
[The actual teaching content]
```

This rich metadata enables sophisticated retrieval based on:
- **Topics**: Broad themes like relationships, spiritual practice, etc.
- **Keywords**: Specific terms for exact matching
- **Problem Categories**: Types of problems the teaching addresses
- **Emotional States**: Emotions the teaching helps with
- **Life Situations**: Contexts where the teaching applies

## 🎯 How It Works

### 1. Context Gathering
- User provides information about their situation, emotional state, and what type of guidance they seek
- This context is stored and used to enhance all subsequent queries

### 2. Intelligent Retrieval
- User's question is enhanced with their context
- Vector similarity search finds relevant teachings
- Metadata filtering ensures contextually appropriate results
- Custom retriever combines multiple signals for optimal results

### 3. Response Generation
- Selected teachings are provided as context to the AI model
- AI generates compassionate, wisdom-filled responses in Gurudev's spirit
- Sources are provided for transparency and further study

## 🎨 UI Features

- **Saffron Theme**: Beautiful spiritual aesthetic with saffron colors
- **Context Display**: Shows your gathered context throughout the session
- **Chat History**: Maintains conversation flow with full history
- **Source Attribution**: Expandable sections showing which teachings were referenced
- **Random Wisdom**: Get random spiritual insights
- **Configurable Models**: Switch between AI providers on the fly

## 🔧 Troubleshooting

### Common Issues

1. **"No API key found"**
   - Check that your .env file contains valid API keys
   - Ensure the .env file is in the project root directory

2. **"Error loading teachings"**
   - Verify that the Knowledge_Base folder contains .md files
   - Check that the markdown files follow the expected format

3. **"System initialization failed"**
   - Run `python setup.py` to diagnose issues
   - Check your internet connection for API calls
   - Verify Python version is 3.8+

### Performance Tips

- First run takes longer as it builds the vector database
- Subsequent runs are faster as the database is cached
- Use Groq models for faster response times
- Use OpenAI models for higher quality responses

## 🙏 Spiritual Disclaimer

This chatbot is a technological tool created to share the wisdom of Sri Sri Ravi Shankar's teachings. While it provides guidance based on authentic spiritual content, it is not a replacement for:
- Personal spiritual practice
- Direct guidance from qualified teachers
- Professional counseling when needed
- Your own inner wisdom and intuition

Use this tool as a complement to your spiritual journey, not as the sole source of guidance.

## 📞 Support

If you encounter issues:
1. Run `python setup.py` for diagnostics
2. Check the troubleshooting section above
3. Verify your API keys and internet connection

---

**🙏 "Knowledge is structured in consciousness" - Sri Sri Ravi Shankar**

**Jai Guru Dev! 🙏**
