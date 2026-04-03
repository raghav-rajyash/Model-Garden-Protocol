🚀 AI Toolkit (Model Garden)

A modular AI platform built with FastAPI + custom Model Garden architecture, enabling seamless integration of multiple AI models (Groq, OpenAI, Qwen, etc.) with a clean and interactive frontend.

🔥 Features

  🧠 Model Garden Architecture
      Plug-and-play system to register and use multiple AI models
      Easily extendable with new connectors (Groq, OpenAI, Qwen)
      
  ⚡FastAPI Backend
      RESTful API with structured routing
      Scalable and production-ready architecture
      Clean separation of controller, services, and models
      
  💬ChatGPT-style Frontend UI
      Interactive chat interface
      Smooth user experience with chat bubbles
      Markdown-supported responses (bold, lists, formatting)
      
  🔗Unified API Endpoint
      Single endpoint for all model interactions:
      POST /api/v1/model/generate
      
  ⚙️Configurable Model Parameters
      Temperature
      Max tokens
      Top-p sampling
      Seed control
      
  🌐CORS Enabled
      Works seamlessly with local frontend and external clients

🏗️ Project Structure
      model garden/
      │
      ├── app/
      │   ├── controller/        # API routes
      │   ├── services/          # Model connectors & registry
      │   ├── db/                # Database setup
      │   ├── main.py            # FastAPI app entry point
      │
      ├── frontend/              # Chat UI (HTML + JS)
      │
      ├── .env                   # API keys
      ├── requirements.txt


⚡ How It Works
      User sends a prompt from the frontend
      Request hits FastAPI endpoint
      Model Garden selects the appropriate model
      Connector sends request to AI provider (Groq/OpenAI)
      Response is returned and rendered in the UI


📡 API Example
      POST /api/v1/model/generate
      {
        "model": "llama-3.3-70b-versatile",
        "prompt": "Explain AI in simple terms",
        "config": {
          "temperature": 0.7,
          "top_p": 1,
          "max_tokens": 200
        }
      }
