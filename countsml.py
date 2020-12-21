import xml.etree.ElementTree as ET
import os
import cv2
import argparse


parser = argparse.ArgumentParser(description="path info")
parser.add_argument(
        "--path",
        default="datasets/voc/VOC2007/Annotations",
        help="path to result box",
    )
args = parser.parse_args()
path = args.path 
labels = []
files=os.listdir(path)
small = 0
medium = 0
large = 0
all_obj = 0
for xmlFile in files:
	tree = ET.parse(os.path.join(path,xmlFile))
	root = tree.getroot()
	# print(root.find("filename").text)
	boxes =[]
	for obj in root.iter('object'):
		cls_name = obj.find('name').text
		if(cls_name not in labels):
			labels.append(cls_name)
count = [0]*len(labels)
for xmlFile in files:
	# print(xmlFile)
	tree = ET.parse(os.path.join(path,xmlFile))
	root = tree.getroot()
	# print(root.find("filename").text)
	boxes =[]
	for obj in root.iter('object'):
		cls_name = obj.find('name').text
		xml_box = obj.find('bndbox')
		xmin = int(float(xml_box.find('xmin').text)) 
		ymin = int(float(xml_box.find('ymin').text)) 
		xmax = int(float(xml_box.find('xmax').text)) 
		ymax = int(float(xml_box.find('ymax').text)) 
		box = [xmin, ymin,xmax,ymax]
		boxes.append(box)
		all_obj += 1
		ind = labels.index(cls_name)
		count[ind] += 1
	for i in range(0, len(boxes)):
		box = boxes[i]
		m = (box[2]-box[0]) *(box[3]-box[1])
		if m <32*32:
			small +=1
		elif(m<96*96):
			medium += 1
		else:
			large+=1
print(" small",small,"\n medium",medium,"\n large",large,"\n total",small+medium+large,"\n")
for i in range(len(labels)):
	print(labels[i],count[i])
	
