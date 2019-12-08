# -*- coding: utf-8 -*-
# @author:  shenyuxuan
# @contact: 1044808224@qq.com

import cv2
import time
import datetime
import os
import numpy as np
import shutil
import torch
import torch.nn as nn
from torch.autograd import Variable
import torchvision
import matplotlib.pyplot as plt
import sys
from PIL import Image
from config import *

sys.path.append(project_path)

x_array = [[45, 70], [70, 95], [95, 120], [119, 144],  # Year
           [167, 192], [190, 215],  # Month
           [238, 263], [264, 289],  # Date
           [478, 503], [502, 527], [550, 575], [574, 599], [622, 647], [646, 671]]  # Time
y_array = [3, 39]


def model_generator():
    path_model = '/home/jlx/mmap_vsa/feature/time/model_time.pkl'
    model = CNN()
    model.load_state_dict(torch.load(path_model))
    return model


def get_clock(image, model):
    imgs = torch.zeros([len(x_array), 1, 28, 28])
    transforms = torchvision.transforms.ToTensor()
    for index, x in enumerate(x_array):
        temp_image_num = image[y_array[0]:y_array[1], x[0]:x[1]]
        temp_image_num = cv2.resize(temp_image_num, (28, 28))
        temp_image_num = cv2.cvtColor(temp_image_num, cv2.COLOR_BGR2GRAY)
        temp_image_num = Image.fromarray(np.array(temp_image_num), mode='L')
        temp_image_num = transforms(temp_image_num)
        imgs[index] = temp_image_num

    output = model(imgs)[0]
    label = torch.max(output, 1)[1].data.cpu().numpy()

    year = str(label[0]) + str(label[1]) + str(label[2]) + str(label[3])
    month = str(label[4]) + str(label[5])
    date = str(label[6]) + str(label[7])
    hour = str(label[8]) + str(label[9])
    min = str(label[10]) + str(label[11])
    sec = str(label[12]) + str(label[13])

    current_time = year + '-' + month + '-' + date + ' ' + hour + ':' + min + ':' + sec

    dt = current_time

    return dt


def get_all_clock(input_arr, video_path, results_txt_path, model, flag_check=True):
    print('Extracting Time From', video_path, '...')

    with open(results_txt_path, 'w') as f:
        print('time txt will be saved into ' + results_txt_path)
        frame_len = len(input_arr)
        for frame_id in range(1, frame_len + 1):
            img = input_arr[frame_id - 1]
            date = get_clock(img, model)
            res = str(frame_id) + ' ' + str(date) + '\n'
            f.write(res)

    video_name = video_path.split('/')[-1].split('.')[0]
    if flag_check:
        try:
            check_time(video_name, video_path, results_txt_path, frame_len)
        except:
            print('Error in', video_path)


def check_time(video_name, video_path, results_txt_path, frame_len):
    video_date = time2date(video_name)
    list_date = [''] * frame_len
    list_timestamp = [' '] * frame_len
    lines = []

    with open(results_txt_path, 'r') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            # 1 2019-07-12 20:06:27
            index_current, date_current = split_frame_date(lines[index])
            list_date[index] = date_current

    date_first = list_date[0]
    date_last = list_date[-1]

    for index, temp_date in enumerate(list_date):
        if not temp_date[0:7] == video_date[0:7]:
            if index == 0:
                i = index
                while not temp_date[0:7] == video_date[0:7]:
                    i = i + 1
                    temp_date = list_date[i]
                list_date[index] = temp_date

            else:
                count = 0
                index_prep, date_prep = split_frame_date(lines[index - 1])
                j = index - 1
                while lines[j] == lines[j - 1]:
                    count += 1
                if count >= 20:
                    list_date[index] = update_date(list_date[index - 1])
                else:
                    list_date[index] = list_date[index - 1]
        else:
            list_date[index] = temp_date

    for index, temp_date in enumerate(list_date):
        list_timestamp[index] = float(date2time(list_date[index]))

    # Int 2 Float
    index_first = 0
    index_last = 0
    index_end = frame_len - 1
    for index, temp_time_stamp in enumerate(list_timestamp):
        if index <= index_last and index != 0:
            continue
        index_first = index

        if index_first == index_end:
            break

        index_last = index
        temp_index = index + 1
        if temp_index == index_end:
            break

        while list_timestamp[temp_index] == list_timestamp[index_first]:
            index_last += 1
            temp_index += 1
            if temp_index == index_end:
                break

        len_index = (index_last - index_first) + 1
        err_index = 1.0 / float(len_index)

        l = index_first
        while l >= index_first and l <= index_last:
            list_timestamp[l] += float(err_index * (l - index_first))
            l += 1

    os.remove(results_txt_path)
    with open(results_txt_path, 'w') as file:
        for index, line in enumerate(lines):
            # 1 2019-07-12 20:06:27
            temp_time_stamp = str('%.3f' % list_timestamp[index])
            temp_line = line.strip().split(' ')[0] + ' ' + time2date(
                int(list_timestamp[index])) + ' ' + temp_time_stamp + '\n'
            file.write(temp_line)


