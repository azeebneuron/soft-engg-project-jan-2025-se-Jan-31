import os
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def extract_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    parsed_url = urlparse(youtube_url)
    
    if parsed_url.hostname in ('youtu.be',):
        return parsed_url.path[1:]
    
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        if parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        if parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    
    # If we get here, it's not a valid YouTube URL
    return None

def get_video_details(video_id):
    """Get video title and other metadata using YouTube API."""
    api_key = os.getenv('YOUTUBE_API_KEY')
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    
    response = requests.get(url)
    data = response.json()
    
    if not data.get('items'):
        return None
    
    snippet = data['items'][0]['snippet']
    return {
        'title': snippet.get('title'),
        'description': snippet.get('description'),
        'channel': snippet.get('channelTitle'),
        'published_at': snippet.get('publishedAt')
    }

def get_video_transcript(video_id):
    """Get the transcript of a YouTube video."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all transcript segments into a single text
        full_transcript = ""
        for segment in transcript_list:
            full_transcript += segment['text'] + " "
        
        return full_transcript.strip()
    
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None

def get_playlist_videos(playlist_id):
    """Get all videos from a YouTube playlist."""
    api_key = os.getenv('YOUTUBE_API_KEY')
    videos = []
    next_page_token = None
    
    while True:
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={playlist_id}&key={api_key}"
        
        if next_page_token:
            url += f"&pageToken={next_page_token}"
        
        response = requests.get(url)
        data = response.json()
        
        for item in data.get('items', []):
            snippet = item['snippet']
            video_id = snippet['resourceId']['videoId']
            videos.append({
                'video_id': video_id,
                'title': snippet.get('title'),
                'description': snippet.get('description', ''),
                'thumbnail': snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
                'position': snippet.get('position', 0)
            })
        
        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break
    
    return videos

def extract_playlist_id(playlist_url):
    """Extract playlist ID from a YouTube playlist URL."""
    parsed_url = urlparse(playlist_url)
    
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if 'list=' in parsed_url.query:
            return parse_qs(parsed_url.query)['list'][0]
    
    return None