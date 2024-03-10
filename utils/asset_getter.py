import requests
import json
## getting asset from GCS

# 1. get image directory name from api service
# 2. get image from GCS

GCS_STORAGE_URL = 'https://storage.googleapis.com'
GCS_BUCKET_NAME = 'granfondo-photos'

def read_config():
    with open('config/apiserver_connection.json', 'r') as f:
        return json.load(f)

def reqeustAssetInfo(protocol, server_url, port, endpoint, photoId):
    full_url = f'{protocol}://{server_url}:{port}/{endpoint}/{photoId}'
    response = requests.get(full_url)
    print('full_url:', full_url)
    print('response:', response)
    return response.json()

def requestAessetFromGCS(dirPath, photoId):
    full_url = f'{GCS_STORAGE_URL}/{GCS_BUCKET_NAME}/{dirPath}/{photoId}'
    print('full_url:', full_url)
    response = requests.get(full_url)
    if response.status_code != 200:
        print(f"Failed to get asset from GCS. {response.status_code}")
        return None
    return response.content

def get_asset(photoId):
    api_config = read_config()
    asset_info = reqeustAssetInfo(api_config["gfps"]["protocol"], api_config["gfps"]["host"], api_config["gfps"]["port"], api_config["endpoints"]["photo"], photoId)
    asset = requestAessetFromGCS(asset_info["competition"], photoId)
    return asset