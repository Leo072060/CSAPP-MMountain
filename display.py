import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def read_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # 手动定义步长（stride）值（假设是 1, 3, 5, ..., 31）
    strides = np.arange(1, 32, 2)  # [1, 3, 5, ..., 31]
    
    # 提取工作集大小（working set sizes）和吞吐量数据
    working_sizes = []
    data = []
    for line in lines[1:]:  # 跳过第一行（列名）
        parts = line.split()
        # 处理工作集大小（如 '128m' -> 128 * 1e6）
        size_str = parts[0].strip()
        if 'k' in size_str:
            size = int(size_str.replace('k', '')) * 1024
        elif 'm' in size_str:
            size = int(size_str.replace('m', '')) * 1024 * 1024
        else:
            size = int(size_str)
        working_sizes.append(size)
        # 提取吞吐量数据
        data.append([float(x) for x in parts[1:]])
    
    return strides, np.array(working_sizes), np.array(data)

def plot_memory_mountain(strides, working_sizes, data):
    # 创建网格
    X, Y = np.meshgrid(strides, np.log2(working_sizes))
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 绘制曲面
    surf = ax.plot_surface(X, Y, data, cmap='viridis', edgecolor='none')
    
    # 设置标签
    ax.set_xlabel('Stride (elements)', labelpad=10)
    ax.set_ylabel('Working Set Size (log2 bytes)', labelpad=10)
    ax.set_zlabel('Read Throughput (MB/s)', labelpad=10)
    
    # 设置刻度
    ax.set_xticks(strides[::2])
    ax.set_xticklabels(strides[::2])
    
    # 将工作集大小转换为对数刻度
    yticks = np.log2(working_sizes[::2])
    ax.set_yticks(yticks)
    ax.set_yticklabels([f'{s//1024}k' if s < 1024 * 1024 else f'{s//(1024 * 1024)}m' 
                        for s in working_sizes[::2]])
    
    # 添加颜色条
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    plt.title('Memory Mountain')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    strides, working_sizes, data = read_data('data.txt')
    plot_memory_mountain(strides, working_sizes, data)