def show_freq(list):
    index = 0;
    max = 0;
    for i in range(len(list)):
        flag = 0
        for j in range(i + 1, len(list)):
            if list[j] == list[i]:
                flag += 1

            if flag > max:
                max = flag
                index = i
    return list[index]


def date_error(date_1, date_2):
    time_1 = date2time(date_1)
    time_2 = date2time(date_2)
    error = int(time_1) - int(time_2)
    return error


def update_date(date):
    time_curr = int(date2time(date))
    time_next = str(time_curr + 1)
    date_next = time2date(time_next)
    return date_next


def trans_date(year, month, day, hour, min, sec):
    date = year + '-' + month + '-' + day + ' ' + hour + ':' + min + ':' + sec
    return date


def get_date_sub(date):
    # 2019-07-12 20:06:27
    if not isinstance(date, str):
        date = date.strftime("%Y-%m-%d %H:%M:%S")
    year = date.split('-')[0]
    month = date.split('-')[1]
    day = date.split('-')[2][0:2]
    hour = date.split('-')[2][3:5]
    min = date.split(':')[1]
    sec = date.split(':')[2]

    return year, month, day, hour, min, sec


def split_frame_date(str):
    # 1 2019-07-12 20:06:27
    index = str.split(' ')[0]
    date = str.split(' ')[-2] + ' ' + str.split(' ')[-1].strip()

    return index, date


def date2time(date, convert_to_utc=True):
    date = date.strip()
    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    if isinstance(date, datetime.datetime):
        if convert_to_utc:
            date = date + datetime.timedelta(hours=-8)
        date_Epoch = datetime.datetime.strptime('1970-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
        time_stamp = (date - date_Epoch).total_seconds()
        time_stamp = str(int(time_stamp))
        return time_stamp


def time2date(timestamp, convert_to_local=True):
    timestamp = int(timestamp)
    if isinstance(timestamp, (int, float)):
        dt = datetime.datetime.utcfromtimestamp(timestamp)
        if convert_to_local:
            dt = dt + datetime.timedelta(hours=8)
        return str(dt)


def getInputArray(videoPath):
    cap = cv2.VideoCapture()
    cap.open(videoPath)
    input_arr = []
    ret, frame = cap.read()

    while ret:
        # hbc0608  for batch loader
        # frame = cv2.resize(frame, (416, 416))
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        input_arr.append(frame)
        ret, frame = cap.read()
    # return input_arr[:1200]
    return input_arr[:3600]


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(  # input shape (1, 28, 28)
            nn.Conv2d(
                in_channels=1,  # input height
                out_channels=16,  # n_filters
                kernel_size=5,  # filter size
                stride=1,  # filter movement/step
                padding=2,
                # if want same width and length of this image after con2d, padding=(kernel_size-1)/2 if stride=1
            ),  # output shape (16, 28, 28)
            nn.ReLU(),  # activation
            nn.MaxPool2d(kernel_size=2),  # choose max value in 2x2 area, output shape (16, 14, 14)
        )
        self.conv2 = nn.Sequential(  # input shape (16, 14, 14)
            nn.Conv2d(16, 32, 5, 1, 2),  # output shape (32, 14, 14)
            nn.ReLU(),  # activation
            nn.MaxPool2d(2),  # output shape (32, 7, 7)
        )
        self.out = nn.Linear(32 * 7 * 7, 10)  # fully connected layer, output 10 classes

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)  # flatten the output of conv2 to (batch_size, 32 * 7 * 7)
        output = self.out(x)
        return output, x  # return x for visualization


if __name__ == '__main__':
    video_path = '/home/syx/mnt/camera/origin/18/1573010956.mp4'
    input_arr = getInputArray(video_path)

    model = model_generator()
    get_all_clock(input_arr, video_path, '/home/jlx/mmap_vsa/test.txt', model)
