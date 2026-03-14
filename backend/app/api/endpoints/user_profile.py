"""
用户档案系统 API
提供用户管理、学习记录、作品集等功能
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.mysql_db import User, PracticeLog, Portfolio, get_db
from pydantic import BaseModel
from datetime import datetime

# Pydantic 模型用于响应序列化
class UserBase(BaseModel):
    id: int
    name: str
    level: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    level: int = 1

class UserUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None

router = APIRouter()


# ============== 用户管理 ==============

@router.get("/users", response_model=List[dict])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取所有用户列表"""
    users = db.query(User).offset(skip).limit(limit).all()
    return [{"id": u.id, "name": u.name, "level": u.level, "created_at": u.created_at} for u in users]


@router.get("/users/{user_id}", response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """获取单个用户详情"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"id": user.id, "name": user.name, "level": user.level, "created_at": user.created_at}


@router.post("/users", response_model=dict)
def create_user(name: str, level: int = 1, db: Session = Depends(get_db)):
    """创建新用户"""
    user = User(name=name, level=level)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name, "level": user.level, "created_at": user.created_at}


@router.put("/users/{user_id}", response_model=dict)
def update_user(user_id: int, name: Optional[str] = None, level: Optional[int] = None, db: Session = Depends(get_db)):
    """更新用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    if name is not None:
        user.name = name
    if level is not None:
        user.level = level

    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name, "level": user.level, "created_at": user.created_at}


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """删除用户（级联删除学习记录和作品）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    db.delete(user)
    db.commit()
    return {"message": "用户已删除"}


# ============== 学习记录管理 ==============

@router.get("/users/{user_id}/practice-logs", response_model=List[dict])
def get_user_practice_logs(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取用户的学习记录"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    logs = db.query(PracticeLog).filter(PracticeLog.user_id == user_id).offset(skip).limit(limit).all()
    return [{"id": log.id, "user_id": log.user_id, "craft_id": log.craft_id, "craft_name": log.craft_name, "duration": log.duration, "score": log.score, "created_at": log.created_at} for log in logs]


@router.post("/users/{user_id}/practice-logs", response_model=dict)
def create_practice_log(
    user_id: int,
    craft_id: int,
    craft_name: str,
    duration: Optional[int] = None,
    score: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """创建学习记录"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    log = PracticeLog(
        user_id=user_id,
        craft_id=craft_id,
        craft_name=craft_name,
        duration=duration,
        score=score
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return {"id": log.id, "user_id": log.user_id, "craft_id": log.craft_id, "craft_name": log.craft_name, "duration": log.duration, "score": log.score, "created_at": log.created_at}


@router.get("/users/{user_id}/practice-stats", response_model=dict)
def get_user_practice_stats(user_id: int, db: Session = Depends(get_db)):
    """获取用户学习统计"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    logs = db.query(PracticeLog).filter(PracticeLog.user_id == user_id).all()

    total_duration = sum(log.duration or 0 for log in logs)
    total_sessions = len(logs)
    avg_score = sum(log.score or 0 for log in logs) / total_sessions if total_sessions > 0 else 0
    crafts_practiced = len(set(log.craft_id for log in logs))

    return {
        "user_id": user_id,
        "total_duration_seconds": total_duration,
        "total_duration_minutes": round(total_duration / 60, 2),
        "total_sessions": total_sessions,
        "average_score": round(avg_score, 2),
        "crafts_practiced": crafts_practiced
    }


# ============== 作品集管理 ==============

@router.get("/users/{user_id}/portfolios", response_model=List[dict])
def get_user_portfolios(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取用户的作品集"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    portfolios = db.query(Portfolio).filter(Portfolio.user_id == user_id).offset(skip).limit(limit).all()
    return [{"id": p.id, "user_id": p.user_id, "image_url": p.image_url, "craft_type": p.craft_type, "description": p.description, "created_at": p.created_at} for p in portfolios]


@router.post("/users/{user_id}/portfolios", response_model=dict)
def create_portfolio(
    user_id: int,
    image_url: str,
    craft_type: Optional[str] = None,
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """创建作品"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    portfolio = Portfolio(
        user_id=user_id,
        image_url=image_url,
        craft_type=craft_type,
        description=description
    )
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return {"id": portfolio.id, "user_id": portfolio.user_id, "image_url": portfolio.image_url, "craft_type": portfolio.craft_type, "description": portfolio.description, "created_at": portfolio.created_at}


@router.delete("/portfolios/{portfolio_id}")
def delete_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    """删除作品"""
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="作品不存在")

    db.delete(portfolio)
    db.commit()
    return {"message": "作品已删除"}


# ============== 用户完整档案 ==============

@router.get("/users/{user_id}/profile", response_model=dict)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """获取用户完整档案（包含基本信息、学习统计、作品集）"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 获取学习统计
    logs = db.query(PracticeLog).filter(PracticeLog.user_id == user_id).all()
    total_duration = sum(log.duration or 0 for log in logs)
    total_sessions = len(logs)
    avg_score = sum(log.score or 0 for log in logs) / total_sessions if total_sessions > 0 else 0
    crafts_practiced = len(set(log.craft_id for log in logs))

    # 获取作品集
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "level": user.level,
            "created_at": user.created_at
        },
        "stats": {
            "total_duration_seconds": total_duration,
            "total_duration_minutes": round(total_duration / 60, 2),
            "total_sessions": total_sessions,
            "average_score": round(avg_score, 2),
            "crafts_practiced": crafts_practiced
        },
        "portfolios": [{"id": p.id, "user_id": p.user_id, "image_url": p.image_url, "craft_type": p.craft_type, "description": p.description, "created_at": p.created_at} for p in portfolios],
        "portfolio_count": len(portfolios)
    }
