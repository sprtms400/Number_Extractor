# 이미지에서 숫자 추출
import cv2
import easyocr

def extract_number(image_path, tmp_dir):
    license_plate = cv2.imread(image_path)
    # 그레이스케일 변환
    gray = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite(tmp_dir+'/gray_number_plate_gray.jpg', gray)

    # 명암 대비 개선을 위한 적응형 히스토그램 평활화
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1 = clahe.apply(gray)
    # cv2.imwrite(tmp_dir+'/gray_number_plate_clahe.jpg', cl1)

    # 가우시안 블러로 노이즈 제거
    blurred = cv2.GaussianBlur(cl1, (5,5), 0)
    # cv2.imwrite(tmp_dir+'/gray_number_plate_blurred.jpg', blurred)

    # 적응형 이진화 적용
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # cv2.imwrite(tmp_dir+'/gray_number_plate_thresh.jpg', thresh)

    # EasyOCR reader 초기화
    reader = easyocr.Reader(['en'], gpu=True)

    # 전처리된 번호판 이미지에서 텍스트 인식
    detection = reader.readtext(license_plate)
    # detection = reader.readtext(cl1)
    print("Detection: ", detection)

    # 인식된 텍스트가 있는 경우 처리
    if len(detection) == 0:
        text = "Impossible to read the text from the license plate"
    else:
        # 첫 번째 인식된 텍스트와 신뢰도 출력
        text = f"{detection[0][1]} {detection[0][2] * 100:.2f}%"

    print("Number Plate: ", text)
    cv2.imwrite(tmp_dir+'/processed_number_plate.jpg', thresh)