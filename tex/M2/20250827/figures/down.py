from PIL import Image
import os

# 縮小率
scale = 0.5
# 対応画像拡張子
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png')

# 入力
path = input("画像ファイル名またはディレクトリを入力してください: ").strip()

def resize_image(full_path):
    try:
        img = Image.open(full_path)
        new_size = (int(img.width * scale), int(img.height * scale))
        img_resized = img.resize(new_size, Image.LANCZOS)
        img_resized.save(full_path)
        print(f"{os.path.basename(full_path)} を縮小して上書き保存しました。")
    except Exception as e:
        print(f"{os.path.basename(full_path)} の処理中にエラーが発生しました: {e}")

# ファイルかディレクトリか判定
if os.path.isfile(path):
    if path.lower().endswith(IMAGE_EXTENSIONS):
        resize_image(path)
    else:
        print("エラー: 画像ファイルではありません。")
elif os.path.isdir(path):
    image_files = [f for f in os.listdir(path) if f.lower().endswith(IMAGE_EXTENSIONS)]
    if not image_files:
        print("指定されたディレクトリに画像ファイルが見つかりません。")
    else:
        for file in image_files:
            full_path = os.path.join(path, file)
            resize_image(full_path)
else:
    print("エラー: ファイルまたはディレクトリが見つかりません。")
