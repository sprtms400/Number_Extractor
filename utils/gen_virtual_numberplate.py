# #%%
# from PIL import Image, ImageDraw, ImageFont

# # 문자열 설정
# text = "안녕하세요!"

# # 이미지 생성: 배경은 흰색, 충분히 큰 크기 선택
# image = Image.new('RGB', (200, 50), color = (255, 255, 255))

# # 폰트 설정: 같은 디렉토리에 있는 'GothicA1-Bold.ttf' 파일 참조
# font = ImageFont.truetype("GothicA1-Bold.ttf", 24)

# # 드로잉 객체 생성 및 텍스트 그리기
# d = ImageDraw.Draw(image)
# d.text((10,10), text, fill=(0,0,0), font=font)

# # 이미지 저장 또는 보기
# image.save('text_image.png')
# # image.show() # 바로 보고 싶을 경우


#%%
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import requests
import json

def get_photoInfos():
    response = requests.get('http://localhost:3000/photos')
    response_date =response.json()
    return response_date

# 유효한 데이터만 추출
def extract_available_info(photo_list):
    hasNumberPhotos = []
    for photo in photo_list:
        # print('photo["numberPlate"]:', photo["numberPlate"])
        if len(photo["numberPlate"]) > 1:
            hasNumberPhotos.append(photo)
    return hasNumberPhotos

# 텍스트 길이가 4개 이상인 항목을 추출
# def extract_morethan4_info(photo_list):
#     morethan4Photos = []
#     for photo in photo_list:
#         if(len(photo['numberPlate']) > 1):
#             # 유효 데이터가 있으면 배열이 2 이상
#             if(len(photo['numberPlate'][1]['numberPlate']) > 4 and photo['numberPlate'][1]['numberPlate'] != 'unknown'):
#                 morethan4Photos.append(photo['numberPlate'][1]['numberPlate'])
#             if(len(photo['numberPlate'][2]['numberPlate']) > 4 and photo['numberPlate'][2]['numberPlate'] != 'unknown'):
#                 morethan4Photos.append(photo['numberPlate'][2]['numberPlate'])
            
#     return morethan4Photos
def extract_morethan4_info(photo_list):
    morethan4Photos = []
    for photo in photo_list:
        # 첫 번째 numberPlate 검사
        if(len(photo['numberPlate']) > 1):
            # 유효 데이터가 있으면 배열이 2 이상
            if(photo['numberPlate'][1]['numberPlate'] != 'unknown'):
                if(len(photo['numberPlate'][1]['numberPlate']) > 4):
                    morethan4Photos.append(photo['numberPlate'][1]['numberPlate'])
            if(photo['numberPlate'][2]['numberPlate'] != 'unknown'):
                if(len(photo['numberPlate'][2]['numberPlate']) > 4):
                    morethan4Photos.append(photo['numberPlate'][2]['numberPlate'])
            
    return morethan4Photos

# 텍스트 길이를 일관화 하기위해 길이가 긴 텍스트에 대해 폰트 사이즈를 조절
def calcul_fontsize(plate_width, plate_height, fnt_size, text):
    # 초기 폰트 사이즈 설정
    fnt = ImageFont.truetype("GothicA1-Bold.ttf", fnt_size)
    
    # 임시 이미지 생성하여 텍스트 너비 측정
    im = Image.new("RGBA", (plate_width, plate_height), "WHITE")
    draw = ImageDraw.Draw(im)
    
    # 'WWWW'는 4개 문자의 너비를 대표
    target_w = draw.textlength('1111', font=fnt)
    
    # 현재 텍스트의 너비가 목표 너비에 도달할 때까지 폰트 사이즈 조절
    new_fnt_size = 1
    while True:
        fnt = ImageFont.truetype("GothicA1-Bold.ttf", new_fnt_size)
        w = draw.textlength(text, font=fnt)
        
        # 현재 텍스트 너비가 목표 너비보다 크거나 같으면 중단
        if w >= target_w:
            break
        
        # 폰트 사이즈 증가
        new_fnt_size += 1
    
    return new_fnt_size

