# Deployment Guide: Algorithm Performance Analyzer

This guide provides instructions on how to deploy the Algorithm Performance Analyzer to various environments.

## 🐳 Option 1: Docker (Recommended)

Docker is the easiest way to deploy the full stack as it ensures consistency between environments.

### Prerequisites
- Docker and Docker Compose installed on your server.

### Steps
1. **Clone the repository** (if not already on the server).
2. **Configure Backend URL**:
   In `docker-compose.yml`, the frontend is configured to talk to `http://localhost:8000`. If you are deploying to a domain (e.g., `api.example.com`), update the `VITE_API_URL` arg in the frontend service:
   ```yaml
   args:
     - VITE_API_URL=https://api.yourdomain.com
   ```
3. **Run the application**:
   ```bash
   docker-compose up -d --build
   ```
4. **Access the app**:
   - Frontend: `http://your-server-ip:5173`
   - Backend API: `http://your-server-ip:8000`

---

## 🚀 Option 2: Cloud Platforms (PaaS)

### Backend (FastAPI)
You can deploy the backend to platforms like **Render**, **Railway**, or **Google Cloud Run**.

1. **Render/Railway**:
   - Point to the root directory.
   - Run Command: `python backend/main.py` (or `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`)
   - Environment Variables: Ensure any necessary DB paths are set.

### Frontend (React/Vite)
Deploy the frontend to **Vercel**, **Netlify**, or **GitHub Pages**.

1. **Build the project locally**:
   ```bash
   cd frontend
   npm run build
   ```
2. **Deploy the `dist` folder** to your preferred host.
3. **Environment Variables**:
   Set `VITE_API_URL` to your deployed backend URL in the platform's dashboard.

---

## 🛠 Option 3: Manual Deployment (VPS/Nginx)

### 1. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn/Uvicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 2. Frontend Build
```bash
cd frontend
VITE_API_URL=https://api.yourdomain.com npm run build
```

### 3. Nginx Configuration
Configure Nginx to serve the `dist` folder and proxy API requests.

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        root /path/to/algorithm-performance-analyzer/frontend/dist;
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📋 Pre-deployment Checklist
- [ ] Update `allow_origins` in `backend/main.py` if you want to restrict access to specific domains.
- [ ] Set `VITE_API_URL` environment variable for the frontend.
- [ ] Ensure the `results/` directory has write permissions.
- [ ] For production, consider using a production-grade database instead of the local `.db` file if scale is required.
