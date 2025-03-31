import os
from pymongo import MongoClient
import json
import os.path

class LectureStore:
    """Store and retrieve lecture data including transcripts."""
    
    def __init__(self, use_mongo=False):
        """Initialize the lecture store."""
        self.use_mongo = use_mongo
        
        if use_mongo:
            # MongoDB storage
            mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
            db_name = os.getenv('DB_NAME', 'virtual_ta_db')
            
            self.client = MongoClient(mongo_uri)
            self.db = self.client[db_name]
            self.lectures = self.db.lectures
            self.playlists = self.db.playlists
        else:
            # File-based storage
            os.makedirs('data', exist_ok=True)
            self.lectures_file = 'data/lectures.json'
            self.playlists_file = 'data/playlists.json'
            
            # Initialize empty storage files if they don't exist
            if not os.path.exists(self.lectures_file):
                with open(self.lectures_file, 'w') as f:
                    json.dump({}, f)
            
            if not os.path.exists(self.playlists_file):
                with open(self.playlists_file, 'w') as f:
                    json.dump([], f)
    
    def save_lecture(self, video_id, title, transcript):
        """Save a lecture and its transcript."""
        lecture_data = {
            'video_id': video_id,
            'title': title,
            'transcript': transcript
        }
        
        if self.use_mongo:
            # MongoDB storage
            self.lectures.update_one(
                {'video_id': video_id},
                {'$set': lecture_data},
                upsert=True
            )
        else:
            # File-based storage
            with open(self.lectures_file, 'r') as f:
                lectures = json.load(f)
            
            lectures[video_id] = lecture_data
            
            with open(self.lectures_file, 'w') as f:
                json.dump(lectures, f)
        
        return True
    
    def get_lecture(self, video_id):
        """Get a lecture by its video ID."""
        if self.use_mongo:
            # MongoDB storage
            lecture = self.lectures.find_one({'video_id': video_id})

            return lecture
        else:
            # File-based storage
            with open(self.lectures_file, 'r') as f:
                lectures = json.load(f)

            return lectures.get(video_id)
    
    def save_playlist(self, playlist_id, playlist_data):
        """Save a playlist and its videos."""
        if self.use_mongo:
            # MongoDB storage
            self.playlists.update_one(
                {'playlist_id': playlist_id},
                {'$set': {
                    'playlist_id': playlist_id,
                    'videos': playlist_data
                }},
                upsert=True
            )
        else:
            # File-based storage
            with open(self.playlists_file, 'r') as f:
                playlists = json.load(f)
            
            # Check if playlist already exists
            playlist_exists = False
            for i, playlist in enumerate(playlists):
                if playlist.get('playlist_id') == playlist_id:
                    playlists[i] = {'playlist_id': playlist_id, 'videos': playlist_data}
                    playlist_exists = True
                    break
            
            # Add new playlist if it doesn't exist
            if not playlist_exists:
                playlists.append({'playlist_id': playlist_id, 'videos': playlist_data})
            
            with open(self.playlists_file, 'w') as f:
                json.dump(playlists, f)
        
        return True
    
    def get_playlist(self, playlist_id):
        """Get a playlist by its ID."""
        if self.use_mongo:
            # MongoDB storage
            playlist = self.playlists.find_one({'playlist_id': playlist_id})
            return playlist.get('videos') if playlist else []
        else:
            # File-based storage
            with open(self.playlists_file, 'r') as f:
                playlists = json.load(f)
            
            for playlist in playlists:
                if playlist.get('playlist_id') == playlist_id:
                    return playlist.get('videos', [])
            
            return []
    
    def get_all_playlists(self):
        """Get all stored playlists."""
        if self.use_mongo:
            # MongoDB storage
            return list(self.playlists.find({}, {'_id': 0}))
        else:
            # File-based storage
            with open(self.playlists_file, 'r') as f:
                return json.load(f)
    
    def has_lecture(self, video_id):
        """Check if a lecture exists in the store."""
        if self.use_mongo:
            # MongoDB storage
            return self.lectures.count_documents({'video_id': video_id}) > 0
        else:
            # File-based storage
            with open(self.lectures_file, 'r') as f:
                lectures = json.load(f)
            
            return video_id in lectures