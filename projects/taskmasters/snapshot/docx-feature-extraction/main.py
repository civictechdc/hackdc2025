import docx
import csv
import os

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = []
    for para in doc.paragraphs:
        if para.text.strip():
            text.append(para.text.strip())
    return "\n".join(text)

def process_folder(input_folder, output_csv):
    docx_files = []
    # Recursively find all .docx files
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.docx'):
                docx_files.append(os.path.join(root, file))

    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['comment_id', 'comment_text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for docx_file in docx_files:
            comment_id = os.path.splitext(os.path.basename(docx_file))[0]
            try:
                text = extract_text_from_docx(docx_file)
                writer.writerow({'comment_id': comment_id, 'comment_text': text})
                print(f"Processed: {docx_file}")
            except Exception as e:
                print(f"Error processing {docx_file}: {e}")

if __name__ == "__main__":
    input_folder = 'mydata/DEA-2024-0059/raw-data/'
    output_csv = 'all_extracted_comments.csv'
    process_folder(input_folder, output_csv)
    print(f"All comments extracted to {output_csv}")
