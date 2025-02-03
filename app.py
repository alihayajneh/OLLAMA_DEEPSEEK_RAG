import os
import uuid
import markdown2
from flask import Flask, request, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
VECTOR_DB_PATH = "vector_db"
ALLOWED_EXTENSIONS = {'pdf'}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["VECTOR_DB_PATH"] = VECTOR_DB_PATH

# Ensure upload & vector DB folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VECTOR_DB_PATH, exist_ok=True)

# ----------------- Utility Functions -----------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_pdf(file_path, user_session):
    """Extracts text from a PDF and stores embeddings."""
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)

    # Generate embeddings using Granite
    embedding_model = OllamaEmbeddings(model="granite-embedding:278m")

    # Store embeddings in FAISS
    vector_store = FAISS.from_documents(chunks, embedding_model)
    vector_store_path = os.path.join(VECTOR_DB_PATH, f"{user_session}.faiss")
    vector_store.save_local(vector_store_path)

    return vector_store_path

def load_retriever(user_session):
    """Loads FAISS retriever for the current session."""
    embedding_model = OllamaEmbeddings(model="granite-embedding:278m")
    vector_store_path = os.path.join(VECTOR_DB_PATH, f"{user_session}.faiss")

    if os.path.exists(vector_store_path):
        return FAISS.load_local(vector_store_path, embedding_model, allow_dangerous_deserialization=True)
    return None

# ----------------- Routes -----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return render_template("index.html", error="No file uploaded.")

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return render_template("index.html", error="Invalid file type.")

    # Generate a unique session ID
    user_session = str(uuid.uuid4())

    # Save file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{user_session}_{filename}")
    file.save(file_path)

    # Process PDF
    process_pdf(file_path, user_session)

    return render_template("chat.html", session_id=user_session)

@app.route("/ask", methods=["POST"])
@app.route("/ask", methods=["POST"])
def ask_question():
    query = request.form.get("query")
    user_session = request.form.get("session_id")

    if not query or not user_session:
        return render_template("chat.html", session_id=user_session, error="Invalid input.")

    retriever = load_retriever(user_session)
    if not retriever:
        return render_template("chat.html", session_id=user_session, error="Session not found.")

    # Load DeepSeek-R1 for answering
    llm = OllamaLLM(model="deepseek-r1:7b")
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever.as_retriever())

    # Get the response from LangChain
    response = qa_chain.invoke(query)

    # Extract the text result safely
    answer_text = response["result"] if isinstance(response, dict) else response

    # Convert to Markdown format
    answer_markdown = markdown2.markdown(answer_text)

    return render_template("chat.html", session_id=user_session, query=query, answer=answer_markdown)


if __name__ == "__main__":
    app.run(debug=True)
