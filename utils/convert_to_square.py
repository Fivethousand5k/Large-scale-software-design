import numpy as np


def convert_to_square(bbox, img_size, margin_scale=0.22):
    square_bbox = bbox.copy()
    h = bbox[3] - bbox[1] + 1
    w = bbox[2] - bbox[0] + 1
    max_side = np.minimum(h, w)
    margin = margin_scale * max_side
    square_bbox[0] = bbox[0] + w * 0.5 - max_side * 0.5
    square_bbox[1] = bbox[1] + h * 0.5 - max_side * 0.5
    square_bbox[2] = square_bbox[0] + max_side - 1
    square_bbox[3] = square_bbox[1] + max_side - 1

    bb = np.zeros(4, dtype=np.int32)
    bb[0] = np.maximum(square_bbox[0] - margin / 2, 0)
    bb[1] = np.maximum(square_bbox[1] - margin / 2, 0)
    bb[2] = np.minimum(square_bbox[2] + margin / 2, img_size[1])
    bb[3] = np.minimum(square_bbox[3] + margin / 2, img_size[0])

    return bb