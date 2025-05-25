from math import sqrt, sin, cos, tan, radians, atan2
# this is an extremely basic 3d renerer
# (although it might be 917 lines of code)

prog_notes = """
Programmer notes:
The polygon processing is not woring as intedded.
This is becouse many of the calculations 
are flawed. And the general sorting of polygons
can be completeley replaced by cycleing through
distance ranges beteen a near and far plane
from the camera thus properley layering all polygons.
And for some reason the right vertector of the camera
is completeley fine but the forward vector
that it uses to calculate itself if completeley
borked, i dont know why, the camera just moves.
a little funny, for some ungodly reason.
Additionaly i will soon be releasing and working on
a seperate version of this in my github project:
https://github.com/EonCuber28/Libless3D_py
this will be needing the pygame lib to run.
i might work on lighting and textureing later.
the intention of this project is to create aT
CPU based rendering engine without OpenGL.
no gpu accelleration.
at all."""
controls_text = """CONTROLS:
W: move the camera forward (dosent do this in some cases)
S: move the camera backward (same problem as key W)
A: strafe the camera left (different on different systems)
D: strafe the camera rigth (different on different systems)

C: move the camera down(happens for most projection mothods)
Space: move the camera up (same problem as key C)

Up: increase roll
Down: decrease roll
Left: increase pitch
Right: decrease pitch

<: increase yaw
>: decrease yaw

Z: increase fov
X: decrease fov

1: use weak perspective projection (uses fov and focal length)
2: use military projection
3: use orthographic projection
4: use spherical projection
5: use isometric projection
8: toggle vertex rendering
9: toggle edge rendering
0: toggle polgyon rendering

H: toggles this menu"""

# edge and vertex colors
app.vertex_color = "red"
app.edge_color = "green"

# defines stuff for drawing the object
app.object_limit = 100

app.object_group = Group()

app.shape_count = 0
# center of world vertexes and edges
app.cow_vertexes = [
    [0,0,0],
    [0.5,0,0],
    [0,0.5,0],
    [0,0,0.5]]
app.cow_edges = [
    [0,1],
    [0,2],
    [0,3],
    [1,2],
    [1,3],
    [2,3]]
app.cow_polygons = [
    [0,1,2, [255,0,0]],
    [0,1,3, [0,0,255]],
    [0,2,3, [0,255,0]]]
# object data (WIP)
app.object_vertexes = [
    #X,Y,Z, W(for normalization)
    [0,0,0],
    [1,0,0],
    [0,1,0],
    [1,1,0],
    [0,0,1],
    [1,0,1],
    [0,1,1],
    [1,1,1]
    ]
app.object_edges = [
    [6,7],
    [7,5],
    [5,4],
    [4,6],
    
    [7,3],
    [5,1],
    [4,0],
    [2,6],
    
    [2,3],
    [3,1],
    [1,0],
    [0,2],
    
    [5,0],
    [2,4],
    [2,7],
    [6,5],
    [1,7],
    [3,0]]
app.object_polygons = [
    [0,3,1, [255,0,0]],
    [0,3,2, [255,0,0]],
    
    [2,0,4, [0,255,0]],
    [6,2,4, [0,255,0]],
    
    [2,7,6, [255,255,0]],
    [2,3,7, [255,255,0]],
    
    [0,4,5, [0,0,255]],
    [0,1,5, [0,0,255]],
    
    [3,1,7, [255,0,255]],
    [7,1,5, [255,0,255]],
    
    [7,6,5, [0,255,255]],
    [6,5,4, [0,255,255]]]

# screen data (DONE)
app.screen_x = 400
app.screen_y = 400

# camera data (DONE)
app.camera_fov = 60

def calc_focal_length():
    app.camera_focal_length = (app.screen_x/2)/tan(app.camera_fov/2)
    if app.camera_focal_length < 0:
        app.camera_focal_length = app.camera_focal_length*-1
calc_focal_length()

app.camera_x = -0.25
app.camera_y = -0.25
app.camera_z = 0

