# -*- coding:utf-8 -*-
# !/usr/bin/env python
import xml.etree.ElementTree as ET
import argparse
import json
import matplotlib.pyplot as plt
# import skimage.io as io
import cv2
# from labelme import utils
import numpy as np
import glob
import PIL.Image
import os,sys

xml_path = "./datasets/voc/VOC2007/Annotations"
class PascalVOC2coco(object):
    def __init__(self, xml=[], save_json_path='./new.json'):
        '''
        :param xml: 所有Pascal VOC的xml文件路径组成的列表
        :param save_json_path: json保存位置
        '''
        self.xml = xml
        self.save_json_path = save_json_path
        self.images = []
        self.categories = []
        self.annotations = []
        self.label = ["car","bus","person","bicycle","motorbike",]
        for i in range(len(self.label)):
            categorie = {}
            categorie['supercategory'] = self.label[i]
            categorie['id'] = i + 1  # 0 默认为背景
            categorie['name'] = self.label[i]
            self.categories.append(categorie)
        self.annID = 1
        self.height = 0
        self.width = 0

        self.save_json()

    def data_transfer(self):
        for num, json_file in enumerate(self.xml):
            print(json_file)
            self.json_file = json_file
            self.num = num
            path = os.path.dirname(self.json_file)
            path = os.path.dirname(path)
            tree = ET.parse(json_file)
            root = tree.getroot()
            self.filen_ame = root.find("filename").text
            self.filen_ame = self.filen_ame[:-3] + 'jpg'
            size = root.find("size")
            self.width = int(size.find("width").text)
            self.height = int(size.find("height").text)
            print(self.filen_ame, self.width)
            self.images.append(self.image())
            for obj in root.iter('object'):
                cls_name = obj.find('name').text
                xml_box = obj.find('bndbox')
                x1 = int(xml_box.find('xmin').text) 
                y1 = int(xml_box.find('ymin').text) 
                x2 = int(xml_box.find('xmax').text) 
                y2 = int(xml_box.find('ymax').text)
                self.supercategory = cls_name
                if self.supercategory not in self.label:
                    self.categories.append(self.categorie())
                    self.label.append(self.supercategory)
                self.bbox = [x1, y1, x2 - x1, y2 - y1]  # COCO 对应格式[x,y,w,h]
                self.annotations.append(self.annotation())
                self.annID += 1
            

    def image(self):
        image = {}
        image['height'] = self.height
        image['width'] = self.width
        image['id'] = self.num + 1
        image['file_name'] = self.filen_ame
        return image

    def categorie(self):
        categorie = {}
        categorie['supercategory'] = self.supercategory
        categorie['id'] = len(self.label) + 1  # 0 默认为背景
        categorie['name'] = self.supercategory
        return categorie

    def annotation(self):
        annotation = {}
        # annotation['segmentation'] = [self.getsegmentation()]
        # annotation['segmentation'] = [[0.0]]
        annotation['iscrowd'] = 0
        annotation['image_id'] = self.num + 1
        # annotation['bbox'] = list(map(float, self.bbox))
        annotation['bbox'] = self.bbox
        annotation['area'] = self.bbox[2] *  self.bbox[3]
        annotation['category_id'] = self.getcatid(self.supercategory)
        annotation['id'] = self.annID
        return annotation

    def getcatid(self, label):
        for categorie in self.categories:
            if label == categorie['name']:
                return categorie['id']
        return -1

    def data2coco(self):
        data_coco = {}
        data_coco['images'] = self.images
        data_coco['categories'] = self.categories
        data_coco['annotations'] = self.annotations
        return data_coco

    def save_json(self):
        self.data_transfer()
        self.data_coco = self.data2coco()
        # 保存json文件
        json.dump(self.data_coco, open(self.save_json_path, 'w'), indent=4)  # indent=4 更加美观显示


xml_file = glob.glob(os.path.join(xml_path,'*.xml'))
print(xml_path,os.path.join(xml_path,'*.xml'),xml_file)
# xml_file=['./Annotations/000032.xml']

# PascalVOC2coco(xml_file, './instances_train2014.json')
PascalVOC2coco(xml_file, './datasets/coco/annotations/instances_val2014.json')
