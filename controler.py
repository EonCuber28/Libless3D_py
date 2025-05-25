from engine.camera import move_cam_forward,move_cam_backward
from engine.camera import move_cam_left,move_cam_right
from engine.camera import move_cam_up,move_cam_down
from engine.camera import reCalculateFOV
from math import pi
import pygame

def handle_mouse(cam_class,mouse_movement):
    # X --> yaw
    # y --> pitch
    # (idk)
    mouse_gain = 0.005
    x_gain = 1
    y_gain = 1
    # rotate camera up/down
    cam_class.camRotX -= mouse_movement[0]*pi*y_gain*mouse_gain
    # rotate camera left/right
    cam_class.camRotY -= mouse_movement[1]*pi*x_gain*mouse_gain
    # cap cam rotations (optional)
    x_max = pi
    x_min = -pi

    y_max = pi
    y_min = -pi

    if cam_class.camRotX > x_max:
        cam_class.camRotX = x_max
    if cam_class.camRotX < x_min:
        cam_class.camRotX = x_min

    if cam_class.camRotY > y_max:
        cam_class.camRotY = y_max
    if cam_class.camRotY < y_min:
        cam_class.camRotY = y_min

def handle_keyboard(cam_class,keys):
    movement_mod = 0.07
    FB_mod = 1
    LR_mod = 1
    UD_mod = 1
    # move cam forward/backward for W and S
    if keys[pygame.K_w]:
        move_cam_forward((FB_mod*movement_mod),cam_class)
    if keys[pygame.K_s]:
        move_cam_backward((FB_mod*movement_mod),cam_class)
    # strafe cam left/right foe A and D
    if keys[pygame.K_LSHIFT]:
        move_cam_left((LR_mod*movement_mod),cam_class)
    if keys[pygame.K_SPACE]:
        move_cam_right((LR_mod*movement_mod),cam_class)
    # move cam up/down for SHIFT and SPACE
    if keys[pygame.K_a]:
        move_cam_up((UD_mod*movement_mod),cam_class)
    if keys[pygame.K_d]:
        move_cam_down((UD_mod*movement_mod),cam_class)
    # TO BE REMOVED
    # arrow keys for cam rotation
    if keys[pygame.K_LEFT]:
        cam_class.camRotY += 0.03*pi
    if keys[pygame.K_RIGHT]:
        cam_class.camRotY -= 0.03*pi
    if keys[pygame.K_UP]:
        cam_class.camRotX -= 0.03*pi
    if keys[pygame.K_DOWN]:
        cam_class.camRotX += 0.03*pi
    if keys[pygame.K_COMMA]:
        cam_class.camRotZ += 0.03*pi
    if keys[pygame.K_PERIOD]:
        cam_class.camRotZ -= 0.03*pi
    if keys[pygame.K_z]:
        cam_class.FOV += pi/10
        reCalculateFOV(cam_class)
    if keys[pygame.K_x]:
        cam_class.FOV -= pi/10
        reCalculateFOV(cam_class)

def handle_movement(cam_class,events,keys,mouse_movement):
    for event in events:
        if event.type == pygame.QUIT:
            return "exit"
    if keys[pygame.K_ESCAPE]:
        return "exit"
    #handle_mouse(cam_class,mouse_movement)
    handle_keyboard(cam_class,keys)