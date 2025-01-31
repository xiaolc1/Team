import json
import pandas as pd
import numpy as np
import networkx as nx


# 读取论文数据
def load_paper_data(file_path):
    with open(file_path, 'r') as f:
        papers = json.load(f)
    return papers


# 提取作者的H指数、发表年份和引用次数
def extract_author_metrics(papers):
    author_metrics = {}
    for paper in papers:
        year = paper['year']
        citations = paper['n_citation']
        for author in paper['authors']:
            author_id = author['id']
            if author_id:  # 检查作者ID是否为空
                if author_id not in author_metrics:
                    author_metrics[author_id] = {
                        'citations': [],
                        'publication_years': []
                    }
                author_metrics[author_id]['citations'].append(citations)
                author_metrics[author_id]['publication_years'].append(year)

    # 计算H指数
    for author_id, metrics in author_metrics.items():
        metrics['h_index'] = calculate_h_index(metrics['citations'])

    return author_metrics


# 计算H指数
def calculate_h_index(citations):
    citations_sorted = sorted(citations, reverse=True)
    h_index = 0
    for i, c in enumerate(citations_sorted):
        if c >= (i + 1):
            h_index += 1
    return h_index


# 读取合作网络数据
def load_co_authorship_network(file_path):
    edges = pd.read_csv(file_path, sep='\t', header=None)
    return nx.from_pandas_edgelist(edges, 0, 1)


# 计算度中心性
def compute_degree_centrality(G):
    return nx.degree_centrality(G)


# 计算GapYear
def compute_gap_years(author_metrics):
    gap_years = {}
    for author_id, metrics in author_metrics.items():
        publication_years = metrics['publication_years']
        if len(publication_years) > 1:
            gap_years[author_id] = max(publication_years) - min(publication_years)
        else:
            gap_years[author_id] = float('inf')  # 只有一篇论文，设置为无穷大
    return gap_years


# 保存结果到文件
def save_results(author_metrics, degree_centrality, gap_years, output_file):
    results = []
    for author_id, metrics in author_metrics.items():
        if author_id and gap_years[author_id] != float('inf'):  # 检查作者ID不为空且GapYear不为无穷大
            results.append({
                'author_id': author_id,
                'h_index': metrics['h_index'],
                'degree_centrality': degree_centrality.get(author_id, 0),
                'gap_year': gap_years[author_id]
            })

    # 写入文件
    with open(output_file, 'w') as f:
        for result in results:
            f.write(f"{result['author_id']} {result['h_index']} {result['degree_centrality']} {result['gap_year']}\n")


# 主程序
def main(paper_file, co_authorship_file, output_file):
    papers = load_paper_data(paper_file)
    author_metrics = extract_author_metrics(papers)
    G = load_co_authorship_network(co_authorship_file)
    degree_centrality = compute_degree_centrality(G)
    gap_years = compute_gap_years(author_metrics)
    save_results(author_metrics, degree_centrality, gap_years, output_file)
    print("结果已保存到文件:", output_file)


# 调用主程序
main('AMiner-Citation_2014_2024.json', 'author_author.txt', 'author_metrics.txt')
