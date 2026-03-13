# Digital Inheritor Backend

This is the backend service for the "Digital Inheritor" project.

## Tech Stack
- **Framework**: FastAPI
- **Database**: Neo4j (Knowledge Graph)
- **AI**: LangChain, MediaPipe, Stable Diffusion

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuration**:
    - Environment variables are loaded from `.env` file or system environment.
    - See `app/core/config.py` for available settings.
    - Set `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` for Neo4j connection.

3.  **Run the Server**:
    ```bash
    python run.py
    ```
    The API will be available at `http://localhost:8000`.
    API Documentation (Swagger UI): `http://localhost:8000/docs`

## API Endpoints

- **Vision Mentor**: `/api/v1/vision/*` - For pose analysis and feedback.
- **Knowledge Curator**: `/api/v1/knowledge/*` - For RAG-based QA and graph queries.
- **Creative Artisan**: `/api/v1/creative/*` - For image generation and style transfer.
