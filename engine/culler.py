from engine.camera import sculpt_to_frustum,isInFrustum

# check if any of the following are outside of the camera frustum:
# vertex
def cull_vertex(vertex, camera_class):
    if isInFrustum(vertex,camera_class):
        return True # IS WITHIN THE FRUSTUM
    return False # IS NOT WITHIN THE FRUSTUM
# vertexes
def cull_vertexes(vertexes, camera_class):
    pure_vertexes = []
    for vertex in vertexes:
        if cull_vertex(vertex, camera_class):
            pure_vertexes.append(vertex)
    return pure_vertexes
# cull vertexes for edges/polygons
def special_cull_vertexes(vertex_table, camera_class):
    culled_vertex_table = []
    for vertex in vertex_table:
        if not cull_vertex(vertex,camera_class):
            culled_vertex_table.append(None)
        else:
            culled_vertex_table.append(vertex)
    return culled_vertex_table

# Sulpt the following to the camera frustum
# vertex
def sculpt_vertex(vertex, camera_class):
    return sculpt_to_frustum(vertex,camera_class)
# vertexes
def sculpt_vertexes(vertexes, camera_class):
    sculpted_vertexes = []
    for vertex in vertexes:
        sculpted_vertexes.append(sculpt_vertex(camera_class, vertex))
    return sculpted_vertexes
