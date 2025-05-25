from engine.camera import sight_vector_calc
from engine.projection import project_vertexes
from engine.rotat_trans_scal import rotate_vertexes, translate_vertexes, rotate_vertex
from math import sqrt,cos,tan,pi
from time import time
import numpy as np
import pygame
import struct

# the same methods used here were used in QUAKE II
# I
# wikepedia article: https://en.wikipedia.org/wiki/Fast_inverse_square_root
def Q_rsqrt(number):
    # Fast inverse square root using bit manipulation
    threehalfs = 1.5
    x2 = number * 0.5
    y = number
    i = int.from_bytes(struct.pack('f', y), 'little')
    i = 0x5f3759df-(i >> 1)
    y = struct.unpack('f', i.to_bytes(4, 'little'))[0]
    y = y * (threehalfs - (x2 * y * y))
    return y
def normalize_2d_vector(vec):
    length_sq = vec[0]**2 + vec[1]**2
    if length_sq == 0:
        return vec
    inv_sqrt_len = Q_rsqrt(length_sq)
    normalized_vec = [v * inv_sqrt_len for v in vec]
    return normalized_vec

# texturing for faces
def find_face_center(face):
    x_avg = 0
    y_avg = 0
    z_avg = 0
    for vertex in face:
        x_avg += vertex[0]
        y_avg += vertex[1]
        z_avg += vertex[2]
    x_avg = x_avg/len(face)
    y_avg = y_avg/len(face)
    z_avg = z_avg/len(face)
    return [x_avg,y_avg,z_avg]

def calculate_face_normal(face, normal_table):
    # a face is a polygon with n points
    # the normal of a face is the average of the normals of its points
    # face: [[v1,v2,v3...],[Nv1,Nv2,Nv3...],[uv1,uv2,uv3...],[r,g,b]]
    # normal_table: [[Nx,Ny,Nz]...]
    normal_sum = [0,0,0]
    for normal_index in face[1]:
        normal_sum[0] += normal_table[normal_index-1][0]
        normal_sum[1] += normal_table[normal_index-1][1]
        normal_sum[2] += normal_table[normal_index-1][2]
    normal_sum[0] = normal_sum[0]/len(face[1])
    normal_sum[1] = normal_sum[1]/len(face[1])
    normal_sum[2] = normal_sum[2]/len(face[1])
    return normal_sum
def is_face_facing_camera(face, cam_class, normal_table):
    # the dot product of two vectors is: ax × bx + ay × by + az × bz
    # if the dot product is NOT >= to 0 then the face is facing the camera
    # we can find the normal vector of the face by taking the average of all of its normal vectors
    # we can find the camera sight line vector using the function sight_vector_calc in camera.py 
    camera_sight_vector = sight_vector_calc(find_face_center(face),cam_class)
    face_normal = calculate_face_normal(face, normal_table)
    dot_product = camera_sight_vector[0]*face_normal[0]+camera_sight_vector[1]*face_normal[1]+camera_sight_vector[2]*face_normal[2]
    if not dot_product >= 0:
        return True
    return False
def does_point_Yvect_intersect_line(point, line, pre_raster_calc=None):
    if line[0][1] > line[1][1]:
        line_high = line[0][1]
        line_low = line[1][1]
    else:
        line_high = line[1][1]
        line_low = line[0][1]
    if point[1] < line_high:
        if point[1] > line_low:
            if point[0] < (line[0][0]+((point[1]-line[0][1])/(line[1][1]-line[0][1]))*(line[1][0]-line[0][0])):
                return 1
    return 0
def does_point_Yvect_intersect_line_precalced(point, y_clamps, delta_y, x_vals, elements):
    if point[1] > y_clamps[0]:
        if point[1] < y_clamps[1]:
            element1 = -((x_vals[0]-point[1])/delta_y)
            element2 = ((x_vals[1]-point[1])/delta_y)
            element3 = elements[0]
            element4 = elements[1]
            x_int = element1+element2+element3-element4+x_vals[0]
            if point < x_int:
                return True
    return False

def split_object_polygons_into_tris(object):
    Vtable,normals,UVtable,faces,mtl_id = object
    tris = []
    for face in  faces:
        # face example: [[Vi...],[UVi...],[Ni...]]
        for index in range(2,len(face[0])):
            tri = [
                [face[0][0],face[0][index-1],face[0][index]],
                [face[1][0],face[1][index-1],face[1][index]],
                [face[2][0],face[2][index-1],face[2][index]]]
            tris.append(tri)
    return [Vtable,normals,UVtable,tris,mtl_id]
def cull_tris(tris,normal_table,cam_class):
    cam_vect = [0,0,-1]
    # yaw pitch roll
    cam_vect = rotate_vertex(cam_vect,cam_class.camYaw,cam_class.camPitch,cam_class.camRoll)
    cam_vect = normalize_2d_vector(cam_vect)
    clean_tris = []
    for tri in tris:
        tri_normal = [
            (normal_table[tri[1][0]][0]+normal_table[tri[1][0]][0]+normal_table[tri[2][0]][0])/3,
            (normal_table[tri[1][1]][1]+normal_table[tri[1][1]][1]+normal_table[tri[2][1]][1])/3,
            (normal_table[tri[1][2]][2]+normal_table[tri[1][2]][2]+normal_table[tri[2][2]][2])/3]
        tri_normal = normalize_2d_vector(tri_normal)
        DP = (tri_normal[0]*cam_vect[0])+(tri_normal[1]*cam_vect[1])+(tri_normal[2]*cam_vect[2])
        if DP > 0 or DP == 0:
            clean_tris.append(tri)
    return clean_tris
