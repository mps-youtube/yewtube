import json
import os
import glob
import random
import re
import time
import urllib.parse
from urllib.parse import parse_qs, urlparse
import urllib.request
import urllib.error
import typing as T
from datetime import datetime, timezone

from . import util
import yt_dlp


def _format_published_time(entry):
    """Helper to get a standard ISO8601 string from yt-dlp entry."""
    # Try timestamp first (unix epoch)
    ts = entry.get("timestamp")
    if ts:
        return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Try upload_date (YYYYMMDD)
    ud = entry.get("upload_date")
    if ud and len(ud) == 8:
        try:
            return f"{ud[:4]}-{ud[4:6]}-{ud[6:]}T00:00:00Z"
        except Exception:
            pass

    return None


class VideoInfo:
    """Standardized metadata object for videos."""

    def __init__(self, data: T.Dict[str, T.Any]):
        self._data = data
        self._ytid = data.get("id") or data.get("videoId")
        self.title = data.get("title", "Unknown Title")
        self.author = data.get("uploader") or data.get("channel", {}).get("name")
        self.length = data.get("duration") or 0
        self.view_count = data.get("view_count") or 0
        self.likes = data.get("likes") or 0
        self.dislikes = data.get("dislikes") or 0
        self.rating = data.get("averageRating") or 0
        expires = data.get("expires")
        self.expiry = time.time() + (expires if expires is not None else 3600)
        self.fresh = True

    @property
    def ytid(self):
        return self._ytid

    @property
    def videoid(self):
        return self._ytid

    def __getitem__(self, key):
        return self._data.get(key)

    def get(self, key, default=None):
        return self._data.get(key, default)


class ExtractionError(Exception):
    """Base exception for extraction issues."""

    pass


