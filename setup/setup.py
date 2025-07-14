#!/usr/bin/env python3
"""
Setup script for GenAI Apps - Creates vector database by indexing documents.

This script:
1. Loads configuration from config/dev.ini
2. Validates required directories and files exist
3. Calls the indexer to create the vector database
4. Provides detailed logging and error handling
"""

import os
import sys
import logging
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helpers import config_handler, indexer

def setup_logging():
    """Setup logging for the setup process."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('setup.log', mode='a')
        ]
    )
    return logging.getLogger(__name__)

def validate_prerequisites(logger):
    """Validate that all prerequisites are met before setup."""
    logger.info("Validating prerequisites...")
    
    try:
        # Check if config file exists
        config_file = 'config/dev.ini'
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        logger.info(f"✓ Configuration file found: {config_file}")
        
        # Validate configuration parameters
        data_folder = config_handler.get_data_folder()
        db_path = config_handler.get_db_path()
        embedding_model = config_handler.get_embedding_model()
        
        logger.info(f"✓ Data folder: {data_folder}")
        logger.info(f"✓ Database path: {db_path}")
        logger.info(f"✓ Embedding model: {embedding_model}")
        
        # Check if data folder exists
        if not os.path.exists(data_folder):
            raise FileNotFoundError(f"Data folder not found: {data_folder}")
        logger.info(f"✓ Data folder exists and is accessible")
        
        # Check if data folder contains files
        files = []
        for root, dirs, filenames in os.walk(data_folder):
            for filename in filenames:
                if filename.endswith('.md'):
                    files.append(os.path.join(root, filename))
        
        if not files:
            logger.warning(f"⚠ No .md files found in data folder: {data_folder}")
        else:
            logger.info(f"✓ Found {len(files)} .md files to index")
        
        # Create database directory if it doesn't exist
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            logger.info(f"✓ Created database directory: {db_dir}")
        else:
            logger.info(f"✓ Database directory exists: {db_dir}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Prerequisite validation failed: {str(e)}")
        return False

def check_existing_database(logger):
    """Check if vector database already exists."""
    try:
        db_path = config_handler.get_db_path()
        
        # Check for Chroma database files
        chroma_files = [
            os.path.join(db_path, 'chroma.sqlite3'),
            os.path.join(db_path, 'index'),
            os.path.join(db_path, 'chroma-collections.parquet'),
            os.path.join(db_path, 'chroma-embeddings.parquet')
        ]
        
        existing_files = [f for f in chroma_files if os.path.exists(f)]
        
        if existing_files:
            logger.warning(f"⚠ Existing database files found:")
            for file in existing_files:
                logger.warning(f"  - {file}")
            
            response = input("Database already exists. Do you want to recreate it? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                logger.info("User chose to recreate the database")
                return True
            else:
                logger.info("User chose to keep existing database")
                return False
        else:
            logger.info("✓ No existing database found, proceeding with creation")
            return True
            
    except Exception as e:
        logger.error(f"Error checking existing database: {str(e)}")
        return True  # Proceed anyway

def create_vector_database(logger):
    """Create the vector database using the indexer."""
    try:
        logger.info("Starting vector database creation...")
        logger.info("This may take several minutes depending on the number of documents...")
        
        # Call the indexer to create the vector database
        vector_store = indexer.index_files(config_handler)
        
        if vector_store:
            logger.info("✓ Vector database created successfully!")
            
            # Get some statistics about the created database
            db_path = config_handler.get_db_path()
            if os.path.exists(db_path):
                # Calculate database size
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(db_path):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        total_size += os.path.getsize(filepath)
                
                size_mb = total_size / (1024 * 1024)
                logger.info(f"✓ Database size: {size_mb:.2f} MB")
                logger.info(f"✓ Database location: {db_path}")
            
            return True
        else:
            logger.error("✗ Failed to create vector database")
            return False
            
    except Exception as e:
        logger.error(f"✗ Error creating vector database: {str(e)}")
        logger.error("This might be due to:")
        logger.error("  - Ollama not running (start with: ollama serve)")
        logger.error("  - Embedding model not available (install with: ollama pull mxbai-embed-large)")
        logger.error("  - Network connectivity issues")
        logger.error("  - Insufficient disk space")
        return False

def main():
    """Main setup function."""
    logger = setup_logging()
    
    print("=" * 60)
    print("GenAI Apps - Vector Database Setup")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    logger.info("Starting GenAI Apps setup process...")
    
    # Step 1: Validate prerequisites
    if not validate_prerequisites(logger):
        logger.error("Setup failed due to prerequisite validation errors")
        sys.exit(1)
    
    # Step 2: Check for existing database
    if not check_existing_database(logger):
        logger.info("Setup cancelled by user")
        sys.exit(0)
    
    # Step 3: Create vector database
    if create_vector_database(logger):
        print()
        print("=" * 60)
        print("✓ SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Your vector database has been created and is ready to use.")
        print()
        print("Next steps:")
        print("1. Run your chatbot: streamlit run chatbot_ui_rag.py")
        print("2. Run your agent: streamlit run agent_ui_rag.py")
        print("3. Use CLI chatbot: python chatbot_cli.py")
        print()
        logger.info("Setup completed successfully")
    else:
        print()
        print("=" * 60)
        print("✗ SETUP FAILED!")
        print("=" * 60)
        print("Please check the error messages above and try again.")
        print("Common solutions:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Install the embedding model: ollama pull mxbai-embed-large")
        print("3. Check your config/dev.ini file paths")
        print()
        logger.error("Setup failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
