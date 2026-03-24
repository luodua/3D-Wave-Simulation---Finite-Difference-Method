import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import imageio  # 用于保存.gif
import time
plt.rcParams["font.sans-serif"] = "SimHei"
plt.rcParams["axes.unicode_minus"] = False


# 设置参数
Lx = 10            # 模拟区域的长度 (m)
Ly = 10            # 模拟区域的宽度 (m)
Lz = 10            # 模拟区域的高度 (m)
Nx = 100             # x方向的网格点数
Ny = 100             # y方向的网格点数
Nz = 100             # z方向的网格点数
dx = Lx / (Nx - 1)  # x方向的网格间距 (m)
dy = Ly / (Ny - 1)  # y方向的网格间距 (m)
dz = Lz / (Nz - 1)  # z方向的网格间距 (m)
c = 1.0             # 波速 (m/s)
total_time = 25    # 总模拟时间 (s)
dt = 0.01           # 时间步长 (s)
timesteps = int(total_time / dt)  # 总时间步数

# 计算稳定性参数
r_x = (c * dt / dx)**2
r_y = (c * dt / dy)**2
r_z = (c * dt / dz)**2
print(f"稳定性参数 r_x = {r_x:.4f}")
print(f"稳定性参数 r_y = {r_y:.4f}")
print(f"稳定性参数 r_z = {r_z:.4f}")

if r_x > 0.5 or r_y > 0.5 or r_z > 0.5:
    print("警告：时间步长可能过大，解可能不稳定！")
    print(f"建议最大时间步长 dt_max_x = {dx/(c*np.sqrt(3)):.6f} s")
    print(f"建议最大时间步长 dt_max_y = {dy/(c*np.sqrt(3)):.6f} s")
    print(f"建议最大时间步长 dt_max_z = {dz/(c*np.sqrt(3)):.6f} s")

# 初始化网格
u = np.zeros((Nx, Ny, Nz))
u_prev = np.zeros((Nx, Ny, Nz))

# 设置初始条件 - 高斯包络
sigma = 0.1  # 高斯包络的标准差
center_x = Lx / 2
center_y = Ly / 2
center_z = Lz / 2
x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)
z = np.linspace(0, Lz, Nz)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
initial_wave = np.exp(-((X - center_x)**2 + (Y - center_y)**2 + (Z - center_z)**2) / (2 * sigma**2))
print(initial_wave)
u += initial_wave

