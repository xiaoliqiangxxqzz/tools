#!/usr/bin/python
# -*- coding: UTF-8 -*-
start = 0
addtem = 5000
f = './output/last_checkpoint'
import sys

print(int(sys.argv[1]),end=' ')
num = int(sys.argv[1])

ind = start + addtem * num
ind = str(ind).zfill(7)
print(ind)

model = "output/model_" + ind +'.pth'
with open(f,"w") as file:
    file.write(model)
file.close()