app.camera_yaw = 0
app.camera_pitch = 0
app.camera_roll = 0

# camera position and orientation text
app.prog_txt = Group()
starting_y = 30
constant_x = 200
y_step = 16
prev_y = starting_y
for line in prog_notes.split('\n'):
    app.prog_txt.add(Label(line, constant_x,prev_y, fill='cornflowerBlue', size=16))
    prev_y += y_step
app.prog_txt.visible = False

app.controls_menu = Group()
starting_y = 50
constant_x = 200
y_step = 10
prev_y = starting_y
for line in controls_text.split('\n'):
    app.controls_menu.add(Label(line, constant_x,prev_y, fill="crimson"))
    prev_y += y_step
app.controls_menu.visible = False

app.x_txt = Label(("X: "+str(app.camera_x)), 30,10)
app.y_txt = Label(("Y: "+str(app.camera_y)), 30,25)
app.z_txt = Label(("Z: "+str(app.camera_z)), 30,40)

app.yaw_txt = Label(("Yaw: "+str(app.camera_yaw)), 370,10)
app.pitch_txt = Label(("Pitch: "+str(app.camera_pitch)), 370,25)
app.roll_txt = Label(("Roll: "+str(app.camera_roll)), 370,40)

app.fov_txt = Label("FOV: "+str(pythonRound(app.camera_fov)),40,390)
app.focal_length_txt = Label("Focal length: "+str(pythonRound(app.camera_focal_length)),200,10)
app.mode_txt = Label("Using: Weak perspective projection",170,390)

app.controls_txt = Group(
Label("H = toggle control menu",335,390))
# used throught the program for nomalisiong 3d vectors
def normalise_vector(vector):
    if vector == [0,0,0]:
        return [1,1,1]
    # find the vector length
    # using Vl = sqrt(Vx^2+Vy^2+Vz^2)
    Vl = sqrt(vector[0]**2+vector[1]**2+vector[2]**2)
    # devide vector values by vector length
    nVx = vector[0]/Vl
    nVy = vector[1]/Vl
    nVz = vector[2]/Vl
    # return final vector values
    return [nVx,nVy,nVz]
# rotation matrixes (DONE)
# x (DONE)
def rotate_x(degree, vertexes):
    # X' = x
    # y' = y*cos(degree)-z*sin(degree)
    # z' = y*sin(degree)+z*cos(degree)
    rotate_vertexo = []
    for vertex in vertexes:
        newX = vertex[0]
        newY = vertex[1]*cos(degree)-vertex[2]*sin(degree)
        newZ = vertex[1]*sin(degree)+vertex[2]*cos(degree)
        rotate_vertexo.append([newX,newY,newZ])
    return rotate_vertexo

# y (DONE)
def rotate_y(degree, vertexes):
    # X' = X*cos(degree)+Z*sin(degree)
    # Y' = Y
    # z' = -X*sin(degree)+Z*cos(degree)
    rotate_vertexo = []
    for vertex in vertexes:
        newX = vertex[0]*cos(degree)+vertex[2]*sin(degree)
        newY = vertex[1]
        newZ = -vertex[0]*sin(degree)+vertex[2]*cos(degree)
        rotate_vertexo.append([newX,newY,newZ])
    return rotate_vertexo

# z (DONE)
def rotate_z(degree, vertexes):
    # X' = X*cos(degree)-Y*sin(degree)
    # Y' = X*sin(degree)+Y*cos(degree)
    # Z' = Z
    rotate_vertexo = []
    for vertex in vertexes:
        newX = vertex[0]*cos(degree)-vertex[1]*sin(degree)
        newY = vertex[0]*sin(degree)+vertex[1]*cos(degree)
        newZ = vertex[2]
        rotate_vertexo.append([newX,newY,newZ])
    return rotate_vertexo

# translation matrix (DONE)
def translate_vertexes(posX,posY,posZ, vertexes):
    # X' = X+pos_X
    # Y' = Y+pos_Y
    # Z' = Z+pos_Z
    rotate_vertexo = []
    for vertex in vertexes:
        newX = vertex[0]+posX
        newY = vertex[1]+posY
        newZ = vertex[2]+posZ
        rotate_vertexo.append([newX,newY,newZ])
    return rotate_vertexo

