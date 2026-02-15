import os
import cv2
import torch
import numpy as np
from PIL import Image
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

device = 'cuda' if torch.cuda.is_available() else 'cpu'

input_folder = 'input_images'
output_folder = 'output_images'
os.makedirs(output_folder, exist_ok=True)

def demosaic_preprocess(img):
    img = cv2.medianBlur(img, 5)
    img = cv2.bilateralFilter(img, 9, 75, 75)
    return img

model = RRDBNet(
    num_in_ch=3, num_out_ch=3,
    num_feat=64, num_block=23,
    num_grow_ch=32, scale=4
)

upscaler = RealESRGANer(
    scale=4,
    model_path='weights/RealESRGAN_x4plus_anime_6B.pth',
    model=model,
    tile=0,
    tile_pad=32,
    pre_pad=0,
    half=(device == 'cuda'),
    device=device
)

for file in os.listdir(input_folder):
    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
        img = cv2.imread(os.path.join(input_folder, file))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = demosaic_preprocess(img)

        try:
            out, _ = upscaler.enhance(img)
            Image.fromarray(out).save(os.path.join(output_folder, file))
        except Exception as e:
            print(f"失敗: {file} → {e}")
