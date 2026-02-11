import cv2
import matplotlib.pyplot as plt
import sys
import os

def compare_orb_features(image_path_rich, image_path_poor):
    # 1. 画像の読み込み
    if not os.path.exists(image_path_rich) or not os.path.exists(image_path_poor):
        print("エラー: 画像ファイルが見つかりません。パスを確認してください。")
        return

    img_rich = cv2.imread(image_path_rich)
    img_poor = cv2.imread(image_path_poor)

    # 2. ORB検出器の作成 (ORB-SLAMの設定に近いパラメータ)
    # nfeatures=1000: 1画像あたり最大1000個の特徴点を探す
    orb = cv2.ORB_create(nfeatures=1000, scaleFactor=1.2, nlevels=8)

    # 3. 特徴点の検出 (Detect)
    kp_rich = orb.detect(img_rich, None)
    kp_poor = orb.detect(img_poor, None)

    # 4. 特徴点の描画
    # color=(0, 255, 0): 緑色
    img_rich_res = cv2.drawKeypoints(img_rich, kp_rich, None, color=(0, 255, 0), flags=0)
    img_poor_res = cv2.drawKeypoints(img_poor, kp_poor, None, color=(0, 255, 0), flags=0)

    # 5. 表示用にBGRからRGBへ変換 (Matplotlib用)
    img_rich_rgb = cv2.cvtColor(img_rich_res, cv2.COLOR_BGR2RGB)
    img_poor_rgb = cv2.cvtColor(img_poor_res, cv2.COLOR_BGR2RGB)

    # 6. 並べて表示・保存するためのプロット作成
    fig, axes = plt.subplots(2, 1, figsize=(12, 6))

    # 左：特徴が豊かな画像
    axes[0].imshow(img_rich_rgb)
    axes[0].set_title(f"Feature Rich\n(Points: {len(kp_rich)})", fontsize=14, fontweight='bold')
    axes[0].axis('off')

    # 右：特徴が乏しい画像
    axes[1].imshow(img_poor_rgb)
    axes[1].set_title(f"Textureless (Wall)\n(Points: {len(kp_poor)})", fontsize=14, fontweight='bold')
    axes[1].axis('off')

    plt.tight_layout()
    
    # 画像として保存
    output_filename = "orb_comparison_result.png"
    plt.savefig(output_filename, dpi=300)
    print(f"比較画像を保存しました: {output_filename}")
    
    # 画面に表示
    plt.show()

# --- 実行部分 ---
file_rich = 'rich.jpg' 
file_poor = 'wall.jpg' 

# 画像がない場合のダミー生成用コード（テスト用）
# ※実際に使う際は、上記のファイル名をご自身の画像に書き換えてください
if not os.path.exists(file_rich):
    import numpy as np
    # ダミー画像生成: ノイズ画像（特徴多）と真っ白画像（特徴少）
    print("画像ファイルが見つからないため、ダミー画像を生成してテストします...")
    dummy_rich = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    dummy_poor = np.ones((480, 640, 3), dtype=np.uint8) * 240 # 薄いグレー
    cv2.imwrite('rich.jpg', dummy_rich)
    cv2.imwrite('wall.jpg', dummy_poor)

# 実行
compare_orb_features(file_rich, file_poor)