# scale matrix (DONE)
def scale(vertexes, scale=1, scaleX=1,scaleY=1,scaleZ=1):
    # X' = X*scaleX
    # Y' = Y*scaleY
    # Z' = Z*scaleZ
    rotate_vertexo = []
    for vertex in vertexes:
        newX = vertex[0]*scaleX*scale
        newY = vertex[1]*scaleY*scale
        newZ = vertex[2]*scaleZ*scale
        rotate_vertexo.append([newX,newY,newZ])
    return rotate_vertexo

app.cow_vertexes = translate_vertexes(-0.5,-0.5,-0.5, app.cow_vertexes)

# normalise vertexes (DONE)
def normalize_vertexs(vertexes):
    # for each vertex
    normal_vertexies = []
    for vertex in vertexes:
        # devide X Y and Z values by W value
        nX = vertex[0]/vertex[3]
        nY = vertex[1]/vertex[3]
        # add the normalised values to a list
        normal_vertexes.append([nX,nY])
    # return normalised values list
    return normal_vertexies

def military_projection(vertexes):
    projected = []
    for vertex in vertexes:
        X,Y,Z = vertex
        if Z == 0:
            Z += 0.0000000000001
        X_proj = X/Z
        Y_proj = Y/Z
        projected.append([X_proj,Y_proj])
    return projected
def orthographic_projection(vertexes):
    projected = []
    for vertex in vertexes:
        X,Y,Z = vertex
        X_proj = X
        Y_proj = Y
        projected.append([X_proj,Y_proj])
    return projected
def spherical_projection(vertexes):
    projected = []
    for vertex in vertexes:
        X,Y,Z = vertex
        X_proj = atan2(X,Y)
        Y_proj = atan2(Z,sqrt(X**2+Y**2))
        projected.append([X_proj,Y_proj])
    return projected
def isometric_projection(vertexes):
    projected = []
    for vertex in vertexes:
        X,Y,Z = vertex
        X_proj = (1/sqrt(2))*X-(1/sqrt(2))*Z
        Y_proj = (1/sqrt(6))*X-(1/sqrt(6))*Z+Y
        projected.append([X_proj,Y_proj])
    return projected
def weak_perspective_projection(vertexes, focal_length):
    # use projection method for this proccess
    # projecttion math from: [instert matbatwings yt vid]
    projected = []
    for vertex in vertexes:
        X,Y,Z = vertex
        # X porjected/X = Focal length/Focal length + Z
        # becomes
        # X projected = Focal Lenght * X/Focal Length + Z
        X_proj = (focal_length*X)/(focal_length+Z)
        # Y projected = Focal lenght * Y/Focal Lenght + Z
        Y_proj = (focal_length*Y)/(focal_length+Z)
        projected.append([X_proj,Y_proj])
    return projected

# from normal coordinate to screen coordinate matrx (DONE)
def convert_normalised_to_screen(normal_vertexes, screenX,screenY):
    # convertedX = ((projX+1)/2)*screenX
    # convertedY = ((1-projY)/2)*screenY
    converted_vertexes = []
    for normal_vertex in normal_vertexes:
        convertedX = ((normal_vertex[0]+1)/2)*screenX
        convertedY = ((1-normal_vertex[1])/2)*screenY
        converted_vertexes.append([convertedX,convertedY])
    return converted_vertexes

# rotates vetexes to camera orientation for proper positioning for rendering (DONE)
def vertex_rotate_to_camera(camera_orientation, vertexes):
    yaw = camera_orientation[0]
    pitch = camera_orientation[1]
    roll = camera_orientation[2]
    # rotate on x
    vertexes = rotate_x(roll, vertexes)
    # rotate on y
    vertexes = rotate_y(pitch, vertexes)
    # rotate on z
    vertexes = rotate_z(yaw, vertexes)
    return vertexes

