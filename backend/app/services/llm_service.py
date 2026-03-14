"""
LangChain LLM 服务封装
支持 DeepSeek 模型调用
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from app.core.config import settings

class LangChainService:
    """LangChain LLM 服务"""

    def __init__(self):
        """初始化 LLM"""
        try:
            self.llm = ChatOpenAI(
                model_name=settings.DEEPSEEK_MODEL,
                openai_api_key=settings.DEEPSEEK_API_KEY,
                openai_api_base=settings.DEEPSEEK_BASE_URL,
                temperature=0.7,
                max_tokens=1024
            )
            print("LangChain LLM initialized successfully with DeepSeek")
        except Exception as e:
            print(f"Failed to initialize LangChain LLM: {e}")
            self.llm = None

    def chat(self, messages: list, system_prompt: str = None) -> str:
        """
        进行对话

        Args:
            messages: 消息历史列表，每个元素为 {"role": "user|assistant", "content": "消息内容"}
            system_prompt: 系统提示词

        Returns:
            AI 回复的消息
        """
        if not self.llm:
            return "抱歉，AI 服务暂时不可用。"

        langchain_messages = []

        # 添加系统提示
        if system_prompt:
            langchain_messages.append(SystemMessage(content=system_prompt))

        # 添加历史消息
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        try:
            response = self.llm.invoke(langchain_messages)
            return response.content
        except Exception as e:
            print(f"LLM chat error: {e}")
            return "抱歉，我现在无法回答您的问题，请稍后再试。"

    def generate_follow_up_questions(self, context: str, user_query: str, answer: str) -> list:
        """
        根据上下文生成三个追问选项

        Args:
            context: 上下文信息（知识图谱检索结果）
            user_query: 用户问题
            answer: AI 回答

        Returns:
            追问问题列表（最多 3 个）
        """
        prompt = f"""你是一个非遗文化知识助手的追问生成器。根据以下对话内容，生成 3 个用户可能感兴趣的追问问题。

上下文信息：
{context}

用户问题：{user_query}

助手回答：{answer}

请生成 3 个相关的追问问题，要求：
1. 问题应该与上下文和回答相关
2. 问题应该具体、明确
3. 问题应该是用户可能真正想知道的
4. 每个问题控制在 30 字以内

直接输出 3 个问题，用 | 分隔，不要输出其他内容。"""

        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            questions = [q.strip() for q in response.content.split('|') if q.strip()]
            return questions[:3]  # 只返回前 3 个
        except Exception as e:
            print(f"Generate follow-up questions error: {e}")
            # 返回默认追问
            return [
                "这个技艺的历史起源是什么？",
                "有哪些代表性的传承人？",
                "现代如何保护和发展这项技艺？"
            ]

    def answer_with_context(self, question: str, kg_context: str, conversation_history: list = None) -> tuple:
        """
        基于知识图谱上下文回答问题

        Args:
            question: 用户问题
            kg_context: 知识图谱检索到的上下文
            conversation_history: 对话历史

        Returns:
            (回答，追问问题列表)
        """
        system_prompt = """你是一位非遗文化知识馆长，博学且友善。你的职责是根据提供的知识图谱信息回答用户关于非物质文化遗产的问题。

回答规则：
1. 基于提供的知识图谱信息回答，不要编造信息
2. 如果知识图谱中没有相关信息，诚实地告诉用户
3. 回答要清晰、详细，但不要过于冗长（200-300 字为宜）
4. 保持友善、专业的语气
5. 适当引导用户了解更多细节"""

        # 构建上下文消息
        context_message = f"""以下是从知识图谱中检索到的相关信息：

{kg_context}

如果上述信息中没有包含用户问题的答案，请诚实地告知用户。"""

        # 构建消息历史
        messages = []

        # 如果有对话历史，添加前几条
        if conversation_history:
            for msg in conversation_history[-4:]:  # 只保留最近 4 条消息
                messages.append(msg)

        # 添加当前问题的上下文
        messages.append({"role": "user", "content": f"{context_message}\n\n用户问题：{question}"})

        # 获取回答
        answer = self.chat(messages, system_prompt)

        # 生成追问问题
        follow_ups = self.generate_follow_up_questions(kg_context, question, answer)

        return answer, follow_ups


# 全局实例
langchain_service = LangChainService()
