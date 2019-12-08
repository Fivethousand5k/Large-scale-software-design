import os
from config import *

'''
    clear all files
'''

# origin_list = os.listdir(origin_path)
# for i in range(len(origin_list)):
#     file_list = os.listdir(os.path.join(origin_path, origin_list[i]))
#     for j in range(len(file_list)):
#         os.remove(os.path.join(origin_path, origin_list[i], file_list[j]))


video_list = os.listdir(video_path)
for i in range(len(video_list)):
    file_list = os.listdir(os.path.join(video_path, video_list[i]))
    for j in range(len(file_list)):
        os.remove(os.path.join(video_path, video_list[i], file_list[j]))

img_list = os.listdir(img_path)
for i in range(len(img_list)):
    file_list = os.listdir(os.path.join(img_path, img_list[i]))
    for j in range(len(file_list)):
        os.remove(os.path.join(img_path, img_list[i], file_list[j]))

feature_list = os.listdir(feature_path)
for i in range(len(feature_list)):
    file_list = os.listdir(os.path.join(feature_path, feature_list[i]))
    for j in range(len(file_list)):
        os.remove(os.path.join(feature_path, feature_list[i], file_list[j]))

result_list = os.listdir(result_path)
for i in range(len(result_list)):
    file_list = os.listdir(os.path.join(result_path, result_list[i]))
    for j in range(len(file_list)):
        os.remove(os.path.join(result_path, result_list[i], file_list[j]))

detect_result_list = os.listdir(detect_result_path)
for i in range(len(result_list)):
    file_list = os.listdir(os.path.join(detect_result_path, detect_result_list[i]))
    for j in range(len(file_list)):
        os.remove(os.path.join(detect_result_path, detect_result_list[i], file_list[j]))

