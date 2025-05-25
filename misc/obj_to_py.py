from pprint import pprint

def format_vertex_table(vertex_table):
    final_table = []
    for vertex in vertex_table:
        vertex = vertex.replace("v ","")
        vertex_elements = vertex.split(" ")
        float_elements = []
        for element in vertex_elements:
            float_elements.append(float(element))
        final_table.append(float_elements)
    return final_table
def format_vertex_normals(vertex_normals):
    final_normals = []
    for normal in vertex_normals:
        normal = normal.replace("vn ","")
        normal_elements = normal.split(" ")
        float_normals = []
        for element in normal_elements:
            float_normals.append(float(element))
        final_normals.append(float_normals)
    return final_normals
def format_uv_table(uv_table):
    final_uv = []
    for uv in uv_table:
        uv = uv.replace("vt ","")
        uv_lst = []
        for element in uv.split(" "):
            uv_lst.append(float(element))
        if len(uv_lst) == 1:
            uv_lst.apend(float(0))
        elif len(uv_lst) == 3:
            uv_lst = [uv_lst[0],uv_lst[1]]
        final_uv.append(uv_lst)
    return final_uv
def format_face_table(face_table):
    # i want: [[v1...],[nv1...],[uv1...]]
    preped_face_table = []
    for face in face_table:
        face = face.replace("f ","")
        face_elements = face.split(" ")
        parsed_face_elements = []
        for element in face_elements:
            element = element.split("/")
            for elemento in range(len(element)):
                element[elemento] = int(element[elemento])
            parsed_face_elements.append(element)
        normal_table = []
        vertex_table = []
        uv_table = []
        for x in parsed_face_elements:
            vertex_table.append(x[0])
            uv_table.append(x[1])
            normal_table.append(x[2])
        preped_face_table.append([vertex_table,normal_table,uv_table])
    return preped_face_table

def parse_mtl_id(mtl_id):
    mtl_id = mtl_id.replace("mtllib ","")
    return mtl_id
def format_mtl_tags(mtl_id, mtl_tags):
    material_references = []
    material_search = False
    material_id = ""
    for mtl_element in open("E:/Libless3D/assets/models/"+mtl_id,"r").readlines():
        mtl_element = mtl_element.split(" ")
        if mtl_element[0] == "newmtl" and material_search == False:
            for tag in mtl_tags:
                if tag == mtl_element[1]:
                    material_search = True
                    material_id = mtl_element[1]
        elif mtl_element[0] == "map_Kd" and material_search == True:
            material_search = False
            material_references.append([material_id, mtl_element[1]])
def parse_obj(obj_file):
    obj_data = open(obj_file,"r").readlines()
    vertex_table = []
    vertex_normals = []
    uv_table = []   
    face_table = []
    mtl_id = ""
    mtl_tags = []
    for element in obj_data:
        element = element.replace("\n","")
        elements = element.split(" ")
        if elements[0] != "#":
            if elements[0] == "mtllib":
                mtl_id = element
            elif elements[0] == "usemtl":
                mtl_tags.append(element)
            elif elements[0] == "v":
                vertex_table.append(element)
            elif elements[0] == "vt":
                uv_table.append(element)
            elif elements[0] == "vn":
                vertex_normals.append(element)
            elif elements[0] == "f":
                face_table.append(element)
    vertex_table = format_vertex_table(vertex_table)
    vertex_normals = format_vertex_normals(vertex_normals)
    uv_table = format_uv_table(uv_table)
    face_table = format_face_table(face_table)#,uv_table)
    mtl_id = parse_mtl_id(mtl_id)
    #mtl_data = format_mtl_tags(mtl_id,mtl_tags)
    return [vertex_table,vertex_normals,face_table,uv_table,mtl_id]
def parse_obj_to_py(obj_file,output_py):
    parsed_obj = parse_obj(obj_file)
    template_py = """
def {object_name}():
    mtl_id = "{mtl_id}"
    vertex_table = {vertex_table}
    normal_vertex_table = {normal_table}
    uv_table = {uv_table}
    face_table = {face_table}
    return [vertex_table,normal_vertex_table, uv_table, face_table, mtl_id]"""
    template_py = template_py.replace("{object_name}","objecto")
    template_py = template_py.replace("{vertex_table}",str(parsed_obj[0]))
    template_py = template_py.replace("{normal_table}",str(parsed_obj[1]))
    template_py = template_py.replace("{face_table}",str(parsed_obj[2]))
    template_py = template_py.replace("{uv_table}",str(parsed_obj[3]))
    template_py = template_py.replace("{mtl_id}",str(parsed_obj[4]))
    template_py = template_py.replace("], ","],\n        ")
    output_file = open(output_py,"a+")
    output_file.write(template_py)
    output_file.close()

parse_obj_to_py(r"E:\Libless3D\assets\models\banan.obj",r"E:\Libless3D\assets\models\python\new_cube.py")
#pprint(parse_obj(r"E:\Libless3D\assets\models\banan.obj"))