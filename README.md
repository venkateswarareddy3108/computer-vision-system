# Computer Vision Analytics System

A real-time computer vision system built with FastAPI (Python) on the backend and React (TypeScript) on the frontend. The system performs face detection, registration, recognition, eye status analysis (drowsiness detection), expression estimation, and hand/finger tracking.

## Architecture

*   **Backend**: FastAPI, OpenCV, InsightFace, YOLOv8, MediaPipe, SQLAlchemy, pgvector (PostgreSQL).
*   **Frontend**: React 18, TypeScript, Vite, Tailwind CSS (Custom Design System).
*   **Infrastructure**: Docker, Docker Compose.

## Key Features

*   **Real-time Processing**: Fast concurrent pipeline using ThreadPoolExecutor for heavy ML models.
*   **Face Recognition**: ArcFace model for robust face embeddings with pgvector for high-speed similarity search.
*   **Drowsiness Detection**: Facial landmark tracking to calculate Eye Aspect Ratio (EAR).
*   **Expression Estimation**: Real-time emotion/expression classification.
*   **Hand Tracking**: Counting visible fingers per hand.
*   **Web Dashboard**: React-based frontend receiving live camera feeds and annotations via WebSockets.

## Requirements

*   Docker and Docker Compose
*   Webcam attached to the host machine (mapped to `/dev/video0` or local camera index 0)
*   CUDA-compatible GPU (optional but recommended for high FPS)

## Running the System

1.  Start the services using Docker Compose:
    ```bash
    docker-compose up --build
    ```
2.  Open the web dashboard in your browser:
    ```
    http://localhost:5173
    ```
    *(Assuming Vite runs on 5173 or the Nginx container port)*

## Manual Setup (Development)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Structure

*   `/backend`: Python FastAPI application and vision models.
*   `/frontend`: React SPA dashboard.
*   `/database`: PostgreSQL initialization scripts.
