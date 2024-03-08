from PIL import Image
import numpy as np
import cv2

def buffer_to_image(buffer):
    nparr = np.frombuffer(buffer, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

def np_to_image(np_array):
    cropped_image = np.array(np_array) 
    # numpy 배열을 PIL 이미지 객체로 변환
    image = Image.fromarray(cropped_image)
    return image