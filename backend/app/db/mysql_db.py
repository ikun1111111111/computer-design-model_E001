from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from app.core.config import settings

# Database URL
DATABASE_URL = f"mysql+mysqlconnector://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}"

# Create engine
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class Conversation(Base):
    """对话表 - 存储用户与知识馆长的对话历史"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True, nullable=False)  # 会话 ID，用于区分不同用户/会话
    user_query = Column(Text, nullable=False)  # 用户问题
    agent_answer = Column(Text, nullable=False)  # AI 回答
    context_entities = Column(Text, default="")  # 上下文实体，逗号分隔
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联的追问选项
    follow_ups = relationship("FollowUpQuestion", back_populates="conversation", cascade="all, delete-orphan")


class FollowUpQuestion(Base):
    """追问建议表 - 存储为用户生成的追问选项"""
    __tablename__ = "follow_up_questions"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    question_text = Column(Text, nullable=False)  # 追问文本
    sort_order = Column(Integer, default=0)  # 排序顺序

    # 反向关联
    conversation = relationship("Conversation", back_populates="follow_ups")


# ============== E-001 用户数据模型 ==============

class User(Base):
    """用户表 - 存储用户基本信息"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="用户姓名")
    level = Column(Integer, default=1, comment="用户等级 (1-10)")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # 关联的学习记录和作品集
    practice_logs = relationship("PracticeLog", back_populates="user", cascade="all, delete-orphan")
    portfolios = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan")

    # 支持 Pydantic from_attributes
    class Config:
        from_attributes = True


class PracticeLog(Base):
    """学习记录表 - 存储用户的练习记录"""
    __tablename__ = "practice_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户 ID")
    craft_id = Column(Integer, nullable=False, comment="工艺 ID")
    craft_name = Column(String(100), comment="工艺名称")
    duration = Column(Integer, comment="练习时长 (秒)")
    score = Column(Float, comment="评分 (0-100)")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # 反向关联
    user = relationship("User", back_populates="practice_logs")

    # 支持 Pydantic from_attributes
    class Config:
        from_attributes = True


class Portfolio(Base):
    """作品集表 - 存储用户的作品"""
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户 ID")
    image_url = Column(String(500), nullable=False, comment="作品图片 URL")
    craft_type = Column(String(100), comment="工艺类型")
    description = Column(Text, comment="作品描述")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # 反向关联
    user = relationship("User", back_populates="portfolios")

    # 支持 Pydantic from_attributes
    class Config:
        from_attributes = True


def init_db():
    """初始化数据库，创建所有表"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
