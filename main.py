#%%
import sys
from utils import asset_getter, task_collector, garbage_cleaner
from pre_processing import image_reader
from segmentation.semantic_segm import extract_numberplate
from ocr.number_extractor import extract_number

TMP_DIR = 'tmp'

if __name__ == "__main__":
    while True:
        # photoId = task_collector.get_messages_once()
        # if (photoId != None):
        #     print('There is no more message in the queue.')
        #     break
        # temporary photoID
        photoId = '0a0c11aba1a942228162cdeb726b4195'
        asset = asset_getter.get_asset(photoId)
        if asset is None:
            break
        
        # asset is a binary data -> buffer stream
        
        # 1. 번호판 추출 및 tmp파일에 시료 저장
        # 2. 번호판에서 번호정보 추출하기
        # 3. GCS에 업로드 및 DB에 정보 갱신
        # 4. 번호판 이미지 삭제
        
        transformed_image = image_reader.buffer_to_image(asset)
        extract_numberplate(transformed_image, TMP_DIR)
        extract_number(TMP_DIR + '/cropped_number_plate_image.jpg', TMP_DIR)
        # garbage_cleaner.clean(TMP_DIR)
        break