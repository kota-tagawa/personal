from PIL import Image
import sys

# 標準入力からファイル名を受け取る
filename = sys.stdin.readline().strip()

try:
    # 画像を開く
    img = Image.open(filename)

    # 画像の読み込み
    img = Image.open("input.jpg")  # 入力画像ファイル

    # 縮小後の解像度
    scale = 0.25  # 25%の解像度に縮小
    new_size = (int(img.width * scale), int(img.height * scale))

    # 画像をリサイズ
    img_resized = img.resize(new_size, Image.LANCZOS)

    # 上書き保存（元と同じファイル名）
    img_resized.save(filename)

    print(f"{filename} に上書き保存しました。")

except FileNotFoundError:
    print("エラー: ファイルが見つかりません。")
except Exception as e:
    print(f"エラーが発生しました: {e}")