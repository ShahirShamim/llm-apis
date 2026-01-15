import os
import requests
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

# Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
API_KEY = os.getenv("API_KEY", "default-insecure-key")
MODEL_NAME = "gemma3:27b"

@app.get("/generate")
def generate_text(apikey: str, prompt: str):
    """
    Simple GET endpoint to generate text from a prompt.
    """
    if apikey != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        # Construct the request to Ollama
        # Note: gemma3:27b might need specific parameters, but we start simple.
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload)
        response.raise_for_status()
        
        data = response.json()
        return {"response": data.get("response", "")}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {str(e)}")

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}
