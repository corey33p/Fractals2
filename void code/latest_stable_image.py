import time
import os
def latest_stable_image():
    list_files = [os.getcwd() + "\\save\\" + file for file in os.listdir(os.getcwd() + "\\save\\") if '.png' in file]
    if not list_files: return None
    def get_index(name):
        index = name.rfind("-")+1
        jndex = name.rfind(".png")
        return int(name[index:jndex])
    latest_file = max(list_files, key = get_index)
    print("latest_file: " + str(latest_file))
    if time.time() - os.path.getmtime(latest_file) > .25:
        return latest_file
    if len(list_files) > 1:
        list_files.pop(list_files.index(latest_file))
        second_latest_file = max(list_files, key = os.path.getctime)
        return second_latest_file
    else: return None

latest_stable_image()
