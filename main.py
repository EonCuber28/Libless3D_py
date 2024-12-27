# import modules
import pygame, time, object
import render_pipeline
renderer = render_pipeline.renderer()
# define camera variables
camera_x = 0
camera_y = 0
camera_z = 0

camera_yaw = 0
camera_pitch = 0
camera_roll = 0

camera_fov = 60
# start pygame
pygame.init()
# initialise and configure pygame window
window_x = 400
window_y = 400
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
font = pygame.font.Font("/home/pi/python_projects/3d renderer/fonts/Seven Segment.ttf", 15)
vertex_color = (255,255,255)

def get_frame_data(object):
    vertexes,edges,polygons = object
    camera_pos = [camera_x,camera_y,camera_z]
    camera_orientation = [camera_yaw,camera_pitch,camera_roll]
    return renderer.render_object(
        vertexes,edges,polygons, 
        camera_pos, camera_orientation, 
        renderer.calc_focal_length(window_x, camera_fov),
        window_x, window_y)

def proccess_keys():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pass

# start the loop
while True:
    start_time = time.time()
    # proccess key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    # clear screen
    screen.fill(black)
    # draw shapes
    VT,ED,PG = get_frame_data(object.cube())
    renderer.draw(VT,ED,PG, screen, (255,255,255), (255,255,0))
    # calculate render time
    end_time = time.time()
    frame_time = round((end_time-start_time)*1000, 4)
    # update labels
    frame_time_label = font.render(("frame time in ms: "+str(frame_time)), True, white)
    screen.blit(frame_time_label, (3,3))
    # update display
    pygame.display.flip()
    # control FPS
    clock.tick(fps)