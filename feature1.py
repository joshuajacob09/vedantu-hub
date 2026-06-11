from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)

CHANNELS = {
    # ── VEDANTU (OWN CHANNELS) ────────────────────────
    "Vedantu JEE Made Ejee":        "UC91RZv71f8p0VV2gaFI07pg",
    "Vedantu JEE English":          "UCwBfgxcxKUzlhpEMJxWEmdg",
    "Vedantu JEE Vaathi":           "UCUfK8KOu9IygDWI8O3_Vb0Q",
    "Vedantu NEET Made Ejee":       "UCqaq3Cwa7m_EsqlvfZh6uyw",
    "Vedantu NEET English":         "UCt8OFYyeXWmu8jiLU3hUwjw",
    "Vedantu NEET Tamil":           "UCTvn7dytna9k1xIlPAzqprw",
    "Vedantu NEET Vettri":          "UC6f7NHfiJK5GdgY4SumBHng",
    "Sankalp NEET Vedantu":         "UCWFXoexcMI1jQrHH2N-SJzQ",
    "Vedantu Commerce":             "UC4sfE23vp1PaO740hhhqpig",
    "Vedantu CBSE 10th":            "UCMY7ZvLB6-DnuSis_2s37_A",
    "Vedantu 9&10 English":         "UCOZZbzNiwvj308Vt-ndesKA",
    "Vedantu Young Wonders":        "UCK85zyie3OYa7rU494QjPbw",
    "Vedantu Olympiad School":      "UCPFn447O8-X7UdcW3AmIydQ",
    "Vedantu Master Tamil":         "UCo7S5qgzt1H66Qlepl90c1g",
    "Vedantu Telugu":               "UCsq4gc-EDXqxZZbaRjqFeTw",
    "Vedantu Class 6 7 & 8":        "UCi-J9CCaQ8w427GPHmoQGHA",
    "Catalysis by Vedantu":         "UCYIET4VzyU9-vIJhDYNzHPg",
    "Spectrum by Vedantu":          "UC0G5Qkp7bJfHKOCemS3fPAw",
    "Elementary Chemistry Vedantu": "UCG8eg2aeXrKOpcr6fvMX-lQ",

    # ── PHYSICS WALLAH NETWORK ────────────────────────
    "Physics Wallah":               "UCiGyWN6DEbnj2alu7iapuKQ",
    "JEE Wallah":                   "UCVJU_IChPMOe8RWkdVQjtfQ",
    "PW JEE":                       "UCVf1jaub9qzp4rMvdKflZYA",
    "Competition Wallah":           "UCD16eo98AXl-9T61Xd711kQ",
    "PW NEET":                      "UCGw8iWmsw1cPlfcrww-3C0g",

    # ── UNACADEMY NETWORK ─────────────────────────────
    "Yakeen NEET":                  "UCk19x9BG23f5xkHOzihhclA",
    "Unacademy JEE":                "UCcMU5NE1Lmf4Fqpx7n9F3Sw",
    "Unacademy JEE English":        "UCGcukk3AUT_ebF3jRcsdQLg",
    "JEEfinity by Unacademy":       "UCVGJz1j0N7Gk2qayiideOUg",
    "NEET Alchemy by Unacademy":    "UCvSE2vW71NVLqh5IwjhxLBA",
    "Unacademy NEET":               "UCdQwYksctqqiRwqp3PiJMWA",
    "IITian Explains":              "UCvjRa2jVhKVSbVDG85vKGww",

    # ── ALLEN ─────────────────────────────────────────
    "ALLEN NEET":                   "UCySvBtI4jMLXp0BT9osvASw",
    "ALLEN JEE":                    "UCkUI45drrKTWLxy3q3voJRw",

    # ── MOTION KOTA ───────────────────────────────────
    "Motion JEE & NEET":            "UCfl4OhoOv8xF64D5KzJinnA",
    "Motion Kota JEE":              "UCd7OIpmiEXf3iu1cir6-PrA",
    "Motion NEET":                  "UC8UzfGlCDh-Q8WDJfrJ6XoA",

    # ── NEW LIGHT ─────────────────────────────────────
    "New Light NEET":               "UC-NUWDDbu7Yy6dL2YMx2Biw",
    "New Light PRAYAAS":            "UCPWH5p6qAl7fewEzX1iwRFw",

    # ── OTHER COACHING INSTITUTIONS ───────────────────
    "Aakash NEET":                  "UCAPDuc6Kfpe1mKjMX367qmA",
    "Khan Sir Patna":               "UCL77mMHDQV_D2DixeqD1Tyg",
    "Competishun Mohit Tyagi":      "UCpyc1eTpM1cA3P0ZWym4clw",
    "Competishun+":                 "UC6ieIswHA9WInRsa2r88hRw",
    "eSaral JEE & NEET":            "UCddnJhXMUxzHoH8AZkZSd8w",
    "eSaral NEET":                  "UCD7O0ABXcFzKPTAuUTNCE3A",
    "Resonance Eduventures":        "UC_bdItm01JN2xXRz5hXJwTQ",
    "Etoos Education":              "UCa2dTDY1WDY2xWO8pRSES2g",
    "Vora Classes":                 "UCDG_YP69cl42ly3pPy8-Liw",
    "Career Point Kota":            "UCLNYhA7rnXfdaFh-W6hJTSg",
    "Matrix JEE Academy":           "UC1qTGuS_gRjKRburf9i1izg",

    # ── PHYSICS SPECIALISTS ───────────────────────────
    "Physics Galaxy":               "UCgBmfNILAlXmGv3CsJ8oFJA",
    "Eduniti Physics":              "UC7px6OmooQLmsJlYACR_n-A",
    "JeePhyX":                      "UCR91PnmVpl3YO3f0ToCQrig",
    "Physics Sir JEE Janardhan":    "UC8Z_fpEYLtBu3-OuhJGqLZg",
    "Vinay Uppal Physics":          "UC5byrHGQwlhfUanp_ubKwdg",
    "NMS Sir Physics":              "UC-ub6TMPCDj4lxuoZh_ZL8g",
    "Sachin Sir Physics":           "UCwkhjRhv6CHkQa6EiQmcX0g",

    # ── CHEMISTRY SPECIALISTS ─────────────────────────
    "Pankaj Sir Chemistry":         "UCMMlYN-EhNrt0eoEDUK0bdg",
    "Canvas Classes Chemistry":     "UCWGjJvI_6gX-RACsZ6KZyrw",
    "Sachin Rana Chemistry":        "UC1-ZdFLBukC6fTZ8QRWvpDw",

    # ── MATHEMATICS SPECIALISTS ───────────────────────
    "MathonGo":                     "UCNn75PJi2J5OmZGuLCZGJPg",
    "Bhannat Maths":                "UCDSP-sZ5khlym4MucLh77Jw",
    "Best Approach Manoj Chauhan":  "UCr_h4xhYBLawp5bdObn0hbA",
    "Mathsmerizing":                "UCO0s78XLuof9HKSMpUsxMsg",
    "Maths Unplugged":              "UCHWna16c7Ff0mY_QBVF2rXQ",
    "RZ Maths":                     "UCvZCNCHoOINkG24aRruHtcQ",
    "GB Sir Maths":                 "UCjILZDfCFrqeU1EQrAm_ZPw",
    "Factorial Academy":            "UCeSAnGvh_0SXg53on-NQDzQ",

    # ── NEET SPECIALISTS ──────────────────────────────
    "NEETprep NCERT":               "UC4BjX3BqigeWAOp0kLkKSIA",
    "Biomentors Classes Online":    "UCwMNVCXcSWNMS0C8rcRCWxA",
    "Careerwill NEET":              "UCGJJPZRf7mhHqp0X3fpVdyg",
    "NEET Adda247":                 "UC9v_KhFxEX6D4f3oDd9_LIQ",
    "Anmol Sharma Biology":         "UCoSQ_RjcoEnkAtYCVvX7tfA",
    "Biofairy Ritu Rattewal":       "UCBlHYBCoCmfqHnZNk5NyVvQ",
    "Biology at Ease":              "UCYbFCdcMfA68ZvJO__zTUjg",
    "Dr. Rakshita Singh":           "UCObWXIaGPPVjX_RJgYDbB1w",
    "Dr. Parth Goyal":              "UCoh-C01mA3H32unyTAOF0NQ",
    "Tamanna Chaudhary":            "UCLBo1sRUQzDdblEvsytdsig",
    "NEET Kaka JEE":                "UC3wQ-HF4qpZVEUwWAzgRySw",
}


