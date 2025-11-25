# 🚀 Quick Start: Deploy to Render in 5 Minutes

## Step 1: Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo: `amitok2/plan-master-backend`

## Step 2: Fill in the Form

**Root Directory:** (leave empty)

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:** Select **Free**

## Step 3: Add Environment Variables

Click **"Advanced"** → Add these environment variables:

```
GEMINI_API_KEY=your-gemini-api-key-here
PLAN_MASTER_API_KEYS=test-key-123,dev-key-456
```

**Get your Gemini API key:** https://aistudio.google.com/app/apikey

## Step 4: Deploy!

Click **"Deploy Web Service"** and wait ~2-3 minutes.

## Step 5: Test Your API

Once deployed, visit:
```
https://your-app-name.onrender.com/health
```

You should see:
```json
{
  "status": "healthy",
  "gemini_api_configured": true,
  "valid_api_keys_count": 2
}
```

## Step 6: Update Your MCP Client

Copy your Render URL and update the MCP client to use it:

```bash
export PLAN_MASTER_BACKEND_URL=https://your-app-name.onrender.com
```

---

**Done!** 🎉 Your backend is now live and ready to use.

For detailed documentation, see [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md)

