import os

def load_config():
    """
    Load configuration from environment variables.
    
    Supports multiple LLM providers:
    - groq (default, recommended)
    - openai
    - together
    - mistral
    - kimi
    - custom (for any OpenAI-compatible API)
    
    Environment variables required:
    - LLM_PROVIDER: The LLM provider to use (default: groq)
    - LLM_API_KEY: API key for the LLM provider
    - LLM_MODEL: Model name to use
    - LLM_BASE_URL: Base URL for the API (optional, for custom providers)
    - PINECONE_API_KEY: API key for Pinecone
    - PINECONE_ENVIRONMENT: Pinecone environment (e.g., 'us-east-1-aws')
    - PINECONE_INDEX_NAME: Name of the Pinecone index
    - EMBEDDING_PROVIDER: Provider for embeddings (default: cohere)
    - EMBEDDING_API_KEY: API key for embeddings (if different from LLM)
    - RESUME_OWNER_NAME: Name of the resume owner
    """
    
    # LLM Configuration
    llm_provider = os.getenv('LLM_PROVIDER', 'groq').lower()
    
    # Default models for each provider
    default_models = {
        'groq': 'llama-3.1-8b-instant',
        'openai': 'gpt-4o-mini',
        'together': 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',
        'mistral': 'mistral-small-latest',
        'kimi': 'moonshot-v1-8k',  # Example, adjust based on actual Kimi API
        'custom': 'gpt-3.5-turbo'
    }
    
    # Base URLs for each provider
    base_urls = {
        'groq': 'https://api.groq.com/openai/v1',
        'openai': 'https://api.openai.com/v1',
        'together': 'https://api.together.xyz/v1',
        'mistral': 'https://api.mistral.ai/v1',
        'kimi': 'https://api.moonshot.cn/v1',  # Example, adjust based on actual Kimi API
        'custom': os.getenv('LLM_BASE_URL', 'https://api.openai.com/v1')
    }
    
    parameters = {
        # LLM Configuration
        'llm_provider': llm_provider,
        'llm_api_key': os.getenv('LLM_API_KEY'),
        'llm_model': os.getenv('LLM_MODEL', default_models.get(llm_provider, 'llama-3.1-8b-instant')),
        'llm_base_url': os.getenv('LLM_BASE_URL', base_urls.get(llm_provider)),
        'llm_temperature': float(os.getenv('LLM_TEMPERATURE', '0')),
        
        # Embeddings Configuration
        'embedding_provider': os.getenv('EMBEDDING_PROVIDER', 'cohere').lower(),
        'embedding_api_key': os.getenv('EMBEDDING_API_KEY', os.getenv('LLM_API_KEY')),
        'embedding_model': os.getenv('EMBEDDING_MODEL', 'embed-english-v3.0'),
        
        # Pinecone Configuration
        'pinecone_api_key': os.getenv('PINECONE_API_KEY'),
        'pinecone_environment': os.getenv('PINECONE_ENVIRONMENT', 'us-east-1-aws'),
        'pinecone_index_name': os.getenv('PINECONE_INDEX_NAME', 'resume-chatbot'),
        
        # Application Configuration
        'resume_owner_name': os.getenv('RESUME_OWNER_NAME', 'The Candidate'),
        'candidate_gender': os.getenv('CANDIDATE_GENDER', 'neutral').lower(),  # male, female, or neutral
        
        # Legacy compatibility (will be removed in future versions)
        'openai_api_key': os.getenv('LLM_API_KEY') if llm_provider == 'openai' else None,
    }
    
    # Validate required parameters
    required_params = ['llm_api_key', 'pinecone_api_key', 'pinecone_index_name']
    missing_params = [param for param in required_params if not parameters.get(param)]
    
    if missing_params:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_params.upper())}")
    
    return parameters
