import cv2

video_path = '/home/cliang/mmap/experiment/test_video/zjz.mp4'
output_path = '/home/cliang/mmap/experiment/sequences/zjz/'

capture = cv2.VideoCapture(video_path)
ret, frame = capture.read()
index = 0
while ret:
    if index < 1200:
        frame_index = '%04d' % index
        frame_path = output_path + frame_index + '.jpg'
        cv2.imwrite(frame_path, frame)
        index = index+1
        ret, frame = capture.read()
    else:
        break