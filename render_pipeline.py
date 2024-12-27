from math import sqrt, sin, cos, tan, radians, atan2
import pygame
class renderer:
    def __init__(app):
        app.camera_x = 0
        app.camera_y = 0
        app.camera_z = 0

        app.camera_yaw = 0
        app.camera_pitch = 0
        app.camera_roll = 0
        
        app.camera_fov = 60

    def calc_focal_length(app,screen_x,camera_fov):
        camera_focal_length = (screen_x/2)/tan(camera_fov/2)
        if camera_focal_length < 0:
            camera_focal_length = camera_focal_length*-1
        return camera_focal_length
    # used throught the program for nomalisiong 3d vectors
    def normalise_vector(app,vector):
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
    def rotate_x(app,degree, vertexes):
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
    def rotate_y(app,degree, vertexes):
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
    def rotate_z(app,degree, vertexes):
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
    def translate_vertexes(app,posX,posY,posZ, vertexes):
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
    def scale(app,vertexes, scale=1, scaleX=1,scaleY=1,scaleZ=1):
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

    # normalise vertexes (DONE)
    def normalize_vertexs(app,vertexes):
        # for each vertex
        normal_vertexies = []
        for vertex in vertexes:
           # devide X Y and Z values by W value
            nX = vertex[0]/vertex[3]
            nY = vertex[1]/vertex[3]
            # add the normalised values to a list
            normal_vertexies.append([nX,nY])
        # return normalised values list
        return normal_vertexies

    def military_projection(app,vertexes):
        projected = []
        for vertex in vertexes:
            X,Y,Z = vertex
            if Z == 0:
                Z += 0.0000000000001
            X_proj = X/Z
            Y_proj = Y/Z
            projected.append([X_proj,Y_proj])
        return projected
    def orthographic_projection(app,vertexes):
        projected = []
        for vertex in vertexes:
            X,Y,Z = vertex
            X_proj = X
            Y_proj = Y
            projected.append([X_proj,Y_proj])
        return projected
    def spherical_projection(app,vertexes):
        projected = []
        for vertex in vertexes:
            X,Y,Z = vertex
            X_proj = atan2(X,Y)
            Y_proj = atan2(Z,sqrt(X**2+Y**2))
            projected.append([X_proj,Y_proj])
        return projected
    def isometric_projection(app,vertexes):
        projected = []
        for vertex in vertexes:
            X,Y,Z = vertex
            X_proj = (1/sqrt(2))*X-(1/sqrt(2))*Z
            Y_proj = (1/sqrt(6))*X-(1/sqrt(6))*Z+Y
            projected.append([X_proj,Y_proj])
        return projected
    def weak_perspective_projection(app,vertexes, focal_length):
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
    def convert_normalised_to_screen(app,normal_vertexes, screenX,screenY):
        # convertedX = ((projX+1)/2)*screenX
        # convertedY = ((1-projY)/2)*screenY
        converted_vertexes = []
        for normal_vertex in normal_vertexes:
            convertedX = ((normal_vertex[0]+1)/2)*screenX
            convertedY = ((1-normal_vertex[1])/2)*screenY
            converted_vertexes.append([convertedX,convertedY])
        return converted_vertexes

    # rotates vetexes to camera orientation for proper positioning for rendering (DONE)
    def vertex_rotate_to_camera(app,camera_orientation, vertexes):
        yaw = camera_orientation[0]
        pitch = camera_orientation[1]
        roll = camera_orientation[2]
        # rotate on x
        vertexes = app.rotate_x(roll, vertexes)
        # rotate on y
        vertexes = app.rotate_y(pitch, vertexes)
        # rotate on z
        vertexes = app.rotate_z(yaw, vertexes)
        return vertexes

    # camera matrix (DONE)
    def move_to_camera(app,camera_pos, camera_orientation, vertexo):
        # rotate object to camera
        vertexo = app.vertex_rotate_to_camera(camera_orientation, vertexo)
        # move vertexes to camera
        vertexo = app.translate_vertexes(camera_pos[0],camera_pos[1],camera_pos[2], vertexo)
        return vertexo

    # this proccesses are used to render polygons in the correct order
    def purify_polygon(app,polygon, vertexes):
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
    def find_center_of_polygon(app,polygon):
        Cx = (polygon[0]+polygon[3]+polygon[6])/3
        Cy = (polygon[1]+polygon[4]+polygon[7])/3
        Cz = (polygon[2]+polygon[5]+polygon[8])/3

        return [Cx,Cy,Cz]
    def get_polygon_to_camera_distance(app,polygon,camera_pos):
        camX,camY,camZ = camera_pos
        Px,Py,Pz = app.find_center_of_polygon(polygon)
        Distance = sqrt((camX-Px)**2+(camY-Py)**2+(camZ-Pz)**2)
        if Distance < 0:
            Distance = Distance*-1
        return Distance
    def nearest_point_to_camera_in_polygon(app,polygon, camera_pos):
        PX1,PY1,PZ1, PX2,PY2,PZ2, PX3,PY3,PZ3 = polygon
        camX,camY,camZ = camera_pos
        # get the distance from the point on the polygon to the camera
        P1D = sqrt((PX1-camX)**2+(PY1-camY)**2+(PZ1-camZ)**2)
        P2D = sqrt((PX2-camX)**2+(PY2-camY)**2+(PZ2-camZ)**2)
        P3D = sqrt((PX3-camX)**2+(PY3-camY)**2+(PZ3-camZ)**2)
        # sort rhe list using logic
        if P1D <= P2D:
            if P1D <= P3D:
                return [
                    PX1,PY1,PZ1,
                    PX2,PY2,PZ2,
                    PX3,PY3,PZ3]
        if P2D <= P1D:
            if P2D <= P3D:
                return [
                    PX2,PY2,PZ2,
                    PX1,PY1,PZ1,
                    PX3,PY3,PZ3]
        if P3D <= P2D:
            if P3D <= P1D:
                return [
                    PX3,PY3,PZ3,
                    PX2,PY2,PZ2,
                    PX1,PY1,PZ1]
        return [
            PX1,PY1,PZ1,
            PX2,PY2,PZ2,
            PX3,PY3,PZ3]
    def cull_polygon(app,polygon,camera_pos):
        
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
        NVX,NVY,NVZ = app.normalise_vector([NVX,NVY,NVZ])

        CPX,CPY,CPZ,a,b,c,d,e,f = app.nearest_point_to_camera_in_polygon(polygon, camera_pos)

        #print(CPX,CPY,CPZ)
        #print(camera_pos)
        CVX = camX-CPX
        CVY = camY-CPY
        CVZ = camZ-CPZ
        #print(CVX,CVY,CVZ)
        CVX,CVY,CVZ = app.normalise_vector([CVX,CVY,CVZ])

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
    def sort_polygons(app,polygons, vertexes, camera_pos):
        unsorted_polygons = []
        for polygon in polygons:
            og_polygon = polygon
            # purify polygon
            polygon = app.purify_polygon(polygon, vertexes)
            #print()
            #print(polygon)
            # sort the point on the polygon
            polygon = app.nearest_point_to_camera_in_polygon(polygon, camera_pos)
            #print()
            #print(polygon)
            # cull the polygon
            cull_status = app.cull_polygon(polygon, camera_pos)
            #print()
            #print(cull_status)
            if cull_status == "keep":
                # find the distance between the polygon and the camera
                polygon = [app.get_polygon_to_camera_distance(polygon, camera_pos),og_polygon]
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
    def purify_object_data(app,vertexes, edges, polygons):
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
    def draw_background(app, surface):
        surface.fill((0,0,0))
    # draw vertexes (DONE)
    def draw_vertexes(app,vertexes, surface,color):
        for vertex in vertexes:
            pygame.draw.circle(surface,color,(vertex[0],vertex[1]),5)
    # draw edges (DONE)
    def draw_edges(app,edges, surface,color):
        for edge in edges:
            pygame.draw.line(surface,color,
                [edge[0],edge[1]],
                [edge[2],edge[3]])
    # draw polygons(DONE)
    def draw_polygons(app,polygons, surface):
        for polygon in polygons:
            pygame.draw.polygon(surface,polygon[6],
                [(polygon[0],polygon[1]),
                 (polygon[2],polygon[3]),
                 (polygon[4],polygon[5])])
    # drawing function (DONE)
    def draw(app, vertexes,edges,polygons, surface,Vcolor,Ecolor, render_vertexes=True,render_edges=True,render_polygons=True):
        # draw vertexes
        if render_vertexes == True:
            app.draw_vertexes(vertexes,surface,Vcolor)
        # draw edges
        if render_edges == True:
            app.draw_edges(edges,surface,Ecolor)
        # draw polygons
        if render_polygons == True:
            app.draw_polygons(polygons,surface)

    # render object (WIP)
    def render_object(app,vertexes, edges, polygons, camera_pos, camera_orientation, focal_length,screen_x,screen_y, projection_method=""):
        camera_x,camera_y,camera_z = camera_pos
        camera_yaw,camera_pitch,camera_roll = camera_orientation
        # transfer object vertexes from world coordinates to camera coordinates
        vertexes = app.move_to_camera([camera_x,camera_y,camera_z], [camera_yaw,camera_pitch,camera_roll], vertexes)
        # sort polygons
        #polygons = app.sort_polygons(polygons, vertexes, camera_pos)
        # project vertexes
        if projection_method == "MP":
            vertexes = app.military_projection(vertexes)
        elif projection_method == "OTP":
            vertexes = app.orthographic_projection(vertexes)
        elif projection_method == "SP":
            vertexes = app.spherical_projection(vertexes)
        elif projection_method == "IP":
            vertexes = app.isometric_projection(vertexes)
        else:
            vertexes = app.weak_perspective_projection(vertexes, focal_length)
        # convert normalised to screen
        vertexes = app.convert_normalised_to_screen(vertexes, screen_x,screen_y)
        # purify edges and polygons
        edges,polygons = app.purify_object_data(vertexes, edges, polygons)
        # draw the object
        return vertexes, edges, polygons

    # used for strafing the camera right, left, forward, and backward
    def calc_up_vect(app,yaw,pitch,roll):
        pitch = radians(pitch)
        roll = radians(roll)

        Ux = -sin(roll)*cos(pitch)
        Uy = cos(roll)*cos(pitch)
        Uz = sin(pitch)

        return app.normalise_vector([Ux,Uy,Uz])
    def calc_forward_vect(app,yaw,pitch,roll):
        yaw = radians(yaw)
        pitch = radians(pitch)

        Fx = cos(pitch)*sin(yaw)
        Fy = sin(pitch)
        Fz = cos(pitch)*cos(yaw)

        Nv = app.normalise_vector([Fx,Fy,Fz])
        return(Nv)
    def calc_right_vect(app,yaw,pitch,roll):
        FvX,FvY,FvZ = app.calc_forward_vect(yaw,pitch,roll)
        UvX,UvY,UvZ = app.calc_up_vect(yaw,pitch,roll)

        RvX = UvY*FvZ-UvZ*FvY
        RvY = UvZ*FvX-UvX*FvZ
        RvZ = UvX*FvY-UvY*FvX

        return app.normalise_vector([RvX,RvY,RvZ])


    # some wacky method i found in the internet for moving forward,backward, up,down, left right
    def move_cam_up(app,camera_pos,camera_orientation, amount):
        camX,camY,camZ = camera_pos
        yaw,pitch,roll = camera_orientation

        vX,vY,vZ = app.calc_up_vect(yaw,pitch,roll)

        Px = camX+amount*vX
        Py = camY+amount*vY
        Pz = camZ+amount*vZ

        return [Px,Py,Pz]
    def move_cam_down(app,camera_pos,camera_orientation, amount):
        camX,camY,camZ = camera_pos
        yaw,pitch,roll = camera_orientation

        vX,vY,vZ = app.calc_up_vect(yaw,pitch,roll)

        Px = camX-amount*vX
        Py = camY-amount*vY
        Pz = camZ-amount*vZ

        return [Px,Py,Pz]
    def move_cam_left(app,camera_pos,camera_orientation, amount):
        camX,camY,camZ = camera_pos
        yaw,pitch,roll = camera_orientation

        vX,vY,vZ = app.calc_right_vect(yaw,pitch,roll)

        Px = camX-amount*vX
        Py = camY-amount*vY
        Pz = camZ-amount*vZ

        return [Px,Py,Pz]
    def move_cam_right(app,camera_pos,camera_orientation, amount):
        camX,camY,camZ = camera_pos
        yaw,pitch,roll = camera_orientation

        vX,vY,vZ = app.calc_right_vect(yaw,pitch,roll)

        Px = camX+amount*vX
        Py = camY+amount*vY
        Pz = camZ+amount*vZ

        return [Px,Py,Pz]
    def move_cam_forward(app,camera_pos,camera_orientation, amount):
        camX,camY,camZ = camera_pos
        yaw,pitch,roll = camera_orientation

        vX,vY,vZ = app.calc_forward_vect(yaw,pitch,roll)

        Px = camX+amount*vX
        Py = camY+amount*vY
        Pz = camZ+amount*vZ

        return [Px,Py,Pz]
    def move_cam_backward(app,camera_pos,camera_orientation, amount):
        camX,camY,camZ = camera_pos
        yaw,pitch,roll = camera_orientation

        vX,vY,vZ = app.calc_forward_vect(yaw,pitch,roll)

        Px = camX-amount*vX
        Py = camY-amount*vY
        Pz = camZ-amount*vZ

        return [Px,Py,Pz]

    # render_frame function (DONE)
    def render_frame(app):
        app.calc_focal_length()
        # check amount of objects
        app.proccess_objects()
        # process key presses
        app.proccess_key(app.current_key)
        # draw the background
        app.draw_background()
        # render object
        # cube
        app.render_object(app.object_vertexes,app.object_edges,app.object_polygons,
                 [app.camera_x,app.camera_y,app.camera_z],
                 [app.camera_yaw,app.camera_pitch,app.camera_roll],
                 app.camera_focal_length, app.screen_x,app.screen_y)
        # center of world
        app.render_object(app.cow_vertexes,app.cow_edges,app.cow_polygons,
                 [app.camera_x,app.camera_y,app.camera_z],
                 [app.camera_yaw,app.camera_pitch,app.camera_roll],
                 app.camera_focal_length, app.screen_x,app.screen_y)
        # update display info
        app.update_camera_pos_orientation_text()
