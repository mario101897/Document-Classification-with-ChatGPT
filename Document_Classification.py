import os
import shutil
import openai
import json
from PyPDF2 import PdfReader
from docx import Document

# Define constants for file paths
CLIENTS_DIR = 'CLIENTS'            # Main directory containing client folders
INPUT_FOLDER = 'input_files'       # Folder with pre-downloaded files
OUTPUT_FOLDER = 'organized_files'  # Folder where renamed files will be saved temporarily
API_KEY = 'your_openai_api_key'    # Replace with your actual OpenAI API key

# Set OpenAI API key
openai.api_key = API_KEY

# Email-to-client mapping (example)
EMAIL_TO_CLIENT = {
    'client1@example.com': 'Cardozo, Mario',
    'client2@example.com': 'Doe, John',
    # Add more email-to-client mappings here
}

# Function to extract text from PDF files
def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {e}")
        return None

# Function to extract text from DOCX files
def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX {file_path}: {e}")
        return None

# Function to classify the document and get structured JSON response from ChatGPT
def classify_document_with_chatgpt(text):
    prompt = f"""
    You are a document processing assistant. I will provide you with the text of a document, which may fall into one of the following categories: Bank Statements, Paystubs, Tax Returns, IDs, Card Docs, Home Docs, or Legal/Lawsuits and Creditors. Based on the content, please classify the document type, extract the client's first and last name if available, and generate a standardized file name and folder path.

    1. **Classify the Document** and extract specific information:
       - Bank Statements: Label as "BankName Last4Digits From StartDate to EndDate.pdf".
       - Paystubs: Label as "Paystub from StartDate to EndDate.pdf".
       - Tax Returns: Label 1040 Form as "TaxReturn 1040 YYYY" or IRS Transcript as "TaxReturn IRS Transcript YYYY".
       - IDs: Label as "ID SSN" or "ID Card".
       - Card Docs: Label as "CardDocs BankName Statement" or "CardDocs BankName Agreement".
       - Home Docs: Label as "HomeDocs Payment Agreement", "HomeDocs Car Registration", etc.
       - Lawsuits and Creditors: Label as "Legal Lawsuit [CaseName]" or "Legal Creditor [CreditorName]".

    2. **Extract Client Name** if it appears in the document:
       - Provide the "First Name" and "Last Name" separately.

    3. **Response Format**:
       - Respond in JSON format:
         {{
           "Document Type": "string (e.g., 'Bank Statement', 'Paystub', 'Tax Return', etc.)",
           "Suggested File Name": "string",
           "Folder Path": "string (e.g., 'Bank Statements', 'Paystubs', etc.)",
           "Client First Name": "string or null if no first name found",
           "Client Last Name": "string or null if no last name found"
         }}

    Here is the document content:
    {text}
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error with ChatGPT API: {e}")
        return None

# Function to locate the client's folder based on email or extracted name
def get_client_folder(email_address, first_name=None, last_name=None):
    # Step 1: Try email-based identification
    client_folder_name = EMAIL_TO_CLIENT.get(email_address)
    if client_folder_name:
        client_folder_path = os.path.join(CLIENTS_DIR, client_folder_name)
        if os.path.exists(client_folder_path):
            return client_folder_path

    # Step 2: Fallback to name-based identification
    if first_name and last_name:
        formatted_name = f"{last_name}, {first_name}"  # Format as LastName, FirstName
        potential_folder = os.path.join(CLIENTS_DIR, formatted_name)
        if os.path.exists(potential_folder):
            return potential_folder

    # Step 3: Final fallback
    return os.path.join(CLIENTS_DIR, "Uncategorized")


# Function to rename and relocate files based on ChatGPT's JSON response
def process_and_move_file(file_path, classification_data, client_folder_path):
    try:
        # Parse the response as JSON
        data = json.loads(classification_data)

        # Extract classification details
        doc_type = data.get("Document Type", "Uncategorized")
        suggested_name = data.get("Suggested File Name", os.path.basename(file_path))
        folder_path = data.get("Folder Path", "Main Folder")

        # Set up destination directory within the client’s folder
        destination_dir = os.path.join(client_folder_path, folder_path)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Set the destination path with suggested file name
        destination_path = os.path.join(destination_dir, suggested_name)

        # Move and rename the file
        shutil.move(file_path, destination_path)
        print(f"File {file_path} moved to {destination_path}")

    except json.JSONDecodeError:
        print(f"Failed to parse ChatGPT response as JSON for file {file_path}. Response: {classification_data}")
    except Exception as e:
        print(f"Error processing and moving file {file_path}: {e}")

# Main function to process all files in the input folderdef main():
def main():
    # Process each file in the input directory
    for file_name in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, file_name)

        # Extract text based on file type
        if file_name.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_name.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            print(f"Unsupported file type: {file_name}")
            continue

        # Ensure text extraction was successful
        if not text:
            print(f"Skipping file due to extraction error: {file_name}")
            continue

        # Simulate fetching email address associated with file (for testing)
        email_address = "client1@example.com"  # Replace with actual email extraction logic

        # Classify the document and get renaming/relocation data from ChatGPT
        classification_data = classify_document_with_chatgpt(text)
        if classification_data:
            # Retrieve extracted client name from ChatGPT's response
            data = json.loads(classification_data)
            first_name = data.get("Client First Name")
            last_name = data.get("Client Last Name")

            # Identify client's folder
            client_folder_path = get_client_folder(email_address, first_name, last_name)
            process_and_move_file(file_path, classification_data, client_folder_path)
        else:
            print(f"Skipping file due to classification error: {file_name}")


# Run the main function
if __name__ == "__main__":
    main()
