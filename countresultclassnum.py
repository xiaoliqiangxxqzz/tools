import json
import argparse
parser = argparse.ArgumentParser(description="path info")
parser.add_argument(
        "--path",
        default="output_z/inference/coco_2014_val/bbox.json",
        help="path to result box",
    )
args = parser.parse_args()
path = args.path
num_class = 0
small =0
medium = 0
large = 0
with open(path,'r')as fp:
    data = json.load(fp)
    # print(data)
    for i in range(len(data)):
        bbox = data[i]
        if(num_class < bbox['category_id']):
            num_class = bbox['category_id']
    result = [0]*num_class
    for i in range(len(data)):
        bbox = data[i]
        for j in range(num_class):
            if(bbox['category_id']-1==j):
                result[j]+=1
        box = bbox["bbox"]
        x,y,w,h = box
        m = w*h
        if( m <32*32):
            small +=1
        elif(m<96*96):
            medium += 1
        else:
            large+=1
    print("num_class",num_class,result)
    print("small",small,"medium",medium,"large",large)


