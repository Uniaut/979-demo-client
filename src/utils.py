import asyncio
import requests
import json
import numpy as np
import yaml

import cv2

# read yaml
with open("config.yaml", 'r') as f:
    config = yaml.full_load(f)



def request_prediction(image: np.array):
    _, jpeg = cv2.imencode('.jpeg', image)
    response = requests.post(url=config['url'], files={"imageFile": jpeg})

    if not response.ok: 
        print("ERROR: response ", response.status_code)
        return

    result_json = json.loads(response.text)
    return result_json['rois'], result_json['class_ids'], result_json['scores']


def random_box_color():
    # random hsv color: saturation, brightness is always maximum
    hsv_color = np.array([np.random.randint(0, 179), 255, 100], dtype=np.uint8)

    # convert (h, s, v) to (r, g, b) color space
    rgb_color = cv2.cvtColor(np.array([[hsv_color]], dtype=np.uint8), cv2.COLOR_HSV2RGB)[0][0]

    return rgb_color.tolist()

def visualize_bbox(img, bbox, class_name, score, color=(255, 0, 0), thickness=2):
    """Visualizes a single bounding box on the image"""
    # x_min, y_min, w, h = bbox
    # x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)

    x_min, y_min, x_max, y_max = bbox
    x_min, x_max, y_min, y_max = int(x_min), int(x_max), int(y_min), int(y_max)

    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)
    
    text = f'{class_name} {score:.2f}'
    ((text_width, text_height), _) = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1) 
    text_width = int(text_width * 0.75)
    if np.random.random() > 0.5:
        cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), color, -1)
        cv2.putText(
            img,
            text=text,
            org=(x_min + int(0.05 * text_width), y_min - int(0.3 * text_height)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.35, 
            color=(255, 255, 255), 
            lineType=cv2.LINE_AA,
        )
    else:
        cv2.rectangle(img, (x_min, y_max), (x_min + text_width, y_max + int(1.3 * text_height)), color, -1)
        cv2.putText(
            img,
            text=text,
            org=(x_min + int(0.05 * text_width), y_max + int(1.0 * text_height)),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.35, 
            color=(255, 255, 255), 
            lineType=cv2.LINE_AA,
        )
    return img


THRESHOLD = 0.3

def visualize(image, bboxes, category_ids, scores, threshold=THRESHOLD):
    img = image.copy()
    np.random.seed(0)
    for bbox, category_id, score in zip(bboxes, category_ids, scores):
        if score < threshold:
            continue
        class_name = category_id_to_name[category_id]
        img = visualize_bbox(img, bbox, class_name, score, random_box_color())

    return img


def to_items(bboxes, category_ids, scores):
    items = []
    for bbox, category_id, score in zip(bboxes, category_ids, scores):
        # if score < THRESHOLD:
        #     continue
        class_name = category_id_to_name[category_id]
        items.append({
            'class_name': class_name,
            'score': score,
            'bbox': bbox
        })
    items.sort(key=lambda item: item['score'], reverse=True)
    return items



category_id_to_name = [
  'shirt, blouse',
  'top, t-shirt, sweatshirt',
  'sweater',
  'cardigan',
  'jacket',
  'vest',
  'pants',
  'shorts',
  'skirt',
  'coat',
  'dress',
  'jumpsuit',
  'cape',
  'glasses',
  'hat',
  'headband, head covering, hair accessory',
  'tie',
  'glove',
  'watch',
  'belt',
  'leg warmer',
  'tights, stockings',
  'sock',
  'shoe',
  'bag, wallet',
  'scarf',
  'umbrella',
  'hood',
  'collar',
  'lapel',
  'epaulette',
  'sleeve',
  'pocket',
  'neckline',
  'buckle',
  'zipper',
  'applique',
  'bead',
  'bow',
  'flower',
  'fringe',
  'ribbon',
  'rivet',
  'ruffle',
  'sequin',
  'tassel'
]
