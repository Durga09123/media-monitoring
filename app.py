import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

KEY = os.getenv("YOUTUBE_API_KEY")
API = "https://www.googleapis.com/youtube/v3"


def category(title):
    """Keyword-based category for a video title."""
    t = title.lower()
    d = {
        "Sports": "cricket football soccer basketball tennis ipl match",
        "Education": "education tutorial class course exam study python java coding workshop conference",
        "Technology": "technology tech iphone android laptop computer software",
        "Music": "song music lyrics audio singer concert",
        "Entertainment": "movie film cinema trailer actor comedy",
        "News": "news update politics headline",
        "Food": "recipe cooking food restaurant biryani dosa",
        "Travel": "travel trip tour tourism holiday hotel beach",
        "Gaming": "gaming game gameplay minecraft pubg",
        "Fitness": "fitness workout gym exercise yoga",
        "Finance": "finance money investment stock trading business",
        "Interview": "interview podcast discussion",
        "Vlog": "vlog daily day life",
        "Reviews": "review unboxing comparison",
    }
    for c, words in d.items():
        if any(w in t for w in words.split()):
            return c
    return "Others"


def yt(endpoint, **params):
    """Call a YouTube Data API endpoint and return JSON (raises on API error)."""
    params["key"] = KEY
    r = requests.get(f"{API}/{endpoint}", params=params, timeout=20)
    data = r.json()
    if "error" in data:
        raise RuntimeError(data["error"].get("message", "YouTube API error"))
    return data


@app.route("/")
def home():
    return render_template("index.html", error=None)


@app.route("/analyze", methods=["POST"])
def analyze():
    if not KEY:
        return render_template(
            "index.html",
            error="YOUTUBE_API_KEY is not set. Add it to your .env file (or hosting environment variables).",
        )

    link = request.form.get("channel_link", "").strip()
    try:
        # 1. Find channel id
        if "/channel/" in link:
            cid = link.split("/channel/")[1].split("/")[0]
        elif "/@" in link:
            user = link.split("/@")[1].split("/")[0].split("?")[0]
            data = yt("channels", part="snippet", forHandle="@" + user)
            if not data.get("items"):
                return render_template("index.html", error="Channel not found.")
            cid = data["items"][0]["id"]
        else:
            return render_template(
                "index.html",
                error="Invalid channel URL. Use a link like youtube.com/@name or youtube.com/channel/ID.",
            )

        # 2. Channel info + uploads playlist
        data = yt("channels", part="snippet,contentDetails", id=cid)
        if not data.get("items"):
            return render_template("index.html", error="Channel not found.")
        info = data["items"][0]
        name = info["snippet"]["title"]
        playlist = info["contentDetails"]["relatedPlaylists"]["uploads"]

        # 3. All uploaded videos (paginated)
        videos, token = [], None
        while True:
            p = {"part": "snippet", "playlistId": playlist, "maxResults": 50}
            if token:
                p["pageToken"] = token
            data = yt("playlistItems", **p)
            for i in data.get("items", []):
                s = i["snippet"]
                videos.append(
                    {
                        "id": s["resourceId"]["videoId"],
                        "title": s["title"],
                        "date": s["publishedAt"][:10],
                    }
                )
            token = data.get("nextPageToken")
            if not token:
                break

        # 4. View counts (50 ids per request)
        views = {}
        for i in range(0, len(videos), 50):
            ids = ",".join(v["id"] for v in videos[i : i + 50])
            data = yt("videos", part="statistics", id=ids)
            for x in data.get("items", []):
                views[x["id"]] = int(x["statistics"].get("viewCount", 0))

    except requests.RequestException:
        return render_template("index.html", error="Network error while contacting YouTube. Try again.")
    except RuntimeError as e:
        return render_template("index.html", error=f"YouTube API error: {e}")

    # 5. Category analysis
    cats = {}
    for v in videos:
        v["views"] = views.get(v["id"], 0)
        v["category"] = category(v["title"])
        c = v["category"]
        cats.setdefault(c, {"videos": 0, "views": 0})
        cats[c]["videos"] += 1
        cats[c]["views"] += v["views"]
    for c in cats:
        cats[c]["average"] = cats[c]["views"] // cats[c]["videos"]

    # Sort categories by total views (highest first)
    cats = dict(sorted(cats.items(), key=lambda kv: kv[1]["views"], reverse=True))

    total_videos = len(videos)
    total_views = sum(v["views"] for v in videos)
    average_views = total_views // total_videos if total_videos else 0

    return render_template(
        "result.html",
        channel_name=name,
        videos=videos,
        category_data=cats,
        categories=list(cats),
        category_views=[cats[c]["views"] for c in cats],
        total_videos=total_videos,
        total_views=total_views,
        average_views=average_views,
    )


if __name__ == "__main__":
    app.run(debug=True)
