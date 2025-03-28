import os
import secrets
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import google.generativeai as genai
from file_parsing import parse_pdf, parse_docx, parse_xlsx, parse_pptx
from auth import authenticate, login, logout
from text_splitter import split_text
from vector_store import add_texts_to_vector_store, search_query_in_vector_store, vector_store
from chroma_delete import delete_file_from_vector_store 

# Configure Gemini API Key
genai.configure(api_key="AIzaSyAzHxmg7rQDfZAQxBH2IC21")

# Set up Flask application
supersecretkey = secrets.token_hex(32)
app = Flask(__name__)
app.secret_key = supersecretkey
CORS(app, supports_credentials=True, origins="http://localhost:3000")

UPLOAD_FOLDER = 'D:/project/document_search_bot/L2_POC_RAG/uploaded_documents'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'pptx'}

# Function to check if a file is allowed based on extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Login API
@app.route('/login', methods=['POST'])
def login_api():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    result = login(username, password)
    if "error" in result:
        return jsonify(result), 401
    return jsonify(result), 200


# Logout API
@app.route('/logout', methods=['POST'])
def logout_api():
    result = logout()
    return jsonify(result), 200


# File Upload API with Chroma Integration
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text content based on file type
        file_extension = filename.rsplit('.', 1)[1].lower()
        if file_extension == 'pdf':
            file_content = parse_pdf(file_path)
        elif file_extension == 'docx':
            file_content = parse_docx(file_path)
        elif file_extension == 'xlsx':
            file_content = parse_xlsx(file_path)
        elif file_extension == 'pptx':
            file_content = parse_pptx(file_path)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        # Split text and store in Chroma
        text_chunks = split_text(file_content)  # Make sure `split_text` is defined
        metadatas = [{"filename": filename}] * len(text_chunks)
        add_texts_to_vector_store(text_chunks, metadatas)
        return jsonify({'message': 'File uploaded and indexed successfully', 'filename': filename}), 200

    return jsonify({'error': 'Invalid file type'}), 400


# List Documents
@app.route('/list_documents', methods=['GET'])
def list_documents():
    role = authenticate()
    if not role:
        return jsonify({'error': 'Unauthorized access'}), 403

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'documents': files}), 200


# File Deletion (Admin Only)
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    role = authenticate()
    if role != "admin":
        return jsonify({'error': 'Unauthorized access'}), 403

    # Delete file from local storage
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"[INFO] File {filename} deleted from local storage.")
    else:
        print(f"[WARNING] File {filename} not found on disk.")
        return jsonify({'error': 'File not found'}), 404

    # Delete file from Chroma vector store using the new function from chroma_delete
    try:
        delete_file_from_vector_store(vector_store, filename)
        return jsonify({'message': 'File and embeddings deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to delete embeddings from Chroma: {str(e)}'}), 500


@app.route('/query', methods=['POST'])
def process_query():
    data = request.json
    user_query = data.get('query')

    if not user_query:
        return jsonify({'error': 'Query is required'}), 400

    #
    results = search_query_in_vector_store(user_query, k=1)

    if not results:
        return jsonify({'response': 'No relevant document found'}), 200

    
    matched_doc = results[0]

    document_name = matched_doc.metadata.get("filename", "Unknown filename")
    document_content = matched_doc.page_content

    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Document: {document_name}\nContent: {document_content}\nUser Query: {user_query}")

    return jsonify({'document_name': document_name, 'response': response.text}), 200

if __name__ == '__main__':
    app.run(debug=False)
