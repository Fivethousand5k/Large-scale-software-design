import numpy as np
import cv2
import os
import math
from MyColor import MyColor
from config import name_list
from PIL import Image
from PIL import ImageFont, ImageDraw

COLORS_10 =[(144,238,144),(178, 34, 34),(221,160,221),(  0,255,  0),(  0,128,  0),(210,105, 30),(220, 20, 60),
            (192,192,192),(255,228,196),( 50,205, 50),(139,  0,139),(100,149,237),(138, 43,226),(238,130,238),
            (255,  0,255),(  0,100,  0),(127,255,  0),(255,  0,255),(  0,  0,205),(255,140,  0),(255,239,213),
            (199, 21,133),(124,252,  0),(147,112,219),(106, 90,205),(176,196,222),( 65,105,225),(173,255, 47),
            (255, 20,147),(219,112,147),(186, 85,211),(199, 21,133),(148,  0,211),(255, 99, 71),(144,238,144),
            (255,255,  0),(230,230,250),(  0,  0,255),(128,128,  0),(189,183,107),(255,255,224),(128,128,128),
            (105,105,105),( 64,224,208),(205,133, 63),(  0,128,128),( 72,209,204),(139, 69, 19),(255,245,238),
            (250,240,230),(152,251,152),(  0,255,255),(135,206,235),(  0,191,255),(176,224,230),(  0,250,154),
            (245,255,250),(240,230,140),(245,222,179),(  0,139,139),(143,188,143),(255,  0,  0),(240,128,128),
            (102,205,170),( 60,179,113),( 46,139, 87),(165, 42, 42),(178, 34, 34),(175,238,238),(255,248,220),
            (218,165, 32),(255,250,240),(253,245,230),(244,164, 96),(210,105, 30)]

def draw_bbox(img, box, cls_name, identity=None, offset=(0,0)):
    '''
        draw box of an id
    '''
    x1,y1,x2,y2 = [int(i+offset[idx%2]) for idx,i in enumerate(box)]
    # set color and label text
    color = COLORS_10[identity%len(COLORS_10)] if identity is not None else COLORS_10[0]
    label = '{} {}'.format(cls_name, identity)
    # box text and bar
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
    cv2.rectangle(img,(x1, y1),(x2,y2),color,2)
    cv2.rectangle(img,(x1, y1),(x1+t_size[0]+3,y1+t_size[1]+4), color,-1)
    cv2.putText(img,label,(x1,y1+t_size[1]+4), cv2.FONT_HERSHEY_PLAIN, 1, [255,255,255], 1)
    return img

def draw_bbox_for_recog(frame,boxes,screen_num,recog_bbox_GroupBy_TrackId):
    ######adjust the font size according to the number_of screen
    if screen_num==1:
        font_size=20
    elif screen_num==4:
        font_size=40
    elif screen_num==9:
        font_size=60
    elif screen_num==16:
        font_size=80

    font = ImageFont.truetype('/usr/share/fonts/truetype/arphic/ukai.ttc', font_size)
    for i in range(len(boxes)):
        pt1 = (boxes[i][1], boxes[i][0])  # 矩形左上角点
        pt2 = (boxes[i][3], boxes[i][2])  # 矩形右下角点
        track_num = boxes[i][4]  # 轨迹的序�?\
        pred_num = boxes[i][5]   #index of the person predicted
        color = MyColor.colorsHub[track_num % MyColor.color_total]
        cv2.rectangle(frame, pt1, pt2, color, 2)
        pos = (pt1[0], int(pt1[1] - 20*math.sqrt(screen_num)))  # 使得名字出现在人脸上�
        frame_PIL = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(frame_PIL)
        pred_num,revised_tag,is_stranger=strategy(original_pred_num=pred_num,track_id=track_num,recog_bbox_GroupBy_TrackId=recog_bbox_GroupBy_TrackId)
        chinese_name=name_list[pred_num]
        if revised_tag:             # if pred_num has been revised, we set the color of name
            color_of_name=(255,0, 0)
        else:
            color_of_name=(0, 255, 0)
        color_of_name = (0, 255, 0)
        if is_stranger:
            color_of_name = (255, 0, 0)
            chinese_name="不在库中"

        draw.text(pos, chinese_name, font=font, fill=color_of_name)
        frame = cv2.cvtColor(np.asarray(frame_PIL), cv2.COLOR_RGB2BGR)
    return frame

def strategy(original_pred_num,track_id,recog_bbox_GroupBy_TrackId):
    scores=recog_bbox_GroupBy_TrackId[track_id][0]
    persons_id=recog_bbox_GroupBy_TrackId[track_id][1]
    index=np.argmax(scores)
    processed_pred_num=persons_id[index]
    is_stranger=False
    if scores[index]<12:
        is_stranger=True

    revised_tag=None
    if processed_pred_num == original_pred_num:
        revised_tag=False
    else:
        revised_tag=True
    return processed_pred_num,revised_tag,is_stranger
