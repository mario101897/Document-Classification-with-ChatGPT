
# Document Management Automation for Law Firms

### **Overview**

This project automates the tedious process of handling client documents for a law firm. It downloads files from Gmail, uses ChatGPT to classify and label them, and organizes them into the appropriate folders in a structured `CLIENTS` directory. The goal is to reduce human effort, minimize errors, and make document organization scalable for high-volume workflows.

The code doesn't just stop at categorization—it also identifies folders in the `CLIENTS` directory that don’t follow a standardized naming convention, flagging them for manual review. This ensures that automation works smoothly and that client folders remain consistent and reliable.

---

### **Purpose**

Managing client documents can be overwhelming, especially when they’re coming in from various sources. The purpose of this project is to automate and streamline:
- **Downloading Documents**: Integrates with Gmail’s API to fetch attachments.
- **Document Classification**: Uses ChatGPT to intelligently analyze and classify each document into types like "Bank Statements," "Paystubs," or "Tax Returns."
- **File Organization**: Places documents into the appropriate subfolders inside each client’s folder, naming them consistently for easy identification.
- **Folder Standardization**: Identifies inconsistencies (like special characters or duplicates) in the `CLIENTS` directory to ensure a clean, scalable structure.

---

### **Challenges and Lessons Learned**

1. **Integrating the Gmail API**:
   - Gmail’s OAuth2.0 authentication flow was straightforward but required extra attention to token handling and refresh logic. Once implemented, the API integration worked seamlessly, allowing us to filter emails and download attachments efficiently.

2. **Text Extraction**:
   - Extracting text from PDFs was challenging due to inconsistent formatting. Some PDFs were poorly encoded, leading to messy results. After experimenting, **PyPDF2** provided satisfactory results for most cases, though it’s far from perfect.
   - Handling Word documents (DOCX files) was easier thanks to the `python-docx` library, which reliably extracts content.

3. **ChatGPT Prompt Tuning**:
   - Creating a clear, concise prompt for ChatGPT was critical for consistent results. The AI had to classify documents and return JSON-formatted outputs for easy parsing, but small tweaks to the prompt caused unexpected changes in the output.
   - Lesson learned: simplicity is key. Overcomplicating the prompt led to inconsistent responses, so we iterated to find a balance between detail and clarity.

4. **Folder Standardization**:
   - The `CLIENTS` directory had several inconsistencies, such as folders with special characters, inconsistent capitalization, or duplicate names. This caused problems with automation, as the program couldn’t reliably match documents to the correct folder.
   - Instead of renaming folders automatically (to avoid accidental data loss), the program flags non-standard names for manual review. This approach ensures safety while still improving directory structure.

5. **Cost Efficiency with GPT-3.5**:
   - Initially, we estimated higher costs using GPT-4, but GPT-3.5 Turbo proved to be a cost-effective alternative. For 1,000 documents with approximately 2,000 words each, the cost was just **$5.30**, compared to over $80 for GPT-4. Balancing cost and accuracy showed that GPT-3.5 was sufficient for this use case.

---

### **How It Works**

1. **Document Download**:
   - Connects to Gmail via its API to fetch client documents as email attachments.
   - Stores these files temporarily in a local directory for processing.

2. **Document Classification**:
   - Extracts text from each document (PDFs or DOCX files) using `PyPDF2` and `python-docx`.
   - Sends the extracted text to ChatGPT with a structured prompt, instructing it to:
     - Classify the document type (e.g., Bank Statement, Paystub, Tax Return).
     - Extract key details like dates, account numbers, or client names.
     - Provide a standardized file name and suggested folder path in JSON format.
   - The structured JSON output ensures the program can process the results reliably.

3. **File Organization**:
   - Matches the document to the correct client folder using:
     - **Email-based mapping**: Matches the sender’s email to a client’s folder (if available).
     - **Name-based extraction**: If the email doesn’t match, the program uses the client’s name (e.g., "John Doe") extracted by ChatGPT and formats it to match the folder structure (`LastName, FirstName`).
   - Places the document in the appropriate subfolder (e.g., "Bank Statements") within the client folder, using the standardized file name provided by ChatGPT.

4. **Folder Standardization**:
   - Scans the `CLIENTS` directory to identify folders with:
     - Special characters or inconsistent capitalization.
     - Duplicate or non-standard names.
   - Flags these folders in a report for manual correction, ensuring the structure remains clean and reliable.

---

### **Key Features**

- **Flexible Classification**: Handles various document types like "Paystubs," "Tax Returns," and "Bank Statements."
- **Hybrid Client Matching**: Combines email-based mapping with name-based extraction for reliable client folder identification.
- **Cost Efficiency with GPT-3.5 Turbo**: Processes thousands of documents for less than $6, making it highly economical.
- **Folder Validation**: Ensures the `CLIENTS` directory remains clean and standardized for accurate automation.

---

### **Future Improvements**

1. **Extend Folder Standardization**:
   - While currently focused on the `CLIENTS` directory, this process can be applied to other directories in the future to create a fully unified and standardized filing system.

2. **Error Handling Enhancements**:
   - Improve handling of edge cases, such as corrupted PDFs or incomplete API responses, to make the system more robust.

3. **Automatic Folder Renaming**:
   - Add an optional feature to automatically rename non-standard folders, with safeguards to avoid overwriting or data loss.

4. **User-Friendly Interface**:
   - Develop a web-based dashboard for team members to upload documents, monitor progress, and review flagged folders more easily.

---

### **Lessons Learned**

- **Test Real Data Early**: Simulated testing was helpful, but real-world data exposed edge cases, especially with poorly formatted PDFs.
- **Iterate on Prompts**: Tuning the ChatGPT prompt took time, but keeping it simple and clear led to the most consistent results.
- **Balance Automation and Manual Review**: Fully automating folder renaming was tempting but risky. Flagging issues for human review strikes a good balance between efficiency and safety.

---

### **Conclusion**

This project automates a time-consuming process, reducing errors and ensuring consistent organization of client documents. By combining Gmail API integration, ChatGPT-powered classification, and folder validation, the program provides a scalable and cost-effective solution for document management. It’s a big step forward for efficiency, and future enhancements will only make it better.

--- 
