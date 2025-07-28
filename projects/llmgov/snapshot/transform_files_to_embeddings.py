# Populate a vector index with embeddings from Amazon Titan Text Embeddings V2.
import boto3
import json
from bs4 import BeautifulSoup
from pathlib import Path
import PyPDF2
import dotenv
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

dotenv.load_dotenv()

# Create Bedrock Runtime and S3 Vectors clients in the AWS Region of your choice. 
bedrock = boto3.client("bedrock-runtime", region_name='us-east-1')
s3vectors = boto3.client("s3vectors", region_name='us-east-1')

def extract_text_from_html(html_content):
    """Extract text from HTML content, removing HTML tags."""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + " "
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
        return ""

def get_embedding(text):
    """Generate embedding for a given text using Amazon Titan Text Embeddings V2."""
    # Truncate text if it's too long (Titan has a context limit)
    if len(text) > 8000:
        text = text[:8000]
        
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": text})
    )

    # Extract embedding from response.
    response_body = json.loads(response["body"].read())
    return response_body["embedding"]

def get_embeddings_batch(texts, batch_size=10):
    """Generate embeddings for a batch of texts."""
    embeddings = []
    
    # Process in smaller batches to avoid overwhelming the API
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
        
        # Process each text in the batch
        batch_embeddings = []
        for text in batch:
            if len(text) > 8000:
                text = text[:8000]
            batch_embeddings.append(get_embedding(text))
            
        embeddings.extend(batch_embeddings)
        
    return embeddings

def process_docket_dir(cms_dir):
    """Process docket summary files from a CMS directory."""
    results = []
    
    # Navigate to the text directory
    text_dir = next((d for d in cms_dir.iterdir() if d.name.startswith("text-")), None)
    if not text_dir:
        return results
    
    # Navigate to the docket directory
    docket_dir = text_dir / "docket"
    if not docket_dir.exists():
        return results
    
    # Process docket summary file (typically named after the docket ID)
    for file_path in docket_dir.iterdir():
        if file_path.name.endswith(".json"):
            # Read JSON content
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    json_data = json.load(f)
                    
                    # Extract docket ID
                    docket_id = json_data.get('data', {}).get('id', '')
                    
                    # Extract docket attributes
                    attributes = json_data.get('data', {}).get('attributes', {})
                    
                    # Extract docket abstract/description
                    docket_abstract = attributes.get('dkAbstract', '')
                    
                    # Add to our collection
                    results.append({
                        "id": f"{docket_id}_docket_summary",
                        "text": docket_abstract if docket_abstract else "No abstract available",
                        "metadata": {
                            "link": attributes.get("links", {}).get("self", "")
                        },
                        "source_type": "docket_summary"
                    })
                    
                except Exception as e:
                    print(f"Error processing docket file {file_path}: {e}")
    
    return results

