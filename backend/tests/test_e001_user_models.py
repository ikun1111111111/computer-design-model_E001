"""
E-001 用户数据模型测试脚本
测试用户表、学习记录表和作品集表的功能
"""

import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.mysql_db import User, PracticeLog, Portfolio, Base
from app.core.config import settings


def create_test_database():
    """创建测试数据库"""
    from mysql.connector import connect
    try:
        connection = connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS test_inheritor_db")
        cursor.close()
        connection.close()
        print("测试数据库 'test_inheritor_db' 创建成功或已存在。")
        return True
    except Exception as e:
        print(f"创建测试数据库失败：{e}")
        return False


def get_test_engine():
    """获取测试数据库引擎"""
    test_db_url = f"mysql+mysqlconnector://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/test_inheritor_db"
    return create_engine(test_db_url, echo=False)


def setup_test_db():
    """设置测试数据库，创建所有表"""
    test_engine = get_test_engine()
    Base.metadata.create_all(bind=test_engine)
    print("测试数据库表创建成功。")
    return test_engine


def teardown_test_db(test_engine):
    """清理测试数据库，删除所有表"""
    from mysql.connector import connect
    try:
        # 直接使用 SQL 删除数据库，避免外键约束问题
        connection = connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute("DROP DATABASE IF EXISTS test_inheritor_db")
        cursor.close()
        connection.close()
        print("测试数据库表已清理。")
    except Exception as e:
        print(f"清理测试数据库失败：{e}")


def test_user_model(session):
    """测试用户模型 CRUD 操作"""
    print("\n" + "=" * 50)
    print("测试 1: 用户模型 (User)")
    print("=" * 50)

    # Create - 创建用户
    print("\n[创建用户]")
    test_user = User(name="张三", level=1)
    session.add(test_user)
    session.commit()
    print(f"创建用户：id={test_user.id}, name={test_user.name}, level={test_user.level}")
    assert test_user.id is not None
    assert test_user.name == "张三"
    assert test_user.level == 1

    # Read - 查询用户
    print("\n[查询用户]")
    user = session.query(User).filter_by(name="张三").first()
    print(f"查询到用户：id={user.id}, name={user.name}, level={user.level}, created_at={user.created_at}")
    assert user is not None
    assert user.name == "张三"

    # Update - 更新用户
    print("\n[更新用户]")
    user.level = 5
    session.commit()
    updated_user = session.query(User).filter_by(id=user.id).first()
    print(f"更新后用户等级：{updated_user.level}")
    assert updated_user.level == 5

    # Delete - 删除用户
    print("\n[删除用户]")
    session.delete(updated_user)
    session.commit()
    deleted_user = session.query(User).filter_by(id=user.id).first()
    print(f"删除后查询结果：{deleted_user}")
    assert deleted_user is None

    print("\n[OK] 用户模型测试通过！")
    return True


