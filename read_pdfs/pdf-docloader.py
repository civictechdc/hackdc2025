import os
import fitz  # PyMuPDF
from typing import List, Dict, Optional
import pandas as pd
import logging

# Set up logging for better debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_pdfs(folder_path: str) -> Dict[str, Dict]:
    """
    Load PDFs from a folder and extract text content.
    
    Args:
        folder_path (str): Path to folder containing PDF files
        
    Returns:
        Dict[str, Dict]: Dictionary with PDF data
    """
    logger.info(f"Starting PDF loading from: {folder_path}")
    
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    if not os.path.isdir(folder_path):
        raise ValueError(f"Path is not a directory: {folder_path}")
    
    pdf_data = {}
    
    # Get all PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {folder_path}")
        return pdf_data
    
    logger.info(f"Found {len(pdf_files)} PDF file(s): {pdf_files}")
    
    for pdf_file in pdf_files:
        file_path = os.path.join(folder_path, pdf_file)
        logger.info(f"Processing: {pdf_file}")
        
        try:
            # Check file size first
            file_size = os.path.getsize(file_path)
            logger.info(f"File size: {file_size} bytes")
            
            if file_size == 0:
                logger.warning(f"Skipping empty file: {pdf_file}")
                continue
            
            # Open the PDF document
            doc = fitz.open(file_path)
            logger.info(f"PDF opened successfully, pages: {len(doc)}")
            
            # If no pages, skip this file
            if len(doc) == 0:
                logger.warning(f"Skipping PDF with no pages: {pdf_file}")
                doc.close()
                continue

            # Initialize data structure for this PDF
            pdf_content = {
                'comment_id': pdf_file.split('.')[0],  # Use filename without extension as comment_id
                'pdf_file': pdf_file,
                'content': '',
                'page_count': len(doc)
            }

            # Extract content from each page separately
            pages_data = []
            for page_num in range(len(doc)):
                try:
                    page = doc[page_num]
                    page_text = page.get_text()
                    logger.debug(f"Page {page_num + 1}: {len(page_text)} characters")
                    
                    if not page_text or page_text.strip() == '':
                        logger.debug(f"Page {page_num + 1} is empty, adding empty content")
                        # Still add empty pages to maintain page numbering
                        page_content = ""
                    else:
                        # Clean the text
                        page_content = clean_text(page_text)
                    
                    # Store individual page data
                    page_data = {
                        'comment_id': pdf_file.split('.')[0],
                        'pdf_file': pdf_file,
                        'page_number': page_num + 1,
                        'content': page_content,
                        'content_length': len(page_content)
                    }
                    pages_data.append(page_data)
                    
                except Exception as page_error:
                    logger.error(f"Error processing page {page_num + 1} of {pdf_file}: {page_error}")
                    # Add empty page data to maintain sequence
                    page_data = {
                        'comment_id': pdf_file.split('.')[0],
                        'pdf_file': pdf_file,
                        'page_number': page_num + 1,
                        'content': '',
                        'content_length': 0
                    }
                    pages_data.append(page_data)
                    continue
            
            # Store the pages data
            pdf_content['pages_data'] = pages_data
            pdf_content['total_pages'] = len(pages_data)
            pdf_content['total_content_length'] = sum(page['content_length'] for page in pages_data)
            
            # Store in results dictionary
            pdf_data[pdf_file] = pdf_content
            logger.info(f"Successfully loaded: {pdf_file} ({pdf_content['page_count']} pages, {pdf_content['total_content_length']} total chars)")
            
            # Close the document
            doc.close()
            
        except Exception as e:
            logger.error(f"Error loading {pdf_file}: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            continue
    
    logger.info(f"Successfully loaded {len(pdf_data)} PDFs")
    return pdf_data

def clean_text(text: str) -> str:
    """
    Clean text content for CSV compatibility.
    
    Args:
        text (str): Raw text from PDF
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Replace problematic characters
    cleaned = text
    
    # Handle various bullet point encodings
    cleaned = cleaned.replace('‚Ä¢', '• ')
    cleaned = cleaned.replace('\u2022', '• ')
    cleaned = cleaned.replace('•', '• ')
    
    # Handle line endings consistently - CRITICAL FOR CSV
    cleaned = cleaned.replace('\r\n', ' ')
    cleaned = cleaned.replace('\r', ' ')
    cleaned = cleaned.replace('\n', ' ')
    
    # Remove excessive whitespace
    cleaned = ' '.join(cleaned.split())
    
    # Remove or escape characters that can break CSV
    cleaned = cleaned.replace('"', '""')  # Escape quotes for CSV
    cleaned = cleaned.replace('\x00', '')  # Remove null bytes
    
    # Remove other problematic characters that might cause CSV parsing issues
    cleaned = cleaned.replace('\t', ' ')  # Replace tabs with spaces
    cleaned = cleaned.replace('\f', ' ')  # Replace form feeds
    cleaned = cleaned.replace('\v', ' ')  # Replace vertical tabs
    
    return cleaned

def save_to_csv(df: pd.DataFrame, filename: str = 'pdf_content.csv') -> bool:
    """
    Save DataFrame to CSV with proper error handling.
    
    Args:
        df (pd.DataFrame): DataFrame to save
        filename (str): Output filename
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info(f"Saving DataFrame to {filename}")
        logger.info(f"DataFrame shape: {df.shape}")
        
        # Clean content one more time before saving
        df_clean = df.copy()
        if 'content' in df_clean.columns:
            df_clean['content'] = df_clean['content'].apply(
                lambda x: str(x).replace('\n', ' ').replace('\r', ' ').replace('"', '""') if pd.notna(x) else ""
            )
        
        # Save with proper CSV settings - use QUOTE_NONNUMERIC to ensure text fields are quoted
        df_clean.to_csv(
            filename, 
            index=False, 
            encoding='utf-8',
            quotechar='"',
            quoting=2,  # QUOTE_NONNUMERIC - quotes all non-numeric fields
            escapechar=None,
            lineterminator='\n',
            doublequote=True
        )
        
        # Verify the saved file
        try:
            test_df = pd.read_csv(filename, encoding='utf-8')
            logger.info(f"Verification successful: CSV loaded with shape {test_df.shape}")
            
            # Check if content is properly preserved
            if not test_df.empty and 'content' in test_df.columns:
                original_total_chars = df['content'].apply(lambda x: len(str(x)) if pd.notna(x) else 0).sum()
                loaded_total_chars = test_df['content'].apply(lambda x: len(str(x)) if pd.notna(x) else 0).sum()
                logger.info(f"Content preservation check: Original={original_total_chars}, Loaded={loaded_total_chars}")
                
                if abs(original_total_chars - loaded_total_chars) > 100:  # Allow small differences
                    logger.warning("Significant content loss detected in CSV")
            
            return True
        except Exception as verify_error:
            logger.error(f"CSV verification failed: {verify_error}")
            return False
            
    except Exception as save_error:
        logger.error(f"Error saving CSV: {save_error}")
        
        # Try alternative approach with more aggressive cleaning
        try:
            logger.info("Trying alternative CSV save method with aggressive cleaning...")
            df_clean = df.copy()
            
            # More aggressive content cleaning
            if 'content' in df_clean.columns:
                def super_clean(text):
                    if pd.isna(text):
                        return ""
                    text = str(text)
                    # Remove all line breaks and normalize whitespace
                    text = ' '.join(text.split())
                    # Escape quotes properly
                    text = text.replace('"', '""')
                    # Remove any remaining problematic characters
                    text = ''.join(char for char in text if ord(char) >= 32 or char in [' ', '\t'])
                    return text
                
                df_clean['content'] = df_clean['content'].apply(super_clean)
            
            df_clean.to_csv(
                f"backup_{filename}",
                index=False,
                encoding='utf-8',
                sep=',',
                quotechar='"',
                quoting=1,  # QUOTE_ALL
                doublequote=True,
                lineterminator='\n'
            )
            logger.info(f"Backup CSV saved as backup_{filename}")
            return True
        except Exception as backup_error:
            logger.error(f"Backup CSV save also failed: {backup_error}")
            return False

def debug_dataframe(df: pd.DataFrame) -> None:
    """
    Print detailed debugging information about the DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame to debug
    """
    logger.info("=== DataFrame Debug Info ===")
    logger.info(f"Shape: {df.shape}")
    logger.info(f"Columns: {list(df.columns)}")
    logger.info(f"Data types:\n{df.dtypes}")
    
    if not df.empty:
        logger.info("=== Content Summary ===")
        for idx, row in df.head(10).iterrows():  # Show first 10 rows
            content_len = len(str(row.get('content', ''))) if pd.notna(row.get('content')) else 0
            page_num = row.get('page_number', 'N/A')
            logger.info(f"Row {idx}: {row.get('comment_id', 'Unknown')} - Page {page_num} - {row.get('filename', 'Unknown')} - {content_len} chars")
            
            # Check for problematic characters
            content = str(row.get('content', ''))
            if content:
                problematic_chars = [char for char in content[:100] if ord(char) > 127 or char in ['"', '\n', '\r']]
                if problematic_chars:
                    logger.warning(f"Row {idx} has problematic characters: {set(problematic_chars)}")
        
        # Summary by PDF
        logger.info("=== PDF Summary ===")
        pdf_summary = df.groupby('filename').agg({
            'page_number': 'count',
            'content_length': 'sum',
            'total_pages': 'first'
        }).rename(columns={'page_number': 'rows_count'})
        
        for filename, stats in pdf_summary.iterrows():
            logger.info(f"{filename}: {stats['rows_count']} rows, {stats['total_pages']} total pages, {stats['content_length']} total chars")
    
    # Memory usage
    memory_usage = df.memory_usage(deep=True).sum()
    logger.info(f"Memory usage: {memory_usage / 1024 / 1024:.2f} MB")

# Example usage with enhanced debugging:
if __name__ == "__main__":
    # Update this path to your actual folder
    folder_path = "/binary-DEA-2024-0059/comments_attachments/"
    
    try:
        # Check folder first
        if not os.path.exists(folder_path):
            logger.error(f"Folder does not exist: {folder_path}")
            exit(1)
        
        logger.info(f"Folder exists, checking contents...")
        all_files = os.listdir(folder_path)
        pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
        logger.info(f"Total files in folder: {len(all_files)}")
        logger.info(f"PDF files found: {len(pdf_files)}")
        
        if pdf_files:
            logger.info(f"PDF files: {pdf_files[:5]}...")  # Show first 5
        
        # Load PDFs with text extraction
        pdfs = load_pdfs(folder_path)
        
        if not pdfs:
            logger.error("No PDFs were successfully loaded.")
            exit(1)
        
        logger.info(f"Successfully loaded {len(pdfs)} PDF(s)")
        
        # Prepare data for DataFrame - each page is a separate row
        rows = []
        
        for filename, pdf_info in pdfs.items():
            pages_data = pdf_info.get('pages_data', [])
            
            for page_data in pages_data:
                row = {
                    'filename': filename,
                    'comment_id': page_data.get('comment_id', ''),
                    'page_number': page_data.get('page_number', 1),
                    'content': page_data.get('content', ''),
                    'content_length': page_data.get('content_length', 0),
                    'total_pages': pdf_info.get('page_count', 0)
                }
                rows.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(rows)
        
        # Sort by comment_id and then by page_number
        df = df.sort_values(['comment_id', 'page_number'], ascending=True).reset_index(drop=True)
        
        df = df.dropna(subset=['content'])
        df = df[df['content'].str.strip() != '']
        df.reset_index(drop=True, inplace=True)  
        
        # Debug the DataFrame
        debug_dataframe(df)
        
        # Save to CSV
        success = save_to_csv(df, 'pdf_content.csv')
        
        if success:
            logger.info("Process completed successfully!")
        else:
            logger.error("Process completed with errors. Check backup files.")
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")