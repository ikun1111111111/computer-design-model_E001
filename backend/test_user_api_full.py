"""
用户系统完整测试流程脚本
包含：数据库初始化 -> 运行测试 -> 清理数据

使用方法:
    python test_user_api_full.py

或者分步执行:
    1. python test_user_api_full.py --init   # 只初始化数据
    2. python test_user_api_full.py --test   # 只运行测试
    3. python test_user_api_full.py --clean  # 清理测试数据
"""

import sys
import os
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "./"))

from app.db.mysql_db import (
    engine, Base, User, PracticeRecord, UserWork, UserAbility, UserLevel,
    Conversation, FollowUpQuestion, SessionLocal
)
from sqlalchemy import text
from datetime import datetime
import requests
import json

BASE_URL = "http://localhost:8002/api/v1"

# ============== 数据库初始化函数 ==============

def check_mysql_connection():
    """检查 MySQL 连接是否正常"""
    print("\n" + "=" * 60)
    print("检查数据库连接...")
    print("=" * 60)

    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        print("[OK] 数据库连接正常")
        return True
    except Exception as e:
        print(f"[ERROR] 数据库连接失败：{e}")
        print("\n请检查:")
        print("  1. MySQL 服务是否已启动")
        print("  2. 数据库 inheritor_db 是否存在")
        print("  3. .env 文件中的数据库配置是否正确")
        print(f"  4. 当前配置：MYSQL_HOST={os.getenv('MYSQL_HOST', 'localhost')}, MYSQL_USER={os.getenv('MYSQL_USER', 'root')}, MYSQL_PASSWORD='{os.getenv('MYSQL_PASSWORD', '')}'")
        return False


def init_database():
    """初始化数据库"""
    print("\n" + "=" * 60)
    print("初始化数据库")
    print("=" * 60)

    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("[OK] 数据表创建成功")
        return True
    except Exception as e:
        print(f"[ERROR] 数据表创建失败：{e}")
        return False


