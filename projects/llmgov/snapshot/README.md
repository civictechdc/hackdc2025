# CMS Data Embeddings Generator and Agent

This project consists of two main components:

1. A data processing pipeline that extracts CMS document content and generates vector embeddings
2. A RAG-powered agent that answers questions about CMS regulations using the vector database

## Data Processing Pipeline

The `transform_files_to_embeddings.py` script processes CMS document files from local storage, extracts text content, generates embeddings using Amazon Titan Text Embeddings V2, and uploads them to an S3 vector store.

### Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Ensure you have AWS credentials configured with access to Bedrock and S3 Vectors services.

### Usage

Basic usage:

```bash
python transform_files_to_embeddings.py
```

This will process files from `raw_data/CMS` and upload the embeddings to the S3 vector store.

### Data Processing Details

The script:
- Processes multiple CMS directories in parallel
- Extracts text from HTML documents, docket summaries, and comments
- Generates embeddings using Amazon Titan Text Embeddings V2
- Uploads vectors to an S3 vector store in batches
- Preserves metadata from the original documents

## CMS Agent

The project includes a CMS Agent that can answer questions about CMS dockets and regulations using the vector store and RAG (Retrieval-Augmented Generation).

### Web Interface

Run the Streamlit web application:

```bash
streamlit run cms_agent_web.py
```

This starts a user-friendly chat interface where you can:
- Ask questions about CMS dockets and regulations
- Get AI-generated answers based on retrieved document context
- View source information for transparency
- Maintain chat history for continued conversations
- Adjust the number of sources to retrieve

### How the Agent Works

The `cms_agent_web.py` script:
1. Takes user questions through a Streamlit chat interface
2. Converts the question to an embedding using Amazon Titan Text Embeddings V2
3. Queries the S3 vector store to retrieve relevant document chunks
4. Constructs a prompt with the retrieved context
5. Uses Amazon Bedrock (Claude 3 Sonnet) to generate a response
6. Displays the answer along with source information

### Example Questions

- What are common issues with Medicare?
- Explain the latest changes to Medicaid eligibility
- What are the key points in the recent CMS final rule?
- How does CMS regulate telehealth services?
