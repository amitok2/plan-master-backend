# 🚀 Deploying Plan Master Backend to Render

This guide will help you deploy the Plan Master Backend API to Render.

## 📋 Prerequisites

1. A [Render](https://render.com) account (free tier available)
2. Your GitHub repository: `https://github.com/amitok2/plan-master-backend`
3. A Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
4. Your Plan Master API keys for client authentication

---

## 🔧 Step 1: Configure Render Service

### Basic Settings

| Field | Value |
|-------|-------|
| **Root Directory** | Leave empty (or `.`) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | Free (or Starter for production) |

### Important Notes:
- ✅ Render automatically provides `$PORT` environment variable
- ✅ The start command uses `$PORT` instead of hardcoded 8000
- ✅ Python version will be auto-detected from your code

---

## 🔐 Step 2: Set Environment Variables

After creating the service, go to **Environment** tab and add:

### Required Variables:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `GEMINI_API_KEY` | `your-gemini-api-key` | Get from [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `PLAN_MASTER_API_KEYS` | `key1,key2,key3` | Comma-separated list of valid API keys for client authentication |

### Optional Variables:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `PYTHON_VERSION` | `3.11` | Specify Python version (recommended) |

### Example:
```
GEMINI_API_KEY=AIzaSyD...your-actual-key
PLAN_MASTER_API_KEYS=prod-key-abc123,prod-key-xyz789
PYTHON_VERSION=3.11
```

---

## 🧪 Step 3: Test Your Deployment

Once deployed, Render will provide you with a URL like:
```
https://plan-master-backend.onrender.com
```

### Test the health endpoint:
```bash
curl https://your-app-name.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "gemini_api_configured": true,
  "valid_api_keys_count": 2
}
```

### Test the API docs:
Visit: `https://your-app-name.onrender.com/docs`

---

## 🔗 Step 4: Update MCP Client

Update your MCP client's backend URL to point to your Render deployment:

In `/Users/amitlavi/plan-master-mcp/src/index.ts`:

```typescript
const BACKEND_URL = process.env.PLAN_MASTER_BACKEND_URL || "https://your-app-name.onrender.com";
```

Or set it as an environment variable in your MCP configuration.

---

## 🚨 Important Security Notes

1. **Never commit API keys to Git**
   - Use Render's environment variables
   - Keep `.env` in `.gitignore`

2. **Generate Strong API Keys**
   ```bash
   # Generate a random API key
   openssl rand -hex 32
   ```

3. **Update Client Configuration**
   - Distribute your production API keys securely to users
   - Users should add them to their MCP config:
   ```json
   {
     "mcpServers": {
       "plan-master": {
         "command": "npx",
         "args": ["-y", "plan-master-mcp"],
         "env": {
           "PLAN_MASTER_API_KEY": "your-production-key-here",
           "PLAN_MASTER_BACKEND_URL": "https://your-app-name.onrender.com"
         }
       }
     }
   }
   ```

---

## 📊 Monitoring & Logs

### View Logs:
- Go to your Render service dashboard
- Click on **Logs** tab
- Monitor requests and errors in real-time

### Check Service Status:
```bash
curl https://your-app-name.onrender.com/
```

---

## 💰 Pricing & Performance

### Free Tier:
- ✅ 512 MB RAM, 0.1 CPU
- ✅ Spins down after 15 minutes of inactivity
- ✅ Cold start time: ~30 seconds
- ⚠️ Good for testing, not production

### Starter Tier ($7/month):
- ✅ 512 MB RAM, 0.5 CPU
- ✅ Always on (no cold starts)
- ✅ Better for production use

### Recommendations:
- **Development/Testing**: Use Free tier
- **Production**: Use Starter tier or higher
- **High Traffic**: Consider Standard tier (2 GB RAM)

---

## 🔄 Auto-Deploy from GitHub

Render automatically deploys when you push to `main` branch:

```bash
cd /Users/amitlavi/plan-master-backend
git add .
git commit -m "Update backend"
git push origin main
# Render will automatically deploy!
```

---

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not set"
**Solution**: Add `GEMINI_API_KEY` in Render Environment variables

### Issue: "Port already in use"
**Solution**: Make sure start command uses `$PORT` variable

### Issue: "Module not found"
**Solution**: Check that all dependencies are in `requirements.txt`

### Issue: "Cold start is slow"
**Solution**: Upgrade to Starter tier for always-on service

### Issue: "401 Unauthorized"
**Solution**: Check that your API key is in `PLAN_MASTER_API_KEYS` environment variable

---

## 📚 Additional Resources

- [Render Python Docs](https://render.com/docs/deploy-fastapi)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs)

---

## ✅ Deployment Checklist

- [ ] GitHub repo connected to Render
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] `GEMINI_API_KEY` environment variable set
- [ ] `PLAN_MASTER_API_KEYS` environment variable set
- [ ] Health endpoint returns 200 OK
- [ ] API docs accessible at `/docs`
- [ ] MCP client updated with production URL
- [ ] Production API keys distributed to users

---

**Need Help?** Open an issue on GitHub: https://github.com/amitok2/plan-master-backend/issues

