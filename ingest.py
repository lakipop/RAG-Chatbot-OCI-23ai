# ingest.py
"""
Data Ingestion Script for RAG Pipeline

This script performs the ONE-TIME ingestion of documents into our RAG system.
It's like setting up a library - you only do it once (or when you want to add new books).

What this script does:
1. Reads text files from the /data folder
2. Splits them into smaller chunks (better for retrieval)
3. Converts each chunk into a vector embedding (using OCI)
4. Stores the embeddings in Oracle 23ai Vector Database

Run this script BEFORE running the Streamlit app.
Command: python ingest.py

Java Developer Note:
- This is similar to a data migration script or database seeding script
- Think of it like an ETL (Extract, Transform, Load) process
"""

import os
import sys
import config_loader
from langchain_oci.embeddings import OCIGenAIEmbeddings
from langchain_community.vectorstores.oraclevs import OracleVS
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import oracledb

def run_ingestion():
    """
    Main ingestion function that orchestrates the entire process.
    
    This is the entry point - like a 'main' method in Java.
    It coordinates all the steps needed to ingest documents.
    """
    
    print("\n" + "="*60)
    print("🚀 STARTING DATA INGESTION PIPELINE")
    print("="*60 + "\n")
    
    try:
        # ============================================================
        # STEP 1: Load Configuration
        # ============================================================
        # Load all secrets from .env file
        # This is like loading application.properties in Spring Boot
        print("📋 Step 1: Loading configuration from .env file...")
        oci_config, db_config = config_loader.load_config()
        
        # Extract compartment_id separately (it's not part of the standard OCI auth config)
        compartment_id = oci_config.pop("compartment_id")
        print("✓ Configuration loaded successfully\n")

        # ============================================================
        # STEP 2: Load Documents from /data folder
        # ============================================================
        print("📂 Step 2: Loading documents from ./data folder...")
        
        # DirectoryLoader is a LangChain utility that:
        # - Scans a directory for files matching a pattern
        # - Loads them into LangChain's Document format
        # Think of it like a file reader that understands our directory structure
        
        loader = DirectoryLoader(
            "./data",           # The folder to scan
            glob="**/*.txt",    # Pattern: all .txt files in any subdirectory
            loader_cls=TextLoader  # Use TextLoader for .txt files
        )
        
        documents = loader.load()
        
        if not documents:
            print("⚠️  WARNING: No documents found in ./data folder!")
            print("   Please add .txt files to the ./data folder and try again.")
            sys.exit(1)
        
        print(f"✓ Loaded {len(documents)} document(s)")
        
        # Show what we loaded (helpful for debugging)
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get('source', 'Unknown')
            length = len(doc.page_content)
            print(f"   - Document {i}: {source} ({length} characters)")
        print()

        # ============================================================
        # STEP 3: Split Documents into Chunks
        # ============================================================
        print("✂️  Step 3: Splitting documents into chunks...")
        
        # WHY DO WE SPLIT?
        # Large documents are hard to work with in RAG because:
        # 1. Embeddings work better on focused, specific text
        # 2. LLMs have context limits (can't fit entire books)
        # 3. Smaller chunks = more precise retrieval
        #
        # Analogy: Instead of giving someone an entire encyclopedia to answer
        # a question, you give them just the relevant page or paragraph.
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,      # Each chunk will be ~1000 characters
            chunk_overlap=200     # 200 chars overlap between chunks (preserves context)
        )
        
        # RecursiveCharacterTextSplitter is "smart" - it tries to split on
        # paragraph breaks, then sentences, then words (in that order)
        # This keeps related content together
        
        chunks = text_splitter.split_documents(documents)
        print(f"✓ Created {len(chunks)} chunk(s) from {len(documents)} document(s)")
        print(f"   Average chunk size: {sum(len(c.page_content) for c in chunks) // len(chunks)} characters\n")

        # ============================================================
        # STEP 4: Initialize OCI Embeddings Model
        # ============================================================
        print("🧠 Step 4: Initializing OCI Embeddings model...")
        
        # WHAT ARE EMBEDDINGS?
        # Embeddings convert text into vectors (lists of numbers).
        # Similar texts have similar vectors, which allows us to do "semantic search".
        #
        # Example:
        # "What is OCI Compute?" → [0.23, 0.67, 0.12, ...]
        # "Tell me about OCI compute services" → [0.24, 0.65, 0.13, ...]
        # These two would be "close" in vector space even though the words differ!
        
        oci_embeddings = OCIGenAIEmbeddings(
            model_id="cohere.embed-english-v3.0",  # Cohere's embedding model
            service_endpoint=f"https://inference.generativeai.{oci_config['region']}.oci.oraclecloud.com",
            compartment_id=compartment_id,
            auth_type="API_KEY",
            auth_profile=oci_config
        )
        
        print(f"✓ Using embedding model: cohere.embed-english-v3.0")
        print(f"   Region: {oci_config['region']}\n")

        # ============================================================
        # STEP 5: Connect to Oracle Vector Database
        # ============================================================
        print("🗄️  Step 5: Connecting to Oracle 23ai Vector Database...")
        
        # Create a connection to Oracle Database
        # This is similar to creating a JDBC connection in Java
        connection = oracledb.connect(
            user=db_config["DB_USER"],
            password=db_config["DB_PASSWORD"],
            dsn=db_config["DB_DSN"]
        )
        
        print(f"✓ Connected to Oracle Database as {db_config['DB_USER']}\n")

        # ============================================================
        # STEP 6: Initialize Vector Store
        # ============================================================
        print("🔧 Step 6: Initializing Oracle Vector Store...")
        
        # OracleVS is LangChain's integration with Oracle Vector Search
        # It handles:
        # - Creating the vector table (if it doesn't exist)
        # - Storing embeddings
        # - Performing similarity searches
        #
        # Think of it as a specialized DAO (Data Access Object) for vectors
        
        vector_store = OracleVS(
            client=connection,
            embedding_function=oci_embeddings,
            table_name="rag_documents",  # Name of the table to create/use
            distance_strategy=OracleVS.DistanceStrategy.COSINE  # How to measure similarity
        )
        
        print(f"✓ Vector store initialized with table: rag_documents")
        print(f"   Distance strategy: COSINE (measures angle between vectors)\n")

        # ============================================================
        # STEP 7: Clear Existing Data (for clean re-runs)
        # ============================================================
        print("🗑️  Step 7: Clearing any existing data in the table...")
        
        # This is optional but helpful during development
        # It ensures a clean state when you re-run the ingestion
        try:
            # Drop the table if it exists
            cursor = connection.cursor()
            cursor.execute("DROP TABLE rag_documents PURGE")
            connection.commit()
            print("✓ Existing table dropped\n")
        except oracledb.DatabaseError as e:
            # Table doesn't exist - that's fine!
            print("✓ No existing table to drop (this is normal on first run)\n")

        # ============================================================
        # STEP 8: Add Documents to Vector Store (THE MAIN EVENT!)
        # ============================================================
        print("💾 Step 8: Adding documents to vector store...")
        print("   This will:")
        print("   1. Create embeddings for each chunk (calls OCI API)")
        print("   2. Store embeddings + text in Oracle Database")
        print("   3. Create vector index for fast similarity search")
        print("\n   ⏳ This may take 30-60 seconds depending on document size...\n")
        
        # This single call does A LOT behind the scenes:
        # - Calls OCI API to get embeddings for each chunk
        # - Creates the Oracle table with vector column
        # - Inserts all chunks with their embeddings
        # - Creates a vector index for fast retrieval
        vector_store.add_documents(chunks)
        
        print(f"✓ Successfully added {len(chunks)} chunks to vector store!")
        
        # ============================================================
        # STEP 9: Verify the Ingestion
        # ============================================================
        print("\n🔍 Step 9: Verifying ingestion...")
        
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM rag_documents")
        count = cursor.fetchone()[0]
        
        print(f"✓ Verification complete: {count} records in database")
        
        # Close the connection
        connection.close()
        
        # ============================================================
        # SUCCESS!
        # ============================================================
        print("\n" + "="*60)
        print("✅ INGESTION COMPLETE!")
        print("="*60)
        print("\nYour RAG system is now ready to use.")
        print("Next step: Run the Streamlit app with:")
        print("   streamlit run main_app.py")
        print()

    except Exception as e:
        print("\n" + "="*60)
        print("❌ ERROR DURING INGESTION")
        print("="*60)
        print(f"\nError details: {str(e)}")
        print("\nCommon issues:")
        print("  1. Check your .env file - are all credentials correct?")
        print("  2. Is your Oracle Database accessible from this network?")
        print("  3. Do you have files in the ./data folder?")
        print("  4. Are your OCI credentials valid and do you have proper permissions?")
        print()
        sys.exit(1)


# ================================================================
# SCRIPT ENTRY POINT
# ================================================================
# This is Python's equivalent to 'public static void main' in Java
# It ensures this code only runs when the script is executed directly
# (not when imported as a module)

if __name__ == "__main__":
    run_ingestion()
