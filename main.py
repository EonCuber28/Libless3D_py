# import modules
import pygame, time, object
import render_pipeline
# start the renderer script
renderer = render_pipeline.renderer()
# start pygame
pygame.init()
# initialise and configure pygame window
window_x = 1050
window_y = 800
window_size = (window_x,window_y)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("3D renderer")
# start pygame clock and fps
clock = pygame.time.Clock()
fps = 60
# set colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
# set the fonts
font = pygame.font.Font("/home/pi/python_projects/3d renderer/fonts/Seven Segment.ttf", 20)
vertex_color = (255,255,255)
edge_color = (0,255,0)

# set courser visibility
pygame.mouse.set_visible(False)

def get_frame_data(object):
    vertexes,edges,polygons = object
    camera_pos = [renderer.camera_x,renderer.camera_y,renderer.camera_z]
    camera_orientation = [renderer.camera_yaw,renderer.camera_pitch,renderer.camera_roll]
    return renderer.render_object(
        vertexes,edges,polygons, 
        camera_pos, camera_orientation, 
        renderer.calc_focal_length(window_x, renderer.camera_fov),
        window_x, window_y, "")

last_frame_keys = pygame.key.get_pressed()
def proccess_keys():
    global last_frame_keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    keys = pygame.key.get_pressed()    
    if keys[pygame.K_w]:
        renderer.camera_x,renderer.camera_y,renderer.camera_z = renderer.move_cam_forward(
            [renderer.camera_x,renderer.camera_y,renderer.camera_z],
            [renderer.camera_yaw,renderer.camera_pitch,renderer.camera_roll],
            0.5)
    if keys[pygame.K_s]:
        renderer.camera_x,renderer.camera_y,renderer.camera_z = renderer.move_cam_backward(
            [renderer.camera_x,renderer.camera_y,renderer.camera_z],
            [renderer.camera_yaw,renderer.camera_pitch,renderer.camera_roll],
            0.5)
    if keys[pygame.K_a]:
        renderer.camera_x,renderer.camera_y,renderer.camera_z = renderer.move_cam_left(
            [renderer.camera_x,renderer.camera_y,renderer.camera_z],
            [renderer.camera_yaw,renderer.camera_pitch,renderer.camera_roll],
            0.02)
    if keys[pygame.K_d]:
        renderer.camera_x,renderer.camera_y,renderer.camera_z = renderer.move_cam_right(
            [renderer.camera_x,renderer.camera_y,renderer.camera_z],
            [renderer.camera_yaw,renderer.camera_pitch,renderer.camera_roll],
            0.02)
    if keys[pygame.K_LSHIFT] or keys[pygame.K_c]:
        renderer.camera_x,renderer.camera_y,renderer.camera_z = renderer.move_cam_down(
            [renderer.camera_x,renderer.camera_y,renderer.camera_z],
            [renderer.camera_yaw,renderer.camera_pitch,renderer.camera_roll],
            -0.05)
    if keys[pygame.K_SPACE]:
        renderer.camera_x,renderer.camera_y,renderer.camera_z = renderer.move_cam_up(
            [renderer.camera_x,renderer.camera_y,renderer.camera_z],
            [renderer.camera_yaw,renderer.camera_pitch,renderer.camera_roll],
            -0.05)
    last_frame_keys = pygame.key.get_pressed()

def proccess_mouse():
    sensityivity = 0.4
    x_intensity = 0.01
    y_intensity = 0.01
    movement = pygame.mouse.get_rel()
    renderer.camera_pitch -= movement[0]*x_intensity*sensityivity
    renderer.camera_roll -= movement[1]*y_intensity*sensityivity

def proccess_gui():
    # position labels
    labelX = font.render("X: "+str(renderer.camera_x), True, white)
    labelY = font.render("Y: "+str(renderer.camera_y), True, white)
    labelZ = font.render("Z: "+str(renderer.camera_z), True, white)
    # orientation labels
    labelYaw = font.render("Yaw: "+str(renderer.camera_yaw), True, white)
    labelPitch = font.render("Pitch: "+str(renderer.camera_pitch), True, white)
    labelRoll = font.render("Roll: "+str(renderer.camera_roll), True, white)
    # add to screen
    screen.blit(labelX, (3,25))
    screen.blit(labelY, (3,45))
    screen.blit(labelZ, (3,65))

    screen.blit(labelYaw, (3,90))
    screen.blit(labelPitch, (3,115))
    screen.blit(labelRoll, (3,135))

# start the loop
while True:
    start_time = time.time()
    # proccess key presses
    proccess_keys()
    # proccess mosuse movement
    proccess_mouse()
    # clear screen
    screen.fill(black)
    # draw shapes
    VT,ED,PG = get_frame_data(object.cube())
    renderer.draw(VT,ED,PG, screen, vertex_color, edge_color)
    # calculate render time
    end_time = time.time()
    frame_time = round((end_time-start_time)*1000, 4)
    # update labels
    frame_time_label = font.render(("frame time in ms: "+str(frame_time)), True, white)
    screen.blit(frame_time_label, (3,3))
    proccess_gui()
    # update display
    pygame.display.flip()
    # control FPS
    clock.tick(fps)