def test_practice_log_model(session):
    """测试学习记录模型 CRUD 操作"""
    print("\n" + "=" * 50)
    print("测试 2: 学习记录模型 (PracticeLog)")
    print("=" * 50)

    # 先创建测试用户
    test_user = User(name="李四", level=2)
    session.add(test_user)
    session.commit()

    # Create - 创建学习记录
    print("\n[创建学习记录]")
    log = PracticeLog(
        user_id=test_user.id,
        craft_id=101,
        craft_name="苏绣",
        duration=1800,  # 30 分钟
        score=85.5
    )
    session.add(log)
    session.commit()
    print(f"创建学习记录：id={log.id}, user_id={log.user_id}, craft_name={log.craft_name}, duration={log.duration}s, score={log.score}")
    assert log.id is not None
    assert log.duration == 1800
    assert log.score == 85.5

    # Read - 查询学习记录
    print("\n[查询学习记录]")
    practice_log = session.query(PracticeLog).filter_by(user_id=test_user.id).first()
    print(f"查询到学习记录：id={practice_log.id}, craft_name={practice_log.craft_name}, score={practice_log.score}")
    assert practice_log is not None
    assert practice_log.craft_name == "苏绣"

    # 查询用户的学习记录（关联查询）
    print("\n[关联查询 - 用户的学习记录]")
    user = session.query(User).filter_by(id=test_user.id).first()
    user_logs = user.practice_logs
    print(f"用户 '{user.name}' 共有 {len(user_logs)} 条学习记录")
    assert len(user_logs) == 1

    # Update - 更新学习记录
    print("\n[更新学习记录]")
    practice_log.score = 92.0
    practice_log.duration = 2400
    session.commit()
    updated_log = session.query(PracticeLog).filter_by(id=practice_log.id).first()
    print(f"更新后评分：{updated_log.score}, 时长：{updated_log.duration}s")
    assert updated_log.score == 92.0
    assert updated_log.duration == 2400

    # Delete - 删除学习记录
    print("\n[删除学习记录]")
    session.delete(practice_log)
    session.commit()
    deleted_log = session.query(PracticeLog).filter_by(id=practice_log.id).first()
    print(f"删除后查询结果：{deleted_log}")
    assert deleted_log is None

    # 清理测试用户
    session.delete(test_user)
    session.commit()

    print("\n[OK] 学习记录模型测试通过！")
    return True


def test_portfolio_model(session):
    """测试作品集模型 CRUD 操作"""
    print("\n" + "=" * 50)
    print("测试 3: 作品集模型 (Portfolio)")
    print("=" * 50)

    # 先创建测试用户
    test_user = User(name="王五", level=3)
    session.add(test_user)
    session.commit()

    # Create - 创建作品
    print("\n[创建作品]")
    portfolio = Portfolio(
        user_id=test_user.id,
        image_url="/images/portfolios/user_5_work_1.jpg",
        craft_type="苏绣",
        description="双面绣作品 - 小猫，尺寸 30x40cm"
    )
    session.add(portfolio)
    session.commit()
    print(f"创建作品：id={portfolio.id}, user_id={portfolio.user_id}, craft_type={portfolio.craft_type}")
    print(f"  图片 URL: {portfolio.image_url}")
    print(f"  描述：{portfolio.description}")
    assert portfolio.id is not None
    assert portfolio.craft_type == "苏绣"

    # Read - 查询作品
    print("\n[查询作品]")
    user_portfolio = session.query(Portfolio).filter_by(user_id=test_user.id).first()
    print(f"查询到作品：id={user_portfolio.id}, craft_type={user_portfolio.craft_type}")
    assert user_portfolio is not None
    assert user_portfolio.image_url == "/images/portfolios/user_5_work_1.jpg"

    # 查询用户的作品集（关联查询）
    print("\n[关联查询 - 用户的作品集]")
    user = session.query(User).filter_by(id=test_user.id).first()
    user_portfolios = user.portfolios
    print(f"用户 '{user.name}' 共有 {len(user_portfolios)} 个作品")
    assert len(user_portfolios) == 1

    # 创建更多作品用于测试
    print("\n[创建多个作品]")
    for i in range(2, 4):
        new_work = Portfolio(
            user_id=test_user.id,
            image_url=f"/images/portfolios/user_5_work_{i}.jpg",
            craft_type="紫砂" if i == 2 else "皮影戏",
            description=f"作品 {i}"
        )
        session.add(new_work)
    session.commit()

    all_portfolios = session.query(Portfolio).filter_by(user_id=test_user.id).all()
    print(f"用户 '{user.name}' 现在有 {len(all_portfolios)} 个作品")
    assert len(all_portfolios) == 3

    # Update - 更新作品
    print("\n[更新作品]")
    user_portfolio.description = "精美双面绣 - 小猫（已装裱）"
    session.commit()
    updated_portfolio = session.query(Portfolio).filter_by(id=user_portfolio.id).first()
    print(f"更新后描述：{updated_portfolio.description}")
    assert updated_portfolio.description == "精美双面绣 - 小猫（已装裱）"

    # Delete - 删除作品
    print("\n[删除作品]")
    for p in all_portfolios:
        session.delete(p)
    session.commit()

    remaining = session.query(Portfolio).filter_by(user_id=test_user.id).count()
    print(f"删除后剩余作品数：{remaining}")
    assert remaining == 0

    # 清理测试用户
    session.delete(test_user)
    session.commit()

    print("\n[OK] 作品集模型测试通过！")
    return True


