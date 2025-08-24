# File: modules/wordpress_publisher.py

import os
import requests
import json
import base64
import re
from dotenv import load_dotenv

load_dotenv()

def get_wp_config():
    """Reads WordPress configuration from environment variables."""
    # ... (This function remains unchanged)
    WP_URL = os.getenv("WP_URL")
    WP_USER = os.getenv("WP_USER")
    WP_APP_PASSWORD = os.getenv("WP_PASSWORD") or os.getenv("WP_APP_PASSWORD")
    if not all([WP_URL, WP_USER, WP_APP_PASSWORD]):
        raise ValueError("WordPress credentials are not set in the environment.")
    api_base = f"{WP_URL}/wp-json/wp/v2"
    credentials = f"{WP_USER}:{WP_APP_PASSWORD}"
    token = base64.b64encode(credentials.encode())
    headers = {'Authorization': f'Basic {token.decode("utf-8")}'}
    return api_base, headers

# --- MODIFIED: This function now takes a URL ---
def upload_image_to_wordpress(image_url: str, article_title: str) -> int | None:
    """
    Downloads an image from a URL and uploads it to the WordPress Media Library.
    """
    if not image_url:
        print("   [WP] Image URL not provided. Skipping image upload.")
        return None

    try:
        api_base, headers = get_wp_config()
        media_url = f"{api_base}/media"

        # Download the image data from the provided URL
        print(f"   [WP] Downloading image from {image_url}...")
        image_response = requests.get(image_url, verify=False, timeout=60)
        image_response.raise_for_status()
        image_data = image_response.content

        # Create a safe filename from the article title
        safe_title = re.sub(r'[^a-zA-Z0-9_-]', '', article_title.replace(' ', '-')).lower()
        filename = f"{safe_title}.png"

        # Set headers for the file upload
        file_headers = headers.copy()
        file_headers['Content-Disposition'] = f'attachment; filename={filename}'
        file_headers['Content-Type'] = 'image/png'

        print(f"   [WP] Uploading {filename} to WordPress Media Library...")
        upload_response = requests.post(media_url, headers=file_headers, data=image_data, timeout=60, verify=False)
        upload_response.raise_for_status()

        media_id = upload_response.json()['id']
        print(f"   [WP] Image uploaded successfully. Media ID: {media_id}")
        return media_id

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"   [WP] Error handling image for WordPress: {e}")
        return None

def create_wordpress_post(title: str, content: str, status: str, featured_media_id: int | None) -> bool:
    """Creates a new post in WordPress."""
    # ... (This function remains unchanged)
    try:
        api_base, headers = get_wp_config()
        posts_url = f"{api_base}/posts"
        payload = {'title': title, 'content': content, 'status': status}
        if featured_media_id:
            payload['featured_media'] = featured_media_id
        print(f"   [WP] Creating post '{title}' as a '{status}'...")
        response = requests.post(posts_url, headers=headers, json=payload, timeout=60, verify=False)
        response.raise_for_status()
        if response.text:
            post_id = response.json().get('id', 'N/A')
            print(f"   [WP] Successfully created post. Post ID: {post_id}")
            return True
        else:
            print("[WP] Error: Post was created but response was empty.")
            return False
    except (requests.exceptions.RequestException, ValueError, json.JSONDecodeError) as e:
        error_message = str(e)
        if isinstance(e, json.JSONDecodeError):
            error_message = "Expecting JSON but got empty or invalid response from server."
        print(f"   [WP] Error creating post in WordPress: {error_message}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   [WP] Response Body: {e.response.text if e.response.text else 'No Response'}")
        return False