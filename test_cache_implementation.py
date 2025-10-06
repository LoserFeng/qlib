#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试缓存功能实现的简单脚本
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

try:
    from qlib.data.dataset.handler import DataHandler, DataHandlerLP
    from qlib.data.dataset.loader import StaticDataLoader
    print("✓ 成功导入所需模块")
except ImportError as e:
    print(f"✗ 导入模块失败: {e}")
    sys.exit(1)


def create_sample_data():
    """创建示例数据用于测试"""
    # 创建多层索引的示例数据
    dates = pd.date_range('2020-01-01', periods=10, freq='D')
    instruments = ['AAPL', 'GOOGL', 'MSFT']
    
    # 创建多层索引
    index = pd.MultiIndex.from_product(
        [dates, instruments],
        names=['datetime', 'instruments']
    )
    
    # 创建示例数据
    np.random.seed(42)  # 为了结果可重复
    data = {
        'close': np.random.randn(len(index)) * 10 + 100,
        'volume': np.random.randint(1000, 10000, len(index)),
        'open': np.random.randn(len(index)) * 10 + 100,
        'high': np.random.randn(len(index)) * 10 + 105,
        'low': np.random.randn(len(index)) * 10 + 95,
    }
    
    df = pd.DataFrame(data, index=index)
    return df


def test_datahandler_cache():
    """测试 DataHandler 的缓存功能"""
    print("\n=== 测试 DataHandler 缓存功能 ===")
    
    # 创建示例数据
    sample_df = create_sample_data()
    
    # 创建静态数据加载器
    loader = StaticDataLoader(sample_df)
    
    # 测试不使用缓存
    print("1. 测试不使用缓存...")
    handler1 = DataHandler(
        instruments=['AAPL', 'GOOGL'],
        start_time='2020-01-01',
        end_time='2020-01-05',
        data_loader=loader,
        init_data=False
    )
    
    # 设置数据（不使用缓存）
    import time
    start_time = time.time()
    handler1.setup_data(enable_cache=False)
    no_cache_time = time.time() - start_time
    print(f"   不使用缓存加载时间: {no_cache_time:.4f}s")
    print(f"   数据形状: {handler1._data.shape}")
    
    # 测试使用缓存 - 首次加载
    print("2. 测试使用缓存 - 首次加载...")
    handler2 = DataHandler(
        instruments=['AAPL', 'GOOGL'],
        start_time='2020-01-01',
        end_time='2020-01-05',
        data_loader=loader,
        init_data=False
    )
    
    start_time = time.time()
    handler2.setup_data(enable_cache=True)
    first_cache_time = time.time() - start_time
    print(f"   首次缓存加载时间: {first_cache_time:.4f}s")
    print(f"   数据形状: {handler2._data.shape}")
    
    # 验证缓存文件是否被创建
    cache_path = handler2._get_cache_file_path()
    if cache_path.exists():
        print(f"   ✓ 缓存文件已创建: {cache_path}")
    else:
        print(f"   ✗ 缓存文件未找到: {cache_path}")
        return False
    
    # 测试使用缓存 - 从缓存加载
    print("3. 测试使用缓存 - 从缓存加载...")
    handler3 = DataHandler(
        instruments=['AAPL', 'GOOGL'],
        start_time='2020-01-01',
        end_time='2020-01-05',
        data_loader=loader,
        init_data=False
    )
    
    start_time = time.time()
    handler3.setup_data(enable_cache=True)
    cached_load_time = time.time() - start_time
    print(f"   从缓存加载时间: {cached_load_time:.4f}s")
    print(f"   数据形状: {handler3._data.shape}")
    
    # 验证数据一致性
    if handler1._data.equals(handler2._data) and handler2._data.equals(handler3._data):
        print("   ✓ 数据一致性验证通过")
    else:
        print("   ✗ 数据一致性验证失败")
        return False
    
    print("   ✓ DataHandler 缓存功能测试通过")
    return True


def main():
    """主测试函数"""
    print("开始测试缓存功能实现...")
    
    try:
        # 测试基本的 DataHandler 缓存
        success = test_datahandler_cache()
        
        if success:
            print("\n🎉 所有测试通过！缓存功能实现成功。")
        else:
            print("\n❌ 测试失败，请检查实现。")
            
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()