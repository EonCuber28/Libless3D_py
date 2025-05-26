## DEPRECATED ##
from math import sqrt, sin, cos, tan, radians, atan2, atan
import pygame
from engine.polygon_proccesing import *
class renderer:
    def __init__(app):
        app.proccess_polygons = True

        app.projection_method = ""

        app.near_plane = 0.000001
        app.far_plane = 1000000
        app.view_planes = [app.near_plane,app.far_plane]

        app.window_h = 500
        app.window_w = 500
        app.aspect_ratio = app.window_w/app.window_h

        app.camera_x = 2
        app.camera_y = -25
        app.camera_z = 5

        app.camera_yaw = 0
        app.camera_pitch = 0
        app.camera_roll = -1.55
        
        app.camera_fov = 120
        app.camera_vfov = app.camera_fov
        app.camera_hfov = 2*atan(tan(radians(app.camera_vfov)/2)*app.aspect_ratio)
        app.camera_fov_data = [app.camera_hfov,app.camera_vfov]
        app.camera_focal_lenght = app.calc_focal_length(app.window_w,app.camera_fov)

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
            rotate_vertexo.append([newX,newY,newZ, vertex[3]])
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
            rotate_vertexo.append([newX,newY,newZ, vertex[3]])
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
            rotate_vertexo.append([newX,newY,newZ, vertex[3]])
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
            rotate_vertexo.append([newX,newY,newZ, vertex[3]])
        return rotate_vertexo

    # scale matrix (DONE)
    def scale(app,vertexes, scale=1, scaleX=1,scaleY=1,scaleZ=1,scaleW=1):
        # X' = X*scaleX
        # Y' = Y*scaleY
        # Z' = Z*scaleZ
        rotate_vertexo = []
        for vertex in vertexes:
            newX = vertex[0]*scaleX*scale
            newY = vertex[1]*scaleY*scale
            newZ = vertex[2]*scaleZ*scale
            newW = vertex[3]*scaleW*scale
            rotate_vertexo.append([newX,newY,newZ,newW])
        return rotate_vertexo

    # normalise polygons (DONE)
    def normalise_polygons(app,polygons):
        normalised_polygons = []
        for polygon in polygons:
            print(polygon)
            px1 = polygon[0]/polygon[3]
            py1 = polygon[1]/polygon[3]
            pz1 = polygon[2]/polygon[3]

            px2 = polygon[4]/polygon[7]
            py2 = polygon[5]/polygon[7]
            pz2 = polygon[6]/polygon[7]

            px3 = polygon[8]/polygon[11]
            py3 = polygon[9]/polygon[11]
            pz3 = polygon[10]/polygon[11]
            # project the points on the polygon
            if app.projection_method == "OTP":
                px1,py1 = app.orthographic_projection([[px1,py1,pz1]])[0]
                px2,py2 = app.orthographic_projection([[px2,py2,pz2]])[0]
                px3,py3 = app.orthographic_projection([[px3,py3,pz3]])[0]
            elif app.projection_method == "MP":
                px1,py1 = app.military_projection([[px1,py1,pz1]])[0]
                px2,py2 = app.military_projection([[px2,py2,pz2]])[0]
                px3,py3 = app.military_projection([[px3,py3,pz3]])[0]
            elif app.projection_method == "SP":
                px1,py1 = app.spherical_projection([[px1,py1,pz1]])[0]
                px2,py2 = app.spherical_projection([[px2,py2,pz2]])[0]
                px3,py3 = app.spherical_projection([[px3,py3,pz3]])[0]
            elif app.projection_method == "IP":
                px1,py1 = app.isometric_projection([[px1,py1,pz1]])[0]
                px2,py2 = app.isometric_projection([[px2,py2,pz2]])[0]
                px3,py3 = app.isometric_projection([[px3,py3,pz3]])[0]
            else:
                px1,py1 = app.weak_perspective_projection([[px1,py1,pz1]],app.camera_focal_lenght)[0]
                px2,py2 = app.weak_perspective_projection([[px2,py2,pz2]],app.camera_focal_lenght)[0]
                px3,py3 = app.weak_perspective_projection([[px3,py3,pz3]],app.camera_focal_lenght)[0]
            # transfer into screen coordinates
            px1,py1 = app.convert_normalised_to_screen([[px1,py1]],app.window_w,app.window_h)[0]
            px2,py2 = app.convert_normalised_to_screen([[px2,py2]],app.window_w,app.window_h)[0]
            px3,py3 = app.convert_normalised_to_screen([[px3,py3]],app.window_w,app.window_h)[0]
            # add
            normalised_polygons.append([
                px1,py1,
                px2,py2,
                px3,py3,
                polygon[12]
            ])
        return normalised_polygons
    # normalise vertexes (DONE)
    def normalize_vertexs(app,vertexes):
        # for each vertex
        normal_vertexies = []
        for vertex in vertexes:
           # devide X Y and Z values by W value
            nX = vertex[0]/vertex[3]
            nY = vertex[1]/vertex[3]
            nZ = vertex[2]/vertex[3]
            # add the normalised values to a list
            normal_vertexies.append([nX,nY,nZ])
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
            print(vertex)
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
        minX = 1
        maxX = 10

        minY = 1
        maxY = 10
        converted_vertexes = []
        for normal_vertex in normal_vertexes:
            normal_vertex[0] = max(1,min(0,normal_vertex[0]))
            normal_vertex[1] = max(1,min(0,normal_vertex[1]))
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
    def purify_polygon(app, polygon,vertexes):
        Px1 = vertexes[polygon[0]][0]
        Py1 = vertexes[polygon[0]][1]
        Pz1 = vertexes[polygon[0]][2]
        Pw1 = vertexes[polygon[0]][3]

        Px2 = vertexes[polygon[1]][0]
        Py2 = vertexes[polygon[1]][1]
        Pz2 = vertexes[polygon[1]][2]
        Pw2 = vertexes[polygon[1]][3]

        Px3 = vertexes[polygon[2]][0]
        Py3 = vertexes[polygon[2]][1]
        Pz3 = vertexes[polygon[2]][2]
        Pw3 = vertexes[polygon[2]][3]
        var = [
            Px1,Py1,Pz1,Pw1,
            Px2,Py2,Pz2,Pw2,
            Px3,Py3,Pz3,Pw3,
            polygon[3]]
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
    def cull_polygon(app,polygon,camera_pos,camera_orientation,view_planes,fov_dat):
        P1 = polygon[0],polygon[1],polygon[2],polygon[3]
        P2 = polygon[4],polygon[5],polygon[6],polygon[7]
        P3 = polygon[8],polygon[9],polygon[10],polygon[11]
        points = [P1,P2,P3]

        Hfov,Vfov = fov_dat

        Cx,Cy,Cz = camera_pos
        Cyaw,Cpitch,Croll = camera_orientation

        near_plane,far_plane = view_planes

        for point in points:
            x,y,z,w = point
            CX1 = -w*tan(Hfov/2)
            CX2 = w*tan(Hfov/2)
            
            CY1 = -w*tan(Vfov/2)
            CY2 = w*tan(Vfov/2)

            CZ1 = near_plane
            CZ2 = far_plane
            if not (x >= CX1 and x <= CX2):
                return "keep"
            if not (y >= CY1 and y <= CY2):
                return "keep"
            if not (z >= CZ1 and z <= CZ2):
                return "keep"
        return None
    
    def sort_polygons(app,polygons, vertexes):
        pure_polygons = []
        for polygon in polygons:
            pure_polygons.append(app.purify_polygon(polygon,vertexes))
        sorted_polygons = sort_polygons_by_depth_numpy(pure_polygons) ## deprecated
        normalised_polgyons = app.normalise_polygons(sorted_polygons)
        return normalised_polgyons

    # conevrt polygons and edge indixes to coordinates (DONE)
    def purify_object_data(app,vertexes, edges, polygons):
        if not app.proccess_polygons:
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
        else:
            pure_polygons = polygons
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
        if app.proccess_polygons:
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
    def render_object(app,vertexes, edges, polygons, camera_pos, camera_orientation, focal_length,screen_x,screen_y, fov_data,view_planes, projection_method=""):
        camera_x,camera_y,camera_z = camera_pos
        camera_yaw,camera_pitch,camera_roll = camera_orientation
        app.projection_method = projection_method
        # transfer object vertexes from world coordinates to camera coordinates
        vertexes = app.move_to_camera([camera_x,camera_y,camera_z], [camera_yaw,camera_pitch,camera_roll], vertexes)
        # sort polygons
        if app.proccess_polygons:
            polygons = app.sort_polygons(polygons, vertexes)
        # normalise vertexes
        vertexes = app.normalize_vertexs(vertexes)
        # project vertexes
        if app.projection_method == "MP":
            vertexes = app.military_projection(vertexes)
        elif app.projection_method == "OTP":
            vertexes = app.orthographic_projection(vertexes)
        elif app.projection_method == "SP":
            vertexes = app.spherical_projection(vertexes)
        elif app.projection_method == "IP":
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

        return app.normalise_vector([0,1,0])#app.normalise_vector([Ux,Uy,Uz])
    def calc_forward_vect(app,yaw,pitch,roll):
        yaw = radians(yaw)
        pitch = radians(pitch)

        Fx = cos(pitch)*sin(yaw)
        Fy = 0#sin(pitch)
        Fz = cos(pitch)*cos(yaw)

        Nv = app.normalise_vector([Fx,Fy,Fz])
        return(Nv)
    def calc_right_vect(app,yaw,pitch,roll):
        FvX,FvY,FvZ = app.calc_forward_vect(yaw,pitch,roll)
        UvX,UvY,UvZ = app.calc_up_vect(yaw,pitch,roll)

        RvX = cos(yaw)#UvY*FvZ-UvZ*FvY
        RvY = 0#UvZ*FvX-UvX*FvZ
        RvZ = -sin(yaw)#UvX*FvY-UvY*FvX

        return app.normalise_vector([1,0,0])#app.normalise_vector([RvX,RvY,RvZ])

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

        Px = camX-amount*vX
        Py = camY-amount*vY
        Pz = camZ-amount*vZ

        return [Px,Py,Pz]
    def move_cam_backward(app,camera_pos,camera_orientation, amount):
        camX,camY,camZ = camera_pos
        yaw,pitch,roll = camera_orientation

        vX,vY,vZ = app.calc_forward_vect(yaw,pitch,roll)

        Px = camX+amount*vX
        Py = camY+amount*vY
        Pz = camZ+amount*vZ

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