def process_documents_dir(cms_dir):
    """Process HTML documents from a CMS directory."""
    results = []
    
    # Navigate to the text directory
    text_dir = next((d for d in cms_dir.iterdir() if d.name.startswith("text-")), None)
    if not text_dir:
        return results
    
    # Navigate to the documents directory
    docs_dir = text_dir / "documents"
    if not docs_dir.exists():
        return results
    
    # Process each document
    for file_path in docs_dir.iterdir():
        if file_path.name.endswith("_content.htm"):
            # Extract document ID from filename
            doc_id = file_path.name.split("_")[0]
            
            # Read HTML content
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Extract text from HTML
            text_content = extract_text_from_html(html_content)
            
            # Get metadata from JSON file if available
            json_path = docs_dir / f"{doc_id}.json"
            metadata = {}
            if json_path.exists():
                with open(json_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    # Extract useful metadata
                    attributes = json_data.get('data', {}).get('attributes', {})
                    metadata = {
                        "title": attributes.get("title", ""),
                        "document_type": attributes.get("documentType", ""),
                        "agency_id": attributes.get("agencyId", ""),
                        "docket_id": attributes.get("docketId", ""),
                        "posted_date": attributes.get("postedDate", ""),
                        "link": attributes.get("links", {}).get("self", "")
                    }
            
            # Add to our collection if text content is not empty
            if text_content.strip():
                results.append({
                    "id": doc_id + "_htm",
                    "text": text_content if text_content else "No text available",
                    "metadata": metadata,
                    "source_type": "html"
                })
    
    return results

def process_comments_dir(cms_dir):
    """Process comments from a CMS directory."""
    results = []
    
    # Navigate to the text directory
    text_dir = next((d for d in cms_dir.iterdir() if d.name.startswith("text-")), None)
    if not text_dir:
        return results
    
    # Navigate to the comments directory
    comments_dir = text_dir / "comments"
    if not comments_dir.exists():
        return results
    
    # Process each comment JSON file
    for file_path in comments_dir.iterdir():
        if file_path.name.endswith(".json"):
            # Read JSON content
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    json_data = json.load(f)
                    
                    # Extract comment ID
                    comment_id = json_data.get('data', {}).get('id', '')
                    link = json_data.get('data', {}).get('links', {}).get('self', '')
                    
                    # Extract comment text
                    attributes = json_data.get('data', {}).get('attributes', {})
                    comment_text = attributes.get('comment', '')
                    print("Comment", comment_id, link)
                    # Extract metadata
                    metadata = {
                        "title": attributes.get("title", ""),
                        "document_type": attributes.get("documentType", ""),
                        "agency_id": attributes.get("agencyId", ""),
                        "docket_id": attributes.get("docketId", ""),
                        "posted_date": attributes.get("postedDate", ""),
                        "comment_on_document_id": attributes.get("commentOnDocumentId", ""),
                        "link": link,
                        "comment_id": comment_id
                    }
                    
                    # Check for attachments
                    has_attachments = False
                    if json_data.get('data', {}).get('relationships', {}).get('attachments', {}).get('data'):
                        has_attachments = True
                    
                    # If comment text is empty or just refers to attachments, note this in metadata
                    if not comment_text or comment_text.lower() == "see attached file(s)":
                        metadata["comment_in_attachments"] = True
                    
                    # Add to our collection
                    results.append({
                        "id": comment_id + "_comment",
                        "text": comment_text if comment_text else "No comment text available",
                        "metadata": metadata,
                        "source_type": "comment",
                        "has_attachments": has_attachments
                    })
                    
                except Exception as e:
                    print(f"Error processing comment file {file_path}: {e}")
    
    return results

def process_cms_directory(cms_dir):
    """Process a CMS directory including dockets, documents, and comments."""
    results = []
    
    # Process docket summaries
    docket_results = process_docket_dir(cms_dir)
    results.extend(docket_results)
    
    # Process documents
    document_results = process_documents_dir(cms_dir)
    results.extend(document_results)
    
    # Process comments
    comment_results = process_comments_dir(cms_dir)
    results.extend(comment_results)
    
    return results

def get_embedding_worker(text):
    """Worker function to generate embedding for a single text."""
    if len(text) > 8000:
        text = text[:8000]
        
    try:
        # Create a new client for each worker to avoid connection issues
        bedrock_client = boto3.client("bedrock-runtime", region_name='us-east-1')
        
        response = bedrock_client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=json.dumps({"inputText": text})
        )

        # Extract embedding from response
        response_body = json.loads(response["body"].read())
        return response_body["embedding"]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Return a zero vector as fallback (adjust dimension as needed)
        return [0.0] * 1536  # Titan embeddings are 1536-dimensional

def upload_vectors_batch(batch, bucket_name, index_name):
    """Upload a batch of vectors to S3 vectors."""
    try:
        # Create a new client for each worker to avoid connection issues
        s3vectors_client = boto3.client("s3vectors", region_name='us-east-1')
        
        s3vectors_client.put_vectors(
            vectorBucketName=bucket_name,
            indexName=index_name,
            vectors=batch
        )
        return len(batch)
    except Exception as e:
        print(f"Error uploading vector batch: {e}")
        return 0

