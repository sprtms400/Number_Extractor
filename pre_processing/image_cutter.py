#이미지 상 하단을 자르는 작업 (관심 없는 부분 제거)
import cv2 

# Cutting image for focus on the main object
def cut_image(original_image, cutting_ratio):
    original_image_height, original_image_width = original_image.shape[:2]
    cut_height = int(original_image_height * cutting_ratio)
    cutted_image = original_image[cut_height:-cut_height, 0:original_image_width]
    return cutted_image

## Crop edge of the Image
def crop_edge_image(original_image, crop_ratio):
    original_image_height, original_image_width = original_image.shape[:2]
    
    # Calculate the crop size
    crop_height = int(original_image_height * crop_ratio)
    crop_width = int(original_image_width * crop_ratio)
    
    cropped_image = original_image[crop_height:-crop_height, crop_width:-crop_width]
    return cropped_image