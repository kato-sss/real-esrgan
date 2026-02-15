import torch
import os

# =========================
# デバイス
# =========================
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# =========================
# パス設定
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_DIR = os.path.join(BASE_DIR, 'input_images')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output_images')
WEIGHTS_PATH = os.path.join(BASE_DIR, 'weights', 'RealESRGAN_x4plus_anime_6B.pth')

# =========================
# モデル設定（anime6b）
# =========================
SCALE = 4
NUM_BLOCK = 6
TILE = 128
TILE_PAD = 20
