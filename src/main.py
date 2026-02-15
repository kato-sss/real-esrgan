from config import DEVICE
from model_loader import load_model
from processor import process_images

def main():
    print(f'Using device: {DEVICE}')
    upscaler = load_model()
    process_images(upscaler)
    print('🎉 全処理完了')

if __name__ == "__main__":
    main()
