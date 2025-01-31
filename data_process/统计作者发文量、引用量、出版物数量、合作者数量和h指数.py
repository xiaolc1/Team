import json
from collections import defaultdict

# 假设你的JSON数据存储在一个文件中
json_file = '../../team_predict/AMiner/data_process/AMiner-Citation_2014_2024.json'
output_file = '../../team_predict/AMiner/data_process/author_stats.txt'

# 读取JSON数据
with open(json_file, 'r') as f:
    data = json.load(f)

# 初始化字典来存储统计信息
author_publications = defaultdict(int)
author_citations = defaultdict(int)
author_paper_citations = defaultdict(list)
author_collaborators = defaultdict(set)
author_venues = defaultdict(set)

# 处理每篇论文
for paper in data:
    paper_id = paper['id']
    citations = paper.get('n_citation', 0)
    venue = paper.get('venue', '')

    authors = paper['authors']
    author_ids = [author['id'] for author in authors if author['id']]

    for author_id in author_ids:
        author_publications[author_id] += 1
        author_citations[author_id] += citations
        author_paper_citations[author_id].append(citations)
        author_venues[author_id].add(venue)

        for coauthor_id in author_ids:
            if coauthor_id != author_id:
                author_collaborators[author_id].add(coauthor_id)

# 计算每个作者的h指数
def calculate_h_index(citations):
    citations.sort(reverse=True)
    h = 0
    for i, c in enumerate(citations):
        if c >= i + 1:
            h = i + 1
        else:
            break
    return h

author_h_index = {author: calculate_h_index(citations) for author, citations in author_paper_citations.items()}

# 保存结果到文件
with open(output_file, 'w') as f:
    for author_id in author_publications:
        publications = author_publications[author_id]
        citations = author_citations[author_id]
        h_index = author_h_index[author_id]
        num_collaborators = len(author_collaborators[author_id])
        num_venues = len(author_venues[author_id])
        f.write(f"{author_id} {publications} {citations} {h_index} {num_collaborators} {num_venues}\n")

print(f"Author statistics have been saved to {output_file}")
