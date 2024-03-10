#%%
import sys
from utils import asset_getter, task_collector, garbage_cleaner, uploader
from pre_processing import image_reader
from segmentation.semantic_segm import extract_numberplate
from ocr.number_extractor import extract_number_easyocr, extract_number_easyocr_thresh

TMP_DIR = 'tmp'

if __name__ == "__main__":
    while True:
        photoId_bytes = task_collector.get_messages_once()
        print('photoId_bytes:', photoId_bytes)
        photoId = photoId_bytes.decode('utf-8')
        print('photoId:', photoId)
        if (photoId == None):
            print('There is no more message in the queue.')
            break
        # temporary photoID
        # photoId = '0e17e9568e294aa6aea0a483be6d95f9'
        # photoId = '0622f4e6077e4811913be679601a2934'
        # photoId = '0e98a7626ff7408b94b087fc5ac223d8' # NOTING
        # photoId = '019b0498577e4642919c943a0afd02c8' # 존재하나 가려짐
        # photoId = '33714d1065564684936964c6ff8d18d1' # 존재하나 가려짐
        asset = asset_getter.get_asset(photoId)
        if asset is None:
            break
        
        # asset is a binary data -> buffer stream
        
        # 1. 번호판 추출 및 tmp파일에 시료 저장
        # 2. 번호판에서 번호정보 추출하기
        # 3. GCS에 업로드 및 DB에 정보 갱신
        # 4. 번호판 이미지 삭제
        
        target_files = []
        transformed_image = image_reader.buffer_to_image(asset)
        cutted_image_path, annotated_image_path, number_path, cropped_number_path, = extract_numberplate(transformed_image, TMP_DIR) # cutted_path, annotated_path, number_path, cropped_path
        # 번호판이 추출됐다면.
        if (cropped_number_path != None):
            result_norm_text = None
            result_norm_prob = None
            result_thresh_text = None
            result_thresh_prob = None
            result_norm_text, result_norm_prob = extract_number_easyocr(TMP_DIR + cropped_number_path, TMP_DIR)
            result_thresh_text, result_thresh_prob = extract_number_easyocr_thresh(TMP_DIR + cropped_number_path, TMP_DIR)
            
            print('result_norm_text:', result_norm_text)
            print('result_norm_prob:', result_norm_prob)
            print('result_thresh_text:', result_thresh_text)
            print('result_thresh_prob:', result_thresh_prob)
            
            # update_responses_norm = uploader.updateNumberPlate(True, result_norm_text, result_norm_prob, photoId) # 분석결과 업로드
            # update_responses_thresh = uploader.updateNumberPlate(True, result_thresh_text, result_thresh_prob, photoId) # 분석결과 업로드
            target_files= [annotated_image_path, number_path, cropped_number_path]
        else:
            target_files= [annotated_image_path]
        # uploader.checkNumberPlateAnalyzed(photoId)                  # 분석끝났다고 알리기
        # uploader.uploadProcessedImages(TMP_DIR, photoId, target_files) # 분석에 도출된 이미지 업로드
        # garbage_cleaner.tmp_cleaner(TMP_DIR)
        break