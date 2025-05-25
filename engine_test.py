from engine.rotat_trans_scal import scale_vertexes
from engine.rotat_trans_scal import translate_vertexes
from engine.rotat_trans_scal import rotate_vertexes

from engine.culler import cull_edges,cull_polygons,cull_vertexes

from engine.polygon_proccesing import sort_polygons_by_nearest_point_np

from engine.projection import project_vertexes
from engine.projection import project_polygons
from engine.projection import project_edges

from engine.renderer import draw_edges
from engine.renderer import draw_polygons
from engine.renderer import draw_vertexes

from engine.camera import camera

from time import time

from pprint import pprint

import pygame

max_process_runtime = 1/60

##polygons
# rotation
def ST_polygon_rotation():
    testing = True
    test_cases = []
    while testing:
        if len(test_cases)%15 == 0:
            print("test cases: "+str(len(test_cases)))
        test_cases.append([
            [1,2,3],
            [4,5,6],
            [7,8,9],
            [0,1,2]])
        runtime_start = time()
        rotate_polygons(test_cases,6,34,9)
        runtime_end = time()
        total_runtime = runtime_end-runtime_start
        if total_runtime > max_process_runtime:
            testing = False
    return len(test_cases)
# translation
def ST_polygon_translation():
    testing = True
    test_cases = []
    while testing:
        if len(test_cases)%15 == 0:
            print("test cases: "+str(len(test_cases)))
        test_cases.append([
            [1,2,3],
            [4,5,6],
            [7,8,9],
            [0,1,2]])
        runtime_start = time()
        translate_polygons(test_cases,6,34,9)
        runtime_end = time()
        total_runtime = runtime_end-runtime_start
        if total_runtime > max_process_runtime:
            testing = False
    return len(test_cases)
# scaling
def ST_polygon_scaling():
    testing = True
    test_cases = []
    while testing:
        if len(test_cases)%15 == 0:
            print("test cases: "+str(len(test_cases)))
        test_cases.append([
            [1,2,3],
            [4,5,6],
            [7,8,9],
            [0,1,2]])
        runtime_start = time()
        scale_polygons(test_cases,6,34,9)
        runtime_end = time()
        total_runtime = runtime_end-runtime_start
        if total_runtime > max_process_runtime:
            testing = False
    return len(test_cases)
# culling
def ST_polygon_culling():
    testing = True
    test_cases = []
    while testing:
        if len(test_cases)%15 == 0:
            print("test cases: "+str(len(test_cases)))
        test_cases.append([
            [1,2,3],
            [4,5,6],
            [7,8,9],
            [0,1,2]])
        runtime_start = time()
        cull_polygons(test_cases,camera())
        runtime_end = time()
        total_runtime = runtime_end-runtime_start
        if total_runtime > max_process_runtime:
            testing = False
    return len(test_cases)
# sorting
def ST_polygon_sorting():
    testing = True
    test_cases = []
    while testing:
        if len(test_cases)%15 == 0:
            print("test cases: "+str(len(test_cases)))
        test_cases.append([
            [1,2,3],
            [4,5,6],
            [7,8,9],
            [0,1,2]])
        runtime_start = time()
        sort_polygons_by_nearest_point_np(test_cases,)
        runtime_end = time()
        total_runtime = runtime_end-runtime_start
        if total_runtime > max_process_runtime:
            testing = False
    return len(test_cases)
# projeciton
def ST_polygon_projection(method="WP"):
    testing = True
    test_cases = []
    while testing:
        if len(test_cases)%15 == 0:
            print("test cases: "+str(len(test_cases)))
        test_cases.append([
            [1,2,3],
            [4,5,6],
            [7,8,9],
            [0,1,2]])
        runtime_start = time()
        project_polygons(test_cases,camera(),method)
        runtime_end = time()
        total_runtime = runtime_end-runtime_start
        if total_runtime > max_process_runtime:
            testing = False
    return len(test_cases)
