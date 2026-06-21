# 🚀 Deployment Guide - AI Research Intelligence System

This guide covers multiple deployment options for the application.

---

## ✅ Option 1: Streamlit Community Cloud (RECOMMENDED)

**Best for:** Quick deployment, portfolios, demos, university projects
**Cost:** 100% FREE
**Difficulty:** ⭐ Very Easy

### Prerequisites
- [x] GitHub account
- [x] Project pushed to GitHub (✓ Already done!)

### Step-by-Step Deployment

#### 1. Sign up for Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign up" or "Sign in with GitHub"
3. Authorize Streamlit to access your GitHub repos

#### 2. Deploy Your App
1. Click "New app" button
2. Select repository: `snehacat/AI_Research_Intelligence_System`
3. Branch: `main`
4. Main file path: `app/main.py`
5. Click "Deploy"

#### 3. Configure Secrets (Optional)
If you have API keys:
1. In app dashboard, click "⚙️ Settings"
2. Go to "Secrets" section
3. Add your keys in TOML format:
   ```toml
   OPENAI_API_KEY = "sk-your-key"
   SEMANTIC_SCHOLAR_API_KEY = "your-key"
   ```
4. Click "Save"

#### 4. Done! 🎉
- Your app will be live at: `https://your-app-name.streamlit.app`
- Auto-deploys on every git push
- Free SSL certificate included
- Custom domain available (settings)

### Troubleshooting

**If build fails:**
1. Check the logs in Streamlit dashboard
2. Ensure `requirements.txt` has all dependencies
3. Verify `packages.txt` for system dependencies

**If app is slow:**
- First load downloads NLP models (1-2 min)
- Subsequent loads are much faster
- Consider adding `@st.cache_resource` for heavy operations

---

## ✅ Option 2: Hugging Face Spaces

**Best for:** ML/NLP projects, model showcases
**Cost:** FREE
**Difficulty:** ⭐⭐ Easy

### Deployment Steps

#### 1. Create Space
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Name: `ai-research-intelligence`
4. SDK: Select "Streamlit"
5. Click "Create Space"

#### 2. Push Your Code
```bash
# Clone the HF space repo
git clone https://huggingface.co/spaces/YOUR_USERNAME/ai-research-intelligence
cd ai-research-intelligence

# Copy your project files
cp -r /path/to/your/project/* .

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

#### 3. Configure
Create a `README.md` in the Space:
```yaml
---
title: AI Research Intelligence System
emoji: 🧠
colorFrom: blue
colorTo: cyan
sdk: streamlit
sdk_version: 1.55.0
app_file: app/main.py
pinned: false
---
```

#### 4. Done! 🎉
- Live at: `https://huggingface.co/spaces/USERNAME/ai-research-intelligence`
- Persistent URL
- Great for sharing with recruiters

---

## ✅ Option 3: Railway.app

**Best for:** More control, custom domains, databases
**Cost:** $5/month free credit (enough for this app)
**Difficulty:** ⭐⭐⭐ Medium

### Deployment Steps

#### 1. Install Railway CLI
```bash
npm install -g @railway/cli
# or
curl -fsSL https://railway.app/install.sh | sh
```

#### 2. Login & Initialize
```bash
railway login
cd /path/to/project
railway init
```

#### 3. Deploy
```bash
railway up
```

#### 4. Configure
In Railway dashboard:
- Set start command: `streamlit run app/main.py --server.port $PORT`
- Add environment variables if needed
- Connect custom domain (optional)

---

## ✅ Option 4: Render

**Best for:** Free tier with auto-deploy
**Cost:** FREE (with limitations)
**Difficulty:** ⭐⭐⭐ Medium

### Deployment Steps

