import numpy as np
from scipy.integrate import quad
from scipy.optimize import fsolve

# 给定常量
a = 55 / (2 * np.pi)
v = 100  # 速度，单位为 cm/s
theta_max = 32 * np.pi  # 极角最大值为 32π


# 定义被积函数
def integrand(theta):
    return np.sqrt(theta ** 2 + 1)


# 定义方程，求解某一时刻的极角 theta
def equation(theta, t):
    # 计算从 theta 到 theta_max 的积分
    integral_value, _ = quad(integrand, theta, theta_max)
    return a * integral_value - v * t


# 定义时间范围，从 0 到 300 秒
time_range = np.arange(0, 301, 1)  # 每秒一组数据，时间从 0s 到 300s

# 求解每一秒的极角 theta
theta_values = []
for t in time_range:
    theta_initial_guess = 30 * np.pi  # 初始猜测值，接近最大极角
    theta_solution = fsolve(equation, theta_initial_guess, args=(t,))[0]
    theta_values.append(theta_solution)

# 将结果转换为 numpy 数组，便于后续处理
theta_values = np.array(theta_values)

# 显示前 10 个和最后 10 个 theta 值作为示例
theta_values[:10], theta_values[-10:]  # 显示前 10 个和最后 10 个 theta 值

## 计算龙头走过的角度
theta_ed = []
for x in theta_values:
    theta_ed.append(32 * np.pi - x)


# print('theta_0:', theta_ed)

## 计算龙头前的半径
r_0 = []
for x in theta_ed:
    r_0.append(880 - 55 / 2 / np.pi * x)


## 计算龙头夹角
theta_0 = []
for r in r_0:
    # 定义方程
    def equation(x):
        term1 = r + (55 * x) / (2 * np.pi)
        return r ** 2 + term1 ** 2 - 2 * r * term1 * np.cos(x) - 286 ** 2


    # 初始猜测值
    x_initial_guess = 2  # 可调整初始猜测值
    # 使用 fsolve 求解
    x_solution = fsolve(equation, x_initial_guess)
    theta_0.append(x_solution[0])
# print('theta_0:', theta_0[0])

## 计算第一龙身半径以及夹角
r_1 = []
theta_1 = []
for i in np.arange(0, 301, 1):
    r = r_0[i] + 55 / (2 * np.pi) * theta_0[i]  # 第一龙身前半径
    r_1.append(r)


    # 定义方程
    def equation(x):
        term1 = r + (55 * x) / (2 * np.pi)
        return r ** 2 + term1 ** 2 - 2 * r * term1 * np.cos(x) - 165 ** 2


    # 初始猜测值
    x_initial_guess = 2  # 可调整初始猜测值

    # 使用 fsolve 求解
    x_solution = fsolve(equation, x_initial_guess)
    theta_1.append(x_solution[0])
    # print(f"求解得到 x = {x_solution[0]:.6f}")

# 计算每节龙身的位置，并输出结果
r_prev = r_1[60]  # 修改此处即可求出各个时间的数据
x_prev = theta_1[60]  # 修改此处即可求出各个时间的数据

# print('r_1:', r_prev)
# print('theta_1:', x_prev)

x_all = theta_0[60] + x_prev  # 修改此处即可求出各个时间的数据
n = 222
r_values = [r_prev]
x_values = [x_prev]
pos = [(r_prev * np.cos(x_all), r_prev * np.sin(x_all))]

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