def test_cascade_delete(session):
    """测试级联删除功能"""
    print("\n" + "=" * 50)
    print("测试 4: 级联删除 (Cascade Delete)")
    print("=" * 50)

    # 创建用户和相关数据
    print("\n[创建用户及关联数据]")
    test_user = User(name="赵六", level=4)
    session.add(test_user)
    session.commit()

    # 添加学习记录
    log = PracticeLog(
        user_id=test_user.id,
        craft_id=102,
        craft_name="紫砂",
        duration=3600,
        score=78.0
    )
    session.add(log)

    # 添加作品
    portfolio = Portfolio(
        user_id=test_user.id,
        image_url="/images/test.jpg",
        craft_type="紫砂",
        description="测试作品"
    )
    session.add(portfolio)
    session.commit()

    print(f"创建用户 (id={test_user.id})，1 条学习记录，1 个作品")

    # 验证关联数据存在
    log_count_before = session.query(PracticeLog).filter_by(user_id=test_user.id).count()
    portfolio_count_before = session.query(Portfolio).filter_by(user_id=test_user.id).count()
    print(f"删除前：学习记录={log_count_before}, 作品={portfolio_count_before}")
    assert log_count_before == 1
    assert portfolio_count_before == 1

    # 删除用户
    print("\n[删除用户]")
    session.delete(test_user)
    session.commit()

    # 验证级联删除
    log_count_after = session.query(PracticeLog).filter_by(user_id=test_user.id).count()
    portfolio_count_after = session.query(Portfolio).filter_by(user_id=test_user.id).count()
    print(f"删除后：学习记录={log_count_after}, 作品={portfolio_count_after}")

    assert log_count_after == 0, "学习记录应该被级联删除"
    assert portfolio_count_after == 0, "作品应该被级联删除"

    print("\n[OK] 级联删除测试通过！")
    return True


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("E-001 用户数据模型测试")
    print("=" * 60)
    print(f"测试数据库：test_inheritor_db")
    print(f"数据库主机：{settings.MYSQL_HOST}:{settings.MYSQL_PORT}")
    print("=" * 60)

    # 创建测试数据库
    if not create_test_database():
        print("无法创建测试数据库，退出测试。")
        return False

    # 设置测试数据库
    test_engine = setup_test_db()
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestSessionLocal()

    all_passed = True

    try:
        # 运行测试
        if not test_user_model(session):
            all_passed = False
            print(f"\n[ERROR] 用户模型测试失败")

        if not test_practice_log_model(session):
            all_passed = False
            print(f"\n[ERROR] 学习记录模型测试失败")

        if not test_portfolio_model(session):
            all_passed = False
            print(f"\n[ERROR] 作品集模型测试失败")

        if not test_cascade_delete(session):
            all_passed = False
            print(f"\n[ERROR] 级联删除测试失败")

    except Exception as e:
        all_passed = False
        print(f"\n[ERROR] 测试执行出错：{e}")
        import traceback
        traceback.print_exc()

    finally:
        # 清理测试数据
        try:
            session.close()
        except:
            pass
        # 使用 SQL 直接删除数据库
        try:
            from mysql.connector import connect
            connection = connect(
                host=settings.MYSQL_HOST,
                port=settings.MYSQL_PORT,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                autocommit=True
            )
            cursor = connection.cursor()
            cursor.execute("DROP DATABASE IF EXISTS test_inheritor_db")
            cursor.close()
            connection.close()
            print("测试数据库表已清理。")
        except Exception as e:
            print(f"清理测试数据库失败：{e}")

    # 输出测试结果
    print("\n" + "=" * 60)
    if all_passed:
        print("[OK] 所有测试通过！")
    else:
        print("[ERROR] 部分测试失败")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