# rasterisation
def ST_polygon_rasterisation(resolution=(400,400)):
    pygame.init()
    temp_screen = pygame.display.set_mode(resolution)
    testing = True
    test_cases = []
    while testing:
        if len(test_cases)%15 == 0:
            print("test cases: "+str(len(test_cases)))
        test_cases.append([
            [2,3],
            [4,6],
            [7,8],
            [0,1,2]])
        runtime_start = time()
        draw_polygons(test_cases,temp_screen)
        pygame.display.flip()
        runtime_end = time()
        total_runtime = runtime_end-runtime_start
        if total_runtime > max_process_runtime:
            testing = False
    pygame.quit()
    return len(test_cases)
# all
def ST_polygons():
    print("finding rotation limit")
    rotation_limit = ST_polygon_rotation()
    print("finding translation limit")
    translation_limit = ST_polygon_translation()
    print("finding scaling limit")
    scaleing_limit = ST_polygon_scaling()
    print("finding culling limit")
    culling_limit = ST_polygon_culling()
    print("finding sorting limit")
    sorting_limit = ST_polygon_sorting()
    print("finding rasterisation limit")
    rasterisation_limit = ST_polygon_rasterisation()
    print("finding projection limit")
    projection_limit = [
        ST_polygon_projection("WP"),
        ST_polygon_projection("MP"),
        ST_polygon_projection("OP"),
        ST_polygon_projection("SP"),
        ST_polygon_projection("IP"),
        ST_polygon_projection("IC")]
    return {
        "rotation limit":rotation_limit,
        "translation limit":translation_limit,
        "scaling limit":scaleing_limit,
        "culling limit":culling_limit,
        "sorting limit":sorting_limit,
        "rasterisation limit":rasterisation_limit,
        "projection limit":projection_limit}
# average of many test results
def ST_polygons_avg(test_count=32):
    rotation_average = 0
    translation_average = 0
    scaleing_average = 0
    culling_average = 0
    sorting_average = 0
    rasterisation_average = 0
    projection_average = [0,0,0,0,0,0]
    for test_run in range(test_count):
        test_run_results = ST_polygons()
        rotation_average += test_run_results["rotation limit"]
        translation_average += test_run_results["translation limit"]
        scaleing_average += test_run_results["scaling limit"]
        culling_average += test_run_results["culling limit"]
        sorting_average += test_run_results["sorting limit"]
        rasterisation_average += test_run_results["rasterisation limit"]
        projection_average[0] += test_run_results["projection limit"][0]
        projection_average[1] += test_run_results["projection limit"][1]
        projection_average[2] += test_run_results["projection limit"][2]
        projection_average[3] += test_run_results["projection limit"][3]
        projection_average[4] += test_run_results["projection limit"][4]
        projection_average[5] += test_run_results["projection limit"][5]
    rotation_average = rotation_average/test_count
    translation_average = translation_average/test_count
    scaleing_average = scaleing_average/test_count
    culling_average = culling_average/test_count
    sorting_average = sorting_average/test_count
    rasterisation_average = rasterisation_average/test_count
    projection_average[0] = projection_average[0]/test_count
    projection_average[1] = projection_average[1]/test_count
    projection_average[2] = projection_average[2]/test_count
    projection_average[3] = projection_average[3]/test_count
    projection_average[4] = projection_average[4]/test_count
    projection_average[5] = projection_average[5]/test_count
    return {
        "test runs":test_count,
        "rotation average":rotation_average,
        "translation average":rotation_average,
        "scaleing average":scaleing_average,
        "culling average":culling_average,
        "sorting average":sorting_average,
        "rasterisation average":rasterisation_average,
        "projection average":projection_average}
pprint(ST_polygons_avg())
##edges
# rotation
def ST_edge_rotation():
    pass
# translation
def ST_edge_translation():
    pass
# culling
def ST_edge_culling():
    pass
# projeciton
def ST_edge_projection():
    pass
# rasterisation
def ST_edge_rasterisation():
    pass
# all
def ST_edges():
    pass

##vertexes
# rotation
def ST_vertex_rotation():
    pass
# translation
def ST_vertex_translation():
    pass
# culling
def ST_vertex_culling():
    pass
# projeciton
def ST_vertex_projection():
    pass
# rasterisation
def ST_vertex_rasterisation():
    pass
# all
def ST_vertexes():
    pass

## TEST ALL
def test_all():
    pass