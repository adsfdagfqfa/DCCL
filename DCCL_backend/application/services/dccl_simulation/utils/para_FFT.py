
def para_FFT(radius):
    # 等效入射面半径 r
    itr = 300  # 迭代次数 itr
    sampling_num = 8192  # 空域/频域采样点数量 M
    window_expand_factor = 3  # 计算窗口扩充因子 G
    window_size = 2 * window_expand_factor * radius  # 计算窗口尺寸 2Gr
    delta = window_size / sampling_num  # 空域采样间隔 delta=2Gr/M
    delta_f = 1.0 / window_size  # 频域采样间隔 deltaF=(2Gr)^(-1)

    return itr, sampling_num, window_expand_factor, window_size, delta, delta_f
