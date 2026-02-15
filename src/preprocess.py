import cv2

def preprocess_for_mosaic(img_np):
    """
    モザイク角をなだらかにする
    """
    return cv2.GaussianBlur(img_np, (3, 3), 0)