class MyLogger:
    def __init__(self, print_info=False):
        self.print_info = print_info

    def debug(self, msg):
        if not msg.startswith("[debug] "):
            self.info(msg)

    def info(self, msg):
        if self.print_info:
            print(msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def get_ydl_opts(extra_opts: T.Optional[T.Dict[str, T.Any]] = None) -> T.Dict[str, T.Any]:
    """Factory for standard yt-dlp options."""
    opts = {
        "logger": MyLogger(),
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
    }
    if extra_opts:
        opts.update(extra_opts)
    return opts


def get_video_streams(ytid):
    """Get different video / audio stream formats for a video id."""
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            info_dict = ydl.extract_info(ytid, download=False)
            return [
                i
                for i in info_dict["formats"]
                if i.get("format_note") != "storyboard"
            ]
    except Exception as e:
        raise ExtractionError(f"Failed to extract streams for {ytid}: {str(e)}")


def download_video(ytid, folder, audio_only=False):
    """Download video or audio to the specified folder."""
    ytdl_format_options = {
        "outtmpl": os.path.join(folder, "%(title)s-%(id)s.%(ext)s")
    }
    if audio_only:
        ytdl_format_options["format"] = "bestaudio/best"
        ytdl_format_options["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]

    try:
        with yt_dlp.YoutubeDL(get_ydl_opts(ytdl_format_options)) as ydl:
            ydl.download(["https://www.youtube.com/watch?v=%s" % ytid])
            return True
    except Exception as e:
        raise ExtractionError(f"Download failed for {ytid}: {str(e)}")


def search_videos(query, pages):
    """Search for videos and return standard results using yt-dlp."""
    return _search_videos_ytdl(query, pages)


def _enrich_results_with_dates(url, results):
    """Scrape relative published times from a YouTube page and enrich results."""
    try:
        # Force English locale via URL parameter and header
        if "?" in url:
            url += "&hl=en"
        else:
            url += "?hl=en"

        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.5"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode(errors="ignore")
            # Regex to find videoId and publishedTimeText
            # Note: "videoId":"ID" can appear before or after publishedTimeText depending on the renderer
            # We use a broad search and map by ID.
            pattern = r'"videoId":"([\w-]{11})".*?"publishedTimeText":\{"simpleText":"([^"]+)"\}'
            matches = re.findall(pattern, html)
            dates = {vid: age for vid, age in matches}
            
            # Alternative pattern for different renderers
            alt_pattern = r'"publishedTimeText":\{"simpleText":"([^"]+)"\}.*?"videoId":"([\w-]{11})"'
            alt_matches = re.findall(alt_pattern, html)
            for age, vid in alt_matches:
                if vid not in dates:
                    dates[vid] = age

            for v in results:
                if v["id"] in dates:
                    v["publishedTime"] = dates[v["id"]]
    except Exception as e:
        util.dbg("Enrichment failed for %s: %s", url, e)


def _search_videos_ytdl(query, pages):
    """Search using yt-dlp with optimized flags."""
    count = pages * 50
    ydl_opts = get_ydl_opts({
        "extract_flat": True,
        "allowed_extractors": ["youtube:search", "youtube", "youtube:search_url", "youtube:playlist", "youtube:tab"],
        "lazy_extract": True,
        "cachedir": False,
    })
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch{count}:{query}", download=False)
            results = []
            for entry in info.get("entries", []):
                # Map yt-dlp entry to youtubesearchpython format
                duration = entry.get("duration")
                if duration:
                    h = int(duration // 3600)
                    m = int((duration % 3600) // 60)
                    s = int(duration % 60)
                    if h > 0:
                        duration_str = f"{h}:{m:02d}:{s:02d}"
                    else:
                        duration_str = f"{m}:{s:02d}"
                else:
                    duration_str = "0:00"

                view_count = entry.get("view_count")
                view_count_str = f"{view_count:,} views" if view_count is not None else "?"

                results.append({
                    "type": "video",
                    "id": entry.get("id"),
                    "title": entry.get("title"),
                    "publishedTime": _format_published_time(entry) or "Unknown",
                    "duration": duration_str,
                    "viewCount": {
                        "text": view_count_str,
                        "short": view_count_str
                    },
                    "channel": {
                        "name": entry.get("uploader") or entry.get("channel"),
                        "id": entry.get("uploader_id") or entry.get("channel_id"),
                    },
                    "link": entry.get("url") or f"https://www.youtube.com/watch?v={entry.get('id')}",
                })
            
            # Enrich with relative dates from the search page
            search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            _enrich_results_with_dates(search_url, results)
            
            return results
    except Exception as e:
        util.dbg("yt-dlp search fallback failed: %s", str(e))
        return []


def channel_search(query):
    """Search for channels using yt-dlp."""
    encoded_query = urllib.parse.quote(query)
    # sp=EgIQAg%3D%3D is the filter for channels
    url = f"https://www.youtube.com/results?search_query={encoded_query}&sp=EgIQAg%3D%3D"
    
    ydl_opts = get_ydl_opts({
        "extract_flat": True,
        "allowed_extractors": ["youtube:search", "youtube", "youtube:search_url", "youtube:playlist", "youtube:tab"],
        "lazy_extract": True,
        "cachedir": False,
    })
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            results = []
            for entry in info.get("entries", []):
                description = entry.get("description", "")
                results.append({
                    "type": "channel",
                    "id": entry.get("id"),
                    "title": entry.get("title") or entry.get("channel"),
                    "thumbnails": entry.get("thumbnails"),
                    "videoCount": entry.get("video_count"),
                    "description": description,
                    "descriptionSnippet": [{"text": description}] if description else None,
                    "link": entry.get("url") or f"https://www.youtube.com/channel/{entry.get('id')}",
                })
            return results
    except Exception as e:
        util.dbg("Channel search failed: %s", str(e))
        return []


def playlist_search(query):
    """Search for playlists using yt-dlp for better reliability."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}&sp=EgIQAw%3D%3D"
    
    ydl_opts = get_ydl_opts({
        "extract_flat": True,
        "allowed_extractors": ["youtube:search", "youtube", "youtube:search_url", "youtube:playlist", "youtube:tab"],
        "lazy_extract": True,
        "cachedir": False,
    })
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            results = []
            for entry in info.get("entries", []):
                # Map yt-dlp entry to expected format for get_pl_from_json
                results.append({
                    "type": "playlist",
                    "id": entry.get("id"),
                    "title": entry.get("title"),
                    "videoCount": entry.get("playlist_count") or "?",
                    "channel": {
                        "name": entry.get("uploader"),
                        "id": entry.get("uploader_id"),
                    },
                    "publishedAt": None, # Not usually available in flat extract
                    "description": entry.get("description", ""),
                })
            return results
    except Exception as e:
        raise ExtractionError(f"Playlist search failed: {str(e)}")



def get_playlist(playlist_id):
    """Get all videos of a playlist using yt-dlp."""
    url = f"https://www.youtube.com/playlist?list={playlist_id}"
    ydl_opts = get_ydl_opts({
        "extract_flat": True,
        "allowed_extractors": ["youtube:search", "youtube", "youtube:search_url", "youtube:playlist", "youtube:tab"],
        "lazy_extract": True,
        "cachedir": False,
    })
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Create a mock object that looks like youtubesearchpython.Playlist
            class MockPlaylist:
                def __init__(self, info):
                    self.videos = []
                    self.info = {"info": {"title": info.get("title", "Unknown Playlist")}}
                    for entry in info.get("entries", []):
                        duration = entry.get("duration")
                        if duration:
                            m, s = divmod(int(duration), 60)
                            h, m = divmod(m, 60)
                            duration_str = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
                        else:
                            duration_str = "0:00"

                        self.videos.append({
                            "id": entry.get("id"),
                            "title": entry.get("title"),
                            "duration": duration_str,
                            "channel": {
                                "name": entry.get("uploader") or entry.get("channel"),
                                "id": entry.get("uploader_id") or entry.get("channel_id"),
                            },
                            "link": f"https://www.youtube.com/watch?v={entry.get('id')}",
                        })
            
            return MockPlaylist(info)
    except Exception as e:
        util.dbg("Failed to get playlist %s: %s", playlist_id, str(e))
        raise ExtractionError(f"Playlist extraction failed: {str(e)}")


def get_video_title_suggestions(query):
    """Get search suggestions using direct Google API call in English."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&hl=en&q={encoded_query}"
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.5"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if not isinstance(data, list) or len(data) < 2 or not data[1]:
                return query
            return random.choice(data[1])
    except Exception:
        return query


def channel_id_from_name(query):
    """Resolve channel ID and name from query."""
    results = channel_search(query)
    if not results:
        return None, None
    channel_info = results[0]
    return channel_info["id"], channel_info["title"]


def all_videos_from_channel(channel_id):
    """Get all videos from a channel using yt-dlp."""
    url = f"https://www.youtube.com/channel/{channel_id}/videos"
    ydl_opts = get_ydl_opts({
        "extract_flat": True,
        "allowed_extractors": ["youtube:search", "youtube", "youtube:search_url", "youtube:playlist", "youtube:tab"],
        "lazy_extract": True,
        "cachedir": False,
    })
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            videos = []
            channel_name = info.get("title") or info.get("uploader")
            for entry in info.get("entries", []):
                duration = entry.get("duration")
                if duration:
                    m, s = divmod(int(duration), 60)
                    h, m = divmod(m, 60)
                    duration_str = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
                else:
                    duration_str = "0:00"

                videos.append({
                    "id": entry.get("id"),
                    "title": entry.get("title"),
                    "description": entry.get("description", ""),
                    "publishedTime": _format_published_time(entry) or "Unknown",
                    "duration": duration_str,
                    "channel": {
                        "name": entry.get("uploader") or entry.get("channel") or channel_name,
                        "id": entry.get("uploader_id") or entry.get("channel_id") or channel_id,
                    },
                    "link": f"https://www.youtube.com/watch?v={entry.get('id')}",
                })
            
            # Enrich with relative dates from the videos tab
            _enrich_results_with_dates(url, videos)
            
            return videos
    except Exception as e:
        util.dbg("Failed to get channel videos for %s: %s", channel_id, str(e))
        return []


def search_videos_from_channel(channel_id, query):
    """Search videos within a specific channel."""
    # This can be done by adding a query string to the channel URL or via search filters
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/channel/{channel_id}/search?query={encoded_query}"
    # Fallback to search if specific channel search fails in flat extract
    return _search_videos_ytdl(f"{query} channel:{channel_id}", 1)


def get_comments(video_id):
    """Get video comments using yt-dlp."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = get_ydl_opts({"getcomments": True, "extract_flat": False})
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            comments = []
            for comment in info.get("comments", []):
                comments.append({
                    "id": comment.get("id"),
                    "author": comment.get("author"),
                    "authorId": comment.get("author_id"),
                    "content": comment.get("text"),
                    "publishedAt": comment.get("timestamp"),
                    "votes": comment.get("like_count"),
                })
            return comments
    except Exception as e:
        util.dbg("Failed to get comments for %s: %s", video_id, str(e))
        return []


import concurrent.futures

def get_video_info(video_id):
    """Get detailed video info including likes/dislikes in parallel."""
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Start dislike fetch in background
            dislike_future = executor.submit(return_dislikes, video_id)

            # Extract info via yt-dlp (main task)
            ydl_opts = get_ydl_opts()
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_id, download=False)

            # Wait for dislikes and merge
            dislikes = dislike_future.result()
            info["likes"] = dislikes["likes"]
            info["dislikes"] = dislikes["dislikes"]
            info["averageRating"] = dislikes["rating"]
            return VideoInfo(info)
    except Exception as e:
        raise ExtractionError(f"Can't get video info: {str(e)}")


def return_dislikes(video_id):
    """Fetch dislike counts from Return YouTube Dislike API."""
    url = f"https://returnyoutubedislikeapi.com/votes?videoId={video_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return {
                "likes": data.get("likes", 0),
                "dislikes": data.get("dislikes", 0),
                "rating": data.get("rating", 0),
            }
    except Exception:
        return {"likes": 0, "dislikes": 0, "rating": 0}


def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    idregx = re.compile(r"[\w-]{11}$")
    url = str(url).strip()

    if idregx.match(url):
        return url

    if "://" not in url:
        url = "//" + url
    parsedurl = urlparse(url)
    if parsedurl.netloc in (
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "gaming.youtube.com",
    ):
        query = parse_qs(parsedurl.query)
        if "v" in query and idregx.match(query["v"][0]):
            return query["v"][0]
    elif parsedurl.netloc in ("youtu.be", "www.youtu.be"):
        vidid = parsedurl.path.split("/")[-1] if parsedurl.path else ""
        if idregx.match(vidid):
            return vidid

    raise ValueError(f"Could not extract video ID from {url}")


def all_playlists_from_channel(channel_id):
    """Get all playlists belonging to a channel using yt-dlp."""
    url = f"https://www.youtube.com/channel/{channel_id}/playlists"
    ydl_opts = get_ydl_opts({
        "extract_flat": True,
        "allowed_extractors": ["youtube:search", "youtube", "youtube:search_url", "youtube:playlist", "youtube:tab"],
        "lazy_extract": True,
        "cachedir": False,
    })
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            playlists = []
            for entry in info.get("entries", []):
                playlists.append({
                    "id": entry.get("id"),
                    "title": entry.get("title"),
                    "videoCount": entry.get("playlist_count") or "?",
                    "channel": {
                        "name": entry.get("uploader") or entry.get("channel"),
                        "id": entry.get("uploader_id") or entry.get("channel_id"),
                    },
                    "description": entry.get("description", ""),
                })
            return playlists
    except Exception as e:
        util.dbg("Failed to get channel playlists for %s: %s", channel_id, str(e))
        return []


def get_subtitles(ytid, output_dir):
    """Download and save subtitles for a video."""
    if output_dir.endswith("/"):
        output_dir = output_dir[:-1]
    outtmpl = f"{output_dir}/subtitles/{ytid}"

    existing_subtitles = glob.glob(os.path.join(outtmpl + "*.vtt"))
    if existing_subtitles:
        return existing_subtitles[0]

    url = f"https://www.youtube.com/watch?v={ytid}"
    ydl_opts = get_ydl_opts({
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        "outtmpl": outtmpl,
    })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            subtitles = info_dict.get("subtitles", {})
            available_formats = list(subtitles.keys())
            lang = available_formats[0] if available_formats else "en"
            ydl.params["subtitleslangs"] = [lang]
            ydl.download([url])
            path = f"{outtmpl}.{lang}.vtt"
            return path if os.path.isfile(path) else None
    except Exception:
        return None