#### 1. Create render.yaml
```yaml
services:
  - type: web
    name: ai-research-intelligence
    env: python
    buildCommand: "pip install -r requirements.txt && python -m spacy download en_core_web_sm"
    startCommand: "streamlit run app/main.py --server.port $PORT --server.address 0.0.0.0"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

#### 2. Deploy
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repo
4. Render auto-detects Python
5. Click "Create Web Service"

#### 3. Note
- Free tier spins down after 15 min inactivity
- First request after sleep takes 30-60 seconds
- Upgrade to paid for always-on service

---

## 🐳 Option 5: Docker + Any Cloud (Advanced)

**Best for:** Full control, production deployment
**Difficulty:** ⭐⭐⭐⭐ Advanced

### Create Dockerfile

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    poppler-utils \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLP models
RUN python -m spacy download en_core_web_sm && \
    python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the app
ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SEMANTIC_SCHOLAR_API_KEY=${SEMANTIC_SCHOLAR_API_KEY}
      - CROSSREF_API_KEY=${CROSSREF_API_KEY}
    volumes:
      - ./reports:/app/reports
      - ./data:/app/data
    restart: unless-stopped
```

### Deploy to:
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**
- **DigitalOcean App Platform**
- **Fly.io**

---

## 📊 Comparison Table

| Platform | Cost | Difficulty | Speed | Best For |
|----------|------|------------|-------|----------|
| **Streamlit Cloud** | Free | ⭐ | Fast | **Portfolios, Demos** ⭐ |
| **Hugging Face** | Free | ⭐⭐ | Fast | ML Projects |
| **Railway** | $5/mo credit | ⭐⭐⭐ | Very Fast | Custom needs |
| **Render** | Free (cold starts) | ⭐⭐⭐ | Medium | Auto-deploy |
| **Docker + Cloud** | Varies | ⭐⭐⭐⭐ | Fastest | Production |

---

## 🎯 Recommendation for Your Use Case

### For University Placements & Portfolio:
**Use Streamlit Community Cloud**
- ✅ Free forever
- ✅ Professional URL (custom domain available)
- ✅ Perfect for demos
- ✅ Easy to update (auto-deploys)
- ✅ Great uptime
- ✅ No credit card required

**Deployment time: 5 minutes**

---

## 📝 Post-Deployment Checklist

After deploying, update your:

### ✅ README.md
Add live demo link:
```markdown
## 🌐 Live Demo

Try the live application: [AI Research Intelligence System](https://your-app.streamlit.app)
```

### ✅ Resume/LinkedIn
Add project with live link:
```
AI Research Intelligence System
- Live Demo: https://your-app.streamlit.app
- GitHub: https://github.com/snehacat/AI_Research_Intelligence_System
- Tech: Python, NLP, Transformers, Streamlit
```

### ✅ GitHub Profile
Pin this repository to show on your profile

### ✅ Share Link
- With professors for evaluation
- With recruiters during interviews
- In job applications

---

## 🔧 Maintenance

### Update Your Deployed App
```bash
# Make changes locally
git add .
git commit -m "Update: description"
git push origin main
```
**Streamlit Cloud auto-deploys within 2-3 minutes!**

### Monitor Your App
- Check Streamlit Cloud dashboard for:
  - Usage stats
  - Error logs
  - Performance metrics

### Optimize for Production
1. Add caching for heavy operations:
   ```python
   @st.cache_resource
   def load_model():
       return load_heavy_model()
   ```

2. Implement error tracking
3. Add analytics (Google Analytics, Mixpanel)
4. Monitor performance

---

## 🆘 Getting Help

- **Streamlit Cloud Issues:** [community.streamlit.io](https://community.streamlit.io)
- **Deployment Errors:** Check app logs in dashboard
- **Performance:** Review Streamlit docs on optimization

---

## 🎉 Success!

Once deployed, your app will be:
- ✅ Live 24/7
- ✅ Accessible worldwide
- ✅ Professional presentation
- ✅ Perfect for interviews
- ✅ Great for your resume

**Share your live link with recruiters and watch the interview requests roll in!** 🚀
