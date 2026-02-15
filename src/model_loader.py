from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from config import *

def load_model():
    model = RRDBNet(
        num_in_ch=3,
        num_out_ch=3,
        num_feat=64,
        num_block=NUM_BLOCK,
        num_grow_ch=32,
        scale=SCALE
    )

    upscaler = RealESRGANer(
        scale=SCALE,
        model_path=WEIGHTS_PATH,
        model=model,
        tile=TILE,
        tile_pad=TILE_PAD,
        pre_pad=0,
        half=True if DEVICE == 'cuda' else False,
        device=DEVICE
    )

    return upscaler
