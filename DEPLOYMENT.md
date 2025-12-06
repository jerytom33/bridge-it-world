# Render.com Deployment Guide for BridgeIT

Your Django project has been configured for deployment on Render. Follow these steps to go live.

## 1. Prerequisites

- A [Render](https://render.com/) account.
- A [GitHub](https://github.com/) repository for this project.
- Your Neon PostgreSQL database URL (or use Render's managed PostgreSQL).

## 2. Configuration Changes Made

We have made the following changes to prepare your project:
- **`render.yaml`**: Infrastructure as Code (IaC) file that tells Render how to deploy your app.
- **`build.sh`**: Script to install dependencies, collect static files, and migrate database.
- **`settings.py`**: Configured to use `Whitenoise` for static files and read settings from environment variables.
- **`requirements.txt`**: Includes `gunicorn` and `whitenoise`.

## 3. Important Note on Media Files ⚠️

**Critical**: Like Vercel, Render's standard Web Services have an **ephemeral file system**. This means any files uploaded by users (profile pictures, resumes, etc.) to the `/media/` folder **WILL BE DELETED** on every deployment or restart.

**Solution for Production**:
To persist user uploads, you must configure a cloud storage provider like:
- **AWS S3** (Recommended)
- **Cloudinary**
- **Google Cloud Storage**
- **Render Disk** (You can attach a persistent disk, but it requires a paid plan and is only accessible by one service).

## 4. Deployment Steps

### Step 1: Push to GitHub
1. Initialize git if you haven't: `git init`
2. Add all files: `git add .`
3. Commit: `git commit -m "Prepare for Render deployment"`
4. Push to your GitHub repository.

### Step 2: Import to Render (Blueprint)
1. Go to your [Render Dashboard](https://dashboard.render.com/).
2. Click **"New +"** -> **"Blueprint"**.
3. Connect your GitHub repository.
4. Render will automatically detect the `render.yaml` file.
5. It will ask you to approve the resources (Web Service).
6. Click **"Apply"**.

### Step 3: Configure Environment Variables
The `render.yaml` sets up some defaults, but you might need to adjust them in the Render Dashboard under **"Environment"**:

| Name | Value | Description |
|------|-------|-------------|
| `SECRET_KEY` | (Auto-generated) | Django secret key |
| `DEBUG` | `False` | Production mode |
| `ALLOWED_HOSTS` | `*` | Allows all hosts (or set to your Render URL) |
| `DATABASE_URL` | `postgresql://...` | **IMPORTANT**: Add your Neon DB URL here if not using Render's DB |

**Database Note**: The `render.yaml` is configured to look for a database named `bridgeit-db` defined in the yaml. If you want to use your **existing Neon DB**, you should:
1.  Go to the Dashboard.
2.  Update the `DATABASE_URL` environment variable to your Neon connection string.
3.  (Optional) Delete the `bridgeit-db` Postgres service if Render created one and you don't want to pay for it.

### Step 4: Verify Deployment
Render will run the `build.sh` script which:
1.  Installs requirements.
2.  Collects static files.
3.  Runs database migrations.

Once finished, your app will be live!

## 5. Troubleshooting

- **Build Fails**: Check the "Logs" tab. Common issues are missing dependencies in `requirements.txt`.
- **Database Errors**: Ensure `DATABASE_URL` is correct and your Neon DB allows connections from anywhere (0.0.0.0/0).
- **Static Files**: If styles are missing, ensure `whitenoise` is configured (it is).
