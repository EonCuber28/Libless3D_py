from math import sin, cos, sqrt

# normalise vector
def normalise_vector(vector):
    # calculatethe vector lenght using the pythagorean theorem
    vector_lenght = sqrt((vector[0]**2)+(vector[1]**2)+(vector[2]**2))
    # devidede the initial vector by the vector length
    normalX = vector[0]/vector_lenght
    normalY = vector[1]/vector_lenght
    normalZ = vector[2]/vector_lenght
    return [normalX,normalY,normalZ]
# normalise vectors
def normalise_vectors(vectors):
    normalised_vectors = []
    for vector in vectors:
        normalised_vectors.append(normalise_vector(vector))
    return normalised_vectors

# rotate X
def rotateX(vertex,amount):
    newX = vertex[0]
    newY = vertex[1]*cos(amount)-vertex[2]*sin(amount)
    newZ = vertex[1]*sin(amount)+vertex[2]*cos(amount)
    return [newX,newY,newZ]
# rotate Y
def rotateY(vertex,amount):
    newX = vertex[0]*cos(amount)+vertex[2]*sin(amount)
    newY = vertex[1]
    newZ = -vertex[0]*sin(amount)+vertex[2]*cos(amount)
    return [newX,newY,newZ]
# rotate Z
def rotateZ(vertex,amount):
    newX = vertex[0]*cos(amount)-vertex[1]*sin(amount)
    newY = vertex[0]*sin(amount)+vertex[1]*cos(amount)
    newZ = vertex[2]
    return [newX,newY,newZ]

# rotate vertex
def rotate_vertex(vertex, X,Y,Z):
    # rotate by X
    rotated_vertex = rotateX(vertex,X)
    # rotate by Y
    rotated_vertex = rotateY(rotated_vertex,Y)
    # rotate by Z
    rotated_vertex = rotateZ(rotated_vertex,Z)
    # return
    return rotated_vertex
# rotate vertexes
def rotate_vertexes(vertexes, X,Y,Z):
    rotate_vertexos = []
    for vertex in vertexes:
        rotate_vertexos.append(rotate_vertex(vertex, X,Y,Z))
    return rotate_vertexos

# translate X
def translateX(vertex,amount):
    return [vertex[0]+amount,vertex[1],vertex[2]]
# translate Y
def translateY(vertex,amount):
    return [vertex[0],vertex[1]+amount,vertex[2]]
# translate Z
def translateZ(vertex,amount):
    return [vertex[0],vertex[1],vertex[2]+amount]

# translate vertex
def translate_vertex(vertex, X,Y,Z):
    # translate X
    translated_vertex = translateX(vertex,X)
    # translate Y
    translated_vertex = translateY(translated_vertex,Y)
    # translate Z
    translated_vertex = translateZ(translated_vertex,Z)
    # return
    return translated_vertex
# translate vertexes
def translate_vertexes(vertexes, X,Y,Z):
    translated_vertexes = []
    for vertex in vertexes:
        translated_vertexes.append(translate_vertex(vertex, X,Y,Z))
    return translated_vertexes

# scale X
def scaleX(vertex,amount):
    return [vertex[0]*amount,vertex[1],vertex[2]]
# scale Y
def scaleY(vertex,amount):
    return [vertex[0],vertex[1]*amount,vertex[2]]
# scale Z
def scaleZ(vertex,amount):
    return [vertex[0],vertex[1],vertex[2]*amount]

# scale vertex
def scale_vertex(vertex, X,Y,Z):
    # scale X
    scaled_vertex = scaleX(vertex, X)
    # scale Y
    scaled_vertex = scaleY(scaled_vertex, Y)
    # scale Z
    scaled_vertex = scaleZ(scaled_vertex, Z)
    # return
    return scaled_vertex
# scale vertexes
def scale_vertexes(vertexes, X,Y,Z):
    scaled_vertexes = []
    for vertex in vertexes:
        scaled_vertexes.append(scale_vertex(vertex, X,Y,Z))
    return scaled_vertexes

def transfer_object_to_world(object,cam_class):
    return rotate_vertexes(object.vertex_table, cam_class.camRotX,cam_class.amRotY,cam_class.camRotZ)
