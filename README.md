# Towa-CPU-Data

[English](#english) | [中文](#中文)

## 中文

### 项目简介

本项目用于分析从 MMT (Multi-Modal Transport) 传输出来的数据包中的后 24 字节数据，以此来分析和监控 CPU 的使用率。

### ⚡ 快速使用（一条命令搞定）

```bash
# 方式 1: 生成 CSV 文件（推荐，无需安装任何库）
python3 pcap2excel.py cpu_usage.pcap --csv

# 方式 2: 生成带图表的 Excel 文件（需要先安装 openpyxl）
pip install openpyxl
python3 pcap2excel.py cpu_usage.pcap
```

**就这么简单！** 程序会自动：
1. 读取 PCAP 文件
2. 提取 CPU 使用率数据
3. 生成 Excel/CSV 文件（包含 5 列数据）
4. 自动创建图表（Excel 模式）
5. 显示统计信息

### 输出文件格式

| Column 1 | Column 2 | Column 3 | Column 4 | Column 5 |
|----------|----------|----------|----------|----------|
| Number | CPU Usage% | Busy Time | Idle Time | Busy Time + Idle Time |

### 环境要求

- Python 3.6 或更高版本
- CSV 模式：无需任何额外库
- Excel 模式：需要 `pip install openpyxl`

---

### 高级使用方法

如果需要查看详细的数据包信息或进行深入分析：

##### 1. 详细分析模式（查看前 N 个数据包的完整信息）

```bash
# 分析前 10 个数据包（默认）
python3 analyze_pcap.py cpu_usage.pcap

# 分析前 50 个数据包
python3 analyze_pcap.py cpu_usage.pcap 50
```

输出内容包括：
- 完整的网络协议层信息（以太网、IP、UDP）
- 十六进制和 ASCII 格式的原始数据
- 后 24 字节的 CPU 数据解析
- Busy/Idle 时间和计算出的 CPU 使用率

##### 2. 概览分析模式（分析所有数据包并生成统计）

```bash
python3 cpu_summary.py cpu_usage.pcap
```

输出内容包括：
- 所有数据包的 CPU 使用率统计（最小值、最大值、平均值、中位数）
- 前 20 个和后 20 个数据包的 CPU 使用率列表
- 自动导出 CSV 文件（包含所有数据包的 CPU 信息）

##### 3. Excel 导出模式（生成包含图表的 Excel 文件）

**方法 A：CSV 格式（推荐，无需额外依赖）**

```bash
python3 export_to_csv.py cpu_usage.pcap cpu_usage_analysis.csv
```

生成的 CSV 文件可以直接在 Excel 中打开，包含以下列：
- Column 1: Number（数据点编号）
- Column 2: CPU Usage%（CPU 使用率）
- Column 3: Busy Time（忙碌时间）
- Column 4: Idle Time（空闲时间）
- Column 5: Busy Time + Idle Time（总时间）

**方法 B：自动生成 Excel 文件（需要安装 openpyxl）**

```bash
# 先安装依赖
pip install openpyxl

# 运行导出
python3 export_to_excel.py cpu_usage.pcap cpu_usage_analysis.xlsx
```

自动生成包含以下内容的 Excel 文件：
- 格式化的数据表格
- CPU 使用率变化折线图
- Busy/Idle 时间对比图表

详细使用说明请参考 [EXCEL_GUIDE.md](EXCEL_GUIDE.md)

### 数据格式

#### 输入数据
- **文件格式**: PCAP (Packet Capture)
- **网络协议**: Ethernet → IPv4 → UDP
- **UDP 端口**: 443 → 8808
- **数据载荷**: 1464 字节，以 "STDV" 开头

#### 后 24 字节数据结构
数据包载荷的最后 24 字节包含 CPU 使用率信息：

| 字节位置 | 数据类型 | 说明 |
|---------|---------|------|
| 0-7     | double (float64) | CPU 使用率原始值（小端序） |
| 8-15    | int64 | Busy 时间（小端序） |
| 16-23   | int64 | Idle 时间（小端序） |

**CPU 使用率计算公式**：
```
CPU 使用率 = (Busy 时间 / (Busy 时间 + Idle 时间)) × 100%
```

#### 输出数据
- **控制台**: 详细的分析报告
- **CSV 文件**: `cpu_usage_cpu_data.csv`，包含字段：
  - packet_num: 数据包序号
  - timestamp: 时间戳
  - cpu_usage: CPU 使用率（%）
  - busy_time: Busy 时间
  - idle_time: Idle 时间

### 项目结构

```
Towa-CPU-Data/
├── pcap2excel.py             # ⭐ 主程序（推荐使用）
├── README.md                 # 项目说明文档
├── requirements.txt          # Python 依赖（仅 Excel 导出需要）
├── cpu_usage.pcap            # 示例 PCAP 文件
│
├── analyze_pcap.py           # 高级工具：详细分析
├── cpu_summary.py            # 高级工具：统计摘要
├── export_to_csv.py          # 高级工具：CSV 导出
├── export_to_excel.py        # 高级工具：Excel 导出
├── EXCEL_GUIDE.md            # Excel 导出详细指南
└── QUICKSTART.md             # 快速开始指南
```

### 示例输出

```
CPU 使用率统计:
  最小值: 15.18%
  最大值: 98.76%
  平均值: 45.32%
  中位数: 39.27%

前 20 个数据包的 CPU 使用率:
  包序号        时间戳                  CPU 使用率
  ---------- -------------------- ---------------
  1          1763684906.627354    16.05%
  2          1763684906.627758    29.26%
  3          1763684906.627803    32.75%
  ...
```

### 贡献

欢迎提交问题和拉取请求。

### 许可证

待定

---

## English

### Project Overview

This project analyzes the last 24 bits of data packets transmitted from MMT (Multi-Modal Transport) to monitor and analyze CPU usage.

### Features

- Parse MMT data packets
- Extract the last 24 bits from data packets
- Analyze CPU usage
- Generate usage reports

### Quick Start

#### Requirements

- TBD (to be added based on development needs)

#### Installation

```bash
git clone <repository-url>
cd Towa-CPU-Data
# Install dependencies (TBD)
```

#### Usage

```bash
# Run example (TBD)
```

### Data Format

- **Input**: MMT data packets
- **Analysis Target**: Last 24 bits of the packet
- **Output**: CPU usage analysis results

### Project Structure

```
Towa-CPU-Data/
├── README.md          # Project documentation
└── ...                # Source code files (TBD)
```

### Development Roadmap

- [ ] Implement packet parser
- [ ] Implement last 24-bit data extraction
- [ ] Implement CPU usage calculation algorithm
- [ ] Add data visualization
- [ ] Write test cases

### Contributing

Issues and pull requests are welcome.

### License

TBD