def get_uploads_playlist_id(channel_id):
    response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()
    if not response.get("items"):
        return None
    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_latest_video_ids(uploads_playlist_id):
    response = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=uploads_playlist_id,
        maxResults=10
    ).execute()
    video_ids = []
    for item in response["items"]:
        video_ids.append(item["contentDetails"]["videoId"])
    return video_ids


def get_video_details(video_ids):
    ids_string = ",".join(video_ids)
    response = youtube.videos().list(
        part="snippet,statistics",
        id=ids_string
    ).execute()
    videos = []
    for item in response["items"]:
        title = item["snippet"]["title"]
        date  = item["snippet"]["publishedAt"][:10]
        views = int(item["statistics"].get("viewCount", "0"))
        url   = f"https://youtube.com/watch?v={item['id']}"
        videos.append({
            "title": title,
            "date":  date,
            "views": views,
            "url":   url,
        })
    return videos


def print_results(channel_name, videos):
    print("\n" + "="*60)
    print(f"  {channel_name} — LATEST 10 UPLOADS")
    print("="*60 + "\n")
    for i, video in enumerate(videos, start=1):
        print(f"{i}. {video['title']}")
        print(f"   Date  : {video['date']}")
        print(f"   Views : {video['views']:,}")
        print(f"   URL   : {video['url']}")
        print()


if __name__ == "__main__":
    skipped = []
    for channel_name, channel_id in CHANNELS.items():
        print(f"Fetching {channel_name}...")
        playlist_id = get_uploads_playlist_id(channel_id)
        if not playlist_id:
            skipped.append(channel_name)
            continue
        video_ids = get_latest_video_ids(playlist_id)
        videos = get_video_details(video_ids)
        print_results(channel_name, videos)

    if skipped:
        print("\n" + "="*60)
        print("  SKIPPED CHANNELS")
        print("="*60)
        for name in skipped:
            print(f"  ⚠ {name}")