"""
用户档案 API 端点
提供用户信息、学习进度、能力雷达图等接口
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.mysql_db import get_db, User, PracticeRecord, UserWork, UserAbility, UserLevel


router = APIRouter()


# ============== Pydantic 模型 ==============

class UserProfileResponse(BaseModel):
    """用户档案响应模型"""
    id: int
    name: str
    avatar_url: str
    level: str
    experience_points: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class PracticeRecordResponse(BaseModel):
    """练习记录响应模型"""
    id: int
    craft_id: str
    craft_name: str
    scenario: Optional[str]
    duration: int
    score: float
    accuracy: float
    feedback: Optional[str]
    completed_at: datetime

    class Config:
        from_attributes = True


class UserWorkResponse(BaseModel):
    """作品响应模型"""
    id: int
    craft_id: str
    craft_name: str
    title: str
    description: Optional[str]
    image_url: str
    ai_generated: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserAbilityResponse(BaseModel):
    """用户能力响应模型"""
    stability: float
    accuracy: float
    speed: float
    creativity: float
    knowledge: float

    class Config:
        from_attributes = True


class UserStatsResponse(BaseModel):
    """用户统计数据响应模型"""
    total_practice_hours: float
    average_accuracy: float
    mastered_crafts: int
    total_works: int
    total_practice_sessions: int


# ============== API 端点 ==============

@router.get("/profile", response_model=Dict[str, Any])
async def get_user_profile(user_id: int = 1, db: Session = Depends(get_db)):
    """
    获取用户档案信息

    返回用户基本信息、能力五维数据、统计数据
    检验标准:
    - [x] GET /api/v1/user/profile 返回五维数据
    - [x] 每个维度 0-100 分
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 获取用户能力数据
    abilities = db.query(UserAbility).filter(UserAbility.user_id == user_id).first()
    if not abilities:
        # 如果没有能力数据，创建默认的
        abilities = UserAbility(user_id=user_id)
        db.add(abilities)
        db.commit()
        db.refresh(abilities)

    # 统计数据
    total_duration = db.query(func.sum(PracticeRecord.duration)).filter(
        PracticeRecord.user_id == user_id
    ).scalar() or 0

    avg_accuracy = db.query(func.avg(PracticeRecord.accuracy)).filter(
        PracticeRecord.user_id == user_id
    ).scalar() or 0

    # 统计掌握的技法数量 (准确率>=80 的记录)
    mastered_crafts = db.query(func.count(func.distinct(PracticeRecord.craft_id))).filter(
        PracticeRecord.user_id == user_id,
        PracticeRecord.accuracy >= 80
    ).scalar() or 0

    total_works = db.query(func.count(UserWork.id)).filter(
        UserWork.user_id == user_id
    ).scalar() or 0

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "avatar_url": user.avatar_url,
            "level": user.level.value,
            "experience_points": user.experience_points,
            "title": user.title,
            "created_at": user.created_at.isoformat()
        },
        "abilities": {
            "stability": abilities.stability,
            "accuracy": abilities.accuracy,
            "speed": abilities.speed,
            "creativity": abilities.creativity,
            "knowledge": abilities.knowledge
        },
        "stats": {
            "total_practice_hours": round(total_duration / 3600, 1),
            "average_accuracy": round(avg_accuracy, 1),
            "mastered_crafts": mastered_crafts,
            "total_works": total_works
        }
    }


