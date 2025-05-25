from math import sqrt, atan2, atan
# transfer from screen to pixel coords
def screen_to_pixel(x,y, resolution):
    return [x*resolution[0],y*resolution[1]]

# the creators projection math
def general_projection(vertex):
    X,Y,Z = vertex
    Xmod = 1
    Ymod = 1
    # base func made in desmos 3d graph:
    # Xproj = atan(X/sqrt(Y+Z))*Z
    # Yproj = atan(Y/sqrt(X+Z))*Z
    Xproj = atan((Xmod*X)/sqrt(Y/Z))*Z
    Yproj = atan((Ymod*Y)/sqrt(X/Z))*Z
    return [Xproj,Yproj]
# isometric
def isometric_projection(vertex):
    X,Y,Z = vertex
    Xmod = 2
    Ymod = 6
    # Xproj = (1/sqrt(Xmod))*X-(1/sqrt(Xmod))*Z
    # Yproj = (1/sqrt(Ymod))*X-(1/sqrt(Ymod))*Z+Y
    Xproj = (1/sqrt(Xmod))*X-(1/sqrt(Xmod))*Z
    Yproj = (1/sqrt(Ymod))*X-(1/sqrt(Ymod))*Z+Y
    return [Xproj,Yproj]
# spherical
def spherical_projection(vertex):
    X,Y,Z = vertex
    # Xproj = atan2(X,Y)
    # Yproj = atan2(Z,sqrt(X^2+Y^2))
    Xproj = atan2(X,Y)
    Yproj = atan2(Z,sqrt(X**2+Y**2))
    return [Xproj,Yproj]
# weak perspective
def weak_perspective_projection(vertex,camera_class,scale_to_screen=True):
    if len(vertex) == 4:
        X,Y,Z,W = vertex
    else:
        X,Y,Z = vertex
    HFL = camera_class.HFL
    VFL = camera_class.VFL
    # Xproj = FL*X/FL+Z
    # Yproj = FL*Y/FL+Y
    if scale_to_screen:
        Xproj = (HFL*X/HFL+Z)*(camera_class.resX*2)
        Yproj = (VFL*Y/VFL+Z)*(camera_class.resY*2)
    else:
        Xproj = (HFL*X/HFL+Z)
        Yproj = (VFL*Y/VFL+Z)
    if len(vertex) == 3:
        return [Xproj,Yproj, Z]
    else:
        return [Xproj,Yproj, W]
# military projection
def military_projection(vertex):
    X,Y,Z = vertex
    # Xproj = X/Z
    # Yproj = Y/Z
    # if Z == 0, then make it more than 0
    if Z < 0:
        Z = float("inf")
    Xproj = X/Z
    Yproj = Y/Z
    return [Xproj,Yproj]
# orthographic
def orthographic_projection(vertex):
    X,Y,Z = vertex
    # Xproj = X
    # Yproj = Y
    return [X,Y]

### LIST OF PROJECTION METHODS ###
# GP: general projection
# IP: isometric projection
# SP: spherical projection
# OP: orthographic projection
# MP: military projection
# WP: weak perspective projection

# vertex
def project_vertex(vertex, camera_class, mode="WP"):
    if mode == "WP":
        return weak_perspective_projection(vertex,camera_class)
    elif mode == "MP":
        return military_projection(vertex)
    elif mode == "OP":
        return orthographic_projection(vertex)
    elif mode == "SP":
        return spherical_projection(vertex)
    elif mode == "IP":
        return isometric_projection(vertex)
    elif mode == "GP":
        return general_projection(vertex)
# vertexes
def project_vertexes(vertexes, camera_class, mode="WP"):
    proj_vertexes = []
    for vertex in vertexes:
        if vertex != None:
            proj_vertexes.append(project_vertex(vertex, camera_class, mode))
        else:
            proj_vertexes.append(None)
    return proj_vertexes