# Main execution
if __name__ == "__main__":
    start_time = time.time()
    
    # Get all CMS directories
    base_path = Path("raw_data/CMS")
    cms_dirs = [d for d in base_path.iterdir() if d.is_dir()]
    
    print(f"Found {len(cms_dirs)} CMS directories to process")
    
    # Process directories in parallel
    cms_docs = []
    num_workers = min(multiprocessing.cpu_count(), len(cms_dirs))
    
    print(f"Using {num_workers} workers for parallel processing")
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Submit all directories for processing
        future_to_dir = {executor.submit(process_cms_directory, cms_dir): cms_dir for cms_dir in cms_dirs}
        
        # Process results as they complete
        for future in as_completed(future_to_dir):
            dir_path = future_to_dir[future]
            try:
                results = future.result()
                cms_docs.extend(results)
                print(f"Processed {dir_path.name}, found {len(results)} items")
            except Exception as e:
                print(f"Error processing {dir_path.name}: {e}")
    
    print(f"Found {len(cms_docs)} documents total")
    print(f"Data extraction completed in {time.time() - start_time:.2f} seconds")
    
    # Generate embeddings for each document in parallel
    print("Generating embeddings...")
    embedding_start_time = time.time()
    
    # Prepare texts for parallel embedding generation
    doc_texts = [(i, doc['id'] + " " + doc["text"]) for i, doc in enumerate(cms_docs)]
    
    # Determine optimal batch size and number of workers for embedding generation
    embedding_workers = min(multiprocessing.cpu_count() * 2, len(cms_docs))
    print(f"Using {embedding_workers} workers for parallel embedding generation")
    
    # Process embeddings in parallel
    with ProcessPoolExecutor(max_workers=embedding_workers) as executor:
        # Submit all texts for embedding generation
        future_to_index = {executor.submit(get_embedding_worker, text): (i, doc_id) 
                          for i, (doc_id, text) in enumerate([(i, t) for i, t in doc_texts])}
        
        # Process results as they complete
        completed = 0
        total = len(future_to_index)
        for future in as_completed(future_to_index):
            i, doc_id = future_to_index[future]
            try:
                embedding = future.result()
                cms_docs[i]["embedding"] = embedding
                completed += 1
                if completed % 10 == 0 or completed == total:
                    print(f"Generated embeddings: {completed}/{total} ({completed/total*100:.1f}%)")
            except Exception as e:
                print(f"Error generating embedding for document {i}: {e}")
    
    print(f"Embedding generation completed in {time.time() - embedding_start_time:.2f} seconds")
    
    # Write embeddings into vector index with metadata
    print("Writing embeddings to vector index...")
    vectors = []
    for doc in cms_docs:
        # Skip documents without embeddings
        if "embedding" not in doc:
            continue
            
        # Create metadata dictionary based on source type
        if doc["source_type"] == "html":
            metadata = {
                "source_text": doc["text"][:1000],  # Truncate text for metadata
                "title": doc["metadata"].get("title", ""),
                "document_type": doc["metadata"].get("document_type", ""),
                "agency_id": doc["metadata"].get("agency_id", ""),
                "docket_id": doc["metadata"].get("docket_id", ""),
                "posted_date": doc["metadata"].get("posted_date", ""),
                "source_type": "html"
            }
        elif doc["source_type"] == "comment":
            metadata = {
                "source_text": doc["text"][:1000],  # Truncate text for metadata
                "title": doc["metadata"].get("title", ""),
                "document_type": doc["metadata"].get("document_type", ""),
                "agency_id": doc["metadata"].get("agency_id", ""),
                "docket_id": doc["metadata"].get("docket_id", ""),
                "posted_date": doc["metadata"].get("posted_date", ""),
                "comment_on_document_id": doc["metadata"].get("comment_on_document_id", ""),
                "source_type": "comment",
                "comment_id": doc["metadata"].get("comment_id", ""),
                "link": doc["metadata"].get("link", "")
            }
        elif doc["source_type"] == "docket_summary":
            metadata = {
                "source_text": doc["text"][:1000],  # Truncate text for metadata
                "title": doc["metadata"].get("title", "") if hasattr(doc, "metadata") else "",
                "agency_id": doc["metadata"].get("agency_id", "") if hasattr(doc, "metadata") else "",
                "docket_type": doc["metadata"].get("docket_type", "") if hasattr(doc, "metadata") else "",
                "effective_date": doc["metadata"].get("effective_date", "") if hasattr(doc, "metadata") else "",
                "modify_date": doc["metadata"].get("modify_date", "") if hasattr(doc, "metadata") else "",
                "rin": doc["metadata"].get("rin", "") if hasattr(doc, "metadata") else "",
                "source_type": "docket_summary"
            }
        else:  # pdf
            continue
        
        vectors.append({
            "key": doc["id"],
            "data": {"float32": doc["embedding"]},
            "metadata": metadata
        })
    
    # Upload vectors in parallel batches
    upload_start_time = time.time()
    if vectors:
        # Process in batches to avoid API limits
        batch_size = 100
        vector_batches = [vectors[i:i+batch_size] for i in range(0, len(vectors), batch_size)]
        
        print(f"Uploading {len(vectors)} vectors in {len(vector_batches)} batches")
        
        # Determine optimal number of workers for upload
        upload_workers = min(8, len(vector_batches))  # Limit to 8 concurrent uploads
        print(f"Using {upload_workers} workers for parallel vector upload")
        
        # Upload batches in parallel
        uploaded_count = 0
        with ProcessPoolExecutor(max_workers=upload_workers) as executor:
            # Submit all batches for upload
            future_to_batch = {executor.submit(upload_vectors_batch, batch, 
                                              "ekim-civictech-hackathon-2025", 
                                              "cms-titan-3"): i 
                              for i, batch in enumerate(vector_batches)}
            
            # Process results as they complete
            for future in as_completed(future_to_batch):
                batch_index = future_to_batch[future]
                try:
                    count = future.result()
                    uploaded_count += count
                    print(f"Uploaded batch {batch_index+1}/{len(vector_batches)} ({uploaded_count}/{len(vectors)} vectors)")
                except Exception as e:
                    print(f"Error uploading batch {batch_index}: {e}")
        
        print(f"Successfully added {uploaded_count} document embeddings to vector index")
        print(f"Upload completed in {time.time() - upload_start_time:.2f} seconds")
    else:
        print("No documents found to process")
    
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")