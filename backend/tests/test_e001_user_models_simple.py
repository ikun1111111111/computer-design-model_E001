"""
E-001 用户数据模型验证测试
不依赖实际数据库连接，仅验证模型定义的正确性
"""

# 设置 UTF-8 编码支持（Windows 控制台）
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, "../"))

from app.db.mysql_db import User, PracticeLog, Portfolio, Base
from sqlalchemy.inspection import inspect


def test_model_definitions():
    """测试模型定义是否正确"""
    print("=" * 60)
    print("E-001 用户数据模型验证测试")
    print("=" * 60)

    all_passed = True

    # 测试 User 模型
    print("\n[Test 1] User 模型定义")
    print("-" * 40)
    mapper = inspect(User)
    columns = {c.key: c for c in mapper.columns}

    # 检查必需字段
    required_fields = ["id", "name", "level", "created_at"]
    for field in required_fields:
        if field in columns:
            print(f"  [OK] 字段 '{field}' 存在")
        else:
            print(f"  [FAIL] 字段 '{field}' 缺失")
            all_passed = False

    # 检查字段类型
    assert columns["id"].primary_key, "id 应该是主键"
    print("  [OK] id 是主键")

    assert not columns["name"].nullable, "name 不应该为空"
    print("  [OK] name 不为空")

    assert columns["level"].default.arg == 1, "level 默认值应该是 1"
    print("  [OK] level 默认值为 1")

    print("\n[PASS] User 模型验证通过！")

    # 测试 PracticeLog 模型
    print("\n[测试 2] PracticeLog 模型定义")
    print("-" * 40)
    mapper = inspect(PracticeLog)
    columns = {c.key: c for c in mapper.columns}

    required_fields = ["id", "user_id", "craft_id", "duration", "score", "created_at"]
    for field in required_fields:
        if field in columns:
            print(f"  [OK] 字段 '{field}' 存在")
        else:
            print(f"  [FAIL] 字段 '{field}' 缺失")
            all_passed = False

    assert columns["id"].primary_key, "id 应该是主键"
    print("  [OK] id 是主键")

    assert not columns["user_id"].nullable, "user_id 不应该为空"
    print("  [OK] user_id 不为空")

    # 检查外键
    fk_columns = [c for c in mapper.columns if c.foreign_keys]
    fk_names = [list(c.foreign_keys)[0].target_fullname for c in fk_columns]
    assert "users.id" in fk_names, "应该有到 users.id 的外键"
    print("  [OK] user_id 是到 users.id 的外键")

    print("\n[PASS] PracticeLog 模型验证通过！")

    # 测试 Portfolio 模型
    print("\n[测试 3] Portfolio 模型定义")
    print("-" * 40)
    mapper = inspect(Portfolio)
    columns = {c.key: c for c in mapper.columns}

    required_fields = ["id", "user_id", "image_url", "created_at"]
    for field in required_fields:
        if field in columns:
            print(f"  [OK] 字段 '{field}' 存在")
        else:
            print(f"  [FAIL] 字段 '{field}' 缺失")
            all_passed = False

    assert columns["id"].primary_key, "id 应该是主键"
    print("  [OK] id 是主键")

    assert not columns["user_id"].nullable, "user_id 不应该为空"
    print("  [OK] user_id 不为空")

    assert not columns["image_url"].nullable, "image_url 不应该为空"
    print("  [OK] image_url 不为空")

    # 检查外键
    fk_columns = [c for c in mapper.columns if c.foreign_keys]
    fk_names = [list(c.foreign_keys)[0].target_fullname for c in fk_columns]
    assert "users.id" in fk_names, "应该有到 users.id 的外键"
    print("  [OK] user_id 是到 users.id 的外键")

    print("\n[PASS] Portfolio 模型验证通过！")

    # 测试关系定义
    print("\n[测试 4] 模型关系定义")
    print("-" * 40)

    # User -> PracticeLog
    user_relations = User.__mapper__.relationships
    assert "practice_logs" in user_relations, "User 应该有 practice_logs 关系"
    print("  [OK] User.practice_logs 关系已定义")

    # User -> Portfolio
    assert "portfolios" in user_relations, "User 应该有 portfolios 关系"
    print("  [OK] User.portfolios 关系已定义")

    # PracticeLog -> User
    practice_relations = PracticeLog.__mapper__.relationships
    assert "user" in practice_relations, "PracticeLog 应该有 user 关系"
    print("  [OK] PracticeLog.user 关系已定义")

    # Portfolio -> User
    portfolio_relations = Portfolio.__mapper__.relationships
    assert "user" in portfolio_relations, "Portfolio 应该有 user 关系"
    print("  [OK] Portfolio.user 关系已定义")

    print("\n[PASS] 模型关系验证通过！")

    # 测试级联删除配置
    print("\n[测试 5] 级联删除配置")
    print("-" * 40)

    for rel_name, rel in user_relations.items():
        if rel_name in ["practice_logs", "portfolios"]:
            assert "delete" in str(rel.cascade), f"{rel_name} 应该配置 delete 级联"
            print(f"  [OK] {rel_name} 配置了 delete 级联")

    print("\n[PASS] 级联删除配置验证通过！")

    # 输出测试结果
    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] 所有模型验证测试通过！")
    else:
        print("[FAILURE] 部分测试失败")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    success = test_model_definitions()
    sys.exit(0 if success else 1)
