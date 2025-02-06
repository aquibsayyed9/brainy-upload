import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    """Handles YouTube API authentication using environment variables"""
    try:
        # Get credentials from environment variables
        refresh_token = os.environ.get('YOUTUBE_REFRESH_TOKEN')
        client_id = os.environ.get('YOUTUBE_CLIENT_ID')
        client_secret = os.environ.get('YOUTUBE_CLIENT_SECRET')

        if not all([refresh_token, client_id, client_secret]):
            raise ValueError("Missing required YouTube credentials in environment variables")

        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES
        )
        
        return build('youtube', 'v3', credentials=creds)
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        raise

def upload_to_youtube(video_file, title, description, tags, privacy="private"):
    """Uploads video to YouTube and deletes the local file after successful upload."""
    try:
        youtube = get_authenticated_service()

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(
            video_file,
            mimetype="video/mp4",
            resumable=True
        )

        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media
        )

        print(f"Starting upload of {video_file}...")
        response = request.execute()
        
        video_id = response.get('id')
        if video_id:
            print(f"Upload successful! Video ID: {video_id}")
            print(f"Video URL: https://youtu.be/{video_id}")
            
            # Delete the local file after successful upload
            if os.path.exists(video_file):
                os.remove(video_file)
                print(f"Deleted local video file: {video_file}")
            
            return True
        
        return False

    except Exception as e:
        print(f"Upload error: {str(e)}")
        return False