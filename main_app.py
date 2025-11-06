# main_app.py
"""
RAG Chatbot - Streamlit Application

This is the main application file that provides a web interface for asking questions
about OCI using Retrieval-Augmented Generation (RAG).

What this app does:
1. Takes a user's question
2. Searches the Oracle Vector Database for relevant document chunks
3. Sends the question + relevant chunks to OCI's LLM
4. Returns a factual answer based ONLY on our documents (no hallucinations!)

Run this AFTER running ingest.py
Command: streamlit run main_app.py

Java Developer Note:
- This is like a Spring Boot web controller, but with a built-in UI
- Streamlit handles all the HTTP/HTML/CSS for you
- You just write Python and Streamlit renders it as a web page
"""

import streamlit as st
import config_loader
from langchain_oci.embeddings import OCIGenAIEmbeddings
from langchain_oci import OCIGenAI
from langchain_community.vectorstores.oraclevs import OracleVS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import oracledb
import sys


# ================================================================
# HELPER FUNCTION: Initialize Services (with Caching)
# ================================================================
@st.cache_resource
def initialize_services():
    """
    Initializes all the services needed for the RAG chatbot.
    
    The @st.cache_resource decorator is CRITICAL for performance:
    - Without it: Reconnects to DB and reinitializes models on EVERY button click
    - With it: Initializes once, then reuses the same connections
    
    Think of it like @Singleton or connection pooling in Java.
    
    Returns:
        tuple: (qa_chain, vector_store) - The ready-to-use RAG chain and vector store
    """
    
    print("🔧 Initializing services (this happens once)...")
    
    try:
        # ========================================================
        # 1. Load Configuration
        # ========================================================
        oci_config, db_config = config_loader.load_config()
        compartment_id = oci_config.pop("compartment_id")
        
        # ========================================================
        # 2. Initialize OCI Embeddings (for query embedding)
        # ========================================================
        # We need this to convert the USER'S QUESTION into a vector
        # so we can search for similar document vectors
        #
        # Example:
        # User asks: "What is OCI Compute?"
        # This model converts it to: [0.23, 0.67, 0.12, ...]
        # Then we search for documents with similar vectors
        
        print("   Loading embeddings model...")
        oci_embeddings = OCIGenAIEmbeddings(
            model_id="cohere.embed-english-v3.0",
            service_endpoint=f"https://inference.generativeai.{oci_config['region']}.oci.oraclecloud.com",
            compartment_id=compartment_id,
            auth_type="API_KEY",
            auth_profile=oci_config
        )
        
        # ========================================================
        # 3. Initialize OCI Generative AI (for answer generation)
        # ========================================================
        # This is the "brain" - the large language model that actually
        # reads the retrieved documents and answers the question
        #
        # Think of it like calling a REST API endpoint for text generation
        
        print("   Loading LLM (Cohere Command)...")
        oci_llm = OCIGenAI(
            model_id="cohere.command-r-plus",  # Cohere's Command-R-Plus model
            service_endpoint=f"https://inference.generativeai.{oci_config['region']}.oci.oraclecloud.com",
            compartment_id=compartment_id,
            auth_type="API_KEY",
            auth_profile=oci_config,
            model_kwargs={
                "max_tokens": 500,      # Maximum length of the answer
                "temperature": 0.3      # Low = more factual, High = more creative
            }
        )
        
        # ========================================================
        # 4. Connect to Oracle Vector Database
        # ========================================================
        # We connect to the EXISTING table created by ingest.py
        # We're NOT inserting data here - just querying it
        
        print("   Connecting to Oracle Vector Database...")
        connection = oracledb.connect(
            user=db_config["DB_USER"],
            password=db_config["DB_PASSWORD"],
            dsn=db_config["DB_DSN"]
        )
        
        # Verify the table exists
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM rag_documents")
            doc_count = cursor.fetchone()[0]
            print(f"   ✓ Connected! Found {doc_count} documents in database")
        except oracledb.DatabaseError:
            st.error("❌ The 'rag_documents' table doesn't exist! Did you run ingest.py first?")
            sys.exit(1)
        
        # ========================================================
        # 5. Initialize Vector Store
        # ========================================================
        # This wraps our Oracle connection and provides semantic search
        vector_store = OracleVS(
            client=connection,
            embedding_function=oci_embeddings,
            table_name="rag_documents",
            distance_strategy=OracleVS.DistanceStrategy.COSINE
        )
        
        # ========================================================
        # 6. Create the Retriever
        # ========================================================
        # A "retriever" is LangChain's abstraction for "find me relevant documents"
        # 
        # search_kwargs={'k': 3} means "return the 3 most similar documents"
        # You can increase this number if you want more context
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={'k': 3}  # Return top 3 most relevant chunks
        )
        
        # ========================================================
        # 7. Create Custom Prompt Template
        # ========================================================
        # This is the instruction we give to the LLM
        # It's CRITICAL for good RAG - it tells the LLM:
        # 1. What its role is
        # 2. To ONLY use the provided context
        # 3. What to do if it doesn't know
        
        prompt_template = """You are a helpful AI assistant answering questions about Oracle Cloud Infrastructure (OCI).

Use the following pieces of context to answer the question at the end.
If you don't know the answer based on the context provided, just say "I don't have enough information in my knowledge base to answer that question." 
Do NOT make up an answer or use information outside of the provided context.

Context:
{context}

Question: {question}

Helpful Answer:"""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # ========================================================
        # 8. Create the RAG Chain (THE MAGIC HAPPENS HERE!)
        # ========================================================
        # RetrievalQA is LangChain's pre-built RAG implementation
        # It chains together:
        #   1. Retriever (finds relevant docs)
        #   2. LLM (generates answer based on those docs)
        #
        # chain_type="stuff" means "stuff all retrieved docs into the prompt"
        # (There are other strategies like "map_reduce" for large documents)
        
        print("   Building RAG chain...")
        qa_chain = RetrievalQA.from_chain_type(
            llm=oci_llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,  # Return which docs were used
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        print("✅ Initialization complete!\n")
        
        return qa_chain, vector_store
        
    except Exception as e:
        st.error(f"❌ Failed to initialize services: {str(e)}")
        st.stop()


# ================================================================
# MAIN APPLICATION UI
# ================================================================

# Configure the Streamlit page (must be the first Streamlit command)
st.set_page_config(
    page_title="OCI RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# App Title and Description
st.title("🤖 OCI RAG Chatbot")
st.markdown("""
Ask me anything about **Oracle Cloud Infrastructure (OCI)**! 

I will search through our knowledge base and provide answers based **only** on the documents I have access to. 
This means I won't hallucinate or make up information - if I don't know, I'll tell you!
""")

st.markdown("---")

# ================================================================
# Initialize Services (runs once due to caching)
# ================================================================
try:
    with st.spinner("🔧 Initializing RAG system..."):
        qa_chain, vector_store = initialize_services()
except Exception as e:
    st.error(f"Failed to initialize: {e}")
    st.stop()

# ================================================================
# User Input Section
# ================================================================
st.subheader("💬 Ask a Question")

# Create a text input for the user's question
user_question = st.text_input(
    "Type your question here:",
    placeholder="Example: What are the benefits of OCI Compute?",
    key="question_input"
)

# Create a button to submit the question
ask_button = st.button("🔍 Get Answer", type="primary")

# ================================================================
# Query Processing and Response
# ================================================================
if ask_button and user_question:
    # User clicked the button and provided a question
    
    # Show a loading spinner while processing
    with st.spinner("🤔 Thinking... (retrieving documents and generating answer)"):
        try:
            print(f"\n{'='*60}")
            print(f"📝 New question: {user_question}")
            print(f"{'='*60}\n")
            
            # ========================================================
            # THE MAGIC CALL - This does everything:
            # ========================================================
            # 1. Embeds the user's question
            # 2. Searches Oracle DB for similar document chunks
            # 3. Constructs a prompt with question + retrieved chunks
            # 4. Sends to OCI LLM
            # 5. Returns the generated answer + source documents
            
            response = qa_chain.invoke({"query": user_question})
            
            # The response is a dictionary with:
            # - 'result': The generated answer
            # - 'source_documents': The chunks that were used
            
            print(f"✅ Response generated successfully\n")
            
            # ========================================================
            # Display the Answer
            # ========================================================
            st.markdown("### 📖 Answer")
            
            # Display the answer in a nice info box
            st.info(response["result"])
            
            # ========================================================
            # Display Source Documents (Optional but Recommended!)
            # ========================================================
            st.markdown("---")
            st.markdown("### 📚 Sources Used")
            
            st.markdown("""
            <small>These are the document chunks that were retrieved from the database 
            and used to generate the answer above. This transparency helps you verify 
            the answer and shows you where to look for more information.</small>
            """, unsafe_allow_html=True)
            
            # Get unique source files (avoid duplicates)
            source_docs = response.get('source_documents', [])
            
            if source_docs:
                # Create expandable sections for each source document
                for i, doc in enumerate(source_docs, 1):
                    source_file = doc.metadata.get('source', 'Unknown')
                    
                    with st.expander(f"📄 Source {i}: {source_file}"):
                        # Show the actual text that was retrieved
                        st.markdown(f"**Content:**")
                        st.text(doc.page_content)
                        
                        # Show metadata (helpful for debugging)
                        st.markdown(f"**Metadata:**")
                        st.json(doc.metadata)
            else:
                st.warning("⚠️ No source documents were returned. This is unusual!")
            
            print(f"Used {len(source_docs)} source document(s)\n")
            
        except Exception as e:
            # Handle any errors gracefully
            st.error(f"❌ An error occurred while processing your question: {str(e)}")
            print(f"❌ Error: {str(e)}\n")
            
            # Show some troubleshooting tips
            with st.expander("🔧 Troubleshooting Tips"):
                st.markdown("""
                **Common issues:**
                1. **Connection timeout**: Check your network connection and OCI credentials
                2. **Database error**: Make sure you ran `ingest.py` successfully
                3. **Rate limiting**: OCI API has rate limits - wait a moment and try again
                4. **Invalid credentials**: Verify your `.env` file has correct values
                """)

elif ask_button and not user_question:
    # User clicked button but didn't enter a question
    st.warning("⚠️ Please enter a question before clicking 'Get Answer'")

# ================================================================
# Sidebar: Additional Info and Instructions
# ================================================================
with st.sidebar:
    st.header("ℹ️ About This App")
    
    st.markdown("""
    This is a **Retrieval-Augmented Generation (RAG)** chatbot that answers questions 
    about Oracle Cloud Infrastructure.
    
    ### How it works:
    
    1. 🔍 **Your question** is converted to a vector
    2. 🗄️ **Oracle Database** finds similar document chunks
    3. 🤖 **OCI LLM** generates an answer using those chunks
    4. ✅ **You get** a factual, grounded answer!
    
    ### Why RAG?
    
    Traditional chatbots can "hallucinate" (make up information). 
    RAG solves this by:
    - ✅ Only using your private documents
    - ✅ Providing source citations
    - ✅ Being transparent about what it knows
    
    ### Technology Stack:
    - **LangChain**: RAG orchestration
    - **OCI Generative AI**: Embeddings & LLM
    - **Oracle 23ai**: Vector database
    - **Streamlit**: Web interface
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### 💡 Example Questions:
    - What is Oracle Cloud Infrastructure?
    - What are the benefits of OCI Compute?
    - How does OCI ensure security?
    - What types of compute instances does OCI offer?
    """)
    
    st.markdown("---")
    
    # Show system status
    st.markdown("### 📊 System Status")
    try:
        # Get document count
        cursor = vector_store.client.cursor()
        cursor.execute("SELECT COUNT(*) FROM rag_documents")
        doc_count = cursor.fetchone()[0]
        st.success(f"✅ {doc_count} documents in knowledge base")
    except:
        st.error("❌ Cannot connect to database")

# ================================================================
# Footer
# ================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>Built with ❤️ using LangChain, OCI Generative AI, and Oracle 23ai Vector Search</small>
</div>
""", unsafe_allow_html=True)
