class cube:
    def __init__(cube):
        cube.texture_id = "minecraft_dirt.webp"

        cube.posX = 0
        cube.posY = 0
        cube.posZ = 0

        cube.rotX = 0
        cube.rotY = 0
        cube.rotZ = 0

        cube.scalX = 0
        cube.scalY = 0
        cube.scalZ = 0

        cube.normal_table = [
            [-0.0, 1.0, -0.0],
            [-0.0, -0.0, 1.0],
            [-1.0, -0.0, -0.0],
            [-0.0, -1.0, -0.0],
            [1.0, -0.0, -0.0],
            [-0.0, -0.0, -1.0]]
        cube.vertex_table = [
            [1.0, 1.0, -1.0],
            [1.0, -1.0, -1.0],
            [1.0, 1.0, 1.0],
            [1.0, -1.0, 1.0],
            [-1.0, 1.0, -1.0],
            [-1.0, -1.0, -1.0],
            [-1.0, 1.0, 1.0],
            [-1.0, -1.0, 1.0]]
        cube.uv_table = [
            [1, 0],
            [1, 1],
            [0, 1],
            [0, 0]]
        cube.face_table = [
            [
                [1, 5, 7, 3],
                [1, 1, 1, 1],
                [1, 2, 3, 4]],
            [
                [4, 3, 7, 8],
                [2, 2, 2, 2],
                [2, 3, 4, 1]],
            [
                [8, 7, 5, 6],
                [3, 3, 3, 3],
                [2, 3, 4, 1]],
            [
                [6, 2, 4, 8],
                [4, 4, 4, 4],
                [1, 2, 3, 4]],
            [
                [2, 1, 3, 4],
                [5, 5, 5, 5],
                [2, 3, 4, 1]],
            [
                [6, 5, 1, 2],
                [6, 6, 6, 6],
                [2, 3, 4, 1]]]


