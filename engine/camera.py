from engine.rotat_trans_scal import rotate_vertex, normalise_vector
from engine.rotat_trans_scal import rotate_vertex, translate_vertex
from math import tan, radians, cos, sin, pi

class camera:
    def __init__(self):
        self.camX = 0
        self.camY = 0
        self.camZ = 0

        self.camRotX = 0
        self.camRotY = 0
        self.camRotZ = 0
        
        self.near_plane = 0.0001
        self.frustum_soft_boundry = 0

        self.resX = 10
        self.resY = 10
        self.screen_ratio = self.resX/self.resY

        self.FOV = pi/2
        self.Hfov = self.FOV
        self.Vfov = self.Hfov*self.screen_ratio
        self.HFL = (self.resX/2)/tan(self.Hfov/2)
        self.VFL = (self.resY/2)/tan(self.Vfov/2)
        
        self.forward_vect = [
            cos(self.camRotX)*sin(self.camRotY),
            sin(self.camRotX),
            cos(self.camRotX)*cos(self.camRotY)]
        self.right_vect = [
            sin(self.camRotY-(pi/2)),
            0,
            cos(self.camRotY-(pi/2))]
        self.up_vect = [
            ((self.forward_vect[1]*self.right_vect[0])-(self.forward_vect[0]*self.right_vect[1])),
            ((self.forward_vect[2]*self.right_vect[0])-(self.forward_vect[0]*self.right_vect[2])),
            ((self.forward_vect[0]*self.right_vect[1])-(self.forward_vect[1]*self.right_vect[0]))
        ]

def recalc_vects(cam_class=camera()):
    cam_class.forward_vect = [
        cos(cam_class.camRotX)*sin(cam_class.camRotY),
        sin(cam_class.camRotX),
        cos(cam_class.camRotX)*cos(cam_class.camRotY)]
    cam_class.right_vect = [
        sin(cam_class.camRotY-(pi/2)),
        0,
        cos(cam_class.camRotY-(pi/2))]
    cam_class.up_vect = [
        ((cam_class.forward_vect[1]*cam_class.right_vect[0])-(cam_class.forward_vect[0]*cam_class.right_vect[1])),
        ((cam_class.forward_vect[2]*cam_class.right_vect[0])-(cam_class.forward_vect[0]*cam_class.right_vect[2])),
        ((cam_class.forward_vect[0]*cam_class.right_vect[1])-(cam_class.forward_vect[1]*cam_class.right_vect[0]))]

def screen_to_pixel_converter(vertex, camera_class=camera()):
    res_x = camera_class.resX
    res_y = camera_class.resY
    Vx = vertex[0]
    Vy = vertex[1]
    return [Vx*res_x, Vy*res_y]
def screen_to_pixel_edges(edges, camera_class=camera()):
    pixel_edges = []
    for edge in edges:
        pixel_edges.append([
            screen_to_pixel_converter(edge[0],camera_class),
            screen_to_pixel_converter(edge[1],camera_class)])
    return pixel_edges
def screen_to_pixel_polygons(polygons, camera_class=camera()):
    pixel_polygons = []
    for polygon in polygons:
        pixel_polygons.append([
            screen_to_pixel_converter(polygon[0],camera_class),
            screen_to_pixel_converter(polygon[1],camera_class),
            screen_to_pixel_converter(polygon[2],camera_class),
            polygon[3]])
    return pixel_polygons

def move_vertex_to_camera_space(vertex,cam_class=camera()):
    # rotate
    vertex = rotate_vertex(vertex, cam_class.camPitch,cam_class.camRoll,cam_class.camYaw)
    # translate
    vertex = translate_vertex(vertex, cam_class.camX,cam_class.camY,cam_class.camZ)
    return vertex

def sculpt_to_frustum(vertex,cam_class=camera()):
    soft_boundry = cam_class.frustum_soft_boundry
    X,Y,Z = vertex
    # calc left boundry
    left_boundry = -tan(cam_class.Hfov/2)*Z+soft_boundry
    # clamp to left boundry
    if X > left_boundry:
        X = left_boundry
    # calc right boundry
    right_boundry = tan(cam_class.Hfov/2)*Z+soft_boundry
    # clamp to lright boundry
    if X < right_boundry:
        X = right_boundry
    # calc top boundry
    top_boundry = tan(cam_class.Vfov/2)*Z+soft_boundry
    # clamp to top boundry
    if Y < top_boundry:
        Y = top_boundry
    # calc bottom boundry
    bottom_boundry = -tan(cam_class.Vfov/2)*Z+soft_boundry
    # clamp to bottom boundry
    if Y > bottom_boundry:
        Y = bottom_boundry
    # clamp to near plane boundry
    if Z < cam_class.near_plane:
        Z = cam_class.near_plane
    return [X,Y,Z]