# 길이가 긴 텍스트는 폰트가 작아 높이차이가 있으므로 텍스트의 높이 차이 비율 계산하는 함수
def calc_text_height_ratio_diff(plate_width, plate_height, fnt_size, text):
    W = plate_width
    H = plate_height
    image = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("GothicA1-Bold.ttf", fnt_size)

    draw.text((0, 0), "1111", font=font)
    bbox = draw.textbbox((0, 0), "1111", font=font)
    draw.rectangle(bbox, outline="red")
    bbox_height = bbox[3] - bbox[1]

    print("bbox:", bbox)
    print("bbox height:", bbox_height)
    # image.show()
    
    # 높이 차이 비율을 반환하는 로직
    target_image = Image.new("RGB", (W, H))
    tartget_fnt_size = calcul_fontsize(W, H, fnt_size, text)
    target_draw = ImageDraw.Draw(target_image)
    font = ImageFont.truetype("GothicA1-Bold.ttf", tartget_fnt_size)
    
    target_draw.text((0, 0), text, font=font)
    target_bbox = target_draw.textbbox((0, 0), text, font=font)
    target_draw.rectangle(target_bbox, outline="red")
    target_bbox_height = target_bbox[3] - target_bbox[1]
    
    print("target_bbox:", target_bbox)
    print("target_bbox height:", target_bbox_height)
    # target_image.show()
    
    diff_h_ratio = bbox_height / target_bbox_height
    print("diff_h_ratio:", diff_h_ratio)
    
    return diff_h_ratio

# 이미지를 특정 비율에 맞춰 상하로 늘려서 반환
def stretch_top_bottom_byRatio(plate_width, plate_height, original_image, ratio):
    # plate_height * ratio의 결과를 정수로 변환
    new_height = int(plate_height * ratio)
    resized_im = original_image.resize((plate_width, new_height))
    return resized_im

# 이미지를 중앙부분을 크롭하여 반환
def crop_to_center(image, new_width, new_height):
    # 이미지의 현재 크기
    width, height = image.size
    
    # 크롭할 영역의 중앙을 계산
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2
    
    # 계산된 영역으로 이미지 크롭
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image

def gen_numberplate(text, file_name):
    # 이미지와 폰트 설정
    W, H = (200, 100)
    fnt_size = 50
    
    # 4개 이상의 항목에 대해선 가변 폰트크기 지정
    if(len(text) > 4):
        print('more than 4 : ', text)
        fnt_size = calcul_fontsize(W, H, fnt_size, text)
        
    im = Image.new("RGBA", (W, H), "WHITE")
    fnt = ImageFont.truetype("GothicA1-Bold.ttf", fnt_size)
    draw = ImageDraw.Draw(im)
    w = draw.textlength(text, font=fnt) # 텍스트의 길이 추출
    draw.text(((W-w)/2, (H-fnt_size)/2), text, font=fnt, fill="black") # 텍스트 중앙정렬

    # 약한 노이즈 추가
    np_im = np.array(im)
    noise = np.random.randint(-10, 10, np_im.shape, dtype='int8')  # 노이즈 값 조정
    np_im = np_im + noise
    np_im = np.clip(np_im, 0, 255)  # 값이 0~255 범위를 벗어나지 않도록 클리핑
    im = Image.fromarray(np_im.astype('uint8'), 'RGBA')

    # 4개 이상의 항목에 대해선 상하 높이를 맞추기위해 늘리기 필요
    if(len(text) > 4):
        print('more than 4 : ', text)
        diff_h_ratio = calc_text_height_ratio_diff(200, 50, 50, text)
        im = stretch_top_bottom_byRatio(W, H, im, diff_h_ratio)
        im = crop_to_center(im, W, H)
    # 이미지 출력
    # im.show()  # 바로 보고 싶을 경우
    im.save('tmp/' + file_name + '.png')

# calc_text_height_ratio_diff(200, 50, 50, 'unknown1234')

def trigger():
    photo_list = get_photoInfos()
    available_numbers = extract_available_info(photo_list)
    print('len of available_numbers:', len(available_numbers))

    needProcessList = extract_morethan4_info(photo_list)
    print('needProcessList :', needProcessList)
    print('len of needProcessList:', len(needProcessList))

    for photo in available_numbers:
        # print('photo:', photo)
        print('photo["numberPlate"][1]:', photo["numberPlate"][1])
        if(photo["numberPlate"][1]['numberPlate'] != 'unknown'):
            gen_numberplate(photo["numberPlate"][1]['numberPlate'], photo["photoId"]+'_1')
        print('photo["numberPlate"][2]:', photo["numberPlate"][2])
        if(photo["numberPlate"][2]['numberPlate'] != 'unknown'):
            gen_numberplate(photo["numberPlate"][2]['numberPlate'], photo["photoId"]+'_2')

trigger()