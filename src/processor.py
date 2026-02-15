import os
import numpy as np
from PIL import Image
from preprocess import preprocess_for_mosaic
from config import *

def process_images(upscaler):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(INPUT_DIR):

        if not filename.lower().endswith(
            ('.png', '.jpg', '.jpeg', '.bmp', '.webp')
        ):
            continue

        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        try:
            print(f'🔄 Processing: {filename}')

            img = Image.open(input_path).convert('RGB')
            img_np = np.array(img)

            # ===== 前処理 =====
            img_np = preprocess_for_mosaic(img_np)

            # ===== 1回目アップスケール =====
            out1, _ = upscaler.enhance(img_np)

            # ===== 2回目アップスケール =====
            out2, _ = upscaler.enhance(out1)

            Image.fromarray(out2).save(output_path)

            print(f'✅ Saved: {output_path}')

        except Exception as e:
            print(f'❌ Error: {filename} → {e}')