# 创建数组存储波形历史 (用于可视化)
history = np.zeros((timesteps//10 + 1, Nx, Ny, Nz))
history[0] = u.copy()

# 显式有限差分法求解波动方程
print(f"开始三维波浪运动模拟 (总时间: {total_time}s, 时间步: {timesteps})...")
start_time = time.time()
# 预先计算常数项，避免循环内重复计算
# 联系作者

    # 打印进度
    if step % 100 == 0:
        print(f"时间步: {step}/{timesteps} (时间: {step*dt:.2f}s), 最大振幅: {np.max(np.abs(u)):.2f}")

end_time = time.time()
print(f"模拟完成! 耗时: {end_time - start_time:.2f} 秒")

# 可视化结果
print("创建可视化...")

# 1. 波形分布随时间变化 (3D表面图)
fig = plt.figure(figsize=(18, 12))
fig.suptitle('三维波浪运动模拟', fontsize=16)

# 选择中间平面
k_slice = Nz // 2
x_slice = Nx // 2
y_slice = Ny // 2

# 创建网格
X_slice, Y_slice = np.meshgrid(x, y)

# 不同时间点的波形分布
time_points = [0, timesteps//4, timesteps//2, timesteps-1]
titles = ['初始状态', f'{total_time/4:.1f}秒', f'{total_time/2:.1f}秒', f'{total_time:.1f}秒']

for idx, t in enumerate(time_points):
    ax = fig.add_subplot(2, 2, idx+1, projection='3d')
    U_slice = history[t//10][:, :, k_slice]
    surf = ax.plot_surface(X_slice, Y_slice, U_slice, cmap='coolwarm', 
                          rstride=2, cstride=2, alpha=0.8)
    ax.set_title(f'{titles[idx]} (z={z[k_slice]:.3f}m平面)')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('振幅')
    fig.colorbar(surf, ax=ax, shrink=0.6, label='振幅')

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

# 2. 波形分布动画 (沿z轴)
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

def update(frame):
    ax.clear()
    time_idx = frame
    U_slice = history[time_idx][:, :, k_slice]
    
    # 绘制表面
    surf = ax.plot_surface(X_slice, Y_slice, U_slice, cmap='coolwarm', 
                          rstride=2, cstride=2, alpha=0.8)
    
    current_time = time_idx * 10 * dt
    ax.set_title(f'波浪运动过程 (时间: {current_time:.2f}s, z={z[k_slice]:.3f}m平面)')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('振幅')
    ax.set_zlim(-1.0, 1.0)
    
    return surf,
fig.colorbar(surf, ax=ax, label='振幅')
# 创建动画
frames = range(0, len(history), 1)  # 每隔2个时间点取一帧
ani = FuncAnimation(fig, update, frames=frames, interval=50, blit=False)

# 保存动画为.mp4
ani.save('wave_3d_animation.mp4', writer='ffmpeg', fps=20)
print("动画已保存为 wave_3d_animation.mp4")

# 保存动画为.gif
writer_gif = imageio.get_writer('wave_3d_animation.gif', mode='I', duration=0.05)
for frame in frames:
    update(frame)
    plt.draw()
    img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    writer_gif.append_data(img)
writer_gif.close()
print("动画已保存为 wave_3d_animation.gif")

plt.tight_layout()
plt.show()
sys.exit()



# 3. 沿中心线的波形分布随时间变化
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# 沿x轴中心线 (y=center, z=center)
center_idx_y = Ny // 2
center_idx_z = Nz // 2
x_line = x
time_points = np.arange(0, len(history)) * 10 * dt

# 创建2D网格用于pcolormesh
X_grid, T_grid = np.meshgrid(x_line, time_points)

# 创建波形矩阵
U_matrix_x = np.zeros((len(history), Nx))
for i in range(len(history)):
    U_matrix_x[i, :] = history[i][:, center_idx_y, center_idx_z]

# 绘制热力图
heatmap_x = axs[0].pcolormesh(X_grid, T_grid, U_matrix_x, cmap='coolwarm', shading='auto')
cbar_x = fig.colorbar(heatmap_x, ax=axs[0], label='振幅')
axs[0].set_title('沿x轴中心线波形分布随时间变化')
axs[0].set_xlabel('X位置 (m)')
axs[0].set_ylabel('时间 (s)')
axs[0].set_ylim(0, total_time)

# 沿y轴中心线 (x=center, z=center)
center_idx_x = Nx // 2
y_line = y
Y_grid, T_grid = np.meshgrid(y_line, time_points)

# 创建波形矩阵
U_matrix_y = np.zeros((len(history), Ny))
for i in range(len(history)):
    U_matrix_y[i, :] = history[i][center_idx_x, :, center_idx_z]

# 绘制热力图
heatmap_y = axs[1].pcolormesh(Y_grid, T_grid, U_matrix_y, cmap='coolwarm', shading='auto')
cbar_y = fig.colorbar(heatmap_y, ax=axs[1], label='振幅')
axs[1].set_title('沿y轴中心线波形分布随时间变化')
axs[1].set_xlabel('Y位置 (m)')
axs[1].set_ylabel('时间 (s)')
axs[1].set_ylim(0, total_time)

# 沿z轴中心线 (x=center, y=center)
z_line = z
Z_grid, T_grid = np.meshgrid(y_line, time_points)

# 创建波形矩阵
U_matrix_z = np.zeros((len(history), Nz))
for i in range(len(history)):
    U_matrix_z[i, :] = history[i][center_idx_x, center_idx_y, :]

# 绘制热力图
heatmap_z = axs[2].pcolormesh(Z_grid, T_grid, U_matrix_z, cmap='coolwarm', shading='auto')
cbar_z = fig.colorbar(heatmap_z, ax=axs[2], label='振幅')
axs[2].set_title('沿z轴中心线波形分布随时间变化')
axs[2].set_xlabel('Z位置 (m)')
axs[2].set_ylabel('时间 (s)')
axs[2].set_ylim(0, total_time)

plt.tight_layout()
plt.show()

# 4. 等值面可视化 (3D等值面)
from skimage import measure

# 选择最后一个时间步的波形场
U_final = history[-1]

# 创建等值面
iso_value = 0.1  # 等值
verts, faces, _, _ = measure.marching_cubes(U_final, iso_value, spacing=(dx, dy, dz))

# 创建3D图
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制等值面
mesh = ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2], 
                      cmap='coolwarm', lw=0.5, alpha=0.8)
mesh.set_array(np.ones_like(verts[:, 0]))  # 单一颜色
mesh.set_clim(iso_value-0.1, iso_value+0.1)  # 设置颜色范围

ax.set_title(f'{total_time:.1f}秒时的{iso_value}等值面')
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.set_xlim(0, Lx)
ax.set_ylim(0, Ly)
ax.set_zlim(0, Lz)

# 添加颜色条
cbar = fig.colorbar(mesh, ax=ax, shrink=0.5, aspect=10, label='振幅')
cbar.set_ticks([iso_value])
cbar.set_ticklabels([f'{iso_value}'])

plt.tight_layout()
plt.show()



