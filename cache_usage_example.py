#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
缓存功能使用示例

这个文件展示了如何在 QLib 的 DataHandler 和 DataHandlerLP 中使用新实现的缓存功能。
"""

# 缓存功能使用示例
# ====================

# 1. DataHandler 基础缓存使用
"""
from qlib.data.dataset.handler import DataHandler
from qlib.data.dataset.loader import StaticDataLoader

# 创建数据处理器
handler = DataHandler(
    instruments=['AAPL', 'GOOGL', 'MSFT'],
    start_time='2020-01-01',
    end_time='2020-12-31',
    data_loader=your_data_loader,
    init_data=False  # 先不初始化数据
)

# 启用缓存进行数据设置
handler.setup_data(enable_cache=True)

# 第一次运行：从数据源加载数据并保存到缓存
# 再次运行：直接从缓存加载数据，大大加快速度
"""

# 2. DataHandlerLP 处理数据缓存使用
"""
from qlib.data.dataset.handler import DataHandlerLP
from qlib.data.dataset.processor import DropnaFeature, MinMaxNorm

# 创建带处理器的数据处理器
handler_lp = DataHandlerLP(
    instruments=['AAPL', 'GOOGL', 'MSFT'],
    start_time='2020-01-01',
    end_time='2020-12-31',
    data_loader=your_data_loader,
    
    # 处理器配置
    shared_processors=[DropnaFeature()],
    infer_processors=[MinMaxNorm()],
    learn_processors=[],
    
    init_data=False
)

# 启用缓存进行数据设置和处理
handler_lp.setup_data(
    init_type=DataHandlerLP.IT_FIT_SEQ,
    enable_cache=True
)

# 第一次运行：
# 1. 加载原始数据
# 2. 拟合和应用处理器
# 3. 保存处理后的数据到缓存
#
# 再次运行：
# 1. 直接从缓存加载处理后的数据
# 2. 跳过耗时的数据处理步骤
"""

# 缓存功能特点
# ==============

print("""
缓存功能特点:
1. 智能缓存键生成
   - 基于数据配置参数（instruments, start_time, end_time）
   - 基于数据加载器配置
   - 基于处理器配置（仅 DataHandlerLP）
   - 确保配置变化时自动使用新缓存

2. 自动缓存管理
   - 自动创建缓存目录
   - 使用配置中的缓存路径或默认临时目录
   - 自动处理缓存文件冲突

3. 错误处理
   - 缓存加载失败时自动回退到原始加载
   - 详细的日志记录
   - 缓存保存失败不影响正常功能

4. 性能优化
   - 大幅减少重复数据加载时间
   - 特别适合数据处理密集的场景
   - 支持原始数据和处理后数据的分别缓存

使用建议:
- 在开发和调试阶段启用缓存以加速迭代
- 在生产环境中根据数据更新频率决定是否使用缓存
- 定期清理旧缓存文件释放存储空间
- 缓存文件名包含配置哈希，配置变化会自动创建新缓存
""")

# 缓存文件位置
# =============

print("""
缓存文件位置:
- 默认位置: 根据 QLib 配置中的 local_cache_path
- 回退位置: 系统临时目录/qlib_cache/
- DataHandler: cache_dir/handler_cache/
- DataHandlerLP: cache_dir/handler_lp_cache/

缓存文件命名:
- DataHandler: handler_data_{hash[:16]}.pkl
- DataHandlerLP: handler_lp_processed_{hash[:16]}.pkl

其中 hash 是基于配置参数生成的 MD5 哈希值前16位
""")