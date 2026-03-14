# E-001 测试说明

## 测试文件

### 1. 模型验证测试（推荐）
**文件**: `test_e001_user_models_simple.py`

**说明**: 不依赖实际数据库连接，仅验证 SQLAlchemy 模型定义的正确性。

**运行命令**:
```bash
cd backend
python tests/test_e001_user_models_simple.py
```

**测试内容**:
- User 模型字段验证（id, name, level, created_at）
- PracticeLog 模型字段验证（id, user_id, craft_id, duration, score, created_at）
- Portfolio 模型字段验证（id, user_id, image_url, craft_type, description, created_at）
- 模型关系验证（外键、反向关系）
- 级联删除配置验证

### 2. 完整集成测试（需要 MySQL）
**文件**: `test_e001_user_models.py`

**说明**: 需要连接 MySQL 数据库，执行完整的 CRUD 操作测试。

**前置条件**:
- MySQL 服务已启动
- 已配置数据库连接（`.env` 或环境变量）

**运行命令**:
```bash
cd backend
python tests/test_e001_user_models.py
```

**测试内容**:
- 用户模型 CRUD 操作
- 学习记录模型 CRUD 操作
- 作品集模型 CRUD 操作
- 级联删除功能测试

## 测试输出示例

```
============================================================
E-001 用户数据模型验证测试
============================================================

[Test 1] User 模型定义
----------------------------------------
  [OK] 字段 'id' 存在
  [OK] 字段 'name' 存在
  [OK] 字段 'level' 存在
  [OK] 字段 'created_at' 存在
  [OK] id 是主键
  [OK] name 不为空
  [OK] level 默认值为 1

[PASS] User 模型验证通过！

[Test 2] PracticeLog 模型定义
----------------------------------------
  [OK] 字段 'id' 存在
  [OK] 字段 'user_id' 存在
  [OK] 字段 'craft_id' 存在
  [OK] 字段 'duration' 存在
  [OK] 字段 'score' 存在
  [OK] 字段 'created_at' 存在
  [OK] id 是主键
  [OK] user_id 不为空
  [OK] user_id 是到 users.id 的外键

[PASS] PracticeLog 模型验证通过！

[Test 3] Portfolio 模型定义
----------------------------------------
  [OK] 字段 'id' 存在
  [OK] 字段 'user_id' 存在
  [OK] 字段 'image_url' 存在
  [OK] 字段 'created_at' 存在
  [OK] id 是主键
  [OK] user_id 不为空
  [OK] image_url 不为空
  [OK] user_id 是到 users.id 的外键

[PASS] Portfolio 模型验证通过！

[Test 4] 模型关系定义
----------------------------------------
  [OK] User.practice_logs 关系已定义
  [OK] User.portfolios 关系已定义
  [OK] PracticeLog.user 关系已定义
  [OK] Portfolio.user 关系已定义

[PASS] 模型关系验证通过！

[Test 5] 级联删除配置
----------------------------------------
  [OK] practice_logs 配置了 delete 级联
  [OK] portfolios 配置了 delete 级联

[PASS] 级联删除配置验证通过！

============================================================
[SUCCESS] 所有模型验证测试通过！
============================================================
```

## 故障排除

### 问题：`ModuleNotFoundError: No module named 'app'`

**解决方案**: 确保在 `backend` 目录下运行测试脚本。

### 问题：`UnicodeEncodeError`

**解决方案**: 设置环境变量 `PYTHONUTF8=1` 或使用 UTF-8 编码的终端。

### 问题：MySQL 连接失败（完整测试）

**解决方案**:
1. 检查 MySQL 服务是否启动
2. 确认 `.env` 文件中的数据库配置正确
3. 确保数据库用户有足够权限
