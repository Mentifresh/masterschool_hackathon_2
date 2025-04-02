import os
import requests
from pathlib import Path

class DataManager:
    def __init__(self, img_dir="img"):
        """Initialize the DataManager with a directory for storing media"""
        self.img_dir = Path(img_dir)
        self.img_dir.mkdir(exist_ok=True)
    
    def save_media_to_img_folder(self, service_sid, media_sid, api_key, api_secret, content_type='image/jpeg'):
        """Download media from Twilio and save it to the img folder"""
        try:
            # Check if we've already downloaded this media
            extension = content_type.split('/')[-1] if '/' in content_type else 'bin'
            if extension == 'jpeg':
                extension = 'jpg'
            
            # Generate filename based on media_sid
            filename = f"media_{media_sid}.{extension}"
            filepath = self.img_dir / filename
            
            # Check if file already exists
            if filepath.exists():
                print(f"✅ Media already exists: {filepath}")
                return str(filepath)
            
            # Construct the media content URL
            media_content_url = f"https://mcs.us1.twilio.com/v1/Services/{service_sid}/Media/{media_sid}/Content"
            
            print(f"... Downloading media from: {media_content_url}")
            
            # Set up authentication
            auth = (api_key, api_secret)
            
            # Make the request with proper authentication
            response = requests.get(
                media_content_url, 
                auth=auth,
                headers={
                    'Accept': content_type,
                }
            )
            
            if response.status_code == 200:
                # Save the file
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                # Check file size to ensure we got actual content
                file_size = os.path.getsize(filepath)
                print(f"✅ Media saved to: {filepath} ({file_size} bytes)")
                
                return str(filepath)
            else:
                print(f"❌ Failed to download media: {response.status_code}")
                
                # Try alternate URL format as fallback
                alt_url = f"https://api.twilio.com/2010-04-01/Accounts/{api_key}/Messages/{media_sid}/Media/Content"
                print(f"🔄 Trying alternate URL: {alt_url}")
                
                alt_response = requests.get(alt_url, auth=auth)
                if alt_response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(alt_response.content)
                    print(f"✅ Media saved to: {filepath}")
                    return str(filepath)
                else:
                    print(f"❌ Alternate method also failed: {alt_response.status_code}")
                
                return None
        except Exception as e:
            print(f"❌ Error downloading media: {str(e)}")
            return None 