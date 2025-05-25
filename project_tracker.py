import os
def find_files_in_folder(folder):
    files = []
    for content in os.listdir(folder):
        if os.path.isfile(folder+content):
            files.append(folder+content)
    return files

def get_length_of_file(file_path):
    file_data = open(file_path, "r")
    file_list = file_data.readlines()
    file_data.close()
    return len(file_list)

def obtain_project_progress(folders):
    progress = 0
    for folder in folders:
        files = find_files_in_folder(folder)
        for file in files:
            progress += get_length_of_file(file)
    return progress

if __name__ == "__main__":
    folders_to_search = [
        "./",
        "./assets/models/",
        "./assets/models/python/",
        "./engine/"]
    print("Total lines of code in project: "+str(obtain_project_progress(folders_to_search)))
