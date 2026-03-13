from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

from app.services.rag_service import rag_service
from app.db.mysql_db import get_db, Conversation, FollowUpQuestion
from sqlalchemy.orm import Session

router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None  # 会话 ID，用于追踪对话历史


class QueryResponse(BaseModel):
    answer: str
    follow_up_questions: List[str]  # 追问选项
    related_entities: List[str]  # 相关实体
    session_id: str  # 返回会话 ID，用于后续追问


@router.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest, db: Session = Depends(get_db)):
    """
    知识图谱问答接口 - 基于 RAG 技术
    结合 Neo4j 知识图谱和 DeepSeek LLM

    请求示例:
    {
        "query": "苏绣的起源历史是什么？",
        "session_id": "user-123-session-456" (可选)
    }

    返回示例:
    {
        "answer": "苏绣起源于...",
        "follow_up_questions": ["苏绣有哪些针法？", "苏绣的代表传承人是谁？", "苏绣如何保护传承？"],
        "related_entities": ["苏绣", "乱针绣", "杨守玉"],
        "session_id": "user-123-session-456"
    }
    """
    query = request.query
    session_id = request.session_id

    # 如果没有提供 session_id，生成一个新的
    if not session_id:
        session_id = str(uuid.uuid4())

    try:
        # 1. 获取对话历史（最近 5 条）
        conversation_history = []
        past_conversations = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).order_by(Conversation.created_at.desc()).limit(5).all()

        if past_conversations:
            # 按时间正序排列
            past_conversations.reverse()
            for conv in past_conversations:
                conversation_history.append({"role": "user", "content": conv.user_query})
                conversation_history.append({"role": "assistant", "content": conv.agent_answer})

        # 2. 执行 RAG 查询
        result = rag_service.query(query, conversation_history)

        answer = result["answer"]
        follow_ups = result["follow_up_questions"]
        related_entities = result["related_entities"]

        # 3. 保存对话到数据库
        context_entities = ",".join(related_entities)
        new_conversation = Conversation(
            session_id=session_id,
            user_query=query,
            agent_answer=answer,
            context_entities=context_entities,
            created_at=datetime.utcnow()
        )
        db.add(new_conversation)
        db.flush()  # 获取 ID

        # 4. 保存追问选项
        for i, fq in enumerate(follow_ups):
            follow_up = FollowUpQuestion(
                conversation_id=new_conversation.id,
                question_text=fq,
                sort_order=i
            )
            db.add(follow_up)

        db.commit()

        return QueryResponse(
            answer=answer,
            follow_up_questions=follow_ups,
            related_entities=related_entities,
            session_id=session_id
        )

    except Exception as e:
        print(f"Query error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}")
async def get_session_history(session_id: str, db: Session = Depends(get_db)):
    """
    获取会话历史
    """
    conversations = db.query(Conversation).filter(
        Conversation.session_id == session_id
    ).order_by(Conversation.created_at.asc()).all()

    history = []
    for conv in conversations:
        history.append({
            "query": conv.user_query,
            "answer": conv.agent_answer,
            "created_at": conv.created_at.isoformat(),
            "follow_up_questions": [fq.question_text for fq in conv.follow_ups]
        })

    return {"session_id": session_id, "history": history}


@router.post("/follow-up")
async def submit_follow_up(
    conversation_id: int,
    follow_up_index: int,
    db: Session = Depends(get_db)
):
    """
    用户点击了追问选项，记录行为
    """
    follow_up = db.query(FollowUpQuestion).filter(
        FollowUpQuestion.id == follow_up_index,
        FollowUpQuestion.conversation_id == conversation_id
    ).first()

    if not follow_up:
        raise HTTPException(status_code=404, detail="Follow-up question not found")

    # 这里可以添加更多逻辑，比如统计追问点击率等
    return {"status": "success", "question": follow_up.question_text}


@router.get("/entities")
async def list_entities(db: Session = Depends(get_db)):
    """
    获取所有相关实体（用于前端自动补全或推荐）
    """
    # 从最近的对话中提取实体
    conversations = db.query(Conversation.context_entities).filter(
        Conversation.context_entities != ""
    ).limit(100).all()

    entity_count = {}
    for conv in conversations:
        if conv.context_entities:
            for entity in conv.context_entities.split(","):
                entity = entity.strip()
                if entity:
                    entity_count[entity] = entity_count.get(entity, 0) + 1

    # 按出现频率排序
    sorted_entities = sorted(entity_count.items(), key=lambda x: x[1], reverse=True)

    return {"entities": [e[0] for e in sorted_entities[:20]]}
