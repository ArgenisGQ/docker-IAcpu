from fastapi import FastAPI, Query
import requests
import os

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
MODEL_NAME = "llama2:8b"   # Modelo fijo

def check_ollama_status():
    """Verifica si Ollama está respondiendo en su endpoint."""
    try:
        r = requests.get(OLLAMA_URL, timeout=5)
        if r.status_code == 200:
            return {"status": "online", "details": "Ollama responde correctamente"}
        else:
            return {"status": "error", "details": f"Respuesta inesperada: {r.status_code}"}
    except Exception as e:
        return {"status": "offline", "details": str(e)}

@app.get("/")
def root():
    """Estado general del Gateway + Ollama."""
    return {
        "message": "Gateway a Ollama",
        "modelo": MODEL_NAME,
        "ollama_status": check_ollama_status()
    }

@app.get("/status")
def status():
    """Endpoint separado solo para chequear Ollama."""
    return {
        "ollama_status": check_ollama_status()
    }

@app.post("/generate")
def generate(prompt: str = Query(..., description="Texto de entrada para la IA")):
    url = f"{OLLAMA_URL}/api/generate"
    payload = {"model": MODEL_NAME, "prompt": prompt}

    try:
        r = requests.post(url, json=payload, timeout=120)
        return r.json()
    except Exception as e:
        return {"error": f"Error al comunicarse con Ollama: {str(e)}"}
