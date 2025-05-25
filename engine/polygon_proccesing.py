from math import sqrt
import numpy as np

def sort_polygons_by_closest_vertex(vertex_table, polygon_table, camera_pos=(0, 0, 0), reverse=False):
    """
    Sorts polygons based on the distance of their closest vertex to the camera using NumPy for efficiency.

    Each vertex in vertex_table is given as [x, y, z, w].
    Each polygon in polygon_table is in the format:
      [vertex_index1, vertex_index2, vertex_index3, [r, g, b], [[u, v], [u, v], [u, v]]]

    Parameters:
        vertex_table (list): List of vertices.
        polygon_table (list): List of polygons.
        camera_pos (tuple): (x, y, z) position of the camera (default: (0, 0, 0)).
        reverse (bool): If True, sorts in descending order (farthest first).

    Returns:
        list: Sorted list of polygons.
    """
    # Convert vertex_table to a NumPy array (shape: [n_vertices, 4])
    vertices = np.array(vertex_table)
    
    # Compute distances from the camera for each vertex (ignoring the w component)
    # Only x, y, z are used
    cam = np.array(camera_pos)
    vertex_positions = vertices[:, :3]
    # Vectorized Euclidean distance computation for each vertex
    distances = np.linalg.norm(vertex_positions - cam, axis=1)
    
    # Create an array to hold the minimum distance for each polygon
    polygon_min_dists = np.empty(len(polygon_table))
    
    # For each polygon, find the smallest distance among its three vertices
    for i, poly in enumerate(polygon_table):
        # Extract the three vertex indices from the polygon
        indices = poly[0:3]
        # Use these indices to lookup distances in the precomputed array
        polygon_min_dists[i] = np.min(distances[indices])
    
    # Sort the polygon indices by the computed minimum distances.
    sort_order = np.argsort(polygon_min_dists)
    if reverse:
        sort_order = sort_order[::-1]
    
    # Generate the sorted list of polygons.
    sorted_polygons = [polygon_table[i] for i in sort_order]
    
    return sorted_polygons

# thank you chatGPT for this funciton
# saved a lot of effort with polygon sorting
# I didnt want to use my O=2^n algorythum for this
# i am in a CS class but not one that will teach me a O=(n log n) algorythum
# or something complicated more complicated
def sort_polygons_by_nearest_point_np(polygons, camera=(0, 0, 0), reverse=False):
    """
    Sort a list of polygons by the distance of their closest vertex to the camera,
    using NumPy for vectorized computations.

    Each polygon is a list where the first elements are vertices ([x, y, z])
    and the last element is the polygon's color (e.g. [r, g, b]).

    Args:
        polygons (list): List of polygons.
        camera (tuple): The (x, y, z) coordinates of the camera.
        reverse (bool): If True, sorts in descending order.

    Returns:
        list: Sorted list of polygons.
    """
    cx, cy, cz = camera
    # Compute minimum squared distance for each polygon:
    min_d2 = []
    for poly in polygons:
        # Convert the vertices (all but the last element) into a NumPy array.
        vertices = np.array(poly[:-1])  # shape (num_vertices, 3)
        # Compute squared distances from camera to each vertex.
        d2 = np.sum((vertices - np.array([cx, cy, cz]))**2, axis=1)
        min_d2.append(np.min(d2))
    min_d2 = np.array(min_d2)
    
    # Get the sorted indices based on the computed distances.
    sorted_indices = np.argsort(min_d2)
    if reverse:
        sorted_indices = sorted_indices[::-1]
    
    # Reassemble the sorted list of polygons.
    return [polygons[i] for i in sorted_indices]

# we need a new version of the funciton above that takes a vertex table and uses it find the nearest point
# on a polygon to the camera, we sort the polygons based on the distance of the nearest point of the polygon 
# to the camera, using the data from the initial process of finding the nearest point on a polygon to the camera
# to reduce needed pythagorean based computations.
# the main reason we sort the polygons by their nearest point to the camera,
# and not on their average positions distance to tha camera is because, when put into practice,
# there are many polygon layering defects caused by sorting by camera distance to the average position of the polygon.
# when we instead sort by the nearest point in a polygon, those artifacts go away. so thats why we take that extra step.

# imma try making one that uses python's list.sort() method. it has a time complexity of O=(n log n)
def sort_polygons(vertex_table, polygon_table, camera_pos=[0,0,0], use_nearest_point=False):
    # what im gonna do it find the distance of each vertex and put that distance into a list for later use
    distance_table = []
    for vertex in vertex_table:
        distance_table.append(sqrt(((vertex[0]-camera_pos[0])**2)+((vertex[1]-camera_pos[1])**2)+((vertex[2]-camera_pos[2])**2)))
    # when we find the nearest point in the polygon we can referance the distance_table
    # then we make a new table with the polygon table data and the distance
    # in the format of: [polygon data, nearest point to camera distance]
    distanced_polygon_table = []
    if use_nearest_point:
        for polygon in polygon_table:
            p0 = distance_table[polygon[0]]
            p1 = distance_table[polygon[1]]
            p2 = distance_table[polygon[2]]
            if p0 >= p1:
                if p0 >= p2:
                    distanced_polygon_table.append([polygon,p0])
            elif p1 >= p0:
                if p1 >= p2:
                    distanced_polygon_table.append([polygon,p1])
            elif p2 >= p0:
                if p2 >= p1:
                    distanced_polygon_table.append([polygon,p2])
    else:
        for polygon in polygon_table:
            p0 = distance_table[polygon[0]]
            p1 = distance_table[polygon[1]]
            p2 = distance_table[polygon[2]]
            avg_distance = (p0+p1+p2)/3
            distanced_polygon_table.append([polygon,avg_distance])
    # using special python sorting args with the use of functions
    def special_thang(value):
        return value[1]
    # hopefully this works :)
    sorted_polygons = distanced_polygon_table.sort(key=special_thang)
    return sorted_polygons
