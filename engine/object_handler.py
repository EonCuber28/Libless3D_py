from engine.rotat_trans_scal import translate_vertexes
def get_origen_of_object(object):
    total_vertexes = len(object[0])
    totalX = 0
    totalY = 0
    totalZ = 0
    for vertex in object[0]:
        totalX += vertex[0]
        totalY += vertex[1]
        totalZ += vertex[2]
    centerX = totalX/total_vertexes
    centerY = totalY/total_vertexes
    centerZ = totalZ/total_vertexes
    return [centerX,centerY,centerZ]
def center_object(object, centering_point=[0,0,0]):
    object_center = get_origen_of_object(object)
    print(object_center)
    center_diffX = object_center[0]-centering_point[0]
    center_diffY = object_center[1]-centering_point[1]
    center_diffZ = object_center[2]-centering_point[2]
    print(center_diffX,center_diffY,center_diffZ)
    object[0] = translate_vertexes(object[0],center_diffX,center_diffY,center_diffZ)
    return object
