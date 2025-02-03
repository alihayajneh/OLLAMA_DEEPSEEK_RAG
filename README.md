# 📚 AI PDF Chatbot with RAG (Retrieval-Augmented Generation)

This is a **Flask-based AI chatbot** that allows users to **upload a PDF document and ask questions about its content**. The system processes the PDF using **Granite Embeddings**, stores embeddings using **FAISS**, and generates responses using **DeepSeek-R1:7B**.

## 🚀 Features

- ✅ **Upload and Process PDFs**
- ✅ **Chatbot Interface with Markdown-Formatted Responses**
- ✅ **Granite Embedding for Vector Search**
- ✅ **DeepSeek-R1:7B for Answer Generation**
- ✅ **Beautiful UI with Bootstrap**
- ✅ **Session-Based Retrieval for Multiple Questions**

---

## 📂 Project Structure

```
📂 AI_PDF_Chatbot
│── 📁 templates
│   ├── index.html  # File Upload Page
│   ├── chat.html   # Chat Interface
│
│── 📁 uploads      # Stores Uploaded PDFs (Auto genrated)
│── 📁 vector_db    # Stores FAISS Index for each session (Auto genrated)
│── app.py          # Main Flask Server
│── requirements.txt # List of Dependencies (This is my entire pip freeze results, some of them are not needed)
│── README.md       # Documentation
```

---

## 🔧 Installation

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/alihayajneh/OLLAMA_DEEPSEEK_RAG.git
cd AI_PDF_Chatbot
```

### **2️⃣ Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

## 🏗️ Install Ollama Models

Since this chatbot uses **Granite Embedding** for text processing and **DeepSeek-R1:7B** for response generation, you need to install these models using **Ollama**.

### **1️⃣ Install Ollama**
First, install Ollama on your system by following the instructions [here](https://ollama.com).

### **2️⃣ Pull the Required Models**
Run the following commands to download the required models:

```bash
# Install Granite Embedding Model (278M)
ollama pull granite-embedding:278m

# Install DeepSeek-R1:7B Model
ollama pull deepseek-r1:7b
```

Once installed, you can run the chatbot without issues.
---

## 🎯 Usage

### **1️⃣ Start the Flask Server**
```bash
python app.py
```
**📌 Access the web interface at:**  
🔗 [http://127.0.0.1:5000](http://127.0.0.1:5000)

### **2️⃣ Upload a PDF**
- Click **"Choose File"** and select a PDF.
- Click **"Upload PDF"** to start processing.

### **3️⃣ Chat with the PDF**
- After processing, you can enter questions in the chatbot.
- The bot will return **context-aware answers** extracted from the PDF.

---

## 🛠️ API Endpoints

| Method | Endpoint      | Description |
|--------|--------------|-------------|
| `GET`  | `/`          | Renders the upload page |
| `POST` | `/upload`    | Uploads a PDF and processes it |
| `POST` | `/ask`       | Accepts user queries and returns AI-generated answers |

---


## 📜 License
This project is licensed under the **MIT License**. Feel free to modify and distribute.

---



## 🌟 Acknowledgments
- **LangChain** for RAG Pipeline
- **FAISS** for Vector Search
- **DeepSeek-R1:7B** for AI-generated responses
- **Flask** for the backend framework
- **Bootstrap** for frontend UI

🔹 **Made with ❤️ for AI-powered knowledge retrieval by Dr Ali Hayajneh** 🚀 

