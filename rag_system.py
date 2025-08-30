import os
import yaml
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManagerForRetrieverRun
from langchain.schema import BaseRetriever
import numpy as np
from document_processor import DocumentProcessor, Teaching

@dataclass
class UserContext:
    """Store user context from preliminary questions"""
    life_aspect: str = ""
    emotional_state: str = ""
    guidance_type: str = ""
    specific_situation: str = ""

class CustomRetriever(BaseRetriever):
    """Custom retriever that combines vector search with metadata filtering"""
    
    def __init__(self, vectorstore, teachings: List[Teaching], top_k: int = 5, **kwargs):
        # Initialize parent class properly
        super().__init__(**kwargs)
        # Set instance attributes
        self.vectorstore = vectorstore
        self.teachings = teachings
        self.top_k = top_k
        self.processor = DocumentProcessor("")
    
    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun = None) -> List[Document]:
        """Get relevant documents using vector search and metadata filtering"""
        try:
            # Get vector search results
            vector_results = self.vectorstore.similarity_search(query, k=self.top_k * 2)
            
            # Extract teaching numbers from results
            teaching_numbers = []
            for doc in vector_results:
                if 'number' in doc.metadata:
                    teaching_numbers.append(doc.metadata['number'])
            
            # Find corresponding teachings
            relevant_teachings = [t for t in self.teachings if t.number in teaching_numbers]
            
            # Convert back to documents with enhanced metadata
            enhanced_docs = []
            for teaching in relevant_teachings[:self.top_k]:
                doc = Document(
                    page_content=teaching.content,
                    metadata={
                        'number': teaching.number,
                        'title': teaching.title,
                        'date': teaching.date,
                        'location': teaching.location,
                        'topics': ', '.join(teaching.topics),
                        'keywords': ', '.join(teaching.keywords),
                        'problem_categories': ', '.join(teaching.problem_categories),
                        'emotional_states': ', '.join(teaching.emotional_states),
                        'life_situations': ', '.join(teaching.life_situations)
                    }
                )
                enhanced_docs.append(doc)
            
            return enhanced_docs
            
        except Exception as e:
            print(f"Error in CustomRetriever._get_relevant_documents: {e}")
            # Fallback to basic vector search
            return self.vectorstore.similarity_search(query, k=self.top_k)