# camera matrix (DONE)
def move_to_camera(camera_pos, camera_orientation, vertexo):
    # rotate object to camera
    vertexo = vertex_rotate_to_camera(camera_orientation, vertexo)
    # move vertexes to camera
    vertexo = translate_vertexes(camera_pos[0],camera_pos[1],camera_pos[2], vertexo)
    return vertexo

# this proccesses are used to render polygons in the correct order
def purify_polygon(polygon, vertexes):
    Px1 = vertexes[polygon[0]][0]
    Py1 = vertexes[polygon[0]][1]
    Pz1 = vertexes[polygon[0]][2]
    
    Px2 = vertexes[polygon[1]][0]
    Py2 = vertexes[polygon[1]][1]
    Pz2 = vertexes[polygon[1]][2]
    
    Px3 = vertexes[polygon[2]][0]
    Py3 = vertexes[polygon[2]][1]
    Pz3 = vertexes[polygon[2]][2]
    var = [
        Px1,Py1,Pz1,
        Px2,Py2,Pz2,
        Px3,Py3,Pz3]
    return var
def find_center_of_polygon(polygon):
    Cx = (polygon[0]+polygon[3]+polygon[6])/3
    Cy = (polygon[1]+polygon[4]+polygon[7])/3
    Cz = (polygon[2]+polygon[5]+polygon[8])/3
    
    return [Cx,Cy,Cz]
def get_polygon_to_camera_distance(polygon,camera_pos):
    camX,camY,camZ = camera_pos
    Px,Py,Pz = find_center_of_polygon(polygon)
    Distance = sqrt((camX-Px)**2+(camY-Py)**2+(camZ-Pz)**2)
    if Distance < 0:
        Distance = Distance*-1
    return Distance
def nearest_point_to_camera_in_polygon(polygon, camera_pos):
    PX1,PY1,PZ1, PX2,PY2,PZ2, PX3,PY3,PZ3 = polygon
    camX,camY,camZ = camera_pos
    # get the distance from the point on the polygon to the camera
    P1D = sqrt((PX1-camX)**2+(PY1-camY)**2+(PZ1-camZ)**2)
    P2D = sqrt((PX2-camX)**2+(PY2-camY)**2+(PZ2-camZ)**2)
    P3D = sqrt((PX3-camX)**2+(PY3-camY)**2+(PZ3-camZ)**2)
    #print()
    #print(P1D,P2D,P3D)
    # sort rhe list using logic
    if P1D <= P2D:
        if P1D <= P3D:
            #print(P1D)
            return [
                PX1,PY1,PZ1,
                PX2,PY2,PZ2,
                PX3,PY3,PZ3]
    if P2D <= P1D:
        if P2D <= P3D:
            #print(P2D)
            return [
                PX2,PY2,PZ2,
                PX1,PY1,PZ1,
                PX3,PY3,PZ3]
    if P3D <= P2D:
        if P3D <= P1D:
            #print(P3D)
            return [
                PX3,PY3,PZ3,
                PX2,PY2,PZ2,
                PX1,PY1,PZ1]
    #print("nothin",P1D)
    return [
        PX1,PY1,PZ1,
        PX2,PY2,PZ2,
        PX3,PY3,PZ3]
