import cv2
import os

frame_path = '/home/cliang/mmap/experiment/sequences/Cam5/'

img_list = os.listdir(frame_path)
img_list.sort()


file_path = '/home/cliang/mmap/experiment/test_video/cam5.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output = cv2.VideoWriter()
output.open(file_path, fourcc, 20, (320, 240))

for i in range(len(img_list)):
    frame = cv2.imread(frame_path+img_list[i])
    print(frame.shape)
    output.write(frame)

output.release()

