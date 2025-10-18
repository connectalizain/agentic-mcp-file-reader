# 🧠 Agentic MCP File Reader

A beginner-friendly **AI File Assistant** powered by **Chainlit**, **Model Context Protocol (MCP)**, and **Gemini API via the OpenAI Agents SDK**.  
This project demonstrates how an AI agent can **read, search, and write local files** using natural language — either via a **chat interface** or **CLI**.

---

## 🚀 Features

- 🤖 **Chat-based File Assistant** (via Chainlit)
- 🧩 **MCP Server** providing tools to read, search, and write files
- 🔗 **Gemini API integration** through OpenAI Agents SDK
- ⚙️ **Streaming responses** with real-time token output
- 💻 **Command-Line Interface (CLI)** version available

---

## 🧱 Project Structure

```
agentic-mcp-file-reader/
│
├── app.py           # Chainlit UI app - Chat interface for File Assistant
├── server.py        # MCP server exposing file read/search/write tools
├── fileagent.py     # CLI-only version of File Assistant
├── .env             # Contains GEMINI_API_KEY and MCP_SERVER_URL
└── requirements.txt # (Recommended) Dependencies list
```

---

## 📦 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/connectalizain/agentic-mcp-file-reader.git
cd agentic-mcp-file-reader
```

### 2️⃣ Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate    # On macOS/Linux
venv\Scripts\activate       # On Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

*(If you don’t have `requirements.txt`, install manually:)*  
```bash
pip install chainlit python-dotenv uvicorn fastapi openai-agents-sdk
```

### 4️⃣ Add Environment Variables

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_gemini_api_key_here
MCP_SERVER_URL=http://localhost:9000/mcp/
```

---

## ⚙️ Run the Project

### 🧩 Step 1 — Start MCP Server

```bash
python server.py
```

This will start the **MCP FastAPI server** exposing these tools:
- `read_file(path)`
- `search_file(path, keyword)`
- `write_file(path, content, mode)`

Default port: **9000**

---

### 💬 Step 2 — Run the Chainlit App

```bash
chainlit run app.py -w
```

Then open the provided **localhost URL** in your browser.

You can chat naturally with your assistant:
> 🗣 “Search the word *future* in `test.txt` and summarize it.”  
> 🗣 “Summarize `report.txt` in 50 words.”  
> 🗣 “Write ‘AI is amazing!’ to `note.txt`.”

---

### 🧑‍💻 Step 3 — Use CLI File Agent (Optional)

For a terminal-only version:

```bash
python fileagent.py "Summarize test.txt in 50 words"
```

or run it interactively:

```bash
python fileagent.py
Enter query: Search 'progress' in test.txt
```

---

## 🧠 How It Works

### 🔹 `server.py`
Implements an **MCP server** using `FastMCP`.  
Exposes tools to:
- Read a file (`read_file`)
- Search for a keyword (`search_file`)
- Write to a file (`write_file`)

### 🔹 `app.py`
Launches a **Chainlit web interface** where:
- Gemini model (`gemini-2.5-flash`) is connected through OpenAI Agents SDK.
- The agent connects to the local MCP server to access file tools.
- User inputs are streamed with live token updates.
- Tools usage is displayed in chat (e.g., “🔧 Tool called: read_file”).

### 🔹 `fileagent.py`
A **CLI version** of the File Assistant that:
- Connects to the same MCP server.
- Streams output to the terminal.
- Handles queries without UI.

---

## 🧩 Example Flow

1. You ask:  
   > “Search for the word *innovation* in `notes.txt` and summarize.”

2. The agent:
   - Calls `search_file`
   - Reads the matching lines
   - Calls `read_file` for context
   - Summarizes the full content using Gemini

3. You see real-time streaming output in Chainlit or CLI.

---

## 🧰 Tech Stack

| Component | Description |
|------------|-------------|
| **Chainlit** | UI for chat-based LLM apps |
| **OpenAI Agents SDK** | Framework to run and manage AI agents |
| **Gemini 2.5 Flash** | Google’s LLM used as the reasoning engine |
| **MCP (Model Context Protocol)** | Enables external tool access like reading/writing files |
| **FastMCP** | Python framework to implement MCP servers easily |
| **Uvicorn + FastAPI** | For running the MCP server backend |

---

## 🔒 Environment Variables

| Variable | Description |
|-----------|--------------|
| `GEMINI_API_KEY` | Your Gemini API key from Google AI Studio |
| `MCP_SERVER_URL` | MCP server URL (default: http://localhost:9000/mcp/) |

---

## 🧩 Future Improvements

- Add multi-file context memory
- Support for file upload and preview in Chainlit UI
- Add authentication and logging
- Docker support for deployment

---

## 📜 License

MIT License © 2025 [connectalizain](https://github.com/connectalizain)

---

## 🌟 Acknowledgments

Thanks to:
- [Chainlit](https://www.chainlit.io/)
- [OpenAI Agents SDK](https://github.com/openai/agents)
- [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol)
- [Google Gemini API](https://ai.google.dev/)
