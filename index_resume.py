"""
Resume Indexation Script

This script indexes a resume (PDF, DOCX, or TXT) into Pinecone vector database.
It splits the document into chunks and creates embeddings for efficient retrieval.

Usage:
    python index_resume.py --file path/to/resume.pdf
    python index_resume.py --file path/to/resume.docx
    python index_resume.py --file path/to/resume.txt
    
    # To clear index before uploading:
    python index_resume.py --file path/to/resume.pdf --clear

    # To upload multiple files:
    python index_resume.py --directory path/to/resume_sections/
"""

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config.configuration import load_config
from backend.retriever import Retriever
from langchain.text_splitter import RecursiveCharacterTextSplitter


def index_file(file_path: str, retriever: Retriever, clear_index: bool = False):
    """Index a single file into Pinecone."""
    
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Determine file type and load accordingly
    extension = file_path.suffix.lower()
    
    print(f"\n📄 Loading document: {file_path.name}")
    
    if extension == '.pdf':
        documents = retriever.pdf_loader(str(file_path))
    elif extension in ['.docx', '.doc']:
        documents = retriever.docx_loader(str(file_path))
    elif extension == '.txt':
        documents = retriever.text_loader(str(file_path))
    else:
        raise ValueError(f"Unsupported file type: {extension}. Supported: .pdf, .docx, .txt")
    
    print(f"✅ Loaded {len(documents)} document(s)")
    
    # Split documents into chunks for better retrieval
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    print("🔪 Splitting documents into chunks...")
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")
    
    # Add metadata to chunks
    for i, chunk in enumerate(chunks):
        chunk.metadata['source'] = file_path.name
        chunk.metadata['chunk_id'] = i
    
    # Clear index if requested
    if clear_index:
        print("\n⚠️  Clearing existing index...")
        try:
            retriever.delete_all_documents()
            print("✅ Index cleared")
        except Exception as e:
            print(f"⚠️  Could not clear index: {e}")
    
    # Upload to Pinecone
    print("\n⬆️  Uploading to Pinecone...")
    try:
        ids = retriever.upload_docs_index(chunks)
        print(f"✅ Successfully indexed {len(ids)} chunks from {file_path.name}")
        return ids
    except Exception as e:
        print(f"❌ Error uploading to Pinecone: {e}")
        raise


def index_directory(directory_path: str, retriever: Retriever, clear_index: bool = False):
    """Index all supported files in a directory."""
    
    directory = Path(directory_path)
    
    if not directory.exists() or not directory.is_dir():
        raise NotADirectoryError(f"Directory not found: {directory}")
    
    # Find all supported files
    supported_extensions = ['.pdf', '.docx', '.doc', '.txt']
    files = [f for f in directory.iterdir() if f.suffix.lower() in supported_extensions]
    
    if not files:
        print(f"⚠️  No supported files found in {directory}")
        return
    
    print(f"\n📁 Found {len(files)} file(s) to index:")
    for f in files:
        print(f"  - {f.name}")
    
    # Clear index only before the first file
    first_file = True
    
    for file in files:
        try:
            index_file(str(file), retriever, clear_index=(clear_index and first_file))
            first_file = False
        except Exception as e:
            print(f"❌ Error indexing {file.name}: {e}")
            continue
    
    print(f"\n✅ Indexing complete!")


def main():
    parser = argparse.ArgumentParser(
        description='Index resume documents into Pinecone vector database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python index_resume.py --file resume.pdf
  python index_resume.py --file resume.docx --clear
  python index_resume.py --directory ./resume_sections/
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', type=str, help='Path to a single resume file (PDF, DOCX, or TXT)')
    group.add_argument('--directory', type=str, help='Path to directory containing resume files')
    
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear the Pinecone index before uploading (WARNING: deletes all existing data)'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    print("🔧 Loading configuration...")
    try:
        parameters = load_config()
        print(f"✅ Configuration loaded")
        print(f"   LLM Provider: {parameters['llm_provider']}")
        print(f"   Embedding Provider: {parameters['embedding_provider']}")
        print(f"   Pinecone Index: {parameters['pinecone_index_name']}")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("\n💡 Make sure you have created a .env file with the required variables.")
        print("   See .env.example for reference.")
        return 1
    
    # Initialize retriever
    print("\n🔌 Connecting to Pinecone...")
    try:
        retriever = Retriever(parameters)
        print("✅ Connected to Pinecone")
    except Exception as e:
        print(f"❌ Failed to connect to Pinecone: {e}")
        return 1
    
    # Index file(s)
    try:
        if args.file:
            index_file(args.file, retriever, args.clear)
        elif args.directory:
            index_directory(args.directory, retriever, args.clear)
        
        print("\n🎉 All done! Your resume is now indexed and ready to use.")
        print(f"   You can now run: python app.py")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Indexing failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
