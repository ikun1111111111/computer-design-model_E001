import sys
import os

# Ensure the backend directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from app.services.neo4j_service import neo4j_service

def seed_data():
    print("Starting data seeding...")

    # Clear existing data
    delete_query = "MATCH (n) DETACH DELETE n"
    neo4j_service.query(delete_query)
    print("Cleared existing database.")

    # Create Heritage Items
    create_heritage_query = """
    // Create Heritage Items
    CREATE (su:Heritage {name: "苏绣", type: "Craft", description: "苏绣是苏州地区刺绣产品的总称，其发源地在苏州吴县一带，现已遍衍无锡、常州等地。刺绣与养蚕，缫丝分不开，所以刺绣，又称丝绣。"})
    CREATE (zi:Heritage {name: "紫砂", type: "Craft", description: "紫砂壶是中国特有的手工制造陶土工艺品，其制作始于明朝正德年间，原产地在江苏宜兴丁蜀镇。"})
    CREATE (shadow:Heritage {name: "皮影戏", type: "Craft", description: "皮影戏是中国古老的民间传统艺术，用灯光照射兽皮或纸板制作的人物剪影来表演故事。2006 年列入国家级非物质文化遗产，2011 年入选联合国教科文组织人类非物质文化遗产代表作名录。"})

    // Create Techniques for 苏绣
    CREATE (luan:Technique {name: "乱针绣", description: "打破传统刺绣"密接其针、排比其线"的规律，运用长短交叉的线条，分层加色。"})
    CREATE (ping:Technique {name: "平针绣", description: "苏绣中最基础的针法，线条排列整齐，平顺光滑。"})

    // Create Techniques for 紫砂
    CREATE (pai:Technique {name: "拍泥片", description: "紫砂壶成型的重要工序，通过拍打使泥片厚度均匀，结构致密。"})

    // Create Techniques for 皮影戏
    CREATE (shadow_craft:Technique {name: "皮影制作工艺", description: "皮影制作需要经过选皮、制皮、画稿、过稿、雕刻、上色、上油、组装等 9 道工序。"})
    CREATE (shadow_tech:Technique {name: "皮影操纵技法", description: "演员用三根竹签操纵影人，一根在颈部控制身体，两根在双手控制手臂动作。"})

    // Create People
    CREATE (yang:Person {name: "杨守玉", description: "近代刺绣大师，乱针绣创始人。"})
    CREATE (lin:Person {name: "林徽音", description: "国家级苏绣传承人 (虚拟角色)。"})
    CREATE (chen:Person {name: "陈曼生", description: "清代紫砂壶艺大师，提倡文人壶。"})

    // Create 皮影戏传承人
    CREATE (wei:Person {name: "魏金全", description: "唐山皮影国家级非遗传承人，从事皮影艺术 60 余年，技艺精湛。"})
    CREATE (zhang:Person {name: "张树山", description: "陕西华县皮影国家级非遗传承人，皮影世家传人。"})
    CREATE (wang:Person {name: "汪天稳", description: "陕西皮影艺术大师，雕刻技艺精湛，作品被多家博物馆收藏。"})

    // Create Relationships for 苏绣
    CREATE (su)-[:HAS_TECHNIQUE]->(luan)
    CREATE (su)-[:HAS_TECHNIQUE]->(ping)
    CREATE (yang)-[:INVENTED]->(luan)
    CREATE (yang)-[:MASTER_OF]->(su)
    CREATE (lin)-[:MASTER_OF]->(su)

    // Create Relationships for 紫砂
    CREATE (zi)-[:HAS_TECHNIQUE]->(pai)
    CREATE (chen)-[:MASTER_OF]->(zi)

    // Create Relationships for 皮影戏
    CREATE (shadow)-[:HAS_TECHNIQUE]->(shadow_craft)
    CREATE (shadow)-[:HAS_TECHNIQUE]->(shadow_tech)
    CREATE (wei)-[:MASTER_OF]->(shadow)
    CREATE (zhang)-[:MASTER_OF]->(shadow)
    CREATE (wang)-[:MASTER_OF]->(shadow)

    RETURN su, zi, shadow, luan, ping, pai, shadow_craft, shadow_tech, yang, lin, chen, wei, zhang, wang
    """

    try:
        neo4j_service.query(create_heritage_query)
        print("Data seeded successfully!")
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        neo4j_service.close()

if __name__ == "__main__":
    seed_data()
