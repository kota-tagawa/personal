import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# === Windows用フォント設定 (Windows以外ではコメントアウトしても良い) ===
plt.rcParams['font.family'] = 'MS Gothic'

# 図全体の定義（レイアウト設定）
fig = plt.figure(figsize=(14, 8))
# width_ratiosで左右の幅の比率を調整。wspace, hspaceで間隔を調整。
gs = fig.add_gridspec(2, 2, width_ratios=[1.3, 1], wspace=0.15, hspace=0.3)

# サブプロットの配置
ax_a = fig.add_subplot(gs[:, 0]) # 左側 (a) 縦ぶち抜き
ax_b = fig.add_subplot(gs[0, 1]) # 右上 (b)
ax_c = fig.add_subplot(gs[1, 1]) # 右下 (c)

# 凡例用の軸を最下部に作成
ax_legend = fig.add_axes([0.1, 0.02, 0.8, 0.05])
ax_legend.axis('off')


# === 共通描画関数 ===
def draw_floor_base(ax, p0_label=r'$\mathbf{p}_0$', p1_label=r'$\mathbf{p}_1$'):
    ax.set_aspect('equal')
    ax.axis('off')
    # 床の線
    ax.plot([0, 10], [0, 0], color='black', linewidth=3)
    # 端点 p0, p1 (黒塗り丸)
    ax.plot(0, 0, 'o', color='black', markersize=12, zorder=3)
    ax.plot(10, 0, 'o', color='black', markersize=12, zorder=3)
    ax.text(0, -1.0, p0_label, ha='center', va='top', fontsize=18, fontweight='bold')
    ax.text(10, -1.0, p1_label, ha='center', va='top', fontsize=18, fontweight='bold')
    # X軸の範囲を少し広めに取って文字が切れないようにする
    ax.set_xlim(-1, 11)


# =========================================
# (a) 射影と検証（左側）
# =========================================
draw_floor_base(ax_a)
cx, cy = 5, 7  # カメラ位置（中央寄りに変更）
px, py = 5, 0  # 射影点
d_th = 7.5      # 閾値距離（円の半径）

# カメラ
ax_a.plot(cx, cy, 'x', color='black', markersize=14, markeredgewidth=3, zorder=3)
ax_a.text(cx, cy + 0.5, r'$\mathbf{c}$', ha='center', fontsize=20, fontweight='bold')

# 射影点
ax_a.plot(px, py, 'x', color='black', markersize=14, markeredgewidth=3, zorder=3)
ax_a.text(px + 0.5, 0.5, r'$\mathbf{p}_{\mathrm{proj}}$', ha='left', fontsize=20, fontweight='bold')

# 破線（射影線）と直角記号
ax_a.plot([cx, px], [cy, py], '--', color='black', linewidth=2)
rect = patches.Rectangle((px, 0), 0.5, 0.5, linewidth=1.5, edgecolor='black', facecolor='none')
ax_a.add_patch(rect)

# ベクトル矢印 d
ax_a.annotate('', xy=(10, -0.5), xytext=(0, -0.5),
              arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))
ax_a.text(5, -0.8, r'$\mathbf{d}$', ha='center', va='top', fontsize=20, fontweight='bold')

# ベクトル矢印 td
ax_a.annotate('', xy=(px, 0.5), xytext=(0, 0.5),
              arrowprops=dict(arrowstyle='->', lw=2.0, color='black'))
ax_a.text(px/2, 0.8, r'$t\mathbf{d}$', ha='center', fontsize=20, fontweight='bold')

ax_a.text(cx - 2.0,  cy - 3.0, r'$d_{\mathrm{th}}$', fontsize=20)


# 条件式ボックス (白い四角で囲む)
text_box_content = r'$0 \leq t \leq 1$' + '\n' + r'$\|\mathbf{c} - \mathbf{p}_{\mathrm{proj}}\| \leq d_{\mathrm{th}}$'
box_x, box_y = cx + 0.5, cy - 3.0 # 位置調整
rect_box = patches.Rectangle((box_x, box_y), 5.5, 2.5, linewidth=1.5, edgecolor='black', facecolor='white', zorder=4)
ax_a.add_patch(rect_box)
ax_a.text(box_x + 2.7, box_y + 1.25, text_box_content, fontsize=16, ha='center', va='center', zorder=5)

# タイトル
ax_a.text(5, -3.5, '(a) カメラ位置を射影', ha='center', fontsize=18)
# Y軸の表示範囲を調整してタイトルが見えるようにする
ax_a.set_ylim(-4, cy + d_th + 1)


