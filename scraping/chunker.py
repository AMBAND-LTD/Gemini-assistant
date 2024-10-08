import os
import json
import hashlib
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Initialize the tokenizer
tokenizer = tiktoken.get_encoding('cl100k_base')

def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)

def process_jsonl_file(file_path):
    # Initialize text_splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=20,
        length_function=tiktoken_len,
        separators=['\n\n', '\n', ' ', '']
    )

    documents = []

    try:
        # Load the JSONL content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                content = json.loads(line.strip())['text']  # Assuming 'text' is the key in your JSON object

                # Generate a unique ID based on the file path
                m = hashlib.md5()
                m.update(file_path.encode('utf-8'))
                uid = m.hexdigest()[:12]

                # Split the content into chunks
                chunks = text_splitter.split_text(content)

                # Create document data
                for i, chunk in enumerate(chunks):
                    documents.append({
                        'id': f'{uid}-{i}',
                        'text': chunk,
                        'source': file_path
                    })

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

    # Save the documents to a JSON Lines file
    output_file_path = os.path.join(os.path.dirname(file_path), 'vectorizor.jsonl')
    with open(output_file_path, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc) + '\n')  # Write each document as a separate JSON object

    return documents

# Define the path to the token.jsonl file in the data folder
input_file_path = os.path.join("data", "token.jsonl")

# Process the token.jsonl file
documents = process_jsonl_file(input_file_path)
