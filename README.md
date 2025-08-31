# 🙏 JAI GURU DEV AI Chatbot

A spiritual guidance chatbot powered by Sri Sri Ravi Shankar's teachings, built using RAG (Retrieval Augmented Generation) technology with Streamlit UI.

## ✨ New Features & Major Update (Railway-Ready!)

🚀 **Railway Deployment Ready**: One-click cloud deployment with production optimizations  
🎯 **Database Persistence**: ChromaDB now persists through deployments - no data loss!  
⚡ **Lightning Fast**: Optimized performance with health checks and auto-scaling  
🛡️ **Production Grade**: Enhanced security, error handling, and monitoring  
📚 **Complete Documentation**: Comprehensive deployment guides and automation tools  
🔧 **Development Tools**: Cleanup scripts and deployment checklists included  

## ✨ Core Features

- **Intelligent Retrieval**: Advanced RAG system that finds the most relevant teachings based on your questions and context
- **Context-Aware**: Gathers user context (emotional state, life situation, guidance type) for personalized responses
- **Multiple AI Models**: Configurable support for OpenAI GPT and Groq Llama models
- **Beautiful UI**: Saffron-themed Streamlit interface inspired by spiritual aesthetics
- **Comprehensive Knowledge Base**: Contains structured teachings with metadata (topics, keywords, emotional states, etc.)
- **Source Attribution**: Shows which specific teachings were used to generate responses
- **Persistent Database**: Smart ChromaDB management that survives restarts and config changes

## 🚂 Deploy to Railway (NEW!)

### One-Click Deployment
1. **Fork this repository** or use the existing repo
2. **Go to [Railway](https://railway.app)** and connect your GitHub
3. **Add environment variables**:
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `GROQ_API_KEY` - Your Groq API key (optional)
4. **Deploy automatically** - Railway handles everything else!

### Complete Deployment Guide
📖 **[RAILWAY_DEPLOYMENT_GUIDE.md](RAILWAY_DEPLOYMENT_GUIDE.md)** - Comprehensive deployment instructions  
📋 **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Step-by-step checklist  
🛠️ **[deploy_cleanup.sh](deploy_cleanup.sh)** - Automated cleanup script  

### Railway Benefits
- ⚡ **Fast deployments** (~2-3 minutes)
- 🔄 **Auto-scaling** with persistent storage
- 🛡️ **Built-in health monitoring** at `/_stcore/health`
- 💾 **Database persistence** across deployments
- 🌐 **Automatic HTTPS** and custom domain support

## 📁 Project Structure

```
guruji-chatbot/
├── .env.example              # Environment template
├── .gitignore               # Enhanced exclusions
├── config.yaml              # Application configuration
├── requirements.txt         # Optimized dependencies
├── Procfile                 # Railway start command
├── railway.toml             # Production Railway config
├── deploy_cleanup.sh        # Deployment cleanup script
├── RAILWAY_DEPLOYMENT_GUIDE.md  # Detailed deployment guide
├── DEPLOYMENT_CHECKLIST.md     # Step-by-step checklist
├── chatbot.py               # Main Streamlit application
├── rag_system.py            # Enhanced RAG system
├── document_processor.py    # Markdown file processor
├── Knowledge_Base/          # Teaching files
│   ├── ssrs_teachings_batch1.md
│   ├── ssrs_teachings_batch3.md
│   ├── ssrs_teachings_batch4.md
│   └── ssrs_teachings_batch5.md
└── chroma_db/              # Persistent vector database
```

## 🚀 Quick Start

### Option 1: Deploy to Railway (Recommended)
```bash
# 1. Fork this repository
# 2. Connect to Railway
# 3. Add API keys
# 4. Deploy!
```

### Option 2: Run Locally

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

### Railway Production Settings

The `railway.toml` includes optimized production settings:
- Health checks and auto-restart
- Performance optimizations
- Security configurations
- Environment-specific settings

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

### Railway-Specific Troubleshooting

4. **Railway deployment fails**
   - Check build logs in Railway dashboard
   - Verify environment variables are set correctly
   - Ensure API keys have sufficient credits

5. **Database recreates on every deploy**
   - This is now fixed! Database persists across deployments
   - Check logs for "Loaded existing ChromaDB" message

### Performance Tips

- First run takes longer as it builds the vector database
- Subsequent runs are faster as the database is cached
- Use Groq models for faster response times
- Use OpenAI models for higher quality responses
- Railway deployments include automatic optimizations

## 📊 Performance Expectations

### Local Development
- **First run**: 30-60 seconds (database creation)
- **Subsequent runs**: 5-10 seconds
- **Response time**: 2-8 seconds

### Railway Production
- **Cold start**: 30-60 seconds (first access after idle)
- **Warm response**: 1-3 seconds
- **Database loading**: 2-5 seconds (persistent!)
- **Response time**: 2-8 seconds depending on model

## 🙏 Spiritual Disclaimer

This chatbot is a technological tool created to share the wisdom of Sri Sri Ravi Shankar's teachings. While it provides guidance based on authentic spiritual content, it is not a replacement for:
- Personal spiritual practice
- Direct guidance from qualified teachers
- Professional counseling when needed
- Your own inner wisdom and intuition

Use this tool as a complement to your spiritual journey, not as the sole source of guidance.

## 🆘 Support

### For Deployment Issues
1. **Railway**: Check [RAILWAY_DEPLOYMENT_GUIDE.md](RAILWAY_DEPLOYMENT_GUIDE.md)
2. **Checklist**: Follow [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
3. **Railway Support**: [docs.railway.app](https://docs.railway.app)

### For Application Issues
1. Run `python setup.py` for diagnostics
2. Check the troubleshooting section above
3. Verify your API keys and internet connection

## 🚀 Quick Deploy Command

Ready to deploy? Run this one-liner:

```bash
# Clean, commit, and deploy to Railway
./deploy_cleanup.sh && git add . && git commit -m "Ready for Railway" && git push
```

Then connect to Railway and add your API keys!

---

## 🎉 Production Features

✅ **Railway-optimized** configuration  
✅ **Persistent database** across deployments  
✅ **Health monitoring** and auto-restart  
✅ **Production security** settings  
✅ **Comprehensive documentation** and tools  
✅ **One-click deployment** ready  

**🙏 "Knowledge is structured in consciousness" - Sri Sri Ravi Shankar**

**Ready to share spiritual wisdom with the world! Deploy now! 🚀**

**Jai Guru Dev! 🙏**