def convert_to_square(bbox,img_size):
    margin = 20
    square_bbox = bbox.copy()
    h = bbox[3] - bbox[1] + 1
    w = bbox[2] - bbox[0] + 1
    max_side = np.maximum(h, w)
    square_bbox[0] = bbox[0] + w * 0.5 - max_side * 0.5
    square_bbox[1] = bbox[1] + h * 0.5 - max_side * 0.5
    square_bbox[2] = square_bbox[0] + max_side - 1
    square_bbox[3] = square_bbox[1] + max_side - 1
    
    bb = np.zeros(4, dtype=np.int32)
    bb[0] = np.maximum(square_bbox[0]-margin/2, 0)
    bb[1] = np.maximum(square_bbox[1]-margin/2, 0)
    bb[2] = np.minimum(square_bbox[2]+margin/2, img_size[1])
    bb[3] = np.minimum(square_bbox[3]+margin/2, img_size[0])
    return bb
        

def draw_bboxes(img, bbox, identities=None, offset=(0,0)):
    for i,box in enumerate(bbox):
        x1,y1,x2,y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        id = int(identities[i]) if identities is not None else 0    
        color = COLORS_10[id%len(COLORS_10)]
        label = '{} {}'.format("object", id)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1 , 1)[0]
        cv2.rectangle(img,(x1, y1),(x2,y2),color,2)
        cv2.rectangle(img,(x1-1, y1-t_size[1]-3),(x1+t_size[0]+2,y1+2), color,-1)
        cv2.putText(img,label,(x1,y1), cv2.FONT_HERSHEY_PLAIN, 1, [255,255,255], 1)
    return img

def softmax(x):
    assert isinstance(x, np.ndarray), "expect x be a numpy array"
    x_exp = np.exp(x*5)
    return x_exp/x_exp.sum()

def softmin(x):
    assert isinstance(x, np.ndarray), "expect x be a numpy array"
    x_exp = np.exp(-x)
    return x_exp/x_exp.sum()


def readBboxFromTxt(txt_path,result_GroupBy_trackid={}, TaskType='Detection'):

    if not txt_path.endswith('txt'):
        txt_tmp = list(txt_path)
        txt_tmp[-3:]='txt'
        txt_path = "".join(txt_tmp)

    result = {}
    if not os.path.exists(txt_path):
        print("{} not exist, please check it".format(txt_path))
        return result

    if TaskType=='Detection':

        with open(txt_path) as f:
            for cur_line in f.readlines():
                cur_line = cur_line.split(' ')
                if len(cur_line)<3:break

                frame_id = int(cur_line[0])
                x1 = int(cur_line[1])
                y1 = int(cur_line[2])
                x2 = int(cur_line[3])
                y2 = int(cur_line[4])
                confidence = cur_line[5]
                if frame_id not in result:
                    result[frame_id] = [[x1, y1, x2, y2, confidence]]
                else:
                    result[frame_id].append([x1, y1, x2, y2, confidence])

    elif TaskType=='MOT':

        with open(txt_path) as f:
            for cur_line in f.readlines():
                cur_line = cur_line.split(' ')

                frame_id = int(cur_line[0])
                x1 = int(cur_line[1])
                y1 = int(cur_line[2])
                x2 = int(cur_line[3])
                y2 = int(cur_line[4])
                person_id = int(cur_line[5])
                if frame_id not in result:
                    result[frame_id] = [[x1, y1, x2, y2, person_id]]
                else:
                    result[frame_id].append([x1, y1, x2, y2, person_id])

    elif TaskType=='RECOG':

        with open(txt_path) as f:
            for cur_line in f.readlines():
                cur_line = cur_line.split(' ')

                frame_id = int(cur_line[0])
                x1 = int(cur_line[1])
                y1 = int(cur_line[2])
                x2 = int(cur_line[3])
                y2 = int(cur_line[4])
                track_id = int(cur_line[5])
                person_id = int(cur_line[6])
                score= float(cur_line[7])
                if frame_id not in result:
                    result[frame_id] = [[x1, y1, x2, y2, track_id,person_id,score]]
                else:
                  result[frame_id].append([x1, y1, x2, y2,track_id,person_id,score])

                if track_id not in result_GroupBy_trackid:
                    result_GroupBy_trackid[track_id]=[[score],[person_id]]
                else:
                    result_GroupBy_trackid[track_id][0].append(score)
                    result_GroupBy_trackid[track_id][1].append(person_id)


    else:
        raise(NotImplementedError)


    return result

#########opencv 的行人检测工具############
def draw_person(image,person):
    x,y,w,h=person
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

def is_inside(o,i):
    ox,oy,ow,oh = o
    ix,iy,iw,ih = i
    return ox>ix and oy>iy and ox+ow<ix+iw and oy+oh<iy+ih
#############################################

if __name__ == '__main__':
    x = np.arange(10)/10.
    x = np.array([0.5,0.5,0.5,0.6,1.])
    y = softmax(x)
    z = softmin(x)
    import ipdb; ipdb.set_trace()