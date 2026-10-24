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
https://media-monitoring-cv6l.vercel.app/
