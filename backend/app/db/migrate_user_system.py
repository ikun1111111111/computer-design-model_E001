"""
用户系统数据库迁移脚本
创建用户相关的数据表并初始化默认数据

检验标准:
- [x] 创建数据库迁移脚本
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from app.db.mysql_db import (
    engine, Base, User, PracticeRecord, UserWork, UserAbility, UserLevel,
    Conversation, FollowUpQuestion, SessionLocal
)
from sqlalchemy import text
from datetime import datetime


def create_tables():
    """创建所有用户系统相关的数据表"""
    print("=" * 50)
    print("创建用户系统数据表...")
    print("=" * 50)

    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✓ 数据表创建成功！")
        return True
    except Exception as e:
        print(f"✗ 数据表创建失败：{e}")
        return False


def seed_default_users():
    """初始化默认用户数据"""
    print("\n" + "=" * 50)
    print("初始化默认用户数据...")
    print("=" * 50)

    db = SessionLocal()
    try:
        # 检查是否已有用户
        existing_user = db.query(User).filter_by(name="李明").first()
        if existing_user:
            print("⚠ 默认用户已存在，跳过创建")
            return

        # 创建默认用户
        default_user = User(
            name="李明",
            avatar_url="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix",
            level=UserLevel.APPRENTICE,
            experience_points=1250,
            title="初级学徒"
        )
        db.add(default_user)
        db.commit()
        db.refresh(default_user)

        # 创建默认用户的能力数据
        default_ability = UserAbility(
            user_id=default_user.id,
            stability=75.0,
            accuracy=85.0,
            speed=60.0,
            creativity=70.0,
            knowledge=65.0
        )
        db.add(default_ability)

        # 创建一些模拟练习记录
        practice_records = [
            PracticeRecord(
                user_id=default_user.id,
                craft_id="su-embroidery",
                craft_name="苏绣·平针绣",
                scenario="embroidery",
                duration=1800,  # 30 分钟
                score=85.0,
                accuracy=88.0,
                feedback="运针稳定，但力度需要更加均匀",
                completed_at=datetime(2026, 3, 10, 14, 30)
            ),
            PracticeRecord(
                user_id=default_user.id,
                craft_id="su-embroidery",
                craft_name="苏绣·平针绣",
                scenario="embroidery",
                duration=2400,  # 40 分钟
                score=90.0,
                accuracy=92.0,
                feedback="动作标准度大幅提升，继续保持！",
                completed_at=datetime(2026, 3, 12, 10, 15)
            ),
            PracticeRecord(
                user_id=default_user.id,
                craft_id="purple-clay",
                craft_name="紫砂·拍泥片",
                scenario="clay",
                duration=1200,  # 20 分钟
                score=72.0,
                accuracy=75.0,
                feedback="拍打力度不均匀，需要注意手腕放松",
                completed_at=datetime(2026, 3, 11, 16, 45)
            ),
        ]
        for record in practice_records:
            db.add(record)

        # 创建模拟作品
        user_works = [
            UserWork(
                user_id=default_user.id,
                craft_id="su-embroidery",
                craft_name="苏绣",
                title="我的第一幅刺绣作品",
                description="学习平针绣一周后的练习作品",
                image_url="/assets/works/embroidery_work_001.jpg",
                ai_generated=0,
                status="public"
            ),
            UserWork(
                user_id=default_user.id,
                craft_id="purple-clay",
                craft_name="紫砂",
                title="仿古壶设计",
                description="尝试制作的第一个紫砂壶模型",
                image_url="/assets/works/clay_work_001.jpg",
                ai_generated=0,
                status="public"
            ),
        ]
        for work in user_works:
            db.add(work)

        db.commit()
        print(f"✓ 默认用户 '{default_user.name}' 创建成功！ID: {default_user.id}")
        print(f"  - 等级：{default_user.level.value}")
        print(f"  - 经验值：{default_user.experience_points}")
        print(f"  - 称号：{default_user.title}")
        print(f"  - 练习记录：{len(practice_records)} 条")
        print(f"  - 作品数量：{len(user_works)} 个")

    except Exception as e:
        db.rollback()
        print(f"✗ 初始化用户数据失败：{e}")
        raise
    finally:
        db.close()


def show_table_info():
    """显示数据表信息"""
    print("\n" + "=" * 50)
    print("数据表结构信息")
    print("=" * 50)

    db = SessionLocal()
    try:
        tables_info = [
            ("users", "用户表"),
            ("practice_records", "学习记录表"),
            ("user_works", "作品集表"),
            ("user_abilities", "用户能力表"),
            ("conversations", "对话历史表"),
            ("follow_up_questions", "追问选项表"),
        ]

        for table_name, table_desc in tables_info:
            result = db.execute(text(f"SHOW TABLES LIKE '{table_name}'"))
            if result.fetchone():
                # 获取表结构
                columns = db.execute(text(f"DESCRIBE {table_name}"))
                print(f"\n📋 {table_desc} ({table_name}):")
                for col in columns:
                    print(f"   - {col[0]}: {col[1]} {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
            else:
                print(f"\n✗ 表 {table_name} 不存在")

        # 统计数据量
        print("\n" + "=" * 50)
        print("数据统计")
        print("=" * 50)

        for table_name, _ in tables_info:
            result = db.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            print(f"   {table_name}: {count} 条记录")

    except Exception as e:
        print(f"查询失败：{e}")
    finally:
        db.close()


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("     用户系统数据库迁移工具")
    print("     User System Database Migration Tool")
    print("=" * 60)

    # 步骤 1: 创建数据表
    if not create_tables():
        print("\n迁移失败，退出")
        return

    # 步骤 2: 初始化默认数据
    try:
        seed_default_users()
    except Exception as e:
        print(f"\n初始化默认数据失败：{e}")
        return

    # 步骤 3: 显示表信息
    show_table_info()

    print("\n" + "=" * 60)
    print("✅ 数据库迁移完成！")
    print("=" * 60)
    print(f"\n数据库信息:")
    print(f"  - Host: localhost:3306")
    print(f"  - Database: inheritor_db")
    print("\n已创建的数据表:")
    print("  - users: 用户基本信息表")
    print("  - practice_records: 用户练习记录表")
    print("  - user_works: 用户作品集表")
    print("  - user_abilities: 用户能力五维数据表")
    print("  - conversations: 对话历史表 (原有)")
    print("  - follow_up_questions: 追问选项表 (原有)")
    print("\n📝 提示：")
    print("  - 默认用户：李明 (初级学徒)")
    print("  - 可使用 MySQL 客户端查看和管理数据")


if __name__ == "__main__":
    main()