# version of uv mapping by using classical barycentric tris
# and a suggestion from austin
# nake sure to only use list indexes to reduce memory cost
def full_screen_mapping(objects,textures,cam_class,screen,draw_tris=False,track_telemetry=False,affine_mapping=False,show_depth_values=False):
    # the textures var is a json of {texture_id:texture_data}
    # assuming that the polygons in the objects have been split into tris
    # the reason for this is that calculating barycentric coordinates are realy easy to calculate for tris
    # my brother suggested that instead of per polygon pixel area rasterisation
    # that i instead go through all screen pixels and rasterise those instead
    # so this texture mapping method uses that
    # first thing i want to do is combine all of the objects into one big "super object"
    if track_telemetry:
        tim0 = time()
    uv_table = []
    vertex_table = []
    normal_table = []
    tri_table = []
    for object in objects:
        Vtable,normals,UVtable,tris,mtl_id = object
        UVtable_len = len(uv_table)-1
        Vtable_len = len(vertex_table)-1
        Ntable_len = len(normal_table)-1
        for vertex in Vtable:
            vertex_table.append(vertex)
        for normal in normals:
            normal_table.append(normal)
        for UV in UVtable:
            uv_table.append(UV)
        for tri in tris:
            shifted_tri = [
                [tri[0][0]+Vtable_len,tri[0][1]+Vtable_len,tri[0][2]+Vtable_len],
                [tri[1][0]+UVtable_len,tri[1][1]+UVtable_len,tri[1][2]+UVtable_len],
                [tri[2][0]+Ntable_len,tri[2][1]+Ntable_len,tri[2][2]+Ntable_len],
                mtl_id]
            tri_table.append(shifted_tri)
    # rotate vertex and normal table
    if track_telemetry:
        tim1 = time()
    vertex_table = rotate_vertexes(vertex_table, cam_class.camRotX,cam_class.camRotY,cam_class.camRotZ)
    normal_table = rotate_vertexes(normal_table, cam_class.camRotX,cam_class.camRotY,cam_class.camRotZ)
    # transltate the vertex table
    vertex_table = translate_vertexes(vertex_table, cam_class.camX,cam_class.camY,cam_class.camZ)
    # project the vertex table
    projected_vertexes = project_vertexes(vertex_table,cam_class)
    if show_depth_values:
        for vertex in projected_vertexes:
            pygame.draw.circle(screen,(0,255,0),(int(vertex[0]),int(vertex[1])),vertex[2]*10)
    # cull any polygons facing away from the camera
    #tri_table = cull_tris(tri_table,normal_table,cam_class)
    # debugging
    if draw_tris:
        for tri in tri_table:
            pygame.draw.polygon(screen,(0,0,255),
                [[projected_vertexes[tri[0][0]][0],projected_vertexes[tri[0][0]][1]],
                 [projected_vertexes[tri[0][1]][0],projected_vertexes[tri[0][1]][1]],
                 [projected_vertexes[tri[0][2]][0],projected_vertexes[tri[0][2]][1]]])
    # pre calculate triangle areas
    # as well as an additional calculation for barycentric coordinates
    if track_telemetry:
        tim2 = time()
    tri_bary_table = []
    for tri in tri_table:
        # pre calculate the barycentric div calculations due to it being based on the polygon itself and does not use raterised pixel data
        Xv1 = projected_vertexes[tri[0][0]][0]
        Yv1 = projected_vertexes[tri[0][0]][1]
        Xv2 = projected_vertexes[tri[0][1]][0]
        Yv2 = projected_vertexes[tri[0][1]][1]
        Xv3 = projected_vertexes[tri[0][2]][0]
        Yv3 = projected_vertexes[tri[0][2]][1]
        bary_calc = (Yv2-Yv3)*(Xv1-Xv3)+(Xv3-Xv2)*(Yv1-Yv3)
        tri_bary_table.append(bary_calc)
        # pre calculate linear calculations for rasterisation
        # im done with this shiiiiiiiiieeeett
    if track_telemetry:
        tim3 = time()
    # create any needed buffers
    inf = float("inf")
    depth_buffer = np.array([[[inf,0,0] for x in range(cam_class.resY)] for y in range(cam_class.resX)])
    #print("depth buffer size: ",len(depth_buffer),len(depth_buffer[0]))
    # loop through every pixel in the screen
    for Px in range(cam_class.resX):
        for Py in range(cam_class.resY):
            for tri_index in range(len(tri_table)):
                tri_data = tri_table[tri_index]
                tri_pre_calcs = tri_bary_table[tri_index]
                intersections = 0
                edges = [
                    [projected_vertexes[tri_data[0][0]],projected_vertexes[tri_data[0][1]]],
                    [projected_vertexes[tri_data[0][1]],projected_vertexes[tri_data[0][2]]],
                    [projected_vertexes[tri_data[0][2]],projected_vertexes[tri_data[0][0]]]]
                for edge in edges:
                    if does_point_Yvect_intersect_line([Px,Py],edge):
                        intersections += 1
                # if the amount of intersecitons is odd then we are inside of the tri
                if intersections%2 == 1:
                    # get UVW data
                    # interpolate data with barycentric coordinates
                    # graphical representation: https://www.desmos.com/calculator/vnkm2ajvzz
                    div = tri_pre_calcs
                    
                    Xv1 = projected_vertexes[tri_data[0][0]][0]
                    Yv1 = projected_vertexes[tri_data[0][0]][1]
                    Wv1 = projected_vertexes[tri_data[0][0]][2]
                    if affine_mapping:
                        Uv1 = uv_table[tri_data[2][0]][0]/Wv1
                        Vv1 = uv_table[tri_data[2][0]][1]/Wv1
                    else:
                        Uv1 = uv_table[tri_data[2][0]][0]
                        Vv1 = uv_table[tri_data[2][0]][1]
                    
                    Xv2 = projected_vertexes[tri_data[0][1]][0]
                    Yv2 = projected_vertexes[tri_data[0][1]][1]
                    Wv2 = projected_vertexes[tri_data[0][1]][2]
                    if affine_mapping:
                        Uv2 = uv_table[tri_data[2][1]][0]/Wv2
                        Vv2 = uv_table[tri_data[2][1]][1]/Wv2
                    else:
                        Uv2 = uv_table[tri_data[2][1]][0]
                        Vv2 = uv_table[tri_data[2][1]][1]
                    
                    Xv3 = projected_vertexes[tri_data[0][2]][0]
                    Yv3 = projected_vertexes[tri_data[0][2]][1]
                    Wv3 = projected_vertexes[tri_data[0][2]][2]
                    if affine_mapping:
                        Uv3 = uv_table[tri_data[2][2]][0]/Wv3
                        Vv3 = uv_table[tri_data[2][2]][1]/Wv3
                    else:
                        Uv3 = uv_table[tri_data[2][2]][0]
                        Vv3 = uv_table[tri_data[2][2]][1]
                    
                    W1 = (((Yv2-Yv3)*(Px-Xv3))+((Xv3-Xv2)*(Py-Yv3)))/div
                    W2 = (((Yv3-Yv1)*(Px-Xv3))+((Xv1-Xv3)*(Py-Yv3)))/div
                    W3 = 1-W1-W2
                    
                    Iw = (Wv1*W1)+(Wv2*W2)+(Wv3*W3)
                    # check if the depth
                    if depth_buffer[Px][Py][0] > Iw:
                        depth_buffer[Px][Py][0] = Iw
                        Iu = (Uv1*W1)+(Uv2*W2)+(Uv3*W3)
                        Iv = (Vv1*W1)+(Vv2*W2)+(Vv3*W3)
                        if affine_mapping:
                            Zrecip = 1/Iw
                            Zcorrect = 1/Zrecip
                            Iu *= Zcorrect
                            Iv *= Zcorrect
                        depth_buffer[Px][Py][1] = Iu
                        depth_buffer[Px][Py][2] = Iv
    if track_telemetry:
        tim4 = time()
    # sample the textures
    for x in range(len(depth_buffer)):
        for y in range(len(depth_buffer[0])):
            if depth_buffer[x][y][0] != inf:
                Texture = textures["banan.mtl"]
                Tx = len(Texture)
                Ty = len(Texture[0])
                TSx = round((depth_buffer[x][y][2]*Tx)%(Tx-1))
                TSy = round((depth_buffer[x][y][1]*Ty)%(Ty-1))
                Tc = Texture[TSx][TSy]
                screen.set_at((x,y),(Tc[0],Tc[1],Tc[2]))
    if track_telemetry:
        tim5 = time()
    # draw color buffer to screen
    if track_telemetry:
        tim6 = time()
    # process time taken
    if track_telemetry:
        object_combination_time = str(round((tim1-tim0)*1000,4))+"ms"
        transfer_and_project_time = str(round((tim2-tim1)*1000,4))+"ms"
        tri_pre_processsing_time = str(round((tim3-tim2)*1000,4))+"ms"
        rasterisation_texture_mapping_time = str(round((tim4-tim3)*1000,4))+"ms"
        texture_sampling_time = str(round((tim5-tim4)*1000,4))+"ms"
        screen_mapping_time = str(round((tim6-tim5)*1000,4))+"ms"
        total_time = str(round((tim6-tim0)*1000,4))+"ms"
        print("Object combination time: ",object_combination_time)
        print("Transfer and project time: ",transfer_and_project_time)
        print("Triangle pre processing time: ",tri_pre_processsing_time)
        print("Rasterisation and texture mapping time: ",rasterisation_texture_mapping_time)
        print("Texture sampling time: ",texture_sampling_time)
        print("Screen mapping time: ",screen_mapping_time)
        print("Total time: ",total_time)

