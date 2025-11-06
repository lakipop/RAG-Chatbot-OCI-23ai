# config_loader.py
"""
Configuration Loader Module

This module is responsible for loading all configuration and secrets from the .env file.
It provides a centralized, secure way to access OCI and Database credentials throughout the app.

Why we need this:
- In Java, you might use Spring's @Value or application.properties
- In Python, we use python-dotenv to load environment variables
- This keeps secrets OUT of code and OUT of Git (via .gitignore)

This module returns two dictionaries:
1. oci_config: Contains OCI authentication details
2. db_config: Contains Oracle Database connection details
"""

import os
from dotenv import load_dotenv

def load_config():
    """
    Loads configuration from .env file and returns two configuration dictionaries.
    
    Returns:
        tuple: (oci_config, db_config)
            - oci_config (dict): OCI authentication configuration
            - db_config (dict): Oracle Database connection configuration
    
    Raises:
        ValueError: If any required environment variable is missing
    """
    
    # === Step 1: Load environment variables from .env file ===
    # This reads the .env file and makes all KEY=VALUE pairs available via os.getenv()
    # Think of this like loading a .properties file in Java
    load_dotenv()
    
    print("Loading configuration from .env file...")
    
    # === Step 2: Build OCI Configuration Dictionary ===
    # This dictionary format is what the OCI SDK expects for authentication
    # It's similar to the ~/.oci/config file format, but loaded from environment variables
    
    oci_config = {
        "user": os.getenv("OCI_USER_ID"),
        "tenancy": os.getenv("OCI_TENANCY_ID"),
        "region": os.getenv("OCI_REGION"),
        "fingerprint": os.getenv("OCI_KEY_FINGERPRINT"),
        "key_file": os.getenv("OCI_PRIVATE_KEY_PATH"),
        # Store compartment_id separately since it's not part of the standard OCI auth config
        "compartment_id": os.getenv("COMPARTMENT_ID")
    }
    
    # === Step 3: Build Database Configuration Dictionary ===
    # This contains all the info needed to connect to Oracle Database
    db_config = {
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
        "DB_DSN": os.getenv("DB_DSN")  # DSN = Data Source Name (connection string)
    }
    
    # === Step 4: Validation - Check for Missing Values ===
    # This is defensive programming - fail fast if config is incomplete
    # In Java, you might use @NotNull or validation annotations
    
    # Check OCI config
    for key, value in oci_config.items():
        if not value:
            raise ValueError(
                f"Missing required OCI configuration: {key}. "
                f"Please check your .env file and ensure all OCI_* variables are set."
            )
    
    # Check DB config
    for key, value in db_config.items():
        if not value:
            raise ValueError(
                f"Missing required database configuration: {key}. "
                f"Please check your .env file and ensure all DB_* variables are set."
            )
    
    print("✓ Configuration loaded successfully!")
    print(f"  - OCI Region: {oci_config['region']}")
    print(f"  - DB User: {db_config['DB_USER']}")
    
    # Return both configuration dictionaries as a tuple
    return oci_config, db_config


# === Optional: Standalone Test ===
# This allows you to test the config loader by running: python config_loader.py
if __name__ == "__main__":
    print("\n=== Testing Configuration Loader ===\n")
    try:
        oci_cfg, db_cfg = load_config()
        print("\n✓ All configurations loaded successfully!")
        print("\nOCI Config Keys:", list(oci_cfg.keys()))
        print("DB Config Keys:", list(db_cfg.keys()))
    except ValueError as e:
        print(f"\n✗ Configuration Error: {e}")
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
