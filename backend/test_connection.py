from neo4j import GraphDatabase
import sys

uri = "bolt://localhost:7687"
user = "neo4j"
passwords_to_try = ["fusu2023yzcm", "password"]

def test_connection(password):
    driver = None
    try:
        print(f"Testing with password: '{password}'...")
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        print(f"SUCCESS: Connected to Neo4j at {uri} with password '{password}'")
        return True
    except Exception as e:
        print(f"FAILED with password '{password}': {e}")
        return False
    finally:
        if driver:
            driver.close()

success = False
for pwd in passwords_to_try:
    if test_connection(pwd):
        success = True
        break

if not success:
    print("All attempts failed.")
    sys.exit(1)
else:
    sys.exit(0)
