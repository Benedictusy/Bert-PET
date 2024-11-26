# ... 之前的代码保持不变

# 计算每节龙身的位置，并输出结果
r_prev = r_1[60]  # 修改此处即可求出各个时间的数据
x_prev = theta_1[60]  # 修改此处即可求出各个时间的数据

# 计算龙头位置并加入列表
r_head = r_0[60]
x_head = theta_0[60]
pos_0 = (r_head * np.cos(x_head), r_head * np.sin(x_head))
pos = [pos_0]  # 初始化 pos 列表为包含龙头位置

x_all = x_head + x_prev  # 累积初始角度
n = 222
r_values = [r_prev]
x_values = [x_prev]

# 递推计算
for i in range(2, n + 1):
    # 计算 r_i
    r_i = r_prev + (55 / (2 * np.pi)) * x_prev

    # 计算 x_i
    term1 = r_i ** 2 + (r_i + (55 / (2 * np.pi)) * x_prev) ** 2 - 165 ** 2
    term2 = 2 * (r_i + (55 / (2 * np.pi)) * x_prev) * r_i
    cos_x_i = term1 / term2
    cos_x_i = np.clip(cos_x_i, -1, 1)  # 确保 cos_x_i 在有效范围内
    x_i = np.arccos(cos_x_i)

    # 更新 r_values 和 x_values
    r_values.append(r_i)
    x_values.append(x_i)

    # 累积角度偏移并计算位置
    x_pot = r_i * np.cos(x_all)
    y_pot = r_i * np.sin(x_all)
    pos.append((x_pot, y_pot))
    x_all += x_i

    # 更新上一个 r 和 x
    r_prev = r_i
    x_prev = x_i

# 输出结果
for i in range(n):
    print(
        f"r_{i + 1} = {r_values[i]:.6f}, x_{i + 1} = {x_values[i]:.6f}, pos_{i + 1} = ({pos[i][0]:.6f}, {pos[i][1]:.6f})")
