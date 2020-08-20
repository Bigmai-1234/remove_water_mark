import cv2
import numpy as np
import os

def move_mark(slices,percentile_ratio):
    hight, width, depth = slices.shape[0:3]
    sum_ = slices.sum(2)
    t = list(set(list(np.array(sum_).flat)))
    qual = np.percentile(t,percentile_ratio)
    for h in range(hight):
        for w in range(width):
            if sum_[h][w] > qual:
                slices[h][w] = [255,255,255]
    return slices


def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in range(0, image.shape[0], stepSize[1]):
        for x in range(0, image.shape[1], stepSize[0]):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


# 返回滑动窗结果集合，本示例暂时未用到
def get_slice(image, stepSize, windowSize):
    slice_sets = []
    for (x, y, window) in sliding_window(image, stepSize, windowSize):
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != windowSize[1] or window.shape[1] != windowSize[0]:
            continue
        slice = image[y:y + windowSize[1], x:x + windowSize[0]]
        slice_sets.append(slice)
    return slice_sets


def do_remove_mark(image,percentile_ratio,size_):

    # 自定义滑动窗口的大小
    w = image.shape[1]
    h = image.shape[0]
    # 本代码将图片分为3×3，共九个子区域，winW, winH和stepSize可自行更改
    (winW, winH) = (int(w/size_),int(h/size_))
    stepSize = (int(w/size_), int(h/size_))

    for (x, y, window) in sliding_window(image, stepSize=stepSize, windowSize=(winW, winH)):
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != winH or window.shape[1] != winW:
            continue
        slice = image[y:y+winH,x:x+winW]
        image[y:y+winH,x:x+winW] = move_mark(slice,percentile_ratio)

    return image
    
    
# TODO
# path = "./train/1/"
# for img_ in os.listdir(path):
#     if img_[-3:] != "png":continue
#     image = cv2.imread(path + img_)
#     img = do_remove_mark(image,50,500)
#     img = do_remove_mark(img,50,3)
#     cv2.imwrite("./trainres/" + img_,img)   
