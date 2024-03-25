#%% 

import json
import requests
import time

def read_config():
    with open('../config/apiserver_connection.json', 'r') as f:
        return json.load(f)

def reqeustAssetInfos(protocol, server_url, port, endpoint):
    full_url = f'{protocol}://{server_url}:{port}/{endpoint}'
    response = requests.get(full_url)
    print('full_url:', full_url)
    print('response:', response)
    response_parse = response.json()
    print('len(response_parse):', len(response_parse))
    print('type(response_parse : ', type(response_parse))
    print('response_parse[0]:', response_parse[0])
    return response_parse

def get_asset_infos():
    api_config = read_config()
    asset_info = reqeustAssetInfos(api_config["gfps"]["protocol"], api_config["gfps"]["host"], api_config["gfps"]["port"], 'photos')
    return asset_info

def uploadNumberplate(photoId, numberplate):
    api_config = read_config()
    protocol = api_config["gfps"]["protocol"]
    server_url = api_config["gfps"]["host"]
    port = api_config["gfps"]["port"]
    full_url = f'{protocol}://{server_url}:{port}/photo/{photoId}/uploadNubmerplate'
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "numberplate": numberplate
    }
    response = requests.post(full_url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Failed to upload appearance. {response.status_code}")
        print(response.content)
    return response

photos = get_asset_infos()
i = 0
j = 0
k = 0
lenof_total_photos = len(photos)

for photo in photos:
    number_plate_infos = photo['numberPlate']
    if len(number_plate_infos) == 0:
        print(f'photoId: {photo["photoId"]} does not have number plate')
        continue
    elif len(number_plate_infos) > 1:
        print(f'photoId: {photo["photoId"]} has more than one number plate')
        i += 1
        for number_plate_info in number_plate_infos:
            if number_plate_info["numberPlate"] is not "unknown":
                j = 0

print(f'total number of photos: {lenof_total_photos}')
print(f'The number of photos who has valid values: {i}')
print(f'The number of system have to vecterized.: {j}')

for photo in photos:
    number_plate_infos = photo['numberPlate']
    if len(number_plate_infos) == 0:
        print(f'photoId: {photo["photoId"]} does not have number plate')
        continue
    elif len(number_plate_infos) > 1:
        print(f'photoId: {photo["photoId"]} has more than one number plate')
        for number_plate_info in number_plate_infos:
            if number_plate_info["numberPlate"] != "unknown":
                print(f'{k}: photoId: {photo["photoId"]}, numberPlate: {number_plate_info["numberPlate"]}')
                response = uploadNumberplate(photo['photoId'], number_plate_info["numberPlate"])
                parsed_response = response.json()
                print(parsed_response)
                k += 1
                
print(f'total number of photos: {lenof_total_photos}')
print(f'The number of photos who has valid values: {i}')
print(f'The number of system have to vecterized.: {j}')