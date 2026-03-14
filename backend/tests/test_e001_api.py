"""
E-001 API 端点测试脚本
测试用户档案系统的 API 端点功能
"""

import requests
import sys

# API 基础 URL
BASE_URL = "http://localhost:8002/api/v1/user"


def test_api():
    """测试所有用户档案 API 端点"""
    print("=" * 60)
    print("E-001 API 端点测试")
    print("=" * 60)
    print(f"API 基础 URL: {BASE_URL}")
    print("=" * 60)

    all_passed = True

    try:
        # 1. 测试创建用户
        print("\n[Test 1] 创建用户 POST /users")
        response = requests.post(f"{BASE_URL}/users", params={"name": "测试用户", "level": 1})
        if response.status_code == 200:
            user = response.json()
            user_id = user["id"]
            print(f"  [OK] 创建用户成功：id={user_id}, name={user['name']}")
        else:
            print(f"  [FAIL] 创建用户失败：{response.status_code}")
            all_passed = False
            return all_passed

        # 2. 测试获取用户
        print("\n[Test 2] 获取用户 GET /users/{user_id}")
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        if response.status_code == 200:
            print(f"  [OK] 获取用户成功：{response.json()}")
        else:
            print(f"  [FAIL] 获取用户失败：{response.status_code}")
            all_passed = False

        # 3. 测试更新用户
        print("\n[Test 3] 更新用户 PUT /users/{user_id}")
        response = requests.put(f"{BASE_URL}/users/{user_id}", params={"level": 5})
        if response.status_code == 200:
            print(f"  [OK] 更新用户成功：level={response.json()['level']}")
        else:
            print(f"  [FAIL] 更新用户失败：{response.status_code}")
            all_passed = False

        # 4. 测试创建学习记录
        print("\n[Test 4] 创建学习记录 POST /users/{user_id}/practice-logs")
        response = requests.post(
            f"{BASE_URL}/users/{user_id}/practice-logs",
            params={"craft_id": 101, "craft_name": "苏绣", "duration": 1800, "score": 85.5}
        )
        if response.status_code == 200:
            log = response.json()
            log_id = log["id"]
            print(f"  [OK] 创建学习记录成功：id={log_id}, craft_name={log['craft_name']}")
        else:
            print(f"  [FAIL] 创建学习记录失败：{response.status_code}")
            all_passed = False

        # 5. 测试获取学习记录
        print("\n[Test 5] 获取学习记录 GET /users/{user_id}/practice-logs")
        response = requests.get(f"{BASE_URL}/users/{user_id}/practice-logs")
        if response.status_code == 200:
            logs = response.json()
            print(f"  [OK] 获取学习记录成功：共 {len(logs)} 条记录")
        else:
            print(f"  [FAIL] 获取学习记录失败：{response.status_code}")
            all_passed = False

        # 6. 测试获取学习统计
        print("\n[Test 6] 获取学习统计 GET /users/{user_id}/practice-stats")
        response = requests.get(f"{BASE_URL}/users/{user_id}/practice-stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"  [OK] 获取学习统计成功:")
            print(f"       - 总时长：{stats['total_duration_minutes']} 分钟")
            print(f"       - 总次数：{stats['total_sessions']}")
            print(f"       - 平均分：{stats['average_score']}")
        else:
            print(f"  [FAIL] 获取学习统计失败：{response.status_code}")
            all_passed = False

        # 7. 测试创建作品
        print("\n[Test 7] 创建作品 POST /users/{user_id}/portfolios")
        response = requests.post(
            f"{BASE_URL}/users/{user_id}/portfolios",
            params={"image_url": "/images/test.jpg", "craft_type": "苏绣", "description": "测试作品"}
        )
        if response.status_code == 200:
            portfolio = response.json()
            portfolio_id = portfolio["id"]
            print(f"  [OK] 创建作品成功：id={portfolio_id}, craft_type={portfolio['craft_type']}")
        else:
            print(f"  [FAIL] 创建作品失败：{response.status_code}")
            all_passed = False

        # 8. 测试获取作品集
        print("\n[Test 8] 获取作品集 GET /users/{user_id}/portfolios")
        response = requests.get(f"{BASE_URL}/users/{user_id}/portfolios")
        if response.status_code == 200:
            portfolios = response.json()
            print(f"  [OK] 获取作品集成功：共 {len(portfolios)} 个作品")
        else:
            print(f"  [FAIL] 获取作品集失败：{response.status_code}")
            all_passed = False

        # 9. 测试获取用户完整档案
        print("\n[Test 9] 获取用户完整档案 GET /users/{user_id}/profile")
        response = requests.get(f"{BASE_URL}/users/{user_id}/profile")
        if response.status_code == 200:
            profile = response.json()
            print(f"  [OK] 获取用户档案成功:")
            print(f"       - 用户：{profile['user']['name']} (等级 {profile['user']['level']})")
            print(f"       - 统计：{profile['stats']['total_sessions']} 次练习")
            print(f"       - 作品：{profile['portfolio_count']} 个")
        else:
            print(f"  [FAIL] 获取用户档案失败：{response.status_code}")
            all_passed = False

        # 10. 测试删除作品
        print("\n[Test 10] 删除作品 DELETE /portfolios/{portfolio_id}")
        response = requests.delete(f"{BASE_URL}/portfolios/{portfolio_id}")
        if response.status_code == 200:
            print(f"  [OK] 删除作品成功")
        else:
            print(f"  [FAIL] 删除作品失败：{response.status_code}")
            all_passed = False

        # 11. 测试删除用户
        print("\n[Test 11] 删除用户 DELETE /users/{user_id}")
        response = requests.delete(f"{BASE_URL}/users/{user_id}")
        if response.status_code == 200:
            print(f"  [OK] 删除用户成功（级联删除学习记录和作品）")
        else:
            print(f"  [FAIL] 删除用户失败：{response.status_code}")
            all_passed = False

        # 验证用户已被删除
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        if response.status_code == 404:
            print(f"  [OK] 验证：用户已被删除")
        else:
            print(f"  [FAIL] 验证：用户删除失败")
            all_passed = False

    except requests.exceptions.ConnectionError:
        print("\n[ERROR] 无法连接到 API 服务器")
        print("请确保后端服务正在运行：python run.py")
        all_passed = False
    except Exception as e:
        print(f"\n[ERROR] 测试执行出错：{e}")
        all_passed = False

    # 输出测试结果
    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] 所有 API 测试通过！")
    else:
        print("[FAILURE] 部分测试失败")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
