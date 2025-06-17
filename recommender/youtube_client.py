import requests
import random

# Replace with your RapidAPI key
API_KEY = "72b128c08amshe7d12deb1b44838p1ee32bjsn99d1ca141e74"

def get_music_by_mood(mood):
    url = "https://youtube-search-and-download.p.rapidapi.com/search"
    
    querystring = {
        "query": f"{mood} mood music",
        "type": "v",
        "sort": "relevance"
    }

    headers = {
        "X-RapidAPI-Key": "72b128c08amshe7d12deb1b44838p1ee32bjsn99d1ca141e74",
        "X-RapidAPI-Host": "youtube-search-and-download.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        # Extract video list
        videos = data.get("contents", [])
        music_results = []

        for video in videos:
            if "video" in video:
                video_data = video["video"]
                title = video_data.get("title", "Unknown Title")
                video_id = video_data.get("videoId")
                
                if video_id:
                    youtube_url = f"https://www.youtube.com/embed/{video_id}"
                    music_results.append({
                        "title": title,
                        "youtube": youtube_url
                    })

        # Shuffle and return 3–5 unique songs
        random.shuffle(music_results)
        return music_results[:5]

    except Exception as e:
        print(f"🎵 Error fetching music: {e}")
        return []


