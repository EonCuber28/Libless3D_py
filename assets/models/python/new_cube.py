def new_cube():
    #mtl_id = "path_to.mtl"
    mtl_id = ""
    vertex_table = [
        #[x,y,z, w(optional)]
    ]
    normal_vertex_table = [
        # [Nx,Ny,Nz]
    ]
    uv_table = [
        #[u,v]
    ]
    face_table = [
        #[[v1,v2,v3...],[Nv1,Nv2,Nv3...],[uv1,uv2,uv3...],[r,g,b]]
    ]
    return [vertex_table,normal_vertex_table ,uv_table, face_table, mtl_id]
def objecto():
    mtl_id = "banan.mtl"
    vertex_table = [[0.5, 0.5, -0.5],
        [0.5, -0.5, -0.5],
        [0.5, 0.5, 0.5],
        [0.5, -0.5, 0.5],
        [-0.5, 0.5, -0.5],
        [-0.5, -0.5, -0.5],
        [-0.5, 0.5, 0.5],
        [-0.5, -0.5, 0.5]]
    normal_vertex_table = [[-0.0, 1.0, -0.0],
        [-0.0, -0.0, 1.0],
        [-1.0, -0.0, -0.0],
        [-0.0, -1.0, -0.0],
        [1.0, -0.0, -0.0],
        [-0.0, -0.0, -1.0]]
    uv_table = [[1, 0],
        [1, 1],
        [0, 1],
        [0, 0]]
    face_table = [[[1, 5, 7, 3],
        [1, 1, 1, 1],
        [1, 2, 3, 4]],
        [[4, 3, 7, 8],
        [2, 2, 2, 2],
        [2, 3, 4, 1]],
        [[8, 7, 5, 6],
        [3, 3, 3, 3],
        [2, 3, 4, 1]],
        [[6, 2, 4, 8],
        [4, 4, 4, 4],
        [1, 2, 3, 4]],
        [[2, 1, 3, 4],
        [5, 5, 5, 5],
        [2, 3, 4, 1]],
        [[6, 5, 1, 2],
        [6, 6, 6, 6],
        [2, 3, 4, 1]]]
    return [vertex_table,normal_vertex_table, uv_table, face_table, mtl_id]
