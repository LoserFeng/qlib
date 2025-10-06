# QLib DataHandler 缓存功能实现

## 概述

为 QLib 的 `DataHandler` 和 `DataHandlerLP` 类实现了完整的缓存功能，解决了原代码中的 "TODO: cache" 注释。

## 实现的功能

### 1. DataHandler 基础缓存

- **缓存原始数据**: 缓存从 `data_loader.load()` 加载的原始数据
- **智能缓存键**: 基于 instruments、时间范围、数据加载器配置生成唯一缓存键
- **自动缓存管理**: 自动创建缓存目录，处理缓存文件
- **错误处理**: 缓存失败时自动回退到正常加载流程

### 2. DataHandlerLP 处理数据缓存

- **缓存处理后数据**: 缓存经过 processors 处理后的 infer 和 learn 数据
- **处理器感知**: 缓存键包含所有处理器的配置信息
- **选择性缓存**: 根据 `drop_raw` 设置决定是否缓存原始数据
- **完整状态恢复**: 从缓存恢复时保持完整的处理状态

## 核心实现

### 新增方法

#### DataHandler

```python
def _get_cache_file_path(self, cache_dir: str = None) -> Path:
    """生成缓存文件路径"""
    
def setup_data(self, enable_cache: bool = False):
    """增强的数据设置方法，支持缓存"""
```

#### DataHandlerLP

```python
def _get_processed_cache_file_path(self, cache_dir: str = None) -> Path:
    """生成处理数据的缓存文件路径"""
    
def setup_data(self, init_type: str = IT_FIT_SEQ, **kwargs):
    """增强的数据设置方法，支持处理数据缓存"""
```

### 缓存键生成策略

使用 `hash_args()` 函数基于以下参数生成 MD5 哈希：

**DataHandler**:
- instruments 列表
- start_time, end_time
- data_loader 类型和配置

**DataHandlerLP** (额外包含):
- 所有 processors 的类名和配置
- process_type 设置
- drop_raw 设置

### 缓存文件结构

```
cache_dir/
├── handler_cache/           # DataHandler 缓存
│   └── handler_data_{hash}.pkl
└── handler_lp_cache/        # DataHandlerLP 缓存
    └── handler_lp_processed_{hash}.pkl
```

## 使用方式

### 基础使用

```python
# DataHandler
handler = DataHandler(
    instruments=['AAPL', 'GOOGL'],
    start_time='2020-01-01',
    end_time='2020-12-31',
    data_loader=loader,
    init_data=False
)

# 启用缓存
handler.setup_data(enable_cache=True)
```

### 高级使用 (DataHandlerLP)

```python
# DataHandlerLP
handler = DataHandlerLP(
    instruments=['AAPL', 'GOOGL'],
    start_time='2020-01-01', 
    end_time='2020-12-31',
    data_loader=loader,
    shared_processors=[DropnaFeature()],
    infer_processors=[MinMaxNorm()],
    learn_processors=[],
    init_data=False
)

# 启用缓存
handler.setup_data(
    init_type=DataHandlerLP.IT_FIT_SEQ,
    enable_cache=True
)
```

## 性能优势

1. **显著减少重复加载时间**: 特别是对于大数据集和复杂处理流程
2. **智能缓存失效**: 配置变更时自动使用新缓存
3. **内存优化**: 避免重复的数据处理计算
4. **开发效率**: 在开发和调试阶段大幅提升迭代速度

## 技术特点

1. **向后兼容**: 不影响现有代码，默认不启用缓存
2. **容错性**: 缓存操作失败不影响正常功能
3. **可配置**: 支持自定义缓存目录
4. **安全性**: 使用哈希避免缓存冲突
5. **可维护**: 清晰的日志记录和错误处理

## 文件修改

主要修改了 `qlib/data/dataset/handler.py`:

1. 添加必要的导入模块 (os, pickle, Path, hash_args, C)
2. 为 `DataHandler` 添加 `_get_cache_file_path()` 方法
3. 增强 `DataHandler.setup_data()` 方法支持缓存
4. 为 `DataHandlerLP` 添加 `_get_processed_cache_file_path()` 方法  
5. 增强 `DataHandlerLP.setup_data()` 方法支持处理数据缓存

## 测试验证

- 通过了缓存键生成一致性测试
- 通过了基础缓存读写功能测试
- 验证了错误处理和日志记录功能
- 确认了缓存文件路径管理正确性

这个实现完全解决了原代码中的缓存 TODO 项，为 QLib 提供了强大而可靠的数据缓存功能。