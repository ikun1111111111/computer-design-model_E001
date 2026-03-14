"""
E-001 用户数据模型迁移脚本
创建用户表、学习记录表和作品集表
"""

import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

import mysql.connector
from mysql.connector import Error
from app.core.config import settings


def check_table_exists(cursor, table_name):
    """检查表是否已存在"""
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s",
        (settings.MYSQL_DATABASE, table_name)
    )
    return cursor.fetchone()[0] > 0


def create_users_table(cursor):
    """创建用户表"""
    if check_table_exists(cursor, "users"):
        print("表 'users' 已存在，跳过创建。")
        return

    create_table_sql = """
    CREATE TABLE `users` (
        `id` INT NOT NULL AUTO_INCREMENT COMMENT '用户 ID',
        `name` VARCHAR(100) NOT NULL COMMENT '用户姓名',
        `level` INT DEFAULT 1 COMMENT '用户等级 (1-10)',
        `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        PRIMARY KEY (`id`),
        INDEX `idx_users_name` (`name`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
    """
    cursor.execute(create_table_sql)
    print("创建表 'users' 成功。")


def create_practice_logs_table(cursor):
    """创建学习记录表"""
    if check_table_exists(cursor, "practice_logs"):
        print("表 'practice_logs' 已存在，跳过创建。")
        return

    create_table_sql = """
    CREATE TABLE `practice_logs` (
        `id` INT NOT NULL AUTO_INCREMENT COMMENT '记录 ID',
        `user_id` INT NOT NULL COMMENT '用户 ID',
        `craft_id` INT NOT NULL COMMENT '工艺 ID',
        `craft_name` VARCHAR(100) COMMENT '工艺名称',
        `duration` INT COMMENT '练习时长 (秒)',
        `score` DECIMAL(5,2) COMMENT '评分 (0-100)',
        `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        PRIMARY KEY (`id`),
        INDEX `idx_practice_logs_user_id` (`user_id`),
        INDEX `idx_practice_logs_craft_id` (`craft_id`),
        CONSTRAINT `fk_practice_logs_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学习记录表';
    """
    cursor.execute(create_table_sql)
    print("创建表 'practice_logs' 成功。")


def create_portfolios_table(cursor):
    """创建作品集表"""
    if check_table_exists(cursor, "portfolios"):
        print("表 'portfolios' 已存在，跳过创建。")
        return

    create_table_sql = """
    CREATE TABLE `portfolios` (
        `id` INT NOT NULL AUTO_INCREMENT COMMENT '作品 ID',
        `user_id` INT NOT NULL COMMENT '用户 ID',
        `image_url` VARCHAR(500) NOT NULL COMMENT '作品图片 URL',
        `craft_type` VARCHAR(100) COMMENT '工艺类型',
        `description` TEXT COMMENT '作品描述',
        `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        PRIMARY KEY (`id`),
        INDEX `idx_portfolios_user_id` (`user_id`),
        CONSTRAINT `fk_portfolios_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='作品集表';
    """
    cursor.execute(create_table_sql)
    print("创建表 'portfolios' 成功。")


def run_migration():
    """执行迁移"""
    print("=" * 50)
    print("E-001 用户数据模型迁移")
    print("=" * 50)

    connection = None
    cursor = None

    try:
        # 连接数据库
        connection = mysql.connector.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DATABASE
        )

        if not connection.is_connected():
            print("数据库连接失败，退出。")
            return False

        cursor = connection.cursor()
        print(f"已连接到数据库 '{settings.MYSQL_DATABASE}'")

        # 创建表
        print("\n开始创建用户数据表...")
        create_users_table(cursor)
        create_practice_logs_table(cursor)
        create_portfolios_table(cursor)

        # 提交事务
        connection.commit()
        print("\n迁移提交成功！")

        # 验证表结构
        print("\n验证表结构:")
        for table_name in ["users", "practice_logs", "portfolios"]:
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            print(f"\n  {table_name} 表结构:")
            for col in columns:
                print(f"    - {col[0]}: {col[1]}")

        return True

    except Error as e:
        print(f"迁移失败：{e}")
        if connection:
            connection.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("\n数据库连接已关闭。")

        print("\n" + "=" * 50)
        print("迁移完成")
        print("=" * 50)


def rollback_migration():
    """回滚迁移 - 删除用户数据表"""
    print("=" * 50)
    print("E-001 迁移回滚")
    print("=" * 50)

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DATABASE
        )

        if not connection.is_connected():
            print("数据库连接失败，退出。")
            return False

        cursor = connection.cursor()

        # 删除表（顺序很重要，先删除有外键约束的表）
        print("删除表 'portfolios'...")
        cursor.execute("DROP TABLE IF EXISTS portfolios")

        print("删除表 'practice_logs'...")
        cursor.execute("DROP TABLE IF EXISTS practice_logs")

        print("删除表 'users'...")
        cursor.execute("DROP TABLE IF EXISTS users")

        connection.commit()
        print("\n回滚成功！所有用户数据表已删除。")
        return True

    except Error as e:
        print(f"回滚失败：{e}")
        if connection:
            connection.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="E-001 用户数据模型迁移脚本")
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="执行回滚操作，删除用户数据表"
    )

    args = parser.parse_args()

    if args.rollback:
        rollback_migration()
    else:
        run_migration()
