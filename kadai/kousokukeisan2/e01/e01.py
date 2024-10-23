# CPUスペック
core_count = 14  # コア数
clock_speed = 2.6  # GHz
simd_width = 8  # AVX-512のSIMD数
fma_count = 2  # FMA数

# メモリスペック
memory_clock_speed = 2666  # MHz (DDR4-2666)
memory_channels = 6  # 最大メモリチャネル数
bus_width = 8  # バス幅（1チャネルあたり 64ビット = 8バイト）

# 理論演算性能（GFLOPS）を計算
gflops = clock_speed * core_count * simd_width * fma_count * 2

# メモリバンド幅を計算（GB/s）
memory_bandwidth = (memory_clock_speed / 1000) * memory_channels * bus_width

# B/F値を計算
bf_ratio = memory_bandwidth / gflops

# 結果を表示
print(f"理論演算性能: {gflops} GFLOPS")
print(f"メモリバンド幅: {memory_bandwidth} GB/s")
print(f"B/F値: {bf_ratio} B/F")
