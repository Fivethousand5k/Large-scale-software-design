#!/usr/bin/env python

import collections
import os
import cv2
import numpy as np
import PIL.Image
import scipy.io
import torch
from torch.utils import data
import torchvision.transforms

class VGG_Faces2(data.Dataset):

    mean_bgr = np.array([91.4953, 103.8827, 131.0912])  # from resnet50_ft.prototxt

    def __init__(self, root, split='train', transform=True,
                 horizontal_flip=False, upper=None):
        """
        :param root: dataset directory
        :param image_list_file: contains image file names under root
        :param id_label_dict: X[class_id] -> label
        :param split: train or valid
        :param transform: 
        :param horizontal_flip:
        :param upper: max number of image used for debug
        """
        assert os.path.exists(root), "root: {} not found.".format(root)
        self.root = root
        self.imgs_list=[]
        self.sub_directory_list=os.listdir(self.root)
        self.id_label_dict={}
        self.img_info = []



        #initialize id_label_dict and imgs_list
        for i,sub_directory in enumerate(self.sub_directory_list):
            imgs_list=os.listdir(os.path.join(self.root,sub_directory))
            self.id_label_dict[sub_directory.split("/")[-1]] = i
            for img in imgs_list:
                img=os.path.join(self.root,sub_directory,img)
                class_id = sub_directory
                label = self.id_label_dict[class_id]
                self.img_info.append({
                    'cid': class_id,
                    'img': img,
                    'lbl': i,
                })



        print(self.id_label_dict)

        #
        # for img in self.imgs_list:
        #     img =img.strip()
        #     img=os.path.join(self.root,)
        #     class_id = img.split("/")[-2]
        #     label = self.id_label_dict[class_id]
        #     self.img_info.append({
        #         'cid': class_id,
        #         'img': img,
        #         'lbl': label,
        #     })



        # assert os.path.exists(image_list_file), "image_list_file: {} not found.".format(image_list_file)
        # self.image_list_file = image_list_file
        self.split = split
        self._transform = transform
        # self.id_label_dict = id_label_dict
        self.horizontal_flip = horizontal_flip

        # with open(self.image_list_file, 'r') as f:
        #     for i, img_file in enumerate(f):
        #         img_file = img_file.strip()  # e.g. train/n004332/0317_01.jpg
        #         class_id = img_file.split("/")[1]  # like n004332
        #         label = self.id_label_dict[class_id]
        #         self.img_info.append({
        #             'cid': class_id,
        #             'img': img_file,
        #             'lbl': label,
        #         })
        #         if i % 1000 == 0:
        #             print("processing: {} images for {}".format(i, self.split))
        #         if upper and i == upper - 1:  # for debug purpose
        #             break

    def __len__(self):
        return len(self.img_info)

    def __getitem__(self, index):
        info = self.img_info[index]
        img_file = info['img']
        img = PIL.Image.open(os.path.join(self.root, img_file))
        # self.adjust_size(img)
        img = torchvision.transforms.Resize(224)(img)
        if self.split == 'train':
            img = torchvision.transforms.RandomCrop(224)(img)
            img = torchvision.transforms.RandomGrayscale(p=0.2)(img)
        else:
            img = torchvision.transforms.CenterCrop(224)(img)
        if self.horizontal_flip:
            img = torchvision.transforms.functional.hflip(img)

        img = np.array(img, dtype=np.uint8)
        assert len(img.shape) == 3  # assumes color images and no alpha channel

        label = info['lbl']
        class_id = info['cid']
        if self._transform:
            return self.transform(img), label, img_file, class_id
        else:
            return img, label, img_file, class_id

    def transform(self, img):
        img = img[:, :, ::-1]  # RGB -> BGR
        img = img.astype(np.float32)
        img -= self.mean_bgr
        img = img.transpose(2, 0, 1)  # C x H x W
        img = torch.from_numpy(img).float()
        return img

    def untransform(self, img, lbl):
        img = img.numpy()
        img = img.transpose(1, 2, 0)
        img += self.mean_bgr
        img = img.astype(np.uint8)
        img = img[:, :, ::-1]
        return img, lbl

    def adjust_size(self, RGB_img):
        """
        功能：为了保证图像不形变，适应label的拉伸，而给小图像增加黑边或者对大图像进行等比例放缩
        :param RGB_img:   传入的RGB矩阵
        :return:
        """

        #
        height, width, channel = RGB_img.shape
        MAXSIZE=max(height,width)
        if height <= MAXSIZE and width <= MAXSIZE:  # 如果图片未超过最大尺寸
            background = np.zeros([MAXSIZE, MAXSIZE, channel], np.uint8)  # 制作一个黑色底片
            top_indent = int((MAXSIZE - height) / 2)  # 上方间隙
            left_indent = int((MAXSIZE - width) / 2)  # 侧方间隙
            background[top_indent:(top_indent + height), left_indent:(left_indent + width), :] = RGB_img[:, :, :]
            return background
        else:  # 图片超过最大尺寸
            """

            这一段是在网上找的代码，以后再看，参考链接：https://blog.csdn.net/zhou4411781/article/details/95449322

            """
            size = RGB_img.shape
            h, w = size[0], size[1]
            # 长边缩放为MAXSIZE
            scale = max(w, h) / float(MAXSIZE)
            new_w, new_h = int(w / scale), int(h / scale)
            resize_RGB_img = cv2.resize(RGB_img, (new_w, new_h))
            # 填充至MAXSIZE * MAXSIZE
            if new_w % 2 != 0 and new_h % 2 == 0:
                top, bottom, left, right = (MAXSIZE - new_h) / 2, (MAXSIZE - new_h) / 2, (MAXSIZE - new_w) / 2 + 1, (
                        MAXSIZE - new_w) / 2
            elif new_h % 2 != 0 and new_w % 2 == 0:
                top, bottom, left, right = (MAXSIZE - new_h) / 2 + 1, (MAXSIZE - new_h) / 2, (MAXSIZE - new_w) / 2, (
                        MAXSIZE - new_w) / 2
            elif new_h % 2 == 0 and new_w % 2 == 0:
                top, bottom, left, right = (MAXSIZE - new_h) / 2, (MAXSIZE - new_h) / 2, (MAXSIZE - new_w) / 2, (
                        MAXSIZE - new_w) / 2
            else:
                top, bottom, left, right = (MAXSIZE - new_h) / 2 + 1, (MAXSIZE - new_h) / 2, (
                        MAXSIZE - new_w) / 2 + 1, (MAXSIZE - new_w) / 2
            pad_img = cv2.copyMakeBorder(resize_RGB_img, int(top), int(bottom), int(left), int(right),
                                         cv2.BORDER_CONSTANT,
                                         value=[0, 0, 0])  # 从图像边界向上,下,左,右扩的像素数目
            return pad_img

