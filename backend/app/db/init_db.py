"""
数据库初始化脚本
创建 MySQL 数据库和表
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import mysql.connector
from mysql.connector import Error
from app.core.config import settings
from app.db.mysql_db import init_db


def create_database():
    """创建数据库（如果不存在）"""
    try:
        connection = mysql.connector.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.MYSQL_DATABASE}")
            print(f"Database '{settings.MYSQL_DATABASE}' created or already exists.")
            cursor.close()
            connection.close()
            return True

    except Error as e:
        print(f"Error creating database: {e}")
        return False


def init_database():
    """初始化数据库"""
    print("=" * 50)
    print("数据库初始化")
    print("=" * 50)

    # 1. 创建数据库
    if not create_database():
        print("数据库创建失败，退出")
        return

    # 2. 创建表
    print("\n创建数据表...")
    try:
        init_db()
        print("数据表创建成功！")
    except Exception as e:
        print(f"数据表创建失败：{e}")
        return

    print("\n" + "=" * 50)
    print("数据库初始化完成！")
    print("=" * 50)
    print(f"\n数据库信息:")
    print(f"  - Host: {settings.MYSQL_HOST}:{settings.MYSQL_PORT}")
    print(f"  - Database: {settings.MYSQL_DATABASE}")
    print(f"  - User: {settings.MYSQL_USER}")
    print("\n数据表:")
    print("  - users: 用户基本信息表")
    print("  - practice_records: 用户练习记录表")
    print("  - user_works: 用户作品集表")
    print("  - user_abilities: 用户能力五维数据表")
    print("  - conversations: 对话历史表")
    print("  - follow_up_questions: 追问选项表")


if __name__ == "__main__":
    init_database()