def cull_polygon(polygon,camera_pos):
    
    camX,camY,camZ = camera_pos
    
    P1X = polygon[0]
    P1Y = polygon[1]
    P1Z = polygon[2]
    
    P2X = polygon[3]
    P2Y = polygon[4]
    P2Z = polygon[5]
    
    P3X = polygon[6]
    P3Y = polygon[7]
    P3Z = polygon[8]
    
    V1X = P2X-P1X
    V1Y = P2Y-P1Y
    V1Z = P2Z-P1Z
    
    V2X = P3X-P1X
    V2Y = P3Y-P1Y
    V2Z = P3Z-P1Z
    
    NVX = V1Y*V2Z-V1Z*V2Y
    NVY = -(V1X*V2Z-V1Z*V2X)
    NVZ = V1Z*V2Y-V1Y*V2X
    NVX,NVY,NVZ = normalise_vector([NVX,NVY,NVZ])
    
    CPX,CPY,CPZ,a,b,c,d,e,f = nearest_point_to_camera_in_polygon(polygon, camera_pos)
    
    #print(CPX,CPY,CPZ)
    #print(camera_pos)
    CVX = camX-CPX
    CVY = camY-CPY
    CVZ = camZ-CPZ
    #print(CVX,CVY,CVZ)
    CVX,CVY,CVZ = normalise_vector([CVX,CVY,CVZ])
    
    dot = (NVX*CVX+NVY*CVY+NVZ*CVZ)
    
    #print("dot product: ",dot)
    #print("normal vector: ",NVX,NVY,NVZ)
    #print("camera vector:",CVX,CVY,CVZ)
    
    if dot > 0:
        return "keep"
    if dot == 0:
        return "keep"
    if dot < 0:
        return None
def sort_polygons(polygons, vertexes, camera_pos):
    #print()
    #print()
    #print(polygons)
    #print()
    #print(vertexes)
    #print()
    #print(camera_pos)
    unsorted_polygons = []
    for polygon in polygons:
        og_polygon = polygon
        # purify polygon
        polygon = purify_polygon(polygon, vertexes)
        #print()
        #print(polygon)
        # sort the point on the polygon
        polygon = nearest_point_to_camera_in_polygon(polygon, camera_pos)
        #print()
        #print(polygon)
        # cull the polygon
        cull_status = cull_polygon(polygon, camera_pos)
        #print()
        #print(cull_status)
        if cull_status == "keep":
            # find the distance between the polygon and the camera
            polygon = [get_polygon_to_camera_distance(polygon, camera_pos),og_polygon]
            unsorted_polygons.append(polygon)
    #print()
    #print(unsorted_polygons)
    #print()
    # sort the polygons based on distance to camera
    sorted_polygons = []
    temp_list = unsorted_polygons
    #print()
    #print(temp_list)
    for x in unsorted_polygons:
        next_list = temp_list
        temp_list = []
        lh_value = [0,[0,0,0]]
        for y in next_list:
            if y[0] >= lh_value[0]:
                if lh_value[0] != 0:
                    temp_list.append(lh_value)
                lh_value = y
            else:
                temp_list.append(y)
        #print(lh_value)
        sorted_polygons.append(lh_value[1])
    # return sorted list
    #print()
    #print(sorted_polygons)
    return sorted_polygons

# conevrt polygons and edge indixes to coordinates (DONE)
def purify_object_data(vertexes, edges, polygons):
    pure_polygons = []
    for polygon in polygons:
        Px1 = vertexes[polygon[0]][0]
        Py1 = vertexes[polygon[0]][1]
        Px2 = vertexes[polygon[1]][0]
        Py2 = vertexes[polygon[1]][1]
        Px3 = vertexes[polygon[2]][0]
        Py3 = vertexes[polygon[2]][1]
        pure_polygons.append([
            Px1,Py1,
            Px2,Py2,
            Px3,Py3,
            polygon[3]])
    pure_edges = []
    for edge in edges:
        Px1 = vertexes[edge[0]][0]
        Py1 = vertexes[edge[0]][1]
        Px2 = vertexes[edge[1]][0]
        Py2 = vertexes[edge[1]][1]
        pure_edges.append([
            Px1,Py1,
            Px2,Py2])
    # return purified lists
    return pure_edges, pure_polygons

# draw background (DONE)
def draw_background():
    app.object_group.add(Rect(0,0, 400,400, fill="white"))
    app.shape_count += 1

# draw vertexes (DONE)
def draw_vertexes(vertexes):
    # optimisation
    vertex_color = app.vertex_color
    # loop through all vertexes
    for vertex in vertexes:
        # draw the vertexes
        app.object_group.add(Circle(vertex[0],vertex[1],5, fill=vertex_color))
        app.shape_count += 1

