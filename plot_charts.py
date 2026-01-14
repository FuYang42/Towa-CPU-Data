#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 CSV 文件读取 CPU 数据并生成专业图表
使用 matplotlib 库进行绘图，完全控制布局避免标题重叠
"""

import sys
import csv
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

# 设置中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


def read_csv_data(csv_file):
    """从 CSV 文件读取 CPU 数据"""
    data = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({
                    'number': int(row['Number']),
                    'cpu_usage': float(row['CPU Usage%']),
                    'busy_time': int(row['Busy Time']),
                    'idle_time': int(row['Idle Time']),
                    'total_time': int(row['Busy Time + Idle Time'])
                })
    except FileNotFoundError:
        print(f"错误: 找不到文件 {csv_file}")
        print("请先运行: python pcap2excel.py file_name.pcap --csv")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 读取 CSV 文件失败 - {e}")
        sys.exit(1)

    return data


def plot_cpu_usage(data, output_file='cpu_usage_chart.png'):
    """绘制 CPU 使用率图表"""
    numbers = [d['number'] for d in data]
    cpu_usage = [d['cpu_usage'] for d in data]

    # 创建图表，设置合适的尺寸
    fig, ax = plt.subplots(figsize=(14, 8))

    # 绘制折线图（去掉数据点标记）
    ax.plot(numbers, cpu_usage, color='#4472C4', linewidth=2.5)

    # 设置标题和轴标签 - 增加间距避免重叠
    ax.set_title('CPU Usage Over Time', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Sample Number', fontsize=12, labelpad=10)
    ax.set_ylabel('CPU Usage (%)', fontsize=12, labelpad=10)

    # 计算统计信息
    import numpy as np
    min_cpu = min(cpu_usage)
    max_cpu = max(cpu_usage)
    avg_cpu = np.mean(cpu_usage)
    std_cpu = np.std(cpu_usage)
    cpu_range = max_cpu - min_cpu

    if cpu_range < 1:
        # 极小波动（< 1%）：使用最紧凑范围
        # 数据上下各扩展2个百分点
        y_min = max(0, min_cpu - 2)
        y_max = min(100, max_cpu + 2)
    elif cpu_range < 10:
        # 小波动（1-10%）：使用紧凑范围
        # 在数据中心点上下各扩展7个百分点
        center = (min_cpu + max_cpu) / 2
        y_min = max(0, center - 7)
        y_max = min(100, center + 7)
    else:
        # 大波动（> 10%）：使用适中范围
        margin = cpu_range * 0.2
        y_min = max(0, min_cpu - margin)
        y_max = min(100, max_cpu + margin)

    ax.set_ylim(y_min, y_max)

    # 添加统计信息框（右上角）
    stats_text = f'Max: {max_cpu:.2f}%\nMin: {min_cpu:.2f}%\nAvg: {avg_cpu:.2f}%\nStd: {std_cpu:.4f}%'
    ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # 设置网格
    ax.grid(True, alpha=0.3, linestyle='--')

    # 设置刻度字体大小
    ax.tick_params(axis='both', labelsize=10)

    # 调整布局，确保标签不被裁剪
    plt.tight_layout()

    # 保存图表
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ CPU 使用率图表已保存: {output_file}")
    plt.close()


def plot_busy_idle_time(data, output_file='busy_idle_chart.png'):
    """绘制 Busy Time vs Idle Time 对比图表"""
    numbers = [d['number'] for d in data]
    busy_times = [d['busy_time'] for d in data]
    idle_times = [d['idle_time'] for d in data]

    # 创建图表
    fig, ax = plt.subplots(figsize=(14, 8))

    # 绘制两条折线（去掉数据点标记）
    ax.plot(numbers, busy_times, color='#ED7D31', linewidth=2.5, label='Busy Time')
    ax.plot(numbers, idle_times, color='#70AD47', linewidth=2.5, label='Idle Time')

    # 设置标题和轴标签 - 增加间距避免重叠
    ax.set_title('Busy Time vs Idle Time', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Sample Number', fontsize=12, labelpad=10)
    ax.set_ylabel('Time (ns)', fontsize=12, labelpad=10)

    # 设置网格
    ax.grid(True, alpha=0.3, linestyle='--')

    # 添加图例
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)

    # 设置刻度字体大小
    ax.tick_params(axis='both', labelsize=10)

    # Y 轴使用千位分隔符
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))

    # 调整布局
    plt.tight_layout()

    # 保存图表
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Busy/Idle 时间对比图表已保存: {output_file}")
    plt.close()


def plot_combined_charts(data, output_file='combined_charts.png'):
    """在一个文件中绘制两个图表（上下排列）"""
    numbers = [d['number'] for d in data]
    cpu_usage = [d['cpu_usage'] for d in data]
    busy_times = [d['busy_time'] for d in data]
    idle_times = [d['idle_time'] for d in data]

    # 创建包含两个子图的图表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))

    # === 第一个图表: CPU Usage ===
    ax1.plot(numbers, cpu_usage, color='#4472C4', linewidth=2.5)
    ax1.set_title('CPU Usage Over Time', fontsize=16, fontweight='bold', pad=15)
    ax1.set_xlabel('Sample Number', fontsize=12, labelpad=10)
    ax1.set_ylabel('CPU Usage (%)', fontsize=12, labelpad=10)

    # 计算统计信息
    import numpy as np
    min_cpu = min(cpu_usage)
    max_cpu = max(cpu_usage)
    avg_cpu = np.mean(cpu_usage)
    std_cpu = np.std(cpu_usage)
    cpu_range = max_cpu - min_cpu

    if cpu_range < 1:
        # 极小波动（< 1%）：使用最紧凑范围
        y_min = max(0, min_cpu - 2)
        y_max = min(100, max_cpu + 2)
    elif cpu_range < 10:
        # 小波动（1-10%）：使用紧凑范围
        center = (min_cpu + max_cpu) / 2
        y_min = max(0, center - 7)
        y_max = min(100, center + 7)
    else:
        # 大波动（> 10%）：使用适中范围
        margin = cpu_range * 0.2
        y_min = max(0, min_cpu - margin)
        y_max = min(100, max_cpu + margin)

    ax1.set_ylim(y_min, y_max)

    # 添加统计信息框（右上角）
    stats_text = f'Max: {max_cpu:.2f}%\nMin: {min_cpu:.2f}%\nAvg: {avg_cpu:.2f}%\nStd: {std_cpu:.4f}%'
    ax1.text(0.98, 0.97, stats_text, transform=ax1.transAxes,
            fontsize=10, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.tick_params(axis='both', labelsize=10)

    # === 第二个图表: Busy/Idle Time ===
    ax2.plot(numbers, busy_times, color='#ED7D31', linewidth=2.5, label='Busy Time')
    ax2.plot(numbers, idle_times, color='#70AD47', linewidth=2.5, label='Idle Time')
    ax2.set_title('Busy Time vs Idle Time', fontsize=16, fontweight='bold', pad=15)
    ax2.set_xlabel('Sample Number', fontsize=12, labelpad=10)
    ax2.set_ylabel('Time (ns)', fontsize=12, labelpad=10)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend(loc='upper right', fontsize=11, framealpha=0.9)
    ax2.tick_params(axis='both', labelsize=10)
    ax2.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))

    # 调整子图之间的间距
    plt.tight_layout(pad=3.0)

    # 保存图表
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ 组合图表已保存: {output_file}")
    plt.close()


def main():
    """主函数"""
    import sys
    import io

    # 确保输出使用 UTF-8 编码
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 60)
    print("CPU 数据图表生成工具 (基于 matplotlib)")
    print("=" * 60)
    print()

    # 检查命令行参数
    if len(sys.argv) < 2:
        print("用法:")
        print(f"  python {sys.argv[0]} <csv文件>")
        print()
        print("示例:")
        print(f"  python {sys.argv[0]} cpu_test_analysis.csv")
        print()
        print("选项:")
        print("  默认生成三个图表文件:")
        print("    - cpu_usage_chart.png       (CPU 使用率单独图表)")
        print("    - busy_idle_chart.png       (Busy/Idle 时间对比图表)")
        print("    - combined_charts.png       (组合图表)")
        print()
        sys.exit(1)

    csv_file = sys.argv[1]

    # 检查文件是否存在
    if not Path(csv_file).exists():
        print(f"错误: 文件不存在 - {csv_file}")
        print()
        print("请先生成 CSV 文件:")
        print("  python pcap2excel.py file_name.pcap --csv")
        sys.exit(1)

    print(f"正在读取 CSV 文件: {csv_file}")
    data = read_csv_data(csv_file)
    print(f"✓ 成功读取 {len(data)} 个数据点\n")

    print("正在生成图表...")

    # 生成三个图表
    plot_cpu_usage(data, 'cpu_usage_chart.png')
    plot_busy_idle_time(data, 'busy_idle_chart.png')
    plot_combined_charts(data, 'combined_charts.png')

    print()
    print("完成！生成了以下图表文件:")
    print("  1. cpu_usage_chart.png       - CPU 使用率图表")
    print("  2. busy_idle_chart.png       - Busy/Idle 时间对比图表")
    print("  3. combined_charts.png       - 组合图表（推荐用于报告）")
    print()
    print("图表分辨率: 300 DPI (适合打印和演示)")


if __name__ == "__main__":
    main()
