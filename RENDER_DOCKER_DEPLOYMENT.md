# 🐳 Deploying Plan Master Backend to Render with Docker

This guide shows you how to deploy using Docker on Render.

## 🚀 Quick Start

### Step 1: Go to Render Dashboard
1. Visit [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo: `amitok2/plan-master-backend`

### Step 2: Configure Service

| Field | Value |
|-------|-------|
| **Name** | `plan-master-backend` |
| **Environment** | **Docker** (Important!) |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Root Directory** | Leave empty |
| **Dockerfile Path** | `./Dockerfile` |
| **Docker Build Context Directory** | `.` |

### Step 3: Add Environment Variables

Click **"Advanced"** and add these environment variables:

```
GEMINI_API_KEY=your-gemini-api-key-here
PLAN_MASTER_API_KEYS=test-key-123,dev-key-456
```

**Get your Gemini API key:** https://aistudio.google.com/app/apikey

### Step 4: Deploy!

Click **"Create Web Service"** and wait ~3-5 minutes for the build.

---

## 🔧 What's Different with Docker?

### ✅ Advantages:
- More control over the environment
- Consistent builds across environments
- Can install system dependencies easily
- Health checks built into the container

### ⚙️ How It Works:

1. **Dockerfile** defines the container:
   - Uses Python 3.11 slim
   - Installs dependencies
   - Copies your code
   - Runs uvicorn

2. **Render** automatically:
   - Detects the Dockerfile
   - Builds the Docker image
   - Runs the container
   - Provides `PORT` environment variable

3. **Your app** listens on `$PORT`:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
   ```

---

## 🧪 Test Your Deployment

Once deployed, test these endpoints:

### 1. Root Endpoint
```bash
curl https://plan-master-backend.onrender.com/
```

Expected response:
```json
{
  "message": "Plan Master Backend API is running",
  "status": "healthy",
  "version": "1.0.0",
  "docs": "/docs",
  "gemini_model": "gemini-3-pro-preview"
}
```

### 2. Health Check
```bash
curl https://plan-master-backend.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "gemini_api_configured": true,
  "valid_api_keys_count": 2,
  "version": "1.0.0"
}
```

### 3. API Documentation
Open in browser: https://plan-master-backend.onrender.com/docs

---

## 🐛 Troubleshooting

### Issue: "Failed to build Docker image"
**Solution:** Check the build logs for specific errors. Common issues:
- Missing dependencies in `requirements.txt`
- Syntax errors in `Dockerfile`
- Wrong Python version

### Issue: "Health check failed"
**Solution:** 
- Make sure `GEMINI_API_KEY` is set in environment variables
- Check logs for specific error messages
- Verify the `/health` endpoint is accessible

### Issue: "Container exits immediately"
**Solution:**
- Check that the CMD in Dockerfile is correct
- Verify uvicorn is starting properly
- Look at logs for startup errors

---

## 📊 Monitoring

### View Logs:
1. Go to your Render service dashboard
2. Click **"Logs"** tab
3. Monitor real-time logs

### Check Metrics:
1. Click **"Metrics"** tab
2. View CPU, memory, and request metrics

---

## 🔄 Local Development with Docker

### Build locally:
```bash
cd /Users/amitlavi/plan-master-backend
docker build -t plan-master-backend .
```

### Run locally:
```bash
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your-key \
  -e PLAN_MASTER_API_KEYS=test-key-123 \
  plan-master-backend
```

### Test locally:
```bash
curl http://localhost:8000/health
```

---

## 📝 Files Explained

### `Dockerfile`
- Defines the container image
- Installs Python 3.11 and dependencies
- Copies application code
- Sets up health checks
- Runs uvicorn

### `main.py`
- FastAPI application
- CORS middleware enabled
- Logging configured
- Exception handlers
- Health check endpoints

### `requirements.txt`
- Python dependencies
- Pinned versions for stability

---

## ✅ Deployment Checklist

- [ ] Dockerfile exists in repo
- [ ] GitHub repo connected to Render
- [ ] Environment set to **Docker**
- [ ] `GEMINI_API_KEY` environment variable set
- [ ] `PLAN_MASTER_API_KEYS` environment variable set
- [ ] Build completes successfully
- [ ] Health endpoint returns 200 OK
- [ ] API docs accessible at `/docs`
- [ ] Logs show no errors

---

**Need Help?** Open an issue on GitHub: https://github.com/amitok2/plan-master-backend/issues

