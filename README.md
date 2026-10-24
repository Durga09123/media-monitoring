# Media Monitor – YouTube Channel Views Analysis

Flask app that takes a YouTube channel link, fetches all uploaded videos through the
YouTube Data API v3, categorizes them by title keywords, and shows total/average views,
a category table, a bar chart and a per-video table.

## Project structure
```
media_monitor/
├── app.py
├── requirements.txt
├── .env.example      <- copy to .env and add your API key
├── Procfile          <- for Render / Railway / Heroku
├── render.yaml       <- one-click Render blueprint
├── .gitignore
└── templates/
    ├── index.html
    └── result.html
```

## 1. Get a YouTube API key
1. Go to https://console.cloud.google.com/ and create a project.
2. APIs & Services → Library → enable **YouTube Data API v3**.
3. APIs & Services → Credentials → Create credentials → **API key**.

## 2. Run locally in VS Code
1. Unzip and open the folder: **File → Open Folder → media_monitor**
2. Open the terminal (Ctrl + `) and create a virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and paste your key:
   `YOUTUBE_API_KEY=AIza...`
5. `python app.py`
6. Open http://127.0.0.1:5000 and paste e.g. `https://www.youtube.com/@kamarajcollegeofficial1474`

## 3. Deploy (Render – free)
1. Create a GitHub repo and push this folder (`.env` is git-ignored, so your key stays private).
   ```
   git init
   git add .
   git commit -m "Media Monitor"
   git branch -M main
   git remote add origin https://github.com/<you>/media-monitor.git
   git push -u origin main
   ```
2. On https://render.com → **New → Web Service** → connect the repo.
   (Or **New → Blueprint** to use `render.yaml`.)
3. Settings: Build `pip install -r requirements.txt`, Start `gunicorn app:app --timeout 120`.
4. Add environment variable `YOUTUBE_API_KEY` with your key.
5. Deploy. Your app will be live at `https://<name>.onrender.com`.

Railway / PythonAnywhere also work with the same files.

## Notes
- Free YouTube API quota is 10,000 units/day; each analysis uses roughly 1 unit per 50 videos.
- Free Render services sleep after inactivity, so the first load can take ~30–60 s.
