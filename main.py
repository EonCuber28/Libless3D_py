#!/home/pi/python_projects/bin/python3.11
# import pygame
import pygame
# import renderer
from engine.camera import camera, reCalculateFOV, recalc_vects
from engine.rotat_trans_scal import rotate_vertexes
from engine.object_handler import center_object
from math import pi, radians
from controler import handle_movement
from time import time, sleep
from engine.texture_manager import load_texture, resize_texture
from assets.models.cube import cube
from engine.rotat_trans_scal import scale_vertexes, translate_vertexes
from engine.texture_mapper import full_screen_mapping, split_object_polygons_into_tris
from assets.models.python.new_cube import objecto
# set general vars
background_color = (0,0,0)
# prepare the cube
cube = list(cube())
cube = [cube[0],cube[1],cube[2],cube[3]]
cube[0] = translate_vertexes(cube[0],0,0,1)
cube[0] = scale_vertexes(cube[0],0.1,0.1,0.1)
# start camera class
camera_data = camera()
# define camera params
camera_data.camX = 0.25
camera_data.camY = 0.25
camera_data.camZ = 0

camera_data.camRotX = 0
camera_data.camRotY = 0
camera_data.camRotZ = 0

camera_data.FOV = radians(80)
# start the pygame display
# start pygame
pygame.init()
# initialise and configure pygame window
window_x = 80
window_y = 80
camera_data.resX = window_x
camera_data.resY = window_y
reCalculateFOV(camera_data)
game_res = (window_x,window_y)
final_res = (720,720)
game_screen = pygame.Surface(game_res)
user_screen = pygame.display.set_mode(final_res, pygame.RESIZABLE)
pygame.display.set_caption("3D renderer")
# set fps settings
target_fps = 30
target_frame_time = 1/target_fps
print("Frame time limit: "+str(round(target_frame_time*1000,2))+"ms")
texture = load_texture("texture0.jpg")#cube[3])
texture = resize_texture(texture,800,800)
objecto = objecto()
# center cube around the world origen
objecto = center_object(objecto)
# scale cube down
objecto[0] = scale_vertexes(objecto[0], 0.3,0.3,0.3)
# pre process the object into tris
objecto = split_object_polygons_into_tris(objecto)
#objecto[3] = [objecto[3][0],objecto[3][1]]
frame_count = 0
laggy_frames = 0
worst_frame_time = float("-inf")
best_frame_time = float("inf")
total_frame_time = 0
# define UI variables
UI_color = (73, 214, 127)
font = pygame.font.Font(r"C:\Users\zappa\Desktop\Libless3D\Libless3D_py\assets\fonts\Seven Segment.ttf",20)
# upscale the canvas
pygame.transform.scale(game_screen, (500,500))
objecto_Rx = 0.1
objecto_Ry = 0
objecto_Rz = 0
objecto_Tx = 0
objecto_Ty = 0 
objecto_Tz = 0
# start program loop
frame_time = 0.01
while True:
    frame_time_start = time()
    # rotate the cube
    objecto_Rx = pi*0.005
    objecto_Ry = pi*0.005
    objecto_Rz = pi*0.005
    objecto[0] = rotate_vertexes(objecto[0],objecto_Rx,objecto_Ry,objecto_Rz)
    # re calculate the camera vectors
    recalc_vects(camera_data)
    # get events for mouse, keyboard, and pygame window
    pygame_events = pygame.event.get()
    pressed_keys = pygame.key.get_pressed()
    mouse_movent = pygame.mouse.get_rel()
    # handle keyboard/mouse
    if handle_movement(camera_data,pygame_events,pressed_keys,mouse_movent) == "exit":
        print("exit")
        print("frame count: "+str(frame_count))
        print("laggy frames percentage: "+str(round((laggy_frames/frame_count)*100,2))+"%")
        print("best frame time: "+str(round(best_frame_time*1000,2))+"ms")
        print("worst frame time: "+str(round(worst_frame_time*1000,2))+"ms")
        print("average frame time: "+str(round((total_frame_time/frame_count)*1000,2))+"ms")
        pygame.quit()
        quit()
    # render cube
    # clear the screen
    game_screen.fill(background_color)
    # draw the object
    #uv_map_triangles(prep_tris(cube[2],cube[0]),camera_data,texture,screen)
    full_screen_mapping([objecto],{'banan.mtl':texture},camera_data,game_screen)
    # upscale the display
    upscaled_display = pygame.transform.scale(game_screen, final_res)
    user_screen.blit(upscaled_display, (0,0))
    # draw UI
    # fps display
    frametime_text = "Fps: "+str(round(1/frame_time,2))
    frametime_sprite = font.render(frametime_text, True, UI_color)
    user_screen.blit(frametime_sprite, (5,5))
    # cam_x
    frametime_text = "Cam X: "+str(round(camera_data.camX,2))
    frametime_sprite = font.render(frametime_text, True, UI_color)
    user_screen.blit(frametime_sprite, (5,25))
    # cam_y
    frametime_text = "Cam Y: "+str(round(camera_data.camY,2))
    frametime_sprite = font.render(frametime_text, True, UI_color)
    user_screen.blit(frametime_sprite, (5,45))
    # cam_z
    frametime_text = "Cam Z: "+str(round(camera_data.camZ,2))
    frametime_sprite = font.render(frametime_text, True, UI_color)
    user_screen.blit(frametime_sprite, (5,65))
    # cam_Rx
    frametime_text = "Cam Rx: "+str(round(camera_data.camRotX,2))
    frametime_sprite = font.render(frametime_text, True, UI_color)
    user_screen.blit(frametime_sprite, (5,85))
    # cam_Ry
    frametime_text = "Cam Ry: "+str(round(camera_data.camRotY,2))
    frametime_sprite = font.render(frametime_text, True, UI_color)
    user_screen.blit(frametime_sprite, (5,105))
    # cam_Rz
    frametime_text = "Cam Rz: "+str(round(camera_data.camRotZ,2))
    frametime_sprite = font.render(frametime_text, True, UI_color)
    user_screen.blit(frametime_sprite, (5,125))
    # cam_FOV
    frametime_text = "HFL: "+str(round(camera_data.HFL,2))
    frametime_sprite = font.render(frametime_text, True, UI_color)
    user_screen.blit(frametime_sprite, (5,145))
    # update the display
    pygame.display.flip()
    # get frame end time
    frame_time_end = time()
    frame_time = frame_time_end-frame_time_start
    wait_time = target_frame_time-frame_time
    #print("frame time: "+str(round(frame_time*1000,2))+"ms")
    total_frame_time += frame_time
    if wait_time < 0:
        print("LAGGING!!")
        laggy_frames += 1
        wait_time = 0
    if frame_time < best_frame_time:
        best_frame_time = frame_time
    if frame_time > worst_frame_time:
        worst_frame_time = frame_time
    frame_count += 1
    sleep(wait_time)
