import configparser

def read_config(filename='config.ini'):
    """Reads the configuration from a .ini file."""
    config = configparser.ConfigParser()
    config.read(filename)
    if not config.sections():
        raise ValueError("Configuration file is empty or not found.")   
    # print(f"Database Host: {db_host}")
    # print(f"Database Port: {db_port} (Type: {type(db_port)})")
    # print(f"Database User: {db_user}")
    # print(f"Database Password: {db_password}")

def get_data_folder(config_file='config/dev.ini'):
    """Gets the data folder path from the configuration file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    
    if 'General' not in config or 'DATA_FOLDER' not in config['General']:
        raise ValueError("DATA_FOLDER not found in the configuration file.")
    
    data_folder = config['General']['DATA_FOLDER']
    
    if not data_folder:
        raise ValueError("DATA_FOLDER is empty in the configuration file.")
    
    return data_folder  

def get_db_path(config_file='config/dev.ini'):
    """Gets the database path from the configuration file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    
    if 'General' not in config or 'DB_PATH' not in config['General']:
        raise ValueError("DB_PATH not found in the configuration file.")
    
    db_path = config['General']['DB_PATH']
    
    if not db_path:
        raise ValueError("DB_PATH is empty in the configuration file.")
    
    return db_path  

def get_embedding_model(config_file='config/dev.ini'):
    """Gets the embedding model name from the configuration file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    
    if 'General' not in config or 'EMBEDDING_MODEL' not in config['General']:
        raise ValueError("EMBEDDING_MODEL not found in the configuration file.")
    
    embedding_model = config['General']['EMBEDDING_MODEL']
    
    if not embedding_model:
        raise ValueError("EMBEDDING_MODEL is empty in the configuration file.")
    
    return embedding_model

if __name__ == "__main__":
    read_config()