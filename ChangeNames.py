import bpy
import csv
import numpy as np

data_path = 'D:/BlenderFiles/CC3_to_Apple_AR_KitNamescsv.csv'
object = bpy.context.object
shapekeys = object.data.shape_keys.key_blocks
#for shape in shapekeys:
#    print(shape)
with open(data_path, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    data = np.array(list(reader))

for x in data:
    for shape in shapekeys:
        if x[0] == shape.name:
            shape.name = x[1]
            break
        