def seed_test_data():
    """添加测试数据"""
    print("\n" + "=" * 60)
    print("添加测试数据")
    print("=" * 60)

    db = SessionLocal()
    try:
        # 检查是否已有测试用户
        existing_user = db.query(User).filter_by(name="测试用户").first()
        if existing_user:
            print("[WARN] 测试用户已存在，先清理旧数据")
            db.delete(existing_user)
            db.commit()

        # 创建测试用户
        test_user = User(
            name="测试用户",
            avatar_url="https://api.dicebear.com/7.x/avataaars/svg?seed=TestUser",
            level=UserLevel.APPRENTICE,
            experience_points=500,
            title="初级学徒"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"[OK] 创建测试用户：{test_user.name} (ID: {test_user.id})")

        # 创建能力数据
        test_ability = UserAbility(
            user_id=test_user.id,
            stability=70.0,
            accuracy=80.0,
            speed=65.0,
            creativity=75.0,
            knowledge=60.0
        )
        db.add(test_ability)
        db.commit()
        print(f"[OK] 创建能力数据")

        # 创建练习记录
        test_records = [
            PracticeRecord(
                user_id=test_user.id,
                craft_id="su-embroidery",
                craft_name="苏绣·平针绣",
                scenario="embroidery",
                duration=1800,
                score=85.0,
                accuracy=88.0,
                feedback="运针稳定，力度均匀"
            ),
            PracticeRecord(
                user_id=test_user.id,
                craft_id="purple-clay",
                craft_name="紫砂·拍泥片",
                scenario="clay",
                duration=1200,
                score=75.0,
                accuracy=78.0,
                feedback="拍打力度需要更均匀"
            ),
        ]
        for record in test_records:
            db.add(record)
        db.commit()
        print(f"[OK] 创建 {len(test_records)} 条练习记录")

        # 创建作品
        test_works = [
            UserWork(
                user_id=test_user.id,
                craft_id="su-embroidery",
                craft_name="苏绣",
                title="测试作品 - 平针绣",
                description="练习作品",
                image_url="/assets/works/test_001.jpg",
                ai_generated=0
            ),
        ]
        for work in test_works:
            db.add(work)
        db.commit()
        print(f"[OK] 创建 {len(test_works)} 个作品")

        print("\n[OK] 测试数据添加完成！")
        return test_user.id

    except Exception as e:
        db.rollback()
        print(f"[ERROR] 添加测试数据失败：{e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        db.close()


def clean_test_data():
    """清理测试数据"""
    print("\n" + "=" * 60)
    print("清理测试数据")
    print("=" * 60)

    db = SessionLocal()
    try:
        # 删除测试用户（级联删除相关数据）
        test_user = db.query(User).filter_by(name="测试用户").first()
        if test_user:
            db.delete(test_user)
            db.commit()
            print("[OK] 测试数据已清理")
        else:
            print("[WARN] 未找到测试用户，无需清理")
        return True

    except Exception as e:
        db.rollback()
        print(f"[ERROR] 清理失败：{e}")
        return False
    finally:
        db.close()


# ============== API 测试函数 ==============

def test_get_user_profile(user_id):
    """测试获取用户档案"""
    print("\n" + "-" * 50)
    print("测试：获取用户档案")
    print("-" * 50)

    try:
        response = requests.get(f"{BASE_URL}/user/profile", params={"user_id": user_id}, timeout=5)

        if response.status_code == 200:
            data = response.json()
            print(f"[OK] 请求成功 (状态码：{response.status_code})")
            print(f"  用户：{data['user']['name']}")
            print(f"  等级：{data['user']['level']}")
            print(f"  能力值：稳定性={data['abilities']['stability']}, 准确度={data['abilities']['accuracy']}")
            return True
        else:
            print(f"[ERROR] 请求失败 (状态码：{response.status_code})")
            print(f"  响应：{response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] 连接失败：无法连接到后端服务 (http://localhost:8002)")
        return False
    except Exception as e:
        print(f"[ERROR] 测试异常：{e}")
        return False


def test_get_user_stats(user_id):
    """测试获取用户统计数据"""
    print("\n" + "-" * 50)
    print("测试：获取用户统计数据")
    print("-" * 50)

    try:
        response = requests.get(f"{BASE_URL}/user/profile/{user_id}/stats", timeout=5)

        if response.status_code == 200:
            data = response.json()
            print(f"[OK] 请求成功 (状态码：{response.status_code})")
            print(f"  练习时长：{data['total_practice_hours']} 小时")
            print(f"  平均准确率：{data['average_accuracy']}%")
            return True
        else:
            print(f"[ERROR] 请求失败 (状态码：{response.status_code})")
            return False
    except Exception as e:
        print(f"[ERROR] 测试异常：{e}")
        return False


def test_add_practice_record(user_id):
    """测试添加练习记录"""
    print("\n" + "-" * 50)
    print("测试：添加练习记录")
    print("-" * 50)

    try:
        params = {
            "craft_id": "su-embroidery",
            "craft_name": "苏绣·平针绣",
            "duration": 1500,
            "score": 88.5,
            "accuracy": 90.0,
            "scenario": "embroidery",
            "feedback": "测试数据"
        }

        response = requests.post(
            f"{BASE_URL}/user/profile/{user_id}/practice-record",
            params=params,
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            print(f"[OK] 请求成功 (状态码：{response.status_code})")
            print(f"  记录 ID: {data['record_id']}")
            return True
        else:
            print(f"[ERROR] 请求失败 (状态码：{response.status_code})")
            print(f"  响应：{response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] 测试异常：{e}")
        return False


def test_get_practice_records(user_id):
    """测试获取练习记录"""
    print("\n" + "-" * 50)
    print("测试：获取练习记录")
    print("-" * 50)

    try:
        response = requests.get(
            f"{BASE_URL}/user/profile/{user_id}/practice-records",
            params={"limit": 5},
            timeout=5
        )

        if response.status_code == 200:
            records = response.json()
            print(f"[OK] 请求成功 (状态码：{response.status_code})")
            print(f"  记录数：{len(records)}")
            return True
        else:
            print(f"[ERROR] 请求失败 (状态码：{response.status_code})")
            return False
    except Exception as e:
        print(f"[ERROR] 测试异常：{e}")
        return False


def test_update_abilities(user_id):
    """测试更新用户能力"""
    print("\n" + "-" * 50)
    print("测试：更新用户能力数据")
    print("-" * 50)

    try:
        payload = {
            "stability": 75.0,
            "accuracy": 85.0,
            "speed": 70.0,
            "creativity": 72.0,
            "knowledge": 65.0
        }

        response = requests.put(
            f"{BASE_URL}/user/profile/{user_id}/abilities",
            params={"user_id": user_id},
            json=payload,
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            print(f"[OK] 请求成功 (状态码：{response.status_code})")
            print(f"  更新后的能力值：{data['abilities']}")
            return True
        else:
            print(f"[ERROR] 请求失败 (状态码：{response.status_code})")
            return False
    except Exception as e:
        print(f"[ERROR] 测试异常：{e}")
        return False


def test_add_user_work(user_id):
    """测试添加用户作品"""
    print("\n" + "-" * 50)
    print("测试：添加用户作品")
    print("-" * 50)

    try:
        params = {
            "craft_id": "su-embroidery",
            "craft_name": "苏绣",
            "title": "测试作品",
            "image_url": "/assets/works/test_work.jpg",
            "description": "测试描述",
            "ai_generated": False
        }

        response = requests.post(
            f"{BASE_URL}/user/profile/{user_id}/work",
            params=params,
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            print(f"[OK] 请求成功 (状态码：{response.status_code})")
            print(f"  作品 ID: {data['work_id']}")
            return True
        else:
            print(f"[ERROR] 请求失败 (状态码：{response.status_code})")
            return False
    except Exception as e:
        print(f"[ERROR] 测试异常：{e}")
        return False


def test_get_user_works(user_id):
    """测试获取用户作品集"""
    print("\n" + "-" * 50)
    print("测试：获取用户作品集")
    print("-" * 50)

    try:
        response = requests.get(
            f"{BASE_URL}/user/profile/{user_id}/works",
            params={"limit": 10},
            timeout=5
        )

        if response.status_code == 200:
            works = response.json()
            print(f"[OK] 请求成功 (状态码：{response.status_code})")
            print(f"  作品数：{len(works)}")
            return True
        else:
            print(f"[ERROR] 请求失败 (状态码：{response.status_code})")
            return False
    except Exception as e:
        print(f"[ERROR] 测试异常：{e}")
        return False


def run_all_tests(user_id):
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("开始运行 API 测试")
    print("=" * 60)

    tests = [
        ("获取用户档案", lambda: test_get_user_profile(user_id)),
        ("获取用户统计数据", lambda: test_get_user_stats(user_id)),
        ("添加练习记录", lambda: test_add_practice_record(user_id)),
        ("获取练习记录", lambda: test_get_practice_records(user_id)),
        ("更新用户能力", lambda: test_update_abilities(user_id)),
        ("添加用户作品", lambda: test_add_user_work(user_id)),
        ("获取用户作品集", lambda: test_get_user_works(user_id)),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n[ERROR] 测试异常：{test_name}: {e}")
            results.append((test_name, False))

    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "[OK] 通过" if success else "[ERROR] 失败"
        print(f"  {status}: {test_name}")

    print(f"\n总计：{passed}/{total} 测试通过")

    if passed == total:
        print("\n[SUCCESS] 所有测试通过！")
    else:
        print(f"\n[WARN] 有 {total - passed} 个测试失败")
        print("\n请检查:")
        print("  1. 后端服务是否已启动 (python run.py)")
        print("  2. 数据库是否正确初始化")
        print("  3. 查看上面的错误信息")

    return passed == total


# ============== 主函数 ==============

def main():
    parser = argparse.ArgumentParser(description="用户系统测试工具")
    parser.add_argument("--init", action="store_true", help="只初始化数据库")
    parser.add_argument("--test", action="store_true", help="只运行测试")
    parser.add_argument("--clean", action="store_true", help="清理测试数据")
    parser.add_argument("--full", action="store_true", help="完整流程：初始化 -> 测试 -> 清理")

    args = parser.parse_args()

    # 默认行为：完整流程
    if not any([args.init, args.test, args.clean, args.full]):
        args.full = True

    if args.init:
        # 只初始化
        if check_mysql_connection():
            init_database()
            seed_test_data()

    elif args.test:
        # 只运行测试
        print("\n提示：测试前请确保已运行 --init 初始化数据")
        user_id = 1  # 默认测试用户 ID

        # 先检查用户是否存在
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                print(f"[ERROR] 用户 ID={user_id} 不存在，请先运行 --init")
                return
        finally:
            db.close()

        run_all_tests(user_id)

    elif args.clean:
        # 清理数据
        clean_test_data()

    elif args.full:
        # 完整流程
        print("\n" + "=" * 60)
        print("     用户系统完整测试流程")
        print("     Full Test Suite for User System")
        print("=" * 60)

        # 步骤 1: 检查连接
        if not check_mysql_connection():
            print("\n[ERROR] 数据库连接失败，退出")
            return

        # 步骤 2: 初始化数据库
        init_database()

        # 步骤 3: 添加测试数据
        user_id = seed_test_data()
        if not user_id:
            print("\n[ERROR] 测试数据添加失败，退出")
            return

        # 步骤 4: 运行测试
        print("\n" + "=" * 60)
        print("等待 3 秒后开始测试...")
        print("=" * 60)

        success = run_all_tests(user_id)

        # 步骤 5: 清理（可选）
        if success:
            print("\n" + "=" * 60)
            response = input("是否清理测试数据？(y/n): ")
            if response.lower() == 'y':
                clean_test_data()
        else:
            print("\n[WARN] 测试未全部通过，保留测试数据以便调试")


if __name__ == "__main__":
    main()
