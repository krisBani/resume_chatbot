import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import CohereEmbeddings
from langchain_openai import OpenAIEmbeddings


class Retriever():
    """Retriever Class
    This class encapsulates the functionality for retrieving and managing documents within the Pinecone vector database.
    It handles the creation of embeddings, interaction with the Pinecone service, and the loading of documents.
    It supports multiple embedding providers (Cohere, OpenAI, etc.) to generate vector representations of documents.
    """
    
    def __init__(self, parameters: dict[str, any]):
        self.parameters = parameters
        
        # Initialize embeddings based on provider
        embedding_provider = parameters.get('embedding_provider', 'cohere').lower()
        
        if embedding_provider == 'cohere':
            embeddings = CohereEmbeddings(
                cohere_api_key=parameters['embedding_api_key'],
                model=parameters.get('embedding_model', 'embed-english-v3.0')
            )
        elif embedding_provider == 'openai':
            embeddings = OpenAIEmbeddings(
                openai_api_key=parameters['embedding_api_key'],
                model=parameters.get('embedding_model', 'text-embedding-ada-002')
            )
        else:
            raise ValueError(f"Unsupported embedding provider: {embedding_provider}")
        
        self.embeddings = embeddings
        self.index_name = parameters['pinecone_index_name']
        
        # Initialize Pinecone
        pc = Pinecone(api_key=parameters['pinecone_api_key'])
        
        # Check if index exists, if not create it
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        if self.index_name not in existing_indexes:
            print(f"Index '{self.index_name}' does not exist. Creating new index...")
            # Create index with appropriate dimensions based on embedding model
            dimension = self._get_embedding_dimension(embedding_provider, parameters.get('embedding_model'))
            
            pc.create_index(
                name=self.index_name,
                dimension=dimension,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region=parameters.get('pinecone_environment', 'us-east-1')
                )
            )
            print(f"Index '{self.index_name}' created successfully.")
        
        # Initialize vector store
        self.vector_store = PineconeVectorStore(
            index_name=self.index_name,
            embedding=embeddings,
            pinecone_api_key=parameters['pinecone_api_key']
        )
    
    def _get_embedding_dimension(self, provider, model):
        """Get the dimension of embeddings based on provider and model."""
        dimensions = {
            'cohere': {
                'embed-english-v3.0': 1024,
                'embed-english-light-v3.0': 384,
                'embed-multilingual-v3.0': 1024,
            },
            'openai': {
                'text-embedding-ada-002': 1536,
                'text-embedding-3-small': 1536,
                'text-embedding-3-large': 3072,
            }
        }
        
        return dimensions.get(provider, {}).get(model, 1024)  # Default to 1024
    
    def docx_loader(self, docx_file_path: str):
        """Loads documents from a DOCX file.

        Args:
            docx_file_path (str): The path to the DOCX file.

        Returns:
            list: A list of Document objects loaded from the DOCX file.
        """
        from langchain_community.document_loaders import Docx2txtLoader
        loader = Docx2txtLoader(docx_file_path)
        return loader.load()
    
    def pdf_loader(self, pdf_file_path: str):
        """Loads documents from a PDF file.
        Uses pypdf directly for Windows compatibility.

        Args:
            pdf_file_path (str): The path to the PDF file.

        Returns:
            list: A list of Document objects loaded from the PDF file.
        """
        import pypdf
        from langchain.schema import Document
        
        documents = []
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text.strip():
                    documents.append(Document(
                        page_content=text,
                        metadata={"source": pdf_file_path, "page": page_num}
                    ))
        return documents
    
    def text_loader(self, text_file_path: str):
        """Loads documents from a text file.

        Args:
            text_file_path (str): The path to the text file.

        Returns:
            list: A list of Document objects loaded from the text file.
        """
        from langchain_community.document_loaders import TextLoader
        loader = TextLoader(text_file_path)
        return loader.load()
    
    def upload_docs_index(self, docs):
        """Uploads documents to the Pinecone index.

        Args:
            docs (list): A list of Document objects to be uploaded.
            
        Returns:
            list: List of document IDs that were added.
        """
        try:
            ids = self.vector_store.add_documents(documents=docs)
            print(f"Successfully uploaded {len(ids)} documents to Pinecone index '{self.index_name}'.")
            return ids
        except Exception as e:
            print(f"Error uploading documents to Pinecone: {str(e)}")
            raise

    def get_vector_store(self):
        """Retrieves the vector store object.

        Returns:
            PineconeVectorStore: The vector store object.
        """
        return self.vector_store
    
    def delete_all_documents(self):
        """Deletes all documents from the Pinecone index.
        Warning: This operation cannot be undone.
        """
        pc = Pinecone(api_key=self.parameters['pinecone_api_key'])
        index = pc.Index(self.index_name)
        
        # Delete all vectors in the index
        index.delete(delete_all=True)
        print(f"All documents deleted from index '{self.index_name}'.")
