from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv
from app.core.config import settings
import enum

# Load environment variables from .env file
load_dotenv()

# Database URL
DATABASE_URL = f"mysql+mysqlconnector://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}"

# Create engine
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# ============== 用户系统数据模型 ==============

class UserLevel(enum.Enum):
    """用户等级枚举"""
    BEGINNER = "beginner"       # 初学者
    APPRENTICE = "apprentice"   # 学徒
    ADVANCED = "advanced"       # 进阶
    MASTER = "master"           # 大师
    GRANDMASTER = "grandmaster" # 宗师


class User(Base):
    """
    用户表 - 存储用户基本信息
    检验标准:
    - [x] 用户表：id, name, level, created_at
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, comment="用户名")
    avatar_url = Column(String(255), default="https://api.dicebear.com/7.x/avataaars/svg?seed=default", comment="头像 URL")
    level = Column(Enum(UserLevel), default=UserLevel.BEGINNER, comment="用户等级")
    experience_points = Column(Integer, default=0, comment="经验值")
    title = Column(String(50), default="初学者", comment="称号")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 关联关系
    practice_records = relationship("PracticeRecord", back_populates="user", cascade="all, delete-orphan")
    user_works = relationship("UserWork", back_populates="user", cascade="all, delete-orphan")
    user_abilities = relationship("UserAbility", back_populates="user", cascade="all, delete-orphan", uselist=False)


class PracticeRecord(Base):
    """
    学习记录表 - 存储用户练习记录
    检验标准:
    - [x] 学习记录表：user_id, craft_id, duration, score
    """
    __tablename__ = "practice_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户 ID")
    craft_id = Column(String(50), nullable=False, comment="工艺 ID (如：su-embroidery, purple-clay)")
    craft_name = Column(String(100), comment="工艺名称")
    scenario = Column(String(50), comment="练习场景 (如：embroidery, clay)")
    duration = Column(Integer, default=0, comment="练习时长 (秒)")
    score = Column(Float, default=0.0, comment="得分 (0-100)")
    accuracy = Column(Float, default=0.0, comment="动作准确率 (0-100)")
    feedback = Column(Text, comment="AI 反馈内容")
    completed_at = Column(DateTime, default=datetime.utcnow, comment="完成时间")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # 关联关系
    user = relationship("User", back_populates="practice_records")


class UserWork(Base):
    """
    作品集表 - 存储用户创作的作品
    检验标准:
    - [x] 作品集表：user_id, image_url, created_at
    """
    __tablename__ = "user_works"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户 ID")
    craft_id = Column(String(50), nullable=False, comment="工艺 ID")
    craft_name = Column(String(100), comment="工艺名称")
    title = Column(String(100), comment="作品标题")
    description = Column(Text, comment="作品描述")
    image_url = Column(String(255), nullable=False, comment="作品图片 URL")
    thumbnail_url = Column(String(255), comment="缩略图 URL")
    ai_generated = Column(Integer, default=0, comment="是否 AI 生成 (0:否，1:是)")
    prompt_used = Column(Text, comment="AI 生成提示词")
    style = Column(String(50), comment="艺术风格")
    likes = Column(Integer, default=0, comment="点赞数")
    status = Column(String(20), default="private", comment="状态：private 私有，public 公开")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    # 关联关系
    user = relationship("User", back_populates="user_works")


class UserAbility(Base):
    """
    用户能力表 - 存储用户五维能力数据 (用于雷达图)
    检验标准:
    - [x] 能力五维数据 (稳定性/准确度/速度/创意/知识)
    """
    __tablename__ = "user_abilities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, comment="用户 ID")
    stability = Column(Float, default=0.0, comment="稳定性 (0-100)")      # 动作稳定性
    accuracy = Column(Float, default=0.0, comment="准确度 (0-100)")       # 动作准确度
    speed = Column(Float, default=0.0, comment="速度 (0-100)")           # 完成速度
    creativity = Column(Float, default=0.0, comment="创意 (0-100)")       # 创意能力
    knowledge = Column(Float, default=0.0, comment="知识 (0-100)")        # 知识掌握
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 关联关系
    user = relationship("User", back_populates="user_abilities")


# ============== 原有知识馆长数据模型 ==============

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
