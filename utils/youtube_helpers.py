# utils/youtube_helpers.py
# ─────────────────────────────────────────────────────
# Responsible for: fetching data from YouTube API.
#
# Functions here do ONE thing each — fetch data and
# return clean Python dicts/lists. No UI code here.
# ─────────────────────────────────────────────────────

import isodate
import streamlit as st
from datetime import datetime, timezone
from utils.api_clients import get_youtube_client
from config import MAX_RESULTS


def _youtube():
    """Shorthand to get the cached YouTube client."""
    return get_youtube_client()


@st.cache_data(ttl=3600)  # Cache for 1 hour to save API quota
def get_channel_info(channel_id: str) -> dict:
    """
    Returns basic info about a channel:
    name, subscriber count, total views, video count.
    """
    response = _youtube().channels().list(
        part="snippet,statistics",
        id=channel_id
    ).execute()

    if not response.get("items"):
        return {}

    item  = response["items"][0]
    stats = item.get("statistics", {})
    return {
        "name":        item["snippet"]["title"],
        "description": item["snippet"].get("description", ""),
        "subscribers": int(stats.get("subscriberCount", 0)),
        "total_views": int(stats.get("viewCount", 0)),
        "video_count": int(stats.get("videoCount", 0)),
        "thumbnail":   item["snippet"]["thumbnails"].get("default", {}).get("url", ""),
    }


@st.cache_data(ttl=3600)
def get_recent_uploads(channel_id: str, max_results: int = MAX_RESULTS) -> list[dict]:
    """
    Returns the latest `max_results` regular video uploads for a channel.
    Each item includes: title, views, upload_date, views_per_day, video_id.
    """
    # Step 1: Get the channel's "uploads" playlist ID
    channel_resp = _youtube().channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    if not channel_resp.get("items"):
        return []

    uploads_playlist = (
        channel_resp["items"][0]["contentDetails"]
        ["relatedPlaylists"]["uploads"]
    )

    # Step 2: Get video IDs from that playlist
    playlist_resp = _youtube().playlistItems().list(
        part="contentDetails",
        playlistId=uploads_playlist,
        maxResults=max_results
    ).execute()

    video_ids = [
        item["contentDetails"]["videoId"]
        for item in playlist_resp.get("items", [])
    ]

    if not video_ids:
        return []

    # Step 3: Get full stats for those videos in ONE API call
    return _fetch_video_details(video_ids, video_type="upload")


@st.cache_data(ttl=3600)
def get_recent_livestreams(channel_id: str, max_results: int = MAX_RESULTS) -> list[dict]:
    """
    Returns the latest `max_results` completed livestreams for a channel.
    Uses search API — costs more quota than playlist approach.
    """
    search_resp = _youtube().search().list(
        part="id",
        channelId=channel_id,
        type="video",
        eventType="completed",   # only finished livestreams
        order="date",
        maxResults=max_results
    ).execute()

    video_ids = [
        item["id"]["videoId"]
        for item in search_resp.get("items", [])
    ]

    if not video_ids:
        return []

    return _fetch_video_details(video_ids, video_type="livestream")


def _fetch_video_details(video_ids: list[str], video_type: str) -> list[dict]:
    """
    Internal helper: given a list of video IDs,
    fetches full statistics and returns cleaned records.
    """
    response = _youtube().videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    ).execute()

    results = []
    now = datetime.now(timezone.utc)

    for item in response.get("items", []):
        snippet    = item.get("snippet", {})
        stats      = item.get("statistics", {})
        details    = item.get("contentDetails", {})

        published  = snippet.get("publishedAt", "")
        views      = int(stats.get("viewCount", 0))

        # Calculate days since upload → views per day
        try:
            pub_dt   = datetime.fromisoformat(published.replace("Z", "+00:00"))
            days_old = max((now - pub_dt).days, 1)   # avoid division by zero
        except Exception:
            days_old = 1

        # Parse ISO 8601 duration (e.g. PT1H23M45S → seconds)
        try:
            duration_sec = int(isodate.parse_duration(
                details.get("duration", "PT0S")
            ).total_seconds())
        except Exception:
            duration_sec = 0

        results.append({
            "video_id":      item["id"],
            "title":         snippet.get("title", ""),
            "published":     published[:10],          # YYYY-MM-DD
            "views":         views,
            "likes":         int(stats.get("likeCount", 0)),
            "comments":      int(stats.get("commentCount", 0)),
            "views_per_day": round(views / days_old, 0),
            "duration_sec":  duration_sec,
            "days_old":      days_old,
            "type":          video_type,
            "url":           f"https://youtube.com/watch?v={item['id']}",
            "thumbnail":     snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
        })

    return results