# draw edges (DONE)
def draw_edges(edges):
    # optimisation
    edge_color = app.edge_color
    # loop through all edges
    for edge in edges:
        # draw the edge
        app.object_group.add(Line(edge[0],edge[1], edge[2],edge[3], fill=edge_color))
        app.shape_count += 1

# draw polygons(DONE)
def draw_polygons(polygons):
    # loop thorough all polygons
    for polygon in polygons:
        # draw the polygon
        app.object_group.add(Polygon(
            polygon[0],polygon[1], 
            polygon[2],polygon[3], 
            polygon[4],polygon[5], 
            fill=rgb(polygon[6][0],polygon[6][1],polygon[6][2])))
        app.shape_count += 1

app.render_polygons = False
app.render_edges = True
app.render_vertexes = True
# drawing function (DONE)
def draw(vertexes, edges, polygons):
    # draw vertexes
    if app.render_vertexes == True:
        draw_vertexes(vertexes)
    # draw edges
    if app.render_edges == True:
        draw_edges(edges)
    # draw polygons
    if app.render_polygons == True:
        draw_polygons(polygons)

app.projection_method = "WPP"
# render object (WIP)
def render_object(vertexes, edges, polygons, camera_pos, camera_orientation, focal_length,screen_x,screen_y):
    camera_x,camera_y,camera_z = camera_pos
    camera_yaw,camera_pitch,camera_roll = camera_orientation
    # transfer object vertexes from world coordinates to camera coordinates
    vertexes = move_to_camera([camera_x,camera_y,camera_z], [camera_yaw,camera_pitch,camera_roll], vertexes)
    # sort polygons
    polygons = sort_polygons(polygons, vertexes, camera_pos)
    # project vertexes
    if app.projection_method == "MP":
        vertexes = military_projection(vertexes)
    elif app.projection_method == "OTP":
        vertexes = orthographic_projection(vertexes)
    elif app.projection_method == "SP":
        vertexes = spherical_projection(vertexes)
    elif app.projection_method == "IP":
        vertexes = isometric_projection(vertexes)
    else:
        vertexes = weak_perspective_projection(vertexes, focal_length)
    # convert normalised to screen
    vertexes = convert_normalised_to_screen(vertexes, screen_x,screen_y)
    # purify edges and polygons
    edges,polygons = purify_object_data(vertexes, edges, polygons)
    # draw the object
    draw(vertexes, edges, polygons)

# proccess camera movement (DONE)
app.current_key = ""
def onKeyPress(keys):
    app.current_key = keys

def onKeyRelease(key):
    app.current_key = ""

# used for strafing the camera right, left, forward, and backward
def calc_up_vect(yaw,pitch,roll):
    pitch = radians(pitch)
    roll = radians(roll)
    
    Ux = -sin(roll)*cos(pitch)
    Uy = cos(roll)*cos(pitch)
    Uz = sin(pitch)
    
    return normalise_vector([Ux,Uy,Uz])
def calc_forward_vect(yaw,pitch,roll):
    yaw = radians(yaw)
    pitch = radians(pitch)
    
    Fx = cos(pitch)*sin(yaw)
    Fy = sin(pitch)
    Fz = cos(pitch)*cos(yaw)
    
    Nv = normalise_vector([Fx,Fy,Fz])
    return(Nv)
def calc_right_vect(yaw,pitch,roll):
    FvX,FvY,FvZ = calc_forward_vect(yaw,pitch,roll)
    UvX,UvY,UvZ = calc_up_vect(yaw,pitch,roll)
    
    RvX = UvY*FvZ-UvZ*FvY
    RvY = UvZ*FvX-UvX*FvZ
    RvZ = UvX*FvY-UvY*FvX
    
    return normalise_vector([RvX,RvY,RvZ])


# some wacky method i found in the internet for moving forward,backward, up,down, left right
def move_cam_up(camera_pos,camera_orientation, amount):
    camX,camY,camZ = camera_pos
    yaw,pitch,roll = camera_orientation
    
    vX,vY,vZ = calc_up_vect(yaw,pitch,roll)
    
    Px = camX+amount*vX
    Py = camY+amount*vY
    Pz = camZ+amount*vZ
    
    return [Px,Py,Pz]
