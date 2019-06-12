# -*- coding: utf-8 -*-

# 改变图像大小
import cv2
im1 = cv2.imread("1.jpg")
im2 = cv2.resize(im1, (680, 450))  # 为图片重新指定尺寸
cv2.imwrite("2.jpg", im2)