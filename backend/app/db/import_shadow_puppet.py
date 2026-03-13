# -*- coding: utf-8 -*-
"""
皮影戏数据导入 Neo4j 知识图谱脚本
"""

import json
import sys
import os

# Ensure the backend directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from app.services.neo4j_service import neo4j_service

def load_json_data():
    """加载皮影戏 JSON 数据"""
    json_path = os.path.join(os.path.dirname(__file__), "../../../shadow_puppet_raw.json")
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def import_shadow_puppet_data():
    """导入皮影戏数据到 Neo4j"""
    print("开始导入皮影戏数据到 Neo4j...")

    data = load_json_data()

    # 1. 创建皮影戏主节点
    print("\n[1] 创建皮影戏主节点...")
    main_query = """
    MERGE (shadow:Heritage {name: "皮影戏", type: "Craft"})
    SET shadow.description = "皮影戏是中国古老的民间传统艺术，用灯光照射兽皮或纸板制作的人物剪影来表演故事。2006 年列入国家级非物质文化遗产，2011 年入选联合国教科文组织人类非物质文化遗产代表作名录。",
        shadow.aliases = $aliases,
        shadow.非遗级别 = $level,
        shadow.入选时间 = $time,
        shadow.非遗编号 = $number,
        shadow.世界非遗 = $world_heritage
    RETURN shadow
    """
    neo4j_service.query(main_query, {
        "aliases": data["基本信息"]["别名"],
        "level": data["基本信息"]["非遗级别"],
        "time": data["基本信息"]["入选时间"],
        "number": data["基本信息"]["非遗编号"],
        "world_heritage": "是"
    })
    print("[OK] 皮影戏主节点创建完成")

    # 2. 创建历史起源节点
    print("\n[2] 创建历史起源节点...")
    history_query = """
    MATCH (shadow:Heritage {name: "皮影戏"})
    MERGE (history:History {name: "皮影戏历史"})
    SET history.起源时间 = $origin_time,
        history.起源地点 = $origin_place,
        history.发源地 = $origin_source
    CREATE (shadow)-[:HAS_HISTORY]->(history)
    RETURN history
    """
    neo4j_service.query(history_query, {
        "origin_time": data["历史起源"]["起源时间"],
        "origin_place": data["历史起源"]["起源地点"],
        "origin_source": data["历史起源"]["发源地"]
    })
    print("[OK] 历史起源节点创建完成")

    # 3. 创建发展历程节点
    print("\n[3] 创建发展历程节点...")
    for period in data["历史起源"]["发展历程"]:
        period_query = """
        MATCH (history:History {name: "皮影戏历史"})
        MERGE (p:Period {name: $period_name})
        SET p.朝代 = $dynasty,
            p.时期 = $period,
            p.描述 = $description
        CREATE (history)-[:HAS_PERIOD]->(p)
        RETURN p
        """
        neo4j_service.query(period_query, {
            "period_name": f"{period['朝代']}-{period['时期']}",
            "dynasty": period["朝代"],
            "period": period["时期"],
            "description": period["描述"]
        })
    print(f"[OK] 已创建 {len(data['历史起源']['发展历程'])} 个历史时期节点")

    # 4. 创建主要流派节点
    print("\n[4] 创建主要流派节点...")
    for liupai in data["流派分类"]["主要流派"]:
        liupai_query = """
        MATCH (shadow:Heritage {name: "皮影戏"})
        MERGE (l:School {name: $name})
        SET l.代表地区 = $regions,
            l.特点 = $features,
            l.代表剧目 = $plays
        CREATE (shadow)-[:HAS_SCHOOL]->(l)
        RETURN l
        """
        neo4j_service.query(liupai_query, {
            "name": liupai["名称"],
            "regions": liupai["代表地区"],
            "features": liupai["特点"],
            "plays": liupai.get("代表剧目", [])
        })
    print(f"[OK] 已创建 {len(data['流派分类']['主要流派'])} 个流派节点")

    # 5. 创建制作工艺节点
    print("\n[5] 创建制作工艺节点...")

    # 将造型特点的字典转换为字符串
    features_str = "\n".join([f"{k}: {v}" for k, v in data["制作工艺"]["造型特点"].items()])

    craft_query = """
    MATCH (shadow:Heritage {name: "皮影戏"})
    MERGE (craft:Craft {name: "皮影制作工艺"})
    SET craft.造型特点 = $features
    CREATE (shadow)-[:HAS_CRAFT]->(craft)
    RETURN craft
    """
    neo4j_service.query(craft_query, {
        "features": features_str
    })

    # 创建各制作步骤节点
    for step in data["制作工艺"]["制作流程"]:
        step_query = """
        MATCH (craft:Craft {name: "皮影制作工艺"})
        MERGE (s:Step {name: $step_name})
        SET s.步骤序号 = $step_num,
            s.说明 = $description,
            s.要点 = $points
        CREATE (craft)-[:HAS_STEP]->(s)
        RETURN s
        """
        neo4j_service.query(step_query, {
            "step_name": step["名称"],
            "step_num": step["步骤"],
            "description": step["说明"],
            "points": step.get("要点", [])
        })
    print(f"[OK] 已创建 {len(data['制作工艺']['制作流程'])} 个制作步骤节点")

    # 6. 创建表演技法节点
    print("\n[6] 创建表演技法节点...")
    performance_query = """
    MATCH (shadow:Heritage {name: "皮影戏"})
    MERGE (perf:Performance {name: "皮影表演技法"})
    CREATE (shadow)-[:HAS_PERFORMANCE]->(perf)
    RETURN perf
    """
    neo4j_service.query(performance_query)

    # 创建操纵技法节点
    for tech in data["表演技法"]["操纵技法"]:
        tech_query = """
        MATCH (perf:Performance {name: "皮影表演技法"})
        MERGE (t:Technique {name: $name})
        SET t.说明 = $description
        CREATE (perf)-[:HAS_TECHNIQUE]->(t)
        RETURN t
        """
        neo4j_service.query(tech_query, {
            "name": tech["名称"],
            "description": tech["说明"]
        })
    print(f"[OK] 已创建 {len(data['表演技法']['操纵技法'])} 个操纵技法节点")

    # 7. 创建传承人节点
    print("\n[7] 创建传承人节点...")
    for inheritor in data["代表传承人"]:
        inheritor_query = """
        MATCH (shadow:Heritage {name: "皮影戏"})
        MERGE (p:Person {name: $name})
        SET p.流派 = $school,
            p.级别 = $level,
            p.简介 = $intro,
            p.type = "传承人"
        CREATE (shadow)-[:HAS_INHERITOR]->(p)
        RETURN p
        """
        neo4j_service.query(inheritor_query, {
            "name": inheritor["姓名"],
            "school": inheritor["流派"],
            "level": inheritor["级别"],
            "intro": inheritor["简介"]
        })
    print(f"[OK] 已创建 {len(data['代表传承人'])} 个传承人节点")

    # 8. 创建经典剧目节点
    print("\n[8] 创建经典剧目节点...")
    for play in data["经典剧目"]:
        play_query = """
        MATCH (shadow:Heritage {name: "皮影戏"})
        MERGE (play:Drama {name: $name})
        SET play.类型 = $type,
            play.流派 = $school,
            play.简介 = $intro
        CREATE (shadow)-[:HAS_DRAMA]->(play)
        RETURN play
        """
        neo4j_service.query(play_query, {
            "name": play["剧名"],
            "type": play["类型"],
            "school": play["流派"],
            "intro": play["简介"]
        })
    print(f"[OK] 已创建 {len(data['经典剧目'])} 个剧目节点")

    # 9. 创建工具/道具节点
    print("\n[9] 创建设备道具节点...")
    equipment_query = """
    MATCH (shadow:Heritage {name: "皮影戏"})
    MERGE (equip:Equipment {name: "皮影表演设备"})
    SET equip.影窗 = "白色半透明幕布",
        equip.灯光 = "传统用油灯蜡烛，现代用电灯",
        equip.乐器 = ["二胡", "板胡", "锣鼓", "铙钹", "唢呐", "笛子"]
    CREATE (shadow)-[:HAS_EQUIPMENT]->(equip)
    RETURN equip
    """
    neo4j_service.query(equipment_query)
    print("[OK] 设备道具节点创建完成")

    print("\n" + "=" * 60)
    print("皮影戏数据导入完成！")
    print("=" * 60)
    print("\n数据概览:")
    print(f"  - 流派数量：{len(data['流派分类']['主要流派'])}")
    print(f"  - 制作步骤：{len(data['制作工艺']['制作流程'])}")
    print(f"  - 操纵技法：{len(data['表演技法']['操纵技法'])}")
    print(f"  - 传承人：{len(data['代表传承人'])}")
    print(f"  - 经典剧目：{len(data['经典剧目'])}")

if __name__ == "__main__":
    try:
        import_shadow_puppet_data()
    except Exception as e:
        print(f"导入失败：{e}")
        import traceback
        traceback.print_exc()
    finally:
        neo4j_service.close()
