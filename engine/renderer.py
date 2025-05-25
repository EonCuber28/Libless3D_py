from engine.culler import cull_vertexes,special_cull_vertexes, sculpt_vertexes
from engine.polygon_proccesing import sort_polygons_by_nearest_point_np, sort_polygons
from engine.rotat_trans_scal import rotate_vertexes, translate_vertexes
from engine.projection import project_vertex, project_vertexes
from engine.camera import move_vertex_to_camera_space
import pygame

# merge object data for rendering multiple objects
def merge_objects_data(objects):
    # format [[vertex table, polygon table]...]
    final_vertex_table = []
    final_polygon_table = []
    # for each object
    for object in objects:
        # count up the total amount of vertexes already part of the final vertex_table
        VTL = len(final_vertex_table)
        # when adding polygon tables, add the vertex table length to the indexes of the polygon table
        # to ensure that the polygons are not referencing the incorrect vertexes in 3D space 
        increased_polygons = []
        for polygon in object[1]:
            increased_polygons.append([
                [polygon[0][0]+VTL,polygon[0][1]+VTL,polygon[0][2]+VTL],
                [polygon[1][0]+VTL,polygon[1][1]+VTL,polygon[1][2]+VTL],
                [polygon[2][0]+VTL,polygon[2][1]+VTL,polygon[2][2]+VTL],
                polygon[3]])
        # then add the vertex table to the final table to reduce interaction between it and the begining of the loop
        final_polygon_table.append(increased_polygons)
        final_vertex_table.append(object[0])
    return [final_vertex_table,final_polygon_table]

### SIMPLE GENERAL PROCESS OF RENDERING ###
# 1. move all vertexes into camera space
# 1.1 rotate
# 1.2 translate
# 2. remove any vertexes outside of the camera frustum
# 2.1. if needed, sort polygons into a depth buffer
# 3. project remaining vertexes
# 4. draw vertexes to screen 
# 4.1 update the screen

# pre process vertexes
def pre_process_vertexes(vertex_table, camera_class, sculpt=False,proj_method="WP"):
    cam_x = camera_class.camX
    cam_y = camera_class.camY
    cam_z = camera_class.camZ

    cam_yaw = camera_class.camYaw
    cam_pitch = camera_class.camPitch
    cam_roll = camera_class.camRoll
    # rotate vertexes
    vertex_table = rotate_vertexes(vertex_table, cam_yaw,cam_pitch,cam_roll)
    # translate vertexes
    vertex_table = translate_vertexes(vertex_table, cam_x,cam_y,cam_z)
    # cull any vertexes outside of the camera frustum
    if sculpt:
        vertex_table = sculpt_vertexes(vertex_table,camera_class)
    else:
        vertex_table = cull_vertexes(vertex_table,camera_class)
    # project the vertexes
    proj_vertexes = proj_vertexes(vertex_table,camera_class,proj_method)
    return proj_vertexes
    
# pre process edges
def pre_process_edges(vertex_table,edge_table, camera_class, sculpt=False,proj_method="WP"):
    cam_x = camera_class.camX
    cam_y = camera_class.camY
    cam_z = camera_class.camZ

    cam_yaw = camera_class.camYaw
    cam_pitch = camera_class.camPitch
    cam_roll = camera_class.camRoll
    # rotate vertexes
    vertex_table = rotate_vertexes(vertex_table, cam_yaw,cam_pitch,cam_roll)
    # translate vertexes
    vertex_table = translate_vertexes(vertex_table, cam_x,cam_y,cam_z)
    # cull any vertexes outside of the camera frustum
    if sculpt:
        preped_vertex_table = sculpt_vertexes(vertex_table,camera_class)
    else:
        preped_vertex_table = special_cull_vertexes(vertex_table,camera_class)
    # project the vertexes
    proj_vertexes = project_vertexes(preped_vertex_table,camera_class,proj_method)
    pure_edges = []
    for edge in edge_table:
        v1 = proj_vertexes[edge[0]]
        v2 = proj_vertexes[edge[1]]
        if v1 != None and v2 != None:
            pure_edges.append([v1,v2])
        elif not (v1 == None and v2 != None):
            if v1 == None:
                v1 = project_vertex(vertex_table[edge[0]],camera_class,proj_method)
            if v2 == None:
                v2 = project_vertex(vertex_table[edge[1]],camera_class,proj_method)
            pure_edges.append([v1,v2])
    return pure_edges