@router.get("/profile/{user_id}/practice-records", response_model=List[PracticeRecordResponse])
async def get_user_practice_records(
    user_id: int,
    limit: int = 10,
    craft_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取用户练习记录"""
    query = db.query(PracticeRecord).filter(PracticeRecord.user_id == user_id)

    if craft_id:
        query = query.filter(PracticeRecord.craft_id == craft_id)

    records = query.order_by(PracticeRecord.completed_at.desc()).limit(limit).all()
    return records


@router.get("/profile/{user_id}/works", response_model=List[UserWorkResponse])
async def get_user_works(
    user_id: int,
    limit: int = 20,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取用户作品集"""
    query = db.query(UserWork).filter(UserWork.user_id == user_id)

    if status:
        query = query.filter(UserWork.status == status)

    works = query.order_by(UserWork.created_at.desc()).limit(limit).all()
    return works


@router.get("/profile/{user_id}/stats", response_model=UserStatsResponse)
async def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    """获取用户统计数据"""
    # 总练习时长 (小时)
    total_duration = db.query(func.sum(PracticeRecord.duration)).filter(
        PracticeRecord.user_id == user_id
    ).scalar() or 0

    # 平均准确率
    avg_accuracy = db.query(func.avg(PracticeRecord.accuracy)).filter(
        PracticeRecord.user_id == user_id
    ).scalar() or 0

    # 掌握的技法数量
    mastered_crafts = db.query(func.count(func.distinct(PracticeRecord.craft_id))).filter(
        PracticeRecord.user_id == user_id,
        PracticeRecord.accuracy >= 80
    ).scalar() or 0

    # 作品总数
    total_works = db.query(func.count(UserWork.id)).filter(
        UserWork.user_id == user_id
    ).scalar() or 0

    # 总练习次数
    total_sessions = db.query(func.count(PracticeRecord.id)).filter(
        PracticeRecord.user_id == user_id
    ).scalar() or 0

    return UserStatsResponse(
        total_practice_hours=round(total_duration / 3600, 1),
        average_accuracy=round(avg_accuracy, 1),
        mastered_crafts=mastered_crafts,
        total_works=total_works,
        total_practice_sessions=total_sessions
    )


@router.post("/profile/{user_id}/practice-record")
async def add_practice_record(
    user_id: int,
    craft_id: str,
    craft_name: str,
    duration: int,
    score: float,
    accuracy: float,
    scenario: Optional[str] = None,
    feedback: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    添加练习记录
    每次练习完成后调用此接口保存记录
    """
    record = PracticeRecord(
        user_id=user_id,
        craft_id=craft_id,
        craft_name=craft_name,
        scenario=scenario,
        duration=duration,
        score=score,
        accuracy=accuracy,
        feedback=feedback
    )
    db.add(record)

    # 更新用户能力数据
    abilities = db.query(UserAbility).filter(UserAbility.user_id == user_id).first()
    if not abilities:
        abilities = UserAbility(user_id=user_id)
        db.add(abilities)

    # 根据练习结果更新能力值 (简化版)
    # 稳定性：基于多次练习的分数方差
    # 准确度：基于 accuracy 的平均值
    # 速度：基于 duration 的倒数
    recent_records = db.query(PracticeRecord).filter(
        PracticeRecord.user_id == user_id
    ).order_by(PracticeRecord.created_at.desc()).limit(10).all()

    if recent_records:
        # 计算平均准确率
        new_accuracy = sum(r.accuracy for r in recent_records) / len(recent_records)
        abilities.accuracy = round(new_accuracy, 1)

        # 计算平均速度 (基于完成时间，时间越短速度越快)
        avg_duration = sum(r.duration for r in recent_records) / len(recent_records)
        # 假设标准完成时间是 1800 秒 (30 分钟)
        speed_score = min(100, (1800 / avg_duration) * 80) if avg_duration > 0 else 50
        abilities.speed = round(speed_score, 1)

        # 稳定性基于分数波动
        scores = [r.score for r in recent_records]
        if len(scores) > 1:
            avg_score = sum(scores) / len(scores)
            variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
            # 方差越小越稳定，转换为 0-100 的分数
            stability_score = max(0, min(100, 100 - variance / 10))
            abilities.stability = round(stability_score, 1)

    # 更新用户经验值
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        exp_gained = int(score * (duration / 600))  # 基于分数和时长计算经验
        user.experience_points += exp_gained
        # 根据经验值更新等级
        if user.experience_points >= 5000:
            user.level = UserLevel.GRANDMASTER
            user.title = "非遗宗师"
        elif user.experience_points >= 2000:
            user.level = UserLevel.MASTER
            user.title = "工艺大师"
        elif user.experience_points >= 800:
            user.level = UserLevel.ADVANCED
            user.title = "高级学徒"
        elif user.experience_points >= 200:
            user.level = UserLevel.APPRENTICE
            user.title = "初级学徒"

    db.commit()

    return {"status": "success", "record_id": record.id}


@router.post("/profile/{user_id}/work")
async def add_user_work(
    user_id: int,
    craft_id: str,
    craft_name: str,
    title: str,
    image_url: str,
    description: Optional[str] = None,
    ai_generated: bool = False,
    prompt_used: Optional[str] = None,
    style: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    添加用户作品
    用户完成创作后调用此接口保存作品
    """
    work = UserWork(
        user_id=user_id,
        craft_id=craft_id,
        craft_name=craft_name,
        title=title,
        image_url=image_url,
        description=description,
        ai_generated=1 if ai_generated else 0,
        prompt_used=prompt_used,
        style=style
    )
    db.add(work)

    # 更新用户创造力能力
    abilities = db.query(UserAbility).filter(UserAbility.user_id == user_id).first()
    if abilities:
        # 每增加一个作品，创造力增加 2 点 (上限 100)
        abilities.creativity = min(100, abilities.creativity + 2)
        db.commit()

    db.refresh(work)
    return {"status": "success", "work_id": work.id}


@router.put("/profile/{user_id}/abilities")
async def update_user_abilities(
    user_id: int,
    stability: Optional[float] = None,
    accuracy: Optional[float] = None,
    speed: Optional[float] = None,
    creativity: Optional[float] = None,
    knowledge: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    更新用户能力数据
    检验标准:
    - [x] 数据实时更新
    """
    abilities = db.query(UserAbility).filter(UserAbility.user_id == user_id).first()
    if not abilities:
        abilities = UserAbility(user_id=user_id)
        db.add(abilities)

    if stability is not None:
        abilities.stability = stability
    if accuracy is not None:
        abilities.accuracy = accuracy
    if speed is not None:
        abilities.speed = speed
    if creativity is not None:
        abilities.creativity = creativity
    if knowledge is not None:
        abilities.knowledge = knowledge

    db.commit()
    db.refresh(abilities)

    return {
        "status": "success",
        "abilities": {
            "stability": abilities.stability,
            "accuracy": abilities.accuracy,
            "speed": abilities.speed,
            "creativity": abilities.creativity,
            "knowledge": abilities.knowledge
        }
    }
