import os
import cv2
import torch
import numpy as np
from PIL import Image

from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

# =========================
# デバイス設定
# =========================
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')

# =========================
# パス設定
# =========================
INPUT_DIR = 'input_images'
OUTPUT_DIR = 'output_images'
WEIGHTS_PATH = 'weights/RealESRGAN_x4plus_anime_6B.pth'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# モザイク除去前処理
# =========================
def preprocess_for_mosaic(img_np):
    """
    モザイクのブロック角を軽くなだらかにする
    """
    return cv2.GaussianBlur(img_np, (3, 3), 0)

# =========================
# anime6b専用モデル定義
# =========================
model = RRDBNet(
    num_in_ch=3,
    num_out_ch=3,
    num_feat=64,
    num_block=6,   # ★ anime6bは6ブロック
    num_grow_ch=32,
    scale=4
)

# =========================
# Upscaler 初期化
# =========================
upscaler = RealESRGANer(
    scale=4,
    model_path=WEIGHTS_PATH,
    model=model,
    tile=128,        # モザイク対策
    tile_pad=20,
    pre_pad=0,
    half=True if device == 'cuda' else False,
    device=device
)

# =========================
# 画像処理
# =========================
for filename in os.listdir(INPUT_DIR):

    if not filename.lower().endswith(
        ('.png', '.jpg', '.jpeg', '.bmp', '.webp')
    ):
        continue

    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, filename)

    try:
        print(f'🔄 Processing: {filename}')

        # 画像読み込み
        img = Image.open(input_path).convert('RGB')
        img_np = np.array(img)

        # ===== 前処理 =====
        img_np = preprocess_for_mosaic(img_np)

        # ===== 1回目アップスケール =====
        out1, _ = upscaler.enhance(img_np)

        # ===== 2回目アップスケール =====
        out2, _ = upscaler.enhance(out1)

        # 保存
        Image.fromarray(out2).save(output_path)

        print(f'✅ Saved: {output_path}')

    except Exception as e:
        print(f'❌ Error: {filename} → {e}')

print('🎉 全処理完了')
