from pycocotools.coco import COCO
import requests
import os

import json

coco = COCO('./coco/annotations/instances_train2017.json')
coco_category_load = coco.loadCats(coco.getCatIds())

coco_category_name = [cat['name'] for cat in coco_category_load]

print(coco_category_name)

for i in range(len(coco_category_name)):
    print('id : ' + str(i+1) + ' name : ' + coco_category_name[i])

total_category_name = ['person', 'bottle', 'cup', 'laptop',  'cell phone', 'book']

cat_name_list = ['person',  'bottle', 'cup','laptop', 'cell phone', 'book']
    

#image dictionary 만들기
image_list = []
ann_list = []
category_list = []
image_id = 0
ann_id = 0

image_distribution_list = []
image_name_list = []

for cat_name in cat_name_list:
    catIds = coco.getCatIds(catNms=[cat_name])
    print('cat_name : ', cat_name)
    print('catIds : ', catIds)
        
    tmp_catId = cat_name_list.index(cat_name) + 1
    category = dict()
    category['supercategory'] = 'null'
    category['id'] = tmp_catId
    category['name'] = cat_name
    
    category_list.append(category)
    
    print("cat name : " + cat_name + ", cat ID : " + str(tmp_catId))
    
    imgIds = coco.getImgIds(catIds=catIds)
    coco_image = coco.loadImgs(imgIds)
    
    image_distribution_list.append(len(imgIds))
    
    image_cnt = 1
    
    for i in range(len(imgIds)):
        print('진행 : '+ str(image_cnt) + " '/ " + str(len(imgIds)))
        image_cnt += 1
        images = coco_image[i]
        
        if images['file_name'] not in image_name_list:
            image_name_list.append(images['file_name'])
            image = dict()
            image['id'] = image_name_list.index(images['file_name'])
            image['width'] = images['width']
            image['height'] = images['height']
            image['file_name'] = images['file_name']
            image_list.append(image)        
        
        annIds = coco.getAnnIds(imgIds = images['id'], catIds = catIds, areaRng = [], iscrowd = 0)
        anns = coco.loadAnns(annIds)
    
        
        for ann in anns:
            annotation = dict()
            annotation['segmentation'] = ann['segmentation']
            annotation['bbox'] = ann['bbox']
            annotation['area'] = ann['area']
            annotation['id'] = ann_id
            annotation['image_id'] = image_name_list.index(images['file_name'])
            annotation['category_id'] = total_category_name.index(cat_name) + 1
            annotation['iscrowd'] = ann['iscrowd']
            
            
            ann_list.append(annotation)
        
            ann_id += 1
        
        image_id += 1
        

master_obj = {
    'categories' : category_list,
    'images': image_list,
    'annotations' : ann_list
}

print("ann id : " + str(ann_id))
print("image id : " + str(image_id))
print(category_list)

output_path = 'SUNRGBD_annotation/ann1008_train.json'
with open(output_path, 'w') as output_file:
    json.dump(master_obj, output_file, indent = '\t')
    
    
for i in range(len(cat_name_list)):
    print(cat_name_list[i] + ' : ' + str(image_distribution_list[i]))
    
    
'''

'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'

'''

