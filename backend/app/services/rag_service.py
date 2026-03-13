"""
RAG 服务 - 基于 Neo4j 知识图谱的检索增强生成
"""

from app.services.neo4j_service import neo4j_service
from app.services.llm_service import langchain_service
from typing import List, Dict, Any


class RAGService:
    """RAG 服务 - 结合知识图谱和 LLM"""

    def __init__(self):
        self.neo4j = neo4j_service
        self.llm = langchain_service

    def extract_keywords(self, query: str) -> List[str]:
        """
        从用户问题中提取关键词

        Args:
            query: 用户问题

        Returns:
            关键词列表
        """
        # 使用 LLM 提取关键词
        prompt = f"""从以下问题中提取 2-3 个关键名词或短语，用逗号分隔：

问题：{query}

直接输出关键词，不要其他内容："""

        try:
            response = self.llm.chat([{"role": "user", "content": prompt}])
            keywords = [kw.strip() for kw in response.split(',')]
            return keywords[:3]
        except Exception:
            # 降级：简单分词
            return [query]

    def search_knowledge_graph(self, keywords: List[str]) -> str:
        """
        在知识图谱中搜索相关信息

        Args:
            keywords: 关键词列表

        Returns:
            检索到的上下文文本
        """
        context_parts = []

        for keyword in keywords:
            # 策略 1：搜索匹配的节点（使用 name 属性）
            search_query = """
            MATCH (n)
            WHERE n.name CONTAINS $keyword
            OPTIONAL MATCH (n)-[r]-(related)
            RETURN n, type(r) as relation_type, related
            LIMIT 10
            """

            try:
                results = self.neo4j.query(search_query, {"keyword": keyword})
                print(f"Neo4j search results for '{keyword}': {results}")

                for result in results:
                    # 处理结果格式
                    if isinstance(result, tuple):
                        # 如果是元组格式，转换为字典
                        node = result[0] if len(result) > 0 else {}
                        relation_type = result[1] if len(result) > 1 else None
                        related = result[2] if len(result) > 2 else {}
                    else:
                        # 如果是字典格式
                        node = result.get('n', {})
                        related = result.get('related', {})
                        relation_type = result.get('relation_type', None)

                    # 构建节点信息
                    node_info = self._format_node_info(node)
                    if node_info:
                        context_parts.append(node_info)

                    # 添加关系信息
                    if related and (isinstance(related, dict) and related.get('name')):
                        related_name = related.get('name', '未知')
                        if relation_type:
                            context_parts.append(f"{node.get('name', '未知')} → {relation_type} → {related_name}")
                        else:
                            context_parts.append(f"相关：{related_name}")

            except Exception as e:
                print(f"Neo4j search error for keyword '{keyword}': {e}")
                import traceback
                traceback.print_exc()

        # 策略 2：如果没有搜索结果，根据节点类型搜索
        if not context_parts:
            # 检查是否询问流派
            if any(kw in keywords for kw in ['流派', '分类', '类型']):
                liupai_query = """
                MATCH (n:Heritage {name: "皮影戏"})-[:HAS_SCHOOL]-(school)
                RETURN school
                """
                try:
                    results = self.neo4j.query(liupai_query)
                    print(f"Liupai query results: {results}")
                    for result in results:
                        if isinstance(result, dict):
                            node = result.get('school', {})
                        elif isinstance(result, tuple):
                            node = result[0] if len(result) > 0 else {}
                        else:
                            node = result
                        node_info = self._format_node_info(node)
                        if node_info:
                            context_parts.append(node_info)
                except Exception as e:
                    print(f"Liupai search error: {e}")

            # 检查是否询问历史/起源
            if any(kw in keywords for kw in ['历史', '起源', '来源']):
                history_query = """
                MATCH (n:History)-[:HAS_PERIOD]-(period)
                RETURN n, period
                ORDER BY period.步骤序号
                """
                try:
                    results = self.neo4j.query(history_query)
                    history_info = []
                    for result in results:
                        if isinstance(result, dict):
                            period = result.get('period', {})
                        elif isinstance(result, tuple):
                            period = result[1] if len(result) > 1 else {}
                        else:
                            period = result
                        if period:
                            dynasty = period.get('朝代', '')
                            period_name = period.get('时期', '')
                            desc = period.get('描述', '')
                            if dynasty and desc:
                                history_info.append(f"{dynasty}（{period_name}）：{desc}")
                    if history_info:
                        context_parts.append("**皮影戏历史发展**\n" + "\n\n".join(history_info))
                except Exception as e:
                    print(f"History search error: {e}")

            # 检查是否询问传承人
            if any(kw in keywords for kw in ['传承人', '传人', '大师', '人']):
                inheritor_query = """
                MATCH (n:Heritage {name: "皮影戏"})-[:HAS_INHERITOR]-(person:Person)
                RETURN person
                """
                try:
                    results = self.neo4j.query(inheritor_query)
                    for result in results:
                        if isinstance(result, dict):
                            node = result.get('person', {})
                        elif isinstance(result, tuple):
                            node = result[0] if len(result) > 0 else {}
                        else:
                            node = result
                        node_info = self._format_node_info(node)
                        if node_info:
                            context_parts.append(node_info)
                except Exception as e:
                    print(f"Inheritor search error: {e}")

            # 检查是否询问剧目
            if any(kw in keywords for kw in ['剧目', '戏剧', '戏', '表演']):
                drama_query = """
                MATCH (n:Heritage {name: "皮影戏"})-[:HAS_DRAMA]-(drama)
                RETURN drama
                """
                try:
                    results = self.neo4j.query(drama_query)
                    for result in results:
                        if isinstance(result, dict):
                            node = result.get('drama', {})
                        elif isinstance(result, tuple):
                            node = result[0] if len(result) > 0 else {}
                        else:
                            node = result
                        node_info = self._format_node_info(node)
                        if node_info:
                            context_parts.append(node_info)
                except Exception as e:
                    print(f"Drama search error: {e}")

        # 策略 3：获取所有皮影戏相关实体作为后备
        if not context_parts:
            general_query = """
            MATCH (n)
            WHERE n.name CONTAINS '皮影' OR n.type IN ['非遗项目', 'Craft', '流派', '传承人', '工艺', '剧目']
            OPTIONAL MATCH (n)-[r]-(related)
            RETURN n, type(r) as relation_type, related
            LIMIT 20
            """
            try:
                results = self.neo4j.query(general_query)
                for result in results:
                    if isinstance(result, dict):
                        node = result.get('n', {})
                        related = result.get('related', {})
                        relation_type = result.get('relation_type', None)
                    elif isinstance(result, tuple):
                        node = result[0] if len(result) > 0 else {}
                        relation_type = result[1] if len(result) > 1 else None
                        related = result[2] if len(result) > 2 else {}
                    else:
                        continue

                    node_info = self._format_node_info(node)
                    if node_info:
                        context_parts.append(node_info)
            except Exception as e:
                print(f"General Neo4j search error: {e}")

        # 去重并返回
        unique_context = list(dict.fromkeys(context_parts))
        return "\n\n".join(unique_context) if unique_context else "未找到相关信息"

    def _format_node_info(self, node: Dict) -> str:
        """格式化节点信息"""
        if not node:
            return ""

        name = node.get('name', '未知')
        node_type = node.get('type', node.get('label', '实体'))
        description = node.get('description', '')

        # 收集其他属性
        other_attrs = {k: v for k, v in node.items()
                       if k not in ['name', 'type', 'label', 'description'] and v}

        info = f"**{name}** ({node_type})"
        if description:
            info += f"\n{description}"

        if other_attrs:
            for key, value in other_attrs.items():
                if isinstance(value, list):
                    info += f"\n{key}: {', '.join(value)}"
                elif value:
                    info += f"\n{key}: {value}"

        return info

    def _format_relation_info(self, node: Dict, relation: Dict, related: Dict) -> str:
        """格式化关系信息"""
        if not node or not related:
            return ""

        node_name = node.get('name', '未知')
        related_name = related.get('name', '未知')
        relation_type = relation.get('type', relation.get('label', '相关')) if relation else '相关'

        # 提取关系类型（去掉前缀）
        if isinstance(relation_type, str) and ':' in relation_type:
            relation_type = relation_type.split(':')[1]

        return f"{node_name} → {relation_type} → {related_name}"

    def query(self, question: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        完整的 RAG 查询流程

        Args:
            question: 用户问题
            conversation_history: 对话历史

        Returns:
            包含回答、追问选项等信息的字典
        """
        # 1. 提取关键词
        keywords = self.extract_keywords(question)
        print(f"Extracted keywords: {keywords}")

        # 2. 检索知识图谱
        kg_context = self.search_knowledge_graph(keywords)
        print(f"KG context length: {len(kg_context)}")

        # 3. 使用 LLM 生成回答和追问
        answer, follow_ups = self.llm.answer_with_context(
            question=question,
            kg_context=kg_context,
            conversation_history=conversation_history
        )

        # 4. 提取相关实体（用于前端展示）
        related_entities = self._extract_related_entities(kg_context)

        return {
            "answer": answer,
            "follow_up_questions": follow_ups,
            "related_entities": related_entities,
            "kg_context": kg_context,  # 调试用
            "keywords": keywords
        }

    def _extract_related_entities(self, context: str) -> List[str]:
        """从上下文中提取相关实体名称"""
        entities = []
        for line in context.split('\n'):
            if line.startswith('**') and '**' in line[2:]:
                entity = line.split('**')[1]
                if entity and entity not in entities:
                    entities.append(entity)
        return entities[:5]  # 最多返回 5 个


# 全局实例
rag_service = RAGService()