def move_cam_down(camera_pos,camera_orientation, amount):
    camX,camY,camZ = camera_pos
    yaw,pitch,roll = camera_orientation
    
    vX,vY,vZ = calc_up_vect(yaw,pitch,roll)
    
    Px = camX-amount*vX
    Py = camY-amount*vY
    Pz = camZ-amount*vZ
    
    return [Px,Py,Pz]
def move_cam_left(camera_pos,camera_orientation, amount):
    camX,camY,camZ = camera_pos
    yaw,pitch,roll = camera_orientation
    
    vX,vY,vZ = calc_right_vect(yaw,pitch,roll)
    
    Px = camX-amount*vX
    Py = camY-amount*vY
    Pz = camZ-amount*vZ
    
    return [Px,Py,Pz]
def move_cam_right(camera_pos,camera_orientation, amount):
    camX,camY,camZ = camera_pos
    yaw,pitch,roll = camera_orientation
    
    vX,vY,vZ = calc_right_vect(yaw,pitch,roll)
    
    Px = camX+amount*vX
    Py = camY+amount*vY
    Pz = camZ+amount*vZ
    
    return [Px,Py,Pz]
def move_cam_forward(camera_pos,camera_orientation, amount):
    camX,camY,camZ = camera_pos
    yaw,pitch,roll = camera_orientation
    
    vX,vY,vZ = calc_forward_vect(yaw,pitch,roll)
    
    Px = camX+amount*vX
    Py = camY+amount*vY
    Pz = camZ+amount*vZ
    
    return [Px,Py,Pz]
def move_cam_backward(camera_pos,camera_orientation, amount):
    camX,camY,camZ = camera_pos
    yaw,pitch,roll = camera_orientation
    
    vX,vY,vZ = calc_forward_vect(yaw,pitch,roll)
    
    Px = camX-amount*vX
    Py = camY-amount*vY
    Pz = camZ-amount*vZ
    
    return [Px,Py,Pz]

def proccess_key(keys):
    # w=forward
    if keys == 's':
        app.camera_x,app.camera_y,app.camera_z = move_cam_forward(
            [app.camera_x,app.camera_y,app.camera_z],
            [app.camera_yaw,app.camera_pitch,app.camera_roll],
            0.5)
    # s=backward
    elif keys == 'w':
        app.camera_x,app.camera_y,app.camera_z = move_cam_backward(
            [app.camera_x,app.camera_y,app.camera_z],
            [app.camera_yaw,app.camera_pitch,app.camera_roll],
            0.5)
    # a=strafe left
    elif keys == 'd':
        app.camera_x,app.camera_y,app.camera_z = move_cam_left(
            [app.camera_x,app.camera_y,app.camera_z],
            [app.camera_yaw,app.camera_pitch,app.camera_roll],
            0.1)
    # d=strafe right
    elif keys == 'a':
        app.camera_x,app.camera_y,app.camera_z = move_cam_right(
            [app.camera_x,app.camera_y,app.camera_z],
            [app.camera_yaw,app.camera_pitch,app.camera_roll],
            0.1)
    # space=go uppies
    elif keys == "space":
        app.camera_x,app.camera_y,app.camera_z = move_cam_up(
            [app.camera_x,app.camera_y,app.camera_z],
            [app.camera_yaw,app.camera_pitch,app.camera_roll],
            0.1)
    # c=go down
    elif keys == "c":
        app.camera_x,app.camera_y,app.camera_z = move_cam_down(
            [app.camera_x,app.camera_y,app.camera_z],
            [app.camera_yaw,app.camera_pitch,app.camera_roll],
            0.1)
    # up=look up
    elif keys == 'up':
        app.camera_roll += 0.05
    # down=look down
    elif keys == 'down':
        app.camera_roll -= 0.05
    # left=look left
    elif keys == 'left':
        app.camera_pitch += 0.1
    # right=look right
    elif keys == 'right':
        app.camera_pitch -= 0.1
    # < = roll rigt
    elif keys == ",":
        app.camera_yaw += 0.1
    # > = roll left
    elif keys == ".":
        app.camera_yaw -= 0.1
    # increase camera fov
    elif keys == "z":
        app.camera_fov += 0.1
    # decrease camera fov
    elif keys == "x":
        app.camera_fov -= 0.1
    elif keys == "":
        pass
    # 0 = toggle polygon rendering
    elif keys == "0":
        if app.render_polygons == True:
            app.render_polygons = False
        else:
            app.render_polygons = True
    elif keys == "9":
        if app.render_edges == True:
            app.render_edges = False
        else:
            app.render_edges = True
    elif keys == "8":
        if app.render_vertexes == True:
            app.render_vertexes = False
        else:
            app.render_vertexes = True
    elif keys == "1":
        app.projection_method = "WPP"
        app.mode_txt.value = "Using: Weak perspective projection"
    elif keys == "2":
        app.projection_method = "MP"
        app.mode_txt.value = "Using: Military projection"
    elif keys == "3":
        app.projection_method = "OTP"
        app.mode_txt.value = "Using: Orthographic projection"
    elif keys == "4":
        app.projection_method = "SP"
        app.mode_txt.value = "Using: Spherical projection"
    elif keys == "5":
        app.projection_method = "IP"
        app.mode_txt.value = "Using: Isometric projection"
    elif keys == "h":
        if app.prog_txt.visible == True:
            app.prog_txt.visible = False
        if app.controls_menu.visible == True:
            app.controls_menu.visible = False
        else:
            app.controls_menu.visible = True
    elif keys == "p":
        if app.controls_menu.visible == True:
            app.controls_menu.visible = False
        if app.prog_txt.visible == True:
            app.prog_txt.visible = False
        else:
            app.prog_txt.visible = True
    else:
        print("WAT IS "+str(keys))

