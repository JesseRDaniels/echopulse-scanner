# Railway Deployment Guide

## 🚀 Quick Deploy to Railway

### Step 1: Create GitHub Repository (if you haven't)

```bash
# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/echopulse-scanner.git
git push -u origin main
```

### Step 2: Deploy to Railway

1. **Go to Railway**: https://railway.app/new

2. **Deploy from GitHub**:
   - Click "Deploy from GitHub repo"
   - Select your `echopulse-scanner` repository
   - Railway will auto-detect the configuration from `railway.json`

3. **Configure Environment** (optional for Phase 1):
   - No environment variables needed for manual MVP
   - For Phase 2, you'll add API keys here

4. **Deploy**:
   - Railway will automatically build and deploy
   - Wait 2-3 minutes for first deployment
   - You'll get a URL like: `https://echopulse-scanner-production.up.railway.app`

### Step 3: Add Persistent Storage

1. **In Railway Dashboard**:
   - Go to your service
   - Click "Variables" tab
   - Click "+ New Variable"
   - Add volume mounts:
     - `/data` - for scan data
     - `/briefs` - for generated briefs
     - `/trades` - for trade logs

2. **Redeploy** after adding volumes

### Step 4: Test Your Deployment

1. Visit your Railway URL
2. Click "Get Sample" to download sample data
3. Upload the JSON file
4. View your first ECHOPULSE brief!

---

## 🔧 Alternative: Railway CLI Deploy

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project (in your echopulse-scanner directory)
railway init

# Deploy
railway up

# Open in browser
railway open
```

---

## 📱 Access Your App

### Web Interface
Visit your Railway URL to:
- Upload JSON data files
- View generated briefs
- Download sample data

### API Endpoints
- `GET /health` - Health check
- `POST /api/upload` - Upload data file
- `GET /api/sample-data` - Get sample template
- `GET /api/briefs` - List all briefs
- `GET /api/briefs/{date}` - Get specific brief

---

## 🔄 Updates & Redeployment

Railway automatically redeploys when you push to GitHub:

```bash
# Make changes locally
git add .
git commit -m "Your update message"
git push

# Railway will auto-deploy
```

---

## 📊 Monitoring

### Check Logs
- Railway Dashboard → Your Service → Deployments → View Logs
- Look for errors or issues

### Health Check
```bash
curl https://your-app-url.up.railway.app/health
```

Should return: `{"status":"healthy","version":"3.0"}`

---

## ⚙️ Phase 2: Adding Automation

When you're ready for automated data collection:

1. **Add API Keys** (Railway Dashboard → Variables):
   ```
   ALPHA_VANTAGE_API_KEY=your_key_here
   TZ=America/New_York
   ```

2. **Add Cron Job**:
   - Create `scripts/collector.py` with data collection logic
   - Configure Railway cron to run daily at 8 AM EST
   - Or use external service (GitHub Actions, cron-job.org) to hit a webhook

3. **Redeploy** with new changes

---

## 🐛 Troubleshooting

### App Won't Start
- Check Railway logs for errors
- Verify `requirements.txt` has all dependencies
- Make sure `railway.json` has correct start command

### Can't Access Web UI
- Wait 2-3 minutes after deployment
- Check Railway dashboard for deployment status
- Verify domain settings in Railway

### File Upload Fails
- Check file size (<10MB recommended)
- Verify JSON format matches sample data
- Check Railway logs for error details

### Briefs Not Persisting
- Verify volumes are configured in Railway
- Check write permissions
- Review logs for file system errors

---

## 💰 Cost

Railway free tier includes:
- $5 credit per month
- Perfect for personal projects like this
- Estimated usage: ~$1-2/month

If you exceed free tier:
- Add payment method in Railway dashboard
- You'll only pay for what you use

---

## 🔐 Security Notes

- Never commit `.env` files or API keys to git
- Use Railway environment variables for secrets
- Keep your Railway dashboard secure (2FA recommended)
- This is for personal use - don't expose to public internet without auth

---

## ✅ Phase 1 Complete!

You now have:
- ✅ Railway-deployed web app
- ✅ Manual data upload and analysis
- ✅ ECHOPULSE brief generation
- ✅ Accessible from anywhere

**Next**: Move to Phase 2 for automation!
