# AI Containers with Ollama, FastAPI Gateway, and Open WebUI

This project provides a Docker Compose setup for running AI services including Ollama for model serving, a FastAPI gateway for API access, and Open WebUI for a web interface.

## Overview

The system consists of three main containers:

- **Ollama**: Serves AI models (currently configured for llama3:8b)
- **FastAPI Gateway**: Provides REST API endpoints to interact with Ollama
- **Open WebUI**: Web-based interface for chatting with AI models

## Prerequisites

- Docker installed on your system
- Docker Compose installed
- Sufficient disk space for AI models (several GBs)

## Installation and Setup

1. Clone or download this project to your local machine
2. Ensure Docker is running on your system
3. Open a terminal in the project directory

## Running the Containers

Start all services with Docker Compose:

```bash
docker-compose up -d
```

This will:
- Pull the required Docker images
- Build the FastAPI gateway
- Start all three services in detached mode

To view logs:

```bash
docker-compose logs -f
```

To stop the services:

```bash
docker-compose down
```

## Services and Ports

| Service | Container Name | Host Port | Description |
|---------|----------------|-----------|-------------|
| Ollama | ollama | 11434 | AI model server |
| FastAPI Gateway | fastapi-gateway | 8000 | REST API gateway |
| Open WebUI | open-webui | 3000 | Web interface |

## Usage

### 1. Open WebUI (Web Interface)
Access the web interface at: http://localhost:3000

The Open WebUI provides a chat interface where you can interact with the AI models served by Ollama.

### 2. FastAPI Gateway (REST API)
The FastAPI gateway provides the following endpoints:

- **GET /** - Root endpoint with status information
  ```bash
  curl http://localhost:8000/
  ```

- **GET /status** - Check Ollama connection status
  ```bash
  curl http://localhost:8000/status
  ```

- **POST /generate** - Generate text using the AI model
  ```bash
  curl -X POST "http://localhost:8000/generate?prompt=Hello, how are you?"
  ```

### 3. Direct Ollama Access
You can also access Ollama directly on port 11434:

```bash
curl http://localhost:11434/api/tags
```

## Configuration

### Environment Variables

- `OLLAMA_URL`: URL for Ollama service (default: http://ollama:11434)
- `OLLAMA_KEEP_ALIVE`: Keep alive timeout for Ollama (set to 24h)

### Volume Mounts

- `./ollama_data`: Persistent storage for Ollama models and data
- `./openwebui_config`: Configuration directory for Open WebUI

## Model Configuration

The system is currently configured to use the `llama3:8b` model. To change the model:

1. Edit the `docker-compose.yml` file
2. Modify the model name in the Ollama service command:
   ```yaml
   command: >
     "ollama serve &
      sleep 5 &&
      ollama pull YOUR_MODEL_NAME &&
      tail -f /dev/null"
   ```
3. Update the `MODEL_NAME` in `fastapi/main.py` if using the FastAPI gateway

## Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 11434, 8000, and 3000 are available
2. **Model download issues**: Check internet connection and disk space
3. **Service dependencies**: Ollama must start before other services

### Checking Service Status

```bash
docker-compose ps
```

### Viewing Logs

```bash
docker-compose logs ollama
docker-compose logs fastapi-gateway
docker-compose logs open-webui
```

### Restarting Services

```bash
docker-compose restart
```

## File Structure

```
.
├── docker-compose.yml          # Main Docker Compose configuration
├── fastapi/
│   ├── Dockerfile             # FastAPI container build instructions
│   ├── main.py               # FastAPI application code
│   └── requirements.txt      # Python dependencies
├── ollama_data/              # Persistent data for Ollama (created automatically)
└── openwebui_config/         # Configuration for Open WebUI (created automatically)
```

## Customization

### Adding New Models

To add additional models to Ollama:

```bash
docker exec -it ollama ollama pull MODEL_NAME
```

### Modifying FastAPI Gateway

Edit the `fastapi/main.py` file to add new endpoints or modify existing functionality.

### Open WebUI Configuration

Configuration files for Open WebUI are stored in the `openwebui_config/` directory.

## Support

For issues related to:
- Ollama: https://github.com/ollama/ollama
- Open WebUI: https://github.com/open-webui/open-webui
- FastAPI: https://fastapi.tiangolo.com