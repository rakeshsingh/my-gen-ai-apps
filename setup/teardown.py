#!/usr/bin/env python3
"""
Teardown script for GenAI Apps - Removes vector database and associated files.

This script:
1. Loads configuration from config/dev.ini
2. Identifies and removes vector database files
3. Cleans up temporary files and logs
4. Provides detailed logging and confirmation prompts
"""

import os
import sys
import shutil
import logging
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helpers import config_handler

def setup_logging():
    """Setup logging for the teardown process."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('teardown.log', mode='a')
        ]
    )
    return logging.getLogger(__name__)

def get_database_info(logger):
    """Get information about the existing database."""
    try:
        db_path = config_handler.get_db_path()
        logger.info(f"Database path from config: {db_path}")
        
        if not os.path.exists(db_path):
            logger.info("✓ No database directory found")
            return None, []
        
        # Find all database-related files
        db_files = []
        total_size = 0
        
        for root, dirs, files in os.walk(db_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                total_size += file_size
                db_files.append({
                    'path': file_path,
                    'size': file_size,
                    'relative_path': os.path.relpath(file_path, db_path)
                })
        
        if db_files:
            logger.info(f"Found {len(db_files)} database files")
            logger.info(f"Total database size: {total_size / (1024 * 1024):.2f} MB")
            
            # Show file details
            for file_info in db_files[:10]:  # Show first 10 files
                size_kb = file_info['size'] / 1024
                logger.info(f"  - {file_info['relative_path']} ({size_kb:.1f} KB)")
            
            if len(db_files) > 10:
                logger.info(f"  ... and {len(db_files) - 10} more files")
        
        return db_path, db_files
        
    except Exception as e:
        logger.error(f"Error getting database info: {str(e)}")
        return None, []

def get_additional_cleanup_files(logger):
    """Get list of additional files that can be cleaned up."""
    cleanup_files = []
    
    # Log files
    log_files = ['setup.log', 'teardown.log', 'app.log']
    for log_file in log_files:
        if os.path.exists(log_file):
            cleanup_files.append({
                'path': log_file,
                'type': 'log',
                'size': os.path.getsize(log_file)
            })
    
    # Session files
    session_dir = 'helpers/sessions'
    if os.path.exists(session_dir):
        for file in os.listdir(session_dir):
            if file.endswith('.json'):
                file_path = os.path.join(session_dir, file)
                cleanup_files.append({
                    'path': file_path,
                    'type': 'session',
                    'size': os.path.getsize(file_path)
                })
    
    # Cache files
    cache_dirs = ['__pycache__', 'helpers/__pycache__']
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            for root, dirs, files in os.walk(cache_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    cleanup_files.append({
                        'path': file_path,
                        'type': 'cache',
                        'size': os.path.getsize(file_path)
                    })
    
    if cleanup_files:
        logger.info(f"Found {len(cleanup_files)} additional files for cleanup:")
        for file_info in cleanup_files:
            size_kb = file_info['size'] / 1024
            logger.info(f"  - {file_info['path']} ({file_info['type']}, {size_kb:.1f} KB)")
    
    return cleanup_files

def confirm_deletion(db_path, db_files, cleanup_files):
    """Ask user for confirmation before deletion."""
    print("\n" + "=" * 60)
    print("DELETION CONFIRMATION")
    print("=" * 60)
    
    if db_files:
        total_db_size = sum(f['size'] for f in db_files) / (1024 * 1024)
        print(f"Vector Database:")
        print(f"  Location: {db_path}")
        print(f"  Files: {len(db_files)}")
        print(f"  Size: {total_db_size:.2f} MB")
        print()
    
    if cleanup_files:
        total_cleanup_size = sum(f['size'] for f in cleanup_files) / 1024
        cleanup_by_type = {}
        for f in cleanup_files:
            cleanup_by_type[f['type']] = cleanup_by_type.get(f['type'], 0) + 1
        
        print(f"Additional Files:")
        for file_type, count in cleanup_by_type.items():
            print(f"  {file_type.title()} files: {count}")
        print(f"  Total size: {total_cleanup_size:.1f} KB")
        print()
    
    if not db_files and not cleanup_files:
        print("No files found to delete.")
        return False
    
    print("⚠️  WARNING: This action cannot be undone!")
    print()
    
    # Main deletion confirmation
    response = input("Do you want to delete the vector database? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        return False
    
    # Additional files confirmation
    if cleanup_files:
        response = input("Also delete log files, sessions, and cache? (y/N): ").strip().lower()
        return response in ['y', 'yes']
    
    return True

def delete_database(db_path, logger):
    """Delete the vector database directory."""
    try:
        if os.path.exists(db_path):
            logger.info(f"Deleting database directory: {db_path}")
            shutil.rmtree(db_path)
            logger.info("✓ Database directory deleted successfully")
            return True
        else:
            logger.info("✓ Database directory does not exist")
            return True
    except Exception as e:
        logger.error(f"✗ Error deleting database: {str(e)}")
        return False

def delete_additional_files(cleanup_files, logger):
    """Delete additional cleanup files."""
    success_count = 0
    error_count = 0
    
    for file_info in cleanup_files:
        try:
            file_path = file_info['path']
            if os.path.isfile(file_path):
                os.remove(file_path)
                logger.info(f"✓ Deleted {file_info['type']} file: {file_path}")
                success_count += 1
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                logger.info(f"✓ Deleted {file_info['type']} directory: {file_path}")
                success_count += 1
        except Exception as e:
            logger.error(f"✗ Error deleting {file_path}: {str(e)}")
            error_count += 1
    
    # Clean up empty cache directories
    cache_dirs = ['__pycache__', 'helpers/__pycache__']
    for cache_dir in cache_dirs:
        try:
            if os.path.exists(cache_dir) and not os.listdir(cache_dir):
                os.rmdir(cache_dir)
                logger.info(f"✓ Removed empty directory: {cache_dir}")
        except Exception as e:
            logger.error(f"✗ Error removing directory {cache_dir}: {str(e)}")
    
    logger.info(f"Cleanup summary: {success_count} files deleted, {error_count} errors")
    return error_count == 0

def main():
    """Main teardown function."""
    logger = setup_logging()
    
    print("=" * 60)
    print("GenAI Apps - Vector Database Teardown")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    logger.info("Starting GenAI Apps teardown process...")
    
    try:
        # Step 1: Get database information
        db_path, db_files = get_database_info(logger)
        
        # Step 2: Get additional cleanup files
        cleanup_files = get_additional_cleanup_files(logger)
        
        # Step 3: Confirm deletion
        if not confirm_deletion(db_path, db_files, cleanup_files):
            logger.info("Teardown cancelled by user")
            print("Teardown cancelled.")
            sys.exit(0)
        
        # Step 4: Perform deletion
        success = True
        
        if db_path and db_files:
            success &= delete_database(db_path, logger)
        
        if cleanup_files:
            success &= delete_additional_files(cleanup_files, logger)
        
        # Step 5: Report results
        if success:
            print()
            print("=" * 60)
            print("✓ TEARDOWN COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("All vector database files have been removed.")
            print("You can run setup.py again to recreate the database.")
            print()
            logger.info("Teardown completed successfully")
        else:
            print()
            print("=" * 60)
            print("⚠️  TEARDOWN COMPLETED WITH ERRORS!")
            print("=" * 60)
            print("Some files may not have been deleted.")
            print("Check the log messages above for details.")
            print()
            logger.warning("Teardown completed with errors")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Unexpected error during teardown: {str(e)}")
        print()
        print("=" * 60)
        print("✗ TEARDOWN FAILED!")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        sys.exit(1)

if __name__ == "__main__":
    main()