# does what is says
def update_camera_pos_orientation_text():
    # update pos
    app.x_txt.value = "X: "+str(pythonRound(app.camera_x,1))
    app.x_txt.toFront()
    app.y_txt.value = "Y: "+str(pythonRound(app.camera_y,1))
    app.y_txt.toFront()
    app.z_txt.value = "Z: "+str(pythonRound(app.camera_z,1))
    app.z_txt.toFront()
    # update orientation
    app.yaw_txt.value = "Yaw: "+str(pythonRound(app.camera_yaw,1))
    app.yaw_txt.toFront()
    app.pitch_txt.value = "Pitch: "+str(pythonRound(app.camera_pitch,1))
    app.pitch_txt.toFront()
    app.roll_txt.value = "Roll: "+str(pythonRound(app.camera_roll,1))
    app.roll_txt.toFront()
    app.focal_length_txt.value = (" Focal length: "+str(pythonRound(app.camera_focal_length, 5)))
    app.focal_length_txt.toFront()
    app.fov_txt.value = "FOV: "+str(pythonRound(app.camera_fov,5))
    app.fov_txt.toFront()
    app.prog_txt.toFront()
    app.controls_menu.toFront()

def proccess_objects():
    app.shape_count = 0
    app.object_group.clear()


# onStep function (DONE)
app.stepsPerSecond = 30
def onStep():
    calc_focal_length()
    # check amount of objects
    proccess_objects()
    # process key presses
    proccess_key(app.current_key)
    # draw the background
    draw_background()
    # render object
    # cube
    render_object(app.object_vertexes,app.object_edges,app.object_polygons,
             [app.camera_x,app.camera_y,app.camera_z],
             [app.camera_yaw,app.camera_pitch,app.camera_roll],
             app.camera_focal_length, app.screen_x,app.screen_y)
    # center of world
    render_object(app.cow_vertexes,app.cow_edges,app.cow_polygons,
             [app.camera_x,app.camera_y,app.camera_z],
             [app.camera_yaw,app.camera_pitch,app.camera_roll],
             app.camera_focal_length, app.screen_x,app.screen_y)
    # update display info
    update_camera_pos_orientation_text()