class RAGSystem:
    """RAG System for JAI GURU DEV AI Chatbot"""
    
    def __init__(self, config_path: str, knowledge_base_path: str):
        self.config_path = config_path
        self.knowledge_base_path = knowledge_base_path
        self.config = self.load_config()
        self.teachings = []
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None
        self.llm = None
        
        # Initialize components step by step with error handling
        try:
            print("🔧 Setting up LLM...")
            self.setup_llm()
            print("🔧 Setting up embeddings...")
            self.setup_embeddings()
            print("🔧 Loading and processing documents...")
            self.load_and_process_documents()
            print("🔧 Setting up retrieval chain...")
            self.setup_retrieval_chain()
            print("✅ RAG System initialized successfully!")
        except Exception as e:
            print(f"❌ Error initializing RAG system: {e}")
            raise
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def setup_llm(self):
        """Setup Language Model based on configuration"""
        provider = self.config['model_provider']['default']
        
        if provider == "openai":
            model_config = self.config['model_provider']['openai']
            self.llm = ChatOpenAI(
                model=model_config['model'],
                temperature=model_config['temperature'],
                max_tokens=model_config['max_tokens']
            )
        elif provider == "groq":
            model_config = self.config['model_provider']['groq']
            self.llm = ChatGroq(
                model=model_config['model'],
                temperature=model_config['temperature'],
                max_tokens=model_config['max_tokens']
            )
        else:
            raise ValueError(f"Unsupported model provider: {provider}")
    
    def setup_embeddings(self):
        """Setup embeddings model"""
        self.embeddings = OpenAIEmbeddings(
            model=self.config['embeddings']['model']
        )
    
    def load_and_process_documents(self):
        """Load and process all teachings from markdown files"""
        processor = DocumentProcessor(self.knowledge_base_path)
        self.teachings = processor.load_all_teachings()
        
        if not self.teachings:
            raise ValueError("No teachings found in knowledge base")
        
        # Convert teachings to LangChain documents
        documents = []
        for teaching in self.teachings:
            doc = Document(
                page_content=teaching.content,
                metadata={
                    'number': teaching.number,
                    'title': teaching.title,
                    'date': teaching.date,
                    'location': teaching.location,
                    'topics': ', '.join(teaching.topics),
                    'keywords': ', '.join(teaching.keywords),
                    'problem_categories': ', '.join(teaching.problem_categories),
                    'emotional_states': ', '.join(teaching.emotional_states),
                    'life_situations': ', '.join(teaching.life_situations),
                    'full_text': teaching.get_full_text()
                }
            )
            documents.append(doc)
        
        # Setup vector store
        try:
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory="./chroma_db"
            )
            print(f"✅ Loaded {len(documents)} teachings into vector database")
        except Exception as e:
            print(f"❌ Error creating vector store: {e}")
            raise
    
    def setup_retrieval_chain(self):
        """Setup the retrieval QA chain"""
        
        # Custom prompt template
        template = """
        You are "JAI GURU DEV AI", a compassionate spiritual guide based on Sri Sri Ravi Shankar's teachings. 
        Your purpose is to provide wisdom, guidance, and spiritual insights to help users navigate life's challenges.

        Context: Based on the user's questions and situation, here are relevant teachings:

        {context}

        Human Question: {question}

        Guidelines for your response:
        1. Speak with compassion, wisdom, and gentleness
        2. Draw insights from the provided teachings but explain them in a way that's relevant to the user's situation
        3. If multiple teachings are relevant, synthesize the wisdom
        4. Always maintain the spiritual and philosophical tone of the original teachings
        5. End with a practical suggestion or reflection question when appropriate
        6. Use "Jai Guru Dev" as a blessing at the end when appropriate

        Response:
        """
        
        PROMPT = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Setup custom retriever with error handling
        try:
            print("🔧 Creating custom retriever...")
            self.retriever = CustomRetriever(
                vectorstore=self.vectorstore,
                teachings=self.teachings,
                top_k=self.config['rag']['top_k_results']
            )
            print("✅ Custom retriever created successfully")
        except Exception as e:
            print(f"❌ Error creating custom retriever: {e}")
            print("🔧 Falling back to basic vector store retriever...")
            # Fallback to basic retriever
            self.retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": self.config['rag']['top_k_results']}
            )
        
        # Setup QA chain
        try:
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.retriever,
                chain_type_kwargs={"prompt": PROMPT},
                return_source_documents=True
            )
            print("✅ QA chain setup complete")
        except Exception as e:
            print(f"❌ Error setting up QA chain: {e}")
            raise
    
    def search_by_context(self, user_context: UserContext) -> List[Teaching]:
        """Search teachings based on user context"""
        processor = DocumentProcessor("")
        
        # Extract search terms from user context
        topics = [user_context.life_aspect] if user_context.life_aspect else []
        emotions = [user_context.emotional_state] if user_context.emotional_state else []
        situations = [user_context.specific_situation] if user_context.specific_situation else []
        
        # Use metadata search
        context_teachings = processor.search_teachings_by_metadata(
            teachings=self.teachings,
            query_topics=topics,
            query_emotions=emotions,
            query_situations=situations
        )
        
        return context_teachings[:5]  # Return top 5 contextually relevant teachings
    
    def get_response(self, question: str, user_context: UserContext = None) -> Dict[str, Any]:
        """Get response from RAG system"""
        try:
            # Enhance query with user context
            enhanced_query = question
            if user_context:
                context_parts = []
                if user_context.life_aspect:
                    context_parts.append(f"Life aspect: {user_context.life_aspect}")
                if user_context.emotional_state:
                    context_parts.append(f"Emotional state: {user_context.emotional_state}")
                if user_context.guidance_type:
                    context_parts.append(f"Seeking: {user_context.guidance_type}")
                if user_context.specific_situation:
                    context_parts.append(f"Situation: {user_context.specific_situation}")
                
                if context_parts:
                    enhanced_query = f"{question}\n\nUser Context: {'; '.join(context_parts)}"
            
            # Get response from QA chain
            result = self.qa_chain({"query": enhanced_query})
            
            # Extract source information
            sources = []
            for doc in result.get('source_documents', []):
                source_info = {
                    'teaching_number': doc.metadata.get('number', 'Unknown'),
                    'title': doc.metadata.get('title', 'Unknown'),
                    'topics': doc.metadata.get('topics', ''),
                    'date': doc.metadata.get('date', 'Not specified')
                }
                sources.append(source_info)
            
            return {
                'answer': result['result'],
                'sources': sources,
                'success': True
            }
            
        except Exception as e:
            return {
                'answer': f"I apologize, but I encountered an error while processing your question. Please try rephrasing your question or contact support. Error: {str(e)}",
                'sources': [],
                'success': False,
                'error': str(e)
            }
    
    def get_initial_questions(self) -> List[str]:
        """Get initial questions for user context gathering"""
        return self.config['chatbot']['initial_questions']

def test_openai_connection():
    """Test OpenAI API connection"""
    try:
        import openai
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return {"success": False, "error": "OpenAI API key not found in environment"}
        
        # Test with a simple completion
        client = ChatOpenAI(model="gpt-4o-mini", max_tokens=10, temperature=0)
        response = client.invoke("Say 'Hello'")
        
        return {"success": True, "message": "OpenAI connection successful!", "response": response.content}
        
    except Exception as e:
        return {"success": False, "error": f"OpenAI connection failed: {str(e)}"}

def test_groq_connection():
    """Test Groq API connection"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return {"success": False, "error": "Groq API key not found in environment"}
        
        # Test with a simple completion
        client = ChatGroq(model="llama3-8b-8192", max_tokens=10, temperature=0)
        response = client.invoke("Say 'Hello'")
        
        return {"success": True, "message": "Groq connection successful!", "response": response.content}
        
    except Exception as e:
        return {"success": False, "error": f"Groq connection failed: {str(e)}"}

def test_embeddings_connection():
    """Test OpenAI Embeddings connection"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return {"success": False, "error": "OpenAI API key not found for embeddings"}
        
        # Test embeddings
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        test_embedding = embeddings.embed_query("Hello world")
        
        return {"success": True, "message": f"Embeddings connection successful! (dimension: {len(test_embedding)})"}
        
    except Exception as e:
        return {"success": False, "error": f"Embeddings connection failed: {str(e)}"}

if __name__ == "__main__":
    # Test the RAG system
    rag = RAGSystem(
        config_path="config.yaml",
        knowledge_base_path="Knowledge_Base"
    )
    
    # Test query
    test_context = UserContext(
        life_aspect="relationships",
        emotional_state="confused",
        guidance_type="specific guidance"
    )
    
    response = rag.get_response("How do I deal with relationship conflicts?", test_context)
    print("Response:", response['answer'])
    print("Sources:", response['sources'])
