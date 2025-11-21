# Towa-CPU-Data

PCAP 文件 CPU 使用率分析工具

## 快速开始

### 基本用法

```bash
# 分析所有数据包，生成 CSV 文件（推荐）
python3 pcap2excel.py file_name.pcap --csv

# 分析所有数据包，生成 Excel 文件（需要安装 openpyxl）
python3 pcap2excel.py file_name.pcap
```

### 高级用法

```bash
# 只分析前 3 个数据包
python3 pcap2excel.py file_name.pcap --count 3 --csv

# 分析第 2 到第 5 个数据包
python3 pcap2excel.py file_name.pcap --range 2 5 --csv

# 指定输出文件名
python3 pcap2excel.py file_name.pcap output.xlsx
```

## 环境要求

- Python 3.6+
- CSV 模式：无需额外库
- Excel 模式：需要安装 openpyxl

```bash
# 安装 openpyxl（仅 Excel 模式需要）
sudo apt install python3-pip
pip3 install openpyxl
```

## 输出格式

生成的文件包含以下列：

| Column | 说明 |
|--------|------|
| Number | 数据点编号 |
| CPU Usage% | CPU 使用率百分比 |
| Busy Time | CPU 忙碌时间 |
| Idle Time | CPU 空闲时间 |
| Busy Time + Idle Time | 总时间 |

Excel 模式会自动生成两个图表：
- CPU 使用率变化趋势图
- Busy Time vs Idle Time 对比图

## 数据格式说明

### 输入
- 文件格式：PCAP (Packet Capture)
- 协议：Ethernet → IPv4 → UDP
- 过滤条件：UDP payload 长度为 504 字节

### 数据结构
每个数据包的最后 24 字节包含 CPU 信息：

| 字节位置 | 类型 | 说明 |
|---------|------|------|
| 0-7 | float64 | CPU 使用率原始值 |
| 8-15 | int64 | Busy 时间 |
| 16-23 | int64 | Idle 时间 |

CPU 使用率计算公式：
```
CPU 使用率 = (Busy 时间 / (Busy 时间 + Idle 时间)) × 100%
```

## 命令行选项

```
python3 pcap2excel.py <pcap文件> [输出文件] [选项]

选项:
  --csv              生成 CSV 格式（默认生成 Excel）
  --count N          只分析前 N 个匹配的数据包
  --range START END  分析第 START 到第 END 个数据包
```

## 示例

```bash
# 查看帮助
python3 pcap2excel.py

# 分析所有数据包
python3 pcap2excel.py file_name.pcap --csv

# 只分析前 10 个
python3 pcap2excel.py file_name.pcap --count 10 --csv

# 分析第 5 到第 15 个
python3 pcap2excel.py file_name.pcap --range 5 15

# 生成带图表的 Excel
python3 pcap2excel.py file_name.pcap result.xlsx
```
