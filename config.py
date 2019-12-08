fps = 20
batch_second = 30
batch_frames = fps * batch_second
alternation = 2
max_video = 100

img_width = 960
img_height = 540

# project path
project_path = "/home/mmap/mmap/VSA_Server/"

# camera_local
origin_path = "F:\python_programs\大型软件设计/video-for-map"  # 远程视频解码服务器写入
# origin_path = "/home/mmap/cameraVideos/origin/"  # 远程视频解码服务器写入

# img path
face_detect_img_path = "/home/mmap/vsa_server/camera/imgs/face_detect/"
person_detect_img_path = "/home/mmap/vsa_server/camera/imgs/person_detect/"
person_mot_img_path = "/home/mmap/vsa_server/camera/imgs/person_mot/"

# txt results path
face_detect_txt_path = "/home/mmap/vsa_server/camera/txt_results/face_detect/"
face_mot_txt_path = "/home/mmap/vsa_server/camera/txt_results/face_mot/"
person_detect_txt_path = "F:\python_programs\大型软件设计/txt-results"
person_mot_txt_path = "/home/mmap/vsa_server/camera/txt_results/person_mot/"
person_reid_feature_path = "/home/mmap/vsa_server/camera/txt_results/person_reid_feature/"
time_text_path = "/home/mmap/vsa_server/camera/txt_results/time_stamp/"
segmentation_txt_path = "/home/mmap/vsa_server/camera/txt_results/segmentation/"
# face_recog_txt_path="/home/mmap/vsa_server/camera/txt_results/face_recognition/"
face_recog_txt_path="/home/cliang/5000_face_recog_result/"

# video results path
face_detect_video_path = "/home/mmap/vsa_server/camera/video_results/face_detect/"
face_mot_video_path = "/home/mmap/vsa_server/camera/video_results/face_mot/"
person_detect_video_path = "/home/mmap/vsa_server/camera/video_results/person_detect/"
person_mot_video_path = "/home/mmap/vsa_server/camera/video_results/person_mot/"
segmentation_video_path = "/home/mmap/vsa_server/camera/video_results/segmentation/"

person_detect_switch = True
face_mot_switch = False
person_mot_switch =False
person_reid_feature_switch = False
segmentation_switch = False
face_recognition_switch=False

person_detect_method = 2  # 0:YOLODetector  1:YOLOTinyDetector  2:YOLOBatchDetector
seg_method = 0  # 选择分割算法{0：BiseNet , 1：DeepLab-v3+}
seg_root = '/home/mmap/mmap/VSA_Server/segmentation/'

detect_skip = 1  # 检测跳帧数(≥0的整数)
p = 1  # 分割相对于检测的跳帧数(≥0的整数)
seg_skip = (p + 1) * detect_skip + p  # 分割跳帧数(≥0的整数)
mot_skip = detect_skip

# reid dataset name
dataset = 'cuhk02'

reid_root = '/home/mmap/mmap/VSA_Server/retrieval/'


name_list=['周建力', '姜龙祥', '张精制', '方寒', '柴笑宇', '沈宇轩', 'unknown', '阮威健', '虞吟雪', '郑淇', 'unknown', '陈金', '胡亮', '彭冬梅', '14', '15', '徐东曙', '廖良', '陈俊奎', '洪琪', '高熙越', '黄志兵', '张莎莎', '23', '高腾飞', '陈超', '26', '叶钰', '2', '许海燕', '朱玟谦', '汤云波', '江奎', '33', '丁新', '35', '王旭', '杨光耀', '刘旷也', '39', '王晓芬', '张垒', '郭进', '陈宇静', '胡梦顺', '张钰慧', '梁超', '王南西', '陈宇', '陈军', 'unknown', 'unknown', '2', '刘勇琰', '54', '兰佳梅', 'unknown', '黄鹏', '沈心怡', '陈思维', '陈保金', '王光成', '詹泽行', '赵海法', '焦黎', '胡必成', '孙志宏', '王松', '68', '69', '70', '万东帅', '72', '里想', '74', '陈丹', '76', '魏明高', '聂伟凡', '屈万倩', '柯亨进', '81', '2', '陈培璐', '王晓', '85', '86', '黄文心', '易敏', '张琪', '90', '刘晗', '92', '93', '白云鹏', '95', '96', '阮威健', '98', '99', '5000', '101', '102', '103', '104', '105', '106', '107', '黄文心', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120']

