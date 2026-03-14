import requests
from bs4 import BeautifulSoup
import json
import time
import random
import os

# 定义目标非遗项目及其百科/相关链接 (示例，实际需根据可爬取的合法数据源调整)
# 注意：实际爬虫需遵守 robots.txt 协议。这里演示爬取百度百科的简介信息作为示例。
TARGETS = [
    {"name": "苏绣", "url": "https://baike.baidu.com/item/苏绣"},
    {"name": "紫砂壶", "url": "https://baike.baidu.com/item/紫砂壶"},
    {"name": "剪纸", "url": "https://baike.baidu.com/item/中国剪纸"},
    {"name": "蜡染", "url": "https://baike.baidu.com/item/蜡染"},
    {"name": "皮影戏", "url": "https://baike.baidu.com/item/皮影戏"},
    {"name": "景泰蓝", "url": "https://baike.baidu.com/item/景泰蓝"},
    {"name": "昆曲", "url": "https://baike.baidu.com/item/昆曲"},
    {"name": "木版年画", "url": "https://baike.baidu.com/item/木版年画"}
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def fetch_baike_data(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"Failed to fetch {url}: Status code {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取标题
        title = soup.find('h1').get_text().strip() if soup.find('h1') else "Unknown"
        
        # 提取简介 (通常在 meta description 或 summary div 中)
        summary = ""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            summary = meta_desc['content']
        else:
            # 尝试找 summary div (百度百科结构变动较快，这里做简单适配)
            summary_div = soup.find('div', class_='lemma-summary')
            if summary_div:
                summary = summary_div.get_text().strip()
        
        # 提取基本属性 (如：申报地区、遗产类别等)
        attributes = {}
        basic_info = soup.find('div', class_='basic-info')
        if basic_info:
            dls = basic_info.find_all('dl')
            for dl in dls:
                dts = dl.find_all('dt')
                dds = dl.find_all('dd')
                for dt, dd in zip(dts, dds):
                    key = dt.get_text().strip().replace('\xa0', '')
                    value = dd.get_text().strip()
                    attributes[key] = value
                    
        return {
            "title": title,
            "url": url,
            "summary": summary,
            "attributes": attributes
        }

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    results = []
    print("Starting crawler for ICH (Intangible Cultural Heritage) data...")
    
    for target in TARGETS:
        print(f"Fetching data for: {target['name']}...")
        data = fetch_baike_data(target['url'])
        
        if data:
            # 简单的清洗
            if not data['summary']:
                data['summary'] = "暂无简介数据"
            
            results.append(data)
            print(f"Successfully fetched: {data['title']}")
        else:
            # 如果爬取失败，使用模拟数据填充，确保有数据可用
            print(f"Using mock data for {target['name']}")
            results.append({
                "title": target['name'],
                "url": target['url'],
                "summary": f"{target['name']}是中国传统非物质文化遗产的重要代表之一。此处为模拟数据，因为爬虫未能获取实时信息。",
                "attributes": {"类别": "传统技艺/美术", "地区": "中国"}
            })
            
        # 随机延时，礼貌爬取
        time.sleep(random.uniform(1, 3))
    
    # 保存结果
    output_file = 'ich_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
        
    print(f"\nCrawling finished. Data saved to {os.path.abspath(output_file)}")
    print(f"Total records: {len(results)}")

if __name__ == "__main__":
    main()