def reCalculateFOV(camera_object=camera()):
    camera_object.Hfov = radians(camera_object.FOV)
    camera_object.Vfov = (1/camera_object.Hfov)*camera_object.screen_ratio
    camera_object.HFL = (camera_object.resX/2)/tan(camera_object.Hfov)
    camera_object.VFL = (camera_object.resY/2)/tan(camera_object.Vfov)

def isInFrustum(vertex,cam_class=camera()):
    soft_boundry = cam_class.frustum_soft_boundry
    X,Y,Z = vertex
    # if is farther away than the near plane
    if Z >= cam_class.near_plane:
        # is within the top/bottom frustum
        if Y >= (-tan(cam_class.Vfov/2))*Z+soft_boundry and Y <= (tan(cam_class.Vfov/2))*Z+soft_boundry:
            # is within the left/right frustum
            if X >= (-tan(cam_class.Hfov/2))*Z+soft_boundry and X <= (tan(cam_class.Hfov/2))*Z+soft_boundry:
                return True
    return False

def sight_vector_calc(sight_vertex, cam_class=camera()):
    # to find the sight vector, find the difference between the camera and sight vertex
    # then using that vector, normalise it.
    diffX = sight_vertex[0]-cam_class.camX
    diffY = sight_vertex[1]-cam_class.camY
    diffZ = sight_vertex[2]-cam_class.camZ
    sight_vector = [diffX,diffY,diffZ]
    sight_vector = normalise_vector(sight_vector)
    return sight_vector

def calculate_forward_vector(cam_class=camera()):
    # the forward vector and/or the rotation method have to change for this to work
    forward_vector = rotate_vertex([0,0,1],0,cam_class.camYaw,0)
    forward_vector = normalise_vector(forward_vector)
    return forward_vector
def calculate_up_vector(cam_class=camera()):
    # this should never change for an fps unless you weird
    # (i think that Y is the up direction(idk))
    vector = [0,1,0]
    vector = normalise_vector(vector)
    return [0,1,0]
def calculate_right_vector(cam_class=camera()):
    # what i know:    up
    right_vector = rotate_vertex(calculate_forward_vector(cam_class), 0,0,90)
    return right_vector

def move_cam_left(amount,cam_class=camera()):
    movement_vector = normalise_vector(cam_class.right_vect)
    cam_class.camX += movement_vector[0]*amount
    cam_class.camY += movement_vector[1]*amount
    cam_class.camZ += movement_vector[2]*amount
def move_cam_right(amount,cam_class=camera()):
    movement_vector = normalise_vector(cam_class.right_vect)
    cam_class.camX -= movement_vector[0]*amount
    cam_class.camY -= movement_vector[1]*amount
    cam_class.camZ -= movement_vector[2]*amount

def move_cam_up(amount,cam_class=camera()):
    movement_vector = normalise_vector(cam_class.up_vect)
    cam_class.camX += movement_vector[0]*amount
    cam_class.camY += movement_vector[1]*amount
    cam_class.camZ += movement_vector[2]*amount
def move_cam_down(amount,cam_class=camera()):
    movement_vector = normalise_vector(cam_class.up_vect)
    cam_class.camX -= movement_vector[0]*amount
    cam_class.camY -= movement_vector[1]*amount
    cam_class.camZ -= movement_vector[2]*amount

def move_cam_forward(amount,cam_class=camera()):
    movement_vector = normalise_vector(cam_class.forward_vect)
    cam_class.camX += movement_vector[0]*amount
    cam_class.camY += movement_vector[1]*amount
    cam_class.camZ += movement_vector[2]*amount
def move_cam_backward(amount,cam_class=camera()):
    movement_vector = normalise_vector(cam_class.forward_vect)
    cam_class.camX -= movement_vector[0]*amount
    cam_class.camY -= movement_vector[1]*amount
    cam_class.camZ -= movement_vector[2]*amount
