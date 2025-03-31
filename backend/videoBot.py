from flask import request, jsonify
from flask_restful import Resource
import json
from utils.youtube_utils import (
    extract_video_id, 
    get_video_details, 
    get_video_transcript,
    get_playlist_videos,
    extract_playlist_id
)
from utils.gemini_utils import (
    initialize_gemini, 
    create_lecture_context, 
    get_gemini_response
)
from utils.lecture_store import LectureStore

# Initialize Gemini model
model_name = initialize_gemini()

# Initialize lecture store
lecture_store = LectureStore(use_mongo=False)

# Pre-defined playlists for demo purposes
SAMPLE_PLAYLISTS = [
    {
        "title": "Introduction to Machine Learning",
        "playlist_id": "PLLssT5z_DsK-h9vYZkQkYNWcItqhlRJLN",
        "description": "A beginner-friendly course on machine learning fundamentals by Andrew Ng."
    },
    {
        "title": "Python for Beginners",
        "playlist_id": "PLlrxD0HtieHhS8VzuMCfQD4uJ9yne1mE6", 
        "description": "Learn Python from scratch with hands-on examples by Microsoft."
    },
    {
        "title": "Data Structures and Algorithms",
        "playlist_id": "PLu0W_9lII9ahIappRPN0MCAgtOu3lQjQi",
        "description": "Deep dive into complex data structures and algorithms by CodeWithHarry."
    }
]

class ProcessLecture(Resource):
    def post(self):
        """Process a lecture URL and retrieve its transcript."""
        data = request.json
        youtube_url = data.get('youtube_url')
        video_id = data.get('video_id')  # Added support for direct video_id
        
        if not youtube_url and not video_id:
            return {"error": "No YouTube URL or video ID provided"}, 400
        
        if youtube_url:
            video_id = extract_video_id(youtube_url)
            
            if not video_id:
                return {"error": "Invalid YouTube URL"}, 400
        
        # Check if lecture is already in the store
        if lecture_store.has_lecture(video_id):
            lecture = lecture_store.get_lecture(video_id)
            return {
                "video_id": video_id,
                "title": lecture['title'],
                "transcript": lecture['transcript'][:500] + "...",  # Send preview only
                "status": "success",
                "message": "Lecture loaded from storage"
            }
        
        # Get video details from YouTube API
        video_details = get_video_details(video_id)
        
        if not video_details:
            return {"error": "Could not retrieve video details"}, 404
        
        # Get video transcript
        transcript = get_video_transcript(video_id)
        
        if not transcript:
            return {"error": "Could not retrieve video transcript"}, 404
        
        # Save lecture to store
        lecture_store.save_lecture(video_id, video_details['title'], transcript)
        
        return {
            "video_id": video_id,
            "title": video_details['title'],
            "transcript": transcript[:500] + "...",  # Send preview only
            "status": "success"
        }

class VideoChatbot(Resource):
    def post(self):
        """Get a response from the Virtual TA based on a student's question."""
        data = request.json
        video_id = data.get('video_id')
        question = data.get('question')
        
        if not video_id or not question:
            return {"error": "Video ID and question are required"}, 400
        
        # Get lecture from store
        lecture = lecture_store.get_lecture(video_id)
        
        if not lecture:
            # If lecture is not found, try to fetch and process it first
            # Get video details from YouTube API
            video_details = get_video_details(video_id)
            
            if not video_details:
                return {"error": "Lecture not found and could not retrieve video details"}, 404
            
            # Get video transcript
            transcript = get_video_transcript(video_id)
            
            if not transcript:
                return {"error": "Lecture not found and could not retrieve video transcript"}, 404
            
            # Save lecture to store
            lecture_store.save_lecture(video_id, video_details['title'], transcript)
            lecture = {
                'video_id': video_id,
                'title': video_details['title'],
                'transcript': transcript
            }
        
        # Create context for Gemini
        context = create_lecture_context(lecture['title'], lecture['transcript'])
        
        # Get response from Gemini
        response = get_gemini_response(model_name, question, context)
        
        return {
            "response": response,
            "status": "success"
        }

class ProcessPlaylist(Resource):
    def post(self):
        """Process a YouTube playlist and retrieve all video details."""
        data = request.json
        playlist_url = data.get('playlist_url')
        
        if not playlist_url:
            return {"error": "No playlist URL provided"}, 400
        
        playlist_id = extract_playlist_id(playlist_url)
        
        if not playlist_id:
            return {"error": "Invalid playlist URL"}, 400
        
        # Get videos from playlist
        videos = get_playlist_videos(playlist_id)
        
        if not videos:
            return {"error": "Could not retrieve playlist videos"}, 404
        
        # Save playlist to store
        lecture_store.save_playlist(playlist_id, videos)
        
        return {
            "playlist_id": playlist_id,
            "videos": videos,
            "status": "success"
        }

class GetPlaylistDetails(Resource):
    def get(self, playlist_id):
        """Get details of a stored playlist."""
        videos = lecture_store.get_playlist(playlist_id)
        
        if not videos:
            # Try to fetch videos from YouTube if not in storage
            try:
                videos = get_playlist_videos(playlist_id)
                if videos:
                    # Save playlist to store
                    lecture_store.save_playlist(playlist_id, videos)
                    return {
                        "playlist_id": playlist_id,
                        "videos": videos,
                        "status": "success"
                    }
                else:
                    return {"error": "Could not fetch playlist videos from YouTube"}, 404
            except Exception as e:
                return {"error": f"Playlist not found and could not fetch from YouTube: {str(e)}"}, 404
        
        return {
            "playlist_id": playlist_id,
            "videos": videos,
            "status": "success"
        }

class GetAllPlaylists(Resource):
    def get(self):
        """Get all stored playlists."""
        playlists = lecture_store.get_all_playlists()
        
        if not playlists:
            # Return sample playlists if no playlists are stored
            return {
                "playlists": SAMPLE_PLAYLISTS,
                "status": "success",
                "note": "Sample playlists returned (no user playlists found)"
            }
        
        return {
            "playlists": playlists,
            "status": "success"
        }