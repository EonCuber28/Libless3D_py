from engine.polygon_proccesing import *
from engine.rotat_trans_scal import *
from engine.projection import *
from engine.renderer import *
from engine.camera import *
from engine.culler import *

# culler test
def culler_test():
    # vertex
    # sculpt
    # cull

    # vertexes
    # sculpt
    # cull

    # edge
    # sculpt
    # cull
    
    # edges
    # sculpt
    # cull

    # polygon
    # sculpt
    # cull

    # polygons
    # sculpt
    # cull

    pass
# camera test
def camera_test():
    # tranfer vertex to camera space
    # sculpt to frustum
    # is in frustum
    # calc forward vector
    pass
# renderer test
def renderer_test():
    pass
# projection test
def projection_test():
    pass
# rotation test
def rotation_test():
    pass
# translation test
def translation_test():
    pass
# polygon processing test
def polygon_proccessing_test():
    pass

# selector
def selector():
    selection = input()
    # done
    if selection == "Done":
        print("alrighty!")
        quit()
    # all
    if selection == "all":
        culler_test()
        camera_test()
        renderer_test()
        projection_test()
        rotation_test()
        translation_test()
        polygon_proccessing_test()
        # rotation
    elif selection == "rotation":
        rotation_test()
        # translation
    elif selection == "translation":
        translation_test()
        # camera
    elif selection == "camera":
        camera_test()
        # polygon processing
    elif selection == "polygon processing":
        polygon_proccessing_test()
        # renderer
    elif selection == "renderer":
        renderer_test()
        # culler
    elif selection == "culler":
        culler_test()
    else:
        print("unknown input")
        print("try again")
        selector()

if __name__ == "__main__":
    selector()