# pre process polygons
def pre_process_polygons(vertex_table,polygon_table, camera_class, sculpt=False,proj_method="WP"):
    cam_x = camera_class.camX
    cam_y = camera_class.camY
    cam_z = camera_class.camZ

    cam_yaw = camera_class.camYaw
    cam_pitch = camera_class.camPitch
    cam_roll = camera_class.camRoll
    # sort polygons
    #polygon_table = sort_polygons(vertex_table, polygon_table, [cam_x,cam_y,cam_z])
    # rotate vertexes
    vertex_table = rotate_vertexes(vertex_table, cam_yaw,cam_pitch,cam_roll)
    # translate vertexes
    vertex_table = translate_vertexes(vertex_table, cam_x,cam_y,cam_z)
    # cull any vertexes outside of the camera frustum
    if sculpt:
        vertexo_table = sculpt_vertexes(vertex_table,camera_class)
    else:
        vertexo_table = special_cull_vertexes(vertex_table,camera_class)
    # project the vertexes
    proj_vertexo = project_vertexes(vertexo_table,camera_class,proj_method)
    pure_polygons = []
    for polygon in polygon_table:
        v1 = proj_vertexo[polygon[0]]
        v2 = proj_vertexo[polygon[1]]
        v3 = proj_vertexo[polygon[2]]
        if v1 != None and v2 != None and v3 != None:
            pure_polygons.append([v1,v2,v3,polygon[3]])
        elif not (v1 == None and v2 == None and v3 == None):
            if v1 == None:
                #print(vertex_table[polygon[0]])
                v1 = project_vertex(vertex_table[polygon[0]],camera_class,proj_method)
            if v2 == None:
                #print(vertex_table[polygon[1]])
                v2 = project_vertex(vertex_table[polygon[1]],camera_class,proj_method)
            if v3 == None:
                #print(vertex_table[polygon[2]])
                v3 = project_vertex(vertex_table[polygon[2]],camera_class,proj_method)
            pure_polygons.append([v1,v2,v3,polygon[3]])
    return pure_polygons

# pre process object
def pre_process_object(object_data,camera_class,config={"V":False,"E":False,"P":True,"Proj":"WP","sculpt":False}):
    pass
# pre process objects
def pre_process_objects(objects, camera_class, config={"V":False,"E":False,"P":True,"Proj":"WP","sculpt":False}):
    pass
# pre process n-gons
def pre_process_ngons(ngons, vertex_table, camera_class, sculpt, proj_method="WP"):
    pass

# draw:
# polygons
def draw_polygons(polygons, surface):
    for polygon in polygons:
        print(polygon)
        if polygon != []:
            if polygon[0] != None and polygon[1] != None:
                pygame.draw.polygon(surface, polygon[3],
                [(polygon[0][0],polygon[0][1]),
                (polygon[1][0],polygon[1][1]),
                (polygon[2][0],polygon[2][1])])
# edges
def draw_edges(edges, surface, color=[0,255,0]):
    for edge in edges:
        pygame.draw.line(surface, color, 
        (edge[0][0],edge[0][1]),
        (edge[1][0],edge[1][1]))
# vertexes
def draw_vertexes(vertexes, surface, color=[255,0,0], radius=5):
    for vertex in vertexes:
        pygame.draw.circle(surface, color, (vertex[0],vertex[1]), radius)

