import json
from collections import defaultdict

# 假设你的JSON数据存储在一个文件中
json_file = '../../team_predict/AMiner/data_process/AMiner-Citation_2014_2024.json'
venue_mapping_file = '../../team_predict/AMiner/data_process/venue_id_mapping.txt'
output_file = 'journal_stats.txt'

# 读取映射表
venue_id_mapping = {}
with open(venue_mapping_file, 'r') as f:
    for line in f:
        print(line)
        venue_name, venue_id = line.strip().split(' && ')
        venue_id_mapping[venue_name] = venue_id

# 读取JSON数据
with open(json_file, 'r') as f:
    data = json.load(f)

# 初始化字典来存储期刊统计信息
journal_citations = defaultdict(int)
journal_paper_count = defaultdict(int)

# 处理每篇论文
for paper in data:
    venue = paper.get('venue', '')
    citations = paper.get('n_citation', 0)

    # 使用映射表将 venue 名字转换为编号
    venue_id = venue_id_mapping.get(venue)

    if venue_id:
        journal_citations[venue_id] += citations
        journal_paper_count[venue_id] += 1

# 保存结果到文件
with open(output_file, 'w') as f:
    for venue_id, total_citations in journal_citations.items():
        paper_count = journal_paper_count[venue_id]
        f.write(f"{venue_id} {total_citations} {paper_count}\n")

print(f"Journal statistics have been saved to {output_file}")
