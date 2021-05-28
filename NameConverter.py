import bpy
import csv
import numpy as np

#CHANGE THESE TO MATCH YOUR SET UP OR THE SCRIPT WILL NOT WORK :)
data_path = 'D:/BlenderFiles/example.csv'
bone_name = 'CC_Base_Head'
bone_name2 = 'CC_Base_NeckTwist02'

# Make drivers for bones
def makeDrivers():
        
    headrot0 = ob_armature.pose.bones[bone_name].driver_add('rotation_euler', 0).driver
    headrot1 = ob_armature.pose.bones[bone_name].driver_add('rotation_euler', 1).driver
    headrot2 = ob_armature.pose.bones[bone_name].driver_add('rotation_euler', 2).driver

    neckrot0 = ob_armature.pose.bones[bone_name2].driver_add('rotation_euler', 0).driver
    neckrot1 = ob_armature.pose.bones[bone_name2].driver_add('rotation_euler', 1).driver
    neckrot2 = ob_armature.pose.bones[bone_name2].driver_add('rotation_euler', 2).driver

    h0 = headrot0.variables.new()
    h0.name = 'headrot_x'
    h0.targets[0].id = ob
    h0.targets[0].data_path = 'data.shape_keys.key_blocks["HeadPitch"].value'
    headrot0.expression = "-0.5 *" + h0.name

    h1 = headrot1.variables.new()
    h1.name = 'headrot_y'
    h1.targets[0].id = ob
    h1.targets[0].data_path = 'data.shape_keys.key_blocks["HeadYaw"].value'
    headrot1.expression = "-0.5 *" + h1.name

    h2 = headrot2.variables.new()
    h2.name = 'headrot_z'
    h2.targets[0].id = ob
    h2.targets[0].data_path = 'data.shape_keys.key_blocks["HeadRoll"].value'
    headrot2.expression = "-0.5 *" + h2.name

    n0 = neckrot0.variables.new()
    n0.name = 'neckrot_x'
    n0.targets[0].id = ob
    n0.targets[0].data_path = 'data.shape_keys.key_blocks["HeadPitch"].value'
    neckrot0.expression = "-0.5 *" + n0.name

    n1 = neckrot1.variables.new()
    n1.name = 'neckrot_y'
    n1.targets[0].id = ob
    n1.targets[0].data_path = 'data.shape_keys.key_blocks["HeadYaw"].value'
    neckrot1.expression = "-0.5 *" + n1.name

    n2 = neckrot2.variables.new()
    n2.name = 'neckrot_z'
    n2.targets[0].id = ob
    n2.targets[0].data_path = 'data.shape_keys.key_blocks["HeadRoll"].value'
    neckrot2.expression = "-0.5 *" + n2.name

ob = bpy.context.object
ob_armature = ob.parent

with open(data_path, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    names = next(reader)
    data = np.array(list(reader))

#Look for data for the shape keys in the csv data
shapekeys = ob.data.shape_keys.key_blocks

# Check if shapekeys have already been added. If not add them in.
if 'HeadYaw' in shapekeys and 'HeadRoll' in shapekeys and 'HeadPitch' in shapekeys:
    print('Shape keys already present')
else:
    print('making shapekeys')
    ob.shape_key_add(name = 'HeadYaw')
    ob.data.shape_keys.key_blocks['HeadYaw'].slider_min = -1
    ob.shape_key_add(name = 'HeadRoll')
    ob.data.shape_keys.key_blocks['HeadRoll'].slider_min = -1
    ob.shape_key_add(name = 'HeadPitch')
    ob.data.shape_keys.key_blocks['HeadPitch'].slider_min = -1

# Loop through the rows of the CSV with the coeff values
for i in range(data.shape[0]):
    
    #Check that coeffs were registered on this frame
    if data[i][1] != '0':
        
        for shape in shapekeys:
            if shape.name in names:
                index = names.index(shape.name)
                shape.value=float(data[i][index])
                shape.keyframe_insert("value", frame=i)

drivers = ob_armature.animation_data.drivers

if len(drivers) != 0:
    for driver in drivers:
        if bone_name in driver.data_path and 'rotation' in driver.data_path:
            print('drivers already added')
            break
        else:
            print('drivers found but not associated with rotation. Adding now')
            makeDrivers()
            break
else:
    print('no drivers found. Adding now')
    makeDrivers()
