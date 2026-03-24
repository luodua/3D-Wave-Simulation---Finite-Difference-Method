# 3D Wave Simulation - Finite Difference Method

# 三维波浪模拟 - 有限差分法

---

## 效果预览

### 波浪传播动画

![Wave Animation](img/wave_3d_animation.gif)

### 三维波浪模拟

![3D Wave Simulation](img/1.jpg)

---

## English

### Project Overview

This project simulates 3D wave propagation using the explicit finite difference method to solve the wave equation. The simulation visualizes how a Gaussian pulse evolves over time in a 3D domain with fixed boundary conditions.

### Features

- **3D Wave Equation Solver**: Explicit finite difference scheme for the 3D wave equation
- **Gaussian Initial Condition**: Wave packet with Gaussian envelope
- **Stability Analysis**: Automatic CFL stability check
- **Multiple Visualizations**:
  - 3D surface plots at different time steps
  - Animated 3D wave propagation
  - Space-time heatmaps along coordinate axes
  - 3D isosurface visualization
- **Export Capabilities**: MP4 and GIF animation outputs

### Physics Background

The 3D wave equation:

```
∂²u/∂t² = c²(∂²u/∂x² + ∂²u/∂y² + ∂²u/∂z²)
```

Discretized using explicit finite differences with stability condition:

```
r = c²Δt²(1/Δx² + 1/Δy² + 1/Δz²) ≤ 1
```

### Requirements

```
numpy>=1.19.0
matplotlib>=3.3.0
scikit-image>=0.18.0
imageio>=2.9.0
```

### Usage

```bash
python "main.py"
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Nx, Ny, Nz | 100 | Grid points in each direction |
| Lx, Ly, Lz | 10 m | Domain size |
| c | 1.0 m/s | Wave speed |
| dt | 0.01 s | Time step |
| total_time | 25 s | Total simulation time |

### Output Files

- `wave_3d_animation.mp4` - Animated wave propagation
- `wave_3d_animation.gif` - GIF animation

### Project Structure

```
.
├── README.md
├── README_en.md
└── main.py
```

### References

- Finite Difference Methods for PDEs
- CFL Stability Condition: Courant, Friedrichs, Lewy (1928)

---

## 中文

### 项目简介

本项目是一个波浪仿真测试项目。
有一天突然想到可以使用有限差分法+高斯塞尔德矩阵求解三维波动方程，模拟高斯波包在固定边界条件下的传播过程，并生成多种可视化动画。

后续还是看看用有限体积法吧


### 功能特点

- **三维波动方程求解器**: 基于显式有限差分格式
- **高斯初始条件**: 具有高斯包络的波包
- **稳定性分析**: 自动进行CFL稳定性检验
- **多种可视化**:
  - 不同时刻的三维表面图
  - 三维波浪传播动画
  - 沿坐标轴的时空热力图
  - 三维等值面可视化
- **导出功能**: 支持MP4和GIF动画输出

### 物理原理

三维波动方程:

```
∂²u/∂t² = c²(∂²u/∂x² + ∂²u/∂y² + ∂²u/∂z²)
```

使用显式有限差分格式离散化，稳定性条件:

```
r = c²Δt²(1/Δx² + 1/Δy² + 1/Δz²) ≤ 1
```

### 依赖环境

```
numpy>=1.19.0
matplotlib>=3.3.0
scikit-image>=0.18.0
imageio>=2.9.0
```

### 运行方法

```bash
python "main.py"
```

### 参数配置

| 参数 | 默认值 | 描述 |
|------|--------|------|
| Nx, Ny, Nz | 100 | 各方向网格点数 |
| Lx, Ly, Lz | 10 m | 模拟区域大小 |
| c | 1.0 m/s | 波速 |
| dt | 0.01 s | 时间步长 |
| total_time | 25 s | 总模拟时间 |

### 输出文件

- `wave_3d_animation.mp4` - 波浪传播动画 (MP4格式)
- `wave_3d_animation.gif` - 波浪传播动画 (GIF格式)

### 项目结构

```
.
├── README.md          (本文件)
├── README_en.md       (英文版说明)
└── main.py
```

### 边界条件

本模拟采用**固定边界条件** (Dirichlet边界):
- u = 0 在所有边界处

### 数值方法

- **空间离散化**: 二阶中心差分
- **时间离散化**: Leap-frog格式
- **稳定性条件**: CFL条件

### 扩展

1. 改变初始条件 (多种波包形状)
2. 调整边界条件 (反射、吸收边界)
3. 增加障碍物模拟
4. 并行计算加速 (NumPy向量化已包含)

### 参考资料

- 有限差分法求解偏微分方程
- CFL稳定性条件: Courant, Friedrichs, Lewy (1928)