# =========================================
# (b) サンプリング：間隔が大きい（右上）
# =========================================
draw_floor_base(ax_b)
p1_x, p2_x = 2.0, 8.0
offset = 2.0 # 内側への移動量

# 射影点 (x)
ax_b.plot(p1_x, 0, 'x', color='black', markersize=14, markeredgewidth=3, zorder=3)
ax_b.plot(p2_x, 0, 'x', color='black', markersize=14, markeredgewidth=3, zorder=3)
ax_b.text(p1_x, -1.0, r'$\mathbf{p}_{\mathrm{proj}1}$', ha='center', va='top', fontsize=16, fontweight='bold')
ax_b.text(p2_x, -1.0, r'$\mathbf{p}_{\mathrm{proj}2}$', ha='center', va='top', fontsize=16, fontweight='bold')

# 追加点 (●)
new_p1_x = p1_x + offset
new_p2_x = p2_x - offset
ax_b.plot(new_p1_x, 0, 'o', color='black', markersize=12, zorder=3)
ax_b.plot(new_p2_x, 0, 'o', color='black', markersize=12, zorder=3)

# 説明テキスト
ax_b.annotate('', xy=(p2_x, 0.5), xytext=(p1_x, 0.5),
              arrowprops=dict(arrowstyle='<->', lw=2.0, color='black'))
ax_b.text(5, 1.0, r'$\| \mathbf{p}_{\mathrm{proj1}} - \mathbf{p}_{\mathrm{proj2}} \| > d_{\mathrm{sample}}$', ha='center', fontsize=16, fontweight='bold')
ax_b.text(5, 2.5, '射影点から一定距離内側に\n境界点を追加', ha='center', fontsize=16)

# 説明矢印（直線）
arrow_props = dict(arrowstyle='->', lw=2.0, color='black')

# タイトル
ax_b.text(5, -3.5, '(b) サンプリング (間隔が大きい場合)', ha='center', fontsize=18)
ax_b.set_ylim(-4, 4) # Y軸範囲調整


# =========================================
# (c) サンプリング：間隔が小さい（右下）
# =========================================
draw_floor_base(ax_c)
p1_x_c, p2_x_c = 4.0, 6.0
mid_x_c = (p1_x_c + p2_x_c) / 2

# 射影点 (x)
ax_c.plot(p1_x_c, 0, 'x', color='black', markersize=14, markeredgewidth=3, zorder=3)
ax_c.plot(p2_x_c, 0, 'x', color='black', markersize=14, markeredgewidth=3, zorder=3)
ax_c.text(p1_x_c, -1.0, r'$\mathbf{p}_{\mathrm{proj}1}$', ha='center', va='top', fontsize=16, fontweight='bold')
ax_c.text(p2_x_c, -1.0, r'$\mathbf{p}_{\mathrm{proj}2}$', ha='center', va='top', fontsize=16, fontweight='bold')

# 追加点 (● 中点)
ax_c.plot(mid_x_c, 0, 'o', color='black', markersize=12, zorder=3)

# 説明テキスト
ax_c.annotate('', xy=(p2_x_c, 0.5), xytext=(p1_x_c, 0.5),
              arrowprops=dict(arrowstyle='<->', lw=2.0, color='black'))
ax_c.text(mid_x_c, 1.0, r'$\| \mathbf{p}_{\mathrm{proj1}} - \mathbf{p}_{\mathrm{proj2}} \| < d_{\mathrm{sample}}$', ha='center', fontsize=16, fontweight='bold')
ax_c.text(mid_x_c, 2.5, '射影点の中点に\n境界点を追加', ha='center', fontsize=16)

# タイトル
ax_c.text(5, -3.5, '(c) サンプリング (間隔が小さい場合)', ha='center', fontsize=18)
ax_c.set_ylim(-4, 4) # Y軸範囲調整

# =========================================
# 凡例 (最下部)
# =========================================
# 凡例の要素を手動で作成
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', label=': 床境界点', markerfacecolor='black', markersize=12),
    plt.Line2D([0], [0], marker='x', color='w', label=': カメラの射影点', markeredgecolor='black', markersize=14, markeredgewidth=3),
]
# 凡例を描画
ax_legend.legend(handles=legend_elements, loc='center', ncol=2, frameon=False, fontsize=16)


# plt.tight_layout() # grid_specを使っているのでtight_layoutは使わない方が配置が崩れない
plt.show()