# E-001 用户档案系统 API 使用指南

## API 端点

基础 URL: `/api/v1/user`

### 用户管理

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/users` | 获取所有用户列表 |
| GET | `/users/{user_id}` | 获取单个用户详情 |
| POST | `/users?name={name}&level={level}` | 创建新用户 |
| PUT | `/users/{user_id}?name={name}&level={level}` | 更新用户信息 |
| DELETE | `/users/{user_id}` | 删除用户（级联删除） |

### 学习记录管理

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/users/{user_id}/practice-logs` | 获取用户的学习记录 |
| POST | `/users/{user_id}/practice-logs?craft_id={id}&craft_name={name}&duration={s}&score={score}` | 创建学习记录 |
| GET | `/users/{user_id}/practice-stats` | 获取用户学习统计 |

### 作品集管理

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/users/{user_id}/portfolios` | 获取用户的作品集 |
| POST | `/users/{user_id}/portfolios?image_url={url}&craft_type={type}&description={desc}` | 创建作品 |
| DELETE | `/portfolios/{portfolio_id}` | 删除作品 |

### 用户完整档案

| 方法 | 端点 | 说明 |
|------|------|------|
| GET | `/users/{user_id}/profile` | 获取用户完整档案（含统计和作品） |

---

## 使用示例

### 1. 创建用户

```bash
curl -X POST "http://localhost:8000/api/v1/users?name=张三&level=1"
```

响应:
```json
{
  "id": 1,
  "name": "张三",
  "level": 1,
  "created_at": "2026-03-14T10:00:00"
}
```

### 2. 创建学习记录

```bash
curl -X POST "http://localhost:8000/api/v1/users/1/practice-logs?craft_id=101&craft_name=苏绣&duration=1800&score=85.5"
```

响应:
```json
{
  "id": 1,
  "user_id": 1,
  "craft_id": 101,
  "craft_name": "苏绣",
  "duration": 1800,
  "score": 85.5,
  "created_at": "2026-03-14T10:05:00"
}
```

### 3. 创建作品

```bash
curl -X POST "http://localhost:8000/api/v1/users/1/portfolios?image_url=/images/work1.jpg&craft_type=苏绣&description=双面绣作品"
```

### 4. 获取用户完整档案

```bash
curl "http://localhost:8000/api/v1/users/1/profile"
```

响应:
```json
{
  "user": {
    "id": 1,
    "name": "张三",
    "level": 1,
    "created_at": "2026-03-14T10:00:00"
  },
  "stats": {
    "total_duration_seconds": 1800,
    "total_duration_minutes": 30.0,
    "total_sessions": 1,
    "average_score": 85.5,
    "crafts_practiced": 1
  },
  "portfolios": [...],
  "portfolio_count": 1
}
```

---

## 运行 API 测试

```bash
# 启动后端服务
cd backend
python run.py

# 在另一个终端运行测试
python tests/test_e001_api.py
```

---

## 数据模型

详见 `backend/app/db/mysql_db.py`:

- **User**: 用户表
- **PracticeLog**: 学习记录表
- **Portfolio**: 作品集表

所有关联数据都配置了**级联删除**，删除用户时会自动清理相关数据。
