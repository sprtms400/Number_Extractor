#%%
# Semantic 하게 Segmentation을 수행

from groundingdino.util.inference import load_model, load_image, predict, annotate
import cv2
import torch # for torch.Tensor
import pre_processing.image_cutter as cutter
import pre_processing.image_reader as reader

TEXT_PROMPT = "person . bicycle , number plate ."
TARGET_OBJECT = 'number plate'
BOX_THRESHOLD = 0.35
TEXT_THRESHOLD = 0.25
CUTTING_RATIO = 0.3
CROP_RATIO = 0.15

model = load_model("segmentation/groundingdino/config/GroundingDINO_SwinT_OGC.py", "segmentation/weights/groundingdino_swint_ogc.pth")

def extract_numberplate(origianl_image, tmp_dir):
    cutted_image = cutter.cut_image(origianl_image, CUTTING_RATIO)
    cv2.imwrite(tmp_dir + '/cutted_image.jpg', cutted_image)
    image_source, image = load_image(tmp_dir + '/cutted_image.jpg')
    number_plate_image = None
    
    boxes, logits, phrases = predict(
        model=model,
        image=image,
        caption=TEXT_PROMPT,
        box_threshold=BOX_THRESHOLD,
        text_threshold=TEXT_THRESHOLD
    )
    annotatedImage = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
    img_height, img_width = image_source.shape[:2]
    
    for box, phrase in zip(boxes, phrases):
        if TARGET_OBJECT in phrase.lower():          
            # tensor 타입인 경우 .item()으로 변환
            if isinstance(box, torch.Tensor):
                box = box.numpy()
            rat_x, rat_y, rat_w, rat_h = box

            center_coord_x = int(rat_x * img_width)
            center_coord_y = int(rat_y * img_height)
            box_width = int(rat_w * img_width)
            box_height = int(rat_h * img_height)
            
            coord_x = center_coord_x - box_width // 2
            coord_y = center_coord_y - box_height // 2
            number_plate_image = image_source[coord_y:coord_y+box_height, coord_x:coord_x+box_width]
    
    cutted_path = None
    annotated_path = None
    number_path = None
    cropped_path = None
    
    if number_plate_image is not None:
        cv2.imwrite(tmp_dir + "/number_plate_image.jpg", number_plate_image)
        cv2.imwrite(tmp_dir + "/cropped_number_plate_image.jpg", cutter.crop_edge_image(number_plate_image, CROP_RATIO))
        cutted_path = "/cutted_image.jpg"
        number_path = "/number_plate_image.jpg"
        cropped_path = "/cropped_number_plate_image.jpg"
    else:
        print("Number plate not found.")
    cv2.imwrite(tmp_dir + "/annotated_image.jpg", annotatedImage)
    annotated_path = "/annotated_image.jpg"
    return cutted_path, annotated_path, number_path, cropped_path