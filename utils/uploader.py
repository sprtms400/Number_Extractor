# # GCS에 이미지 업로딩

import json
import requests
import utils.asset_getter

def read_config():
    with open('config/apiserver_connection.json', 'r') as f:
        return json.load(f)

def getPresignedUrl(tmp_dir, photoId, assetName):
    api_config = read_config()
    protocol = api_config["gfps"]["protocol"]
    server_url = api_config["gfps"]["host"]
    port = api_config["gfps"]["port"]
    endpoint_forInfo = api_config["endpoints"]["photo"]
    endpoint_forPresigned = api_config["endpoints"]["getPresignedURL"]
    
    asset_info = utils.asset_getter.reqeustAssetInfo(protocol, server_url, port, endpoint_forInfo, photoId)
    competition = asset_info["competition"]
    data = {
        "accessUserId": "demo",
        "password": "741852963",
        "assetName": f'{competition}/{photoId}-{assetName}',
    }
    full_url = f'{protocol}://{server_url}:{port}/{endpoint_forPresigned}'
    presind_url = None
    response = requests.post(full_url, json=data)
    if response.status_code != 200:
        print(f"Failed to get presigned URL. {response.status_code}")
        presind_url = None
    else :
        print('response.json():', response.json())
        presind_url = response.json()
    return presind_url

def uploadWithPresignedUrl(presignedUrl, Image):
    response = requests.put(presignedUrl, data=Image, headers={'Content-Type': 'application/octet-stream'})
    if response.status_code != 200:
        print(f"Failed to upload image. {response.status_code}")
    return response

    # 'isNumberPlateDetected': True,
    # 'numberPlate': result_norm_text,
    # 'probability': result_norm_prob,
def updateNumberPlate(isNumberPlateDetected, numberPlate, probability, photoId): 
    api_config = read_config()
    protocol = api_config["gfps"]["protocol"]
    server_url = api_config["gfps"]["host"]
    port = api_config["gfps"]["port"]
    full_url = f'{protocol}://{server_url}:{port}/photo/{photoId}/numberPlate'
    numberplate = {
        "accessUserId": "demo",
        "isNumberPlateDetected": isNumberPlateDetected,
        "numberPlate": numberPlate,
        "probability": probability,
    }
    data = {
        "numberplate": numberplate,
    }
    print('full_url:', full_url)
    print('data:', data)
    
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(full_url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Failed to update numberplate. {response.status_code}")
    return response

def uploadProcessedImages(tmp_dir, photoId, target_files):
    for target_file in target_files:
        assetName = target_file.split('/')[-1]
        presignedUrl = getPresignedUrl(tmp_dir, photoId, assetName)
        
        print('target_file:', target_file)
        print('asssetName:', assetName)
        print('presignedUrl:', presignedUrl)
        
        with open(tmp_dir + target_file, 'rb') as f:
            Image = f.read()
            uploadWithPresignedUrl(presignedUrl, Image)
        
def checkNumberPlateAnalyzed(photoId):
    api_config = read_config()
    protocol = api_config["gfps"]["protocol"]
    server_url = api_config["gfps"]["host"]
    port = api_config["gfps"]["port"]
    
    full_url = f'{protocol}://{server_url}:{port}/photo/{photoId}/checkNumberPlateAnalyzed'
    response = requests.patch(full_url)
    if response.status_code != 200:
        print(f"Failed to check analyzed. {response.status_code}")
    return response