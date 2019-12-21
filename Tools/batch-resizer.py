"""
by Fivethousand
"""
import os
import cv2

NEW_SIZE=112        #新的图片的分辨率

Load_Path='F:\python_programs\\tasks_from_King\datasets\CASIA-WebFace-part'                    #读取原来的数据集的地址
Save_Path='F:\python_programs\\tasks_from_King\datasets'                    #要保存的新的数据集的地址


new_name="dataset(resized)"             #resize后的数据集名字
root=os.path.join(Save_Path,new_name).replace('\\','/')            #新数据集的根目录
if os.path.exists(root) is not True:
    os.mkdir(root)                          #创建根目录


for filename in os.listdir(Load_Path):
    print("Processing:"+filename)
    new_file=os.path.join(root,filename)
    if os.path.exists(new_file) is not True:
        os.mkdir(new_file)       #在新数据集根目录下新建同名文件夹
    for img in os.listdir(os.path.join(Load_Path,filename)):
        new_img=os.path.join(new_file,img)
        image=cv2.imread(os.path.join(Load_Path,filename,img))
        if image is not None:
            res=cv2.resize(image,(NEW_SIZE,NEW_SIZE),interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(new_img, res)
