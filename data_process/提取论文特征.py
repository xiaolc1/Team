import json
from collections import defaultdict
from gensim import corpora, models
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import random

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# 假设你的JSON数据存储在一个文件中
json_file = '../../team_predict/AMiner/data_process/AMiner-Citation_2014_2024.json'
output_file = '../../team_predict/AMiner/data_process/paper_stats.txt'

# 读取JSON数据
with open(json_file, 'r') as f:
    data = json.load(f)

# 只处理百分之一的数据
sample_size = max(1, len(data) // 1)
sampled_data = random.sample(data, sample_size)

# 初始化列表来存储论文统计信息
paper_stats = []

# 用于LDA的文本数据
texts = []
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# 处理每篇论文
for i, paper in enumerate(sampled_data):
    paper_id = paper['id']
    citations = paper.get('n_citation', 0)
    references = paper.get('references', [])
    num_references = len(references)
    abstract = paper.get('abstract', '')

    # LDA分析准备：对摘要进行分词、去停用词、词形还原
    tokens = word_tokenize(abstract.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in stop_words]
    texts.append(tokens)

    # 保存统计信息
    paper_stats.append((paper_id, citations, num_references))

    # 每处理 10 篇论文打印一次进度
    if i % 10 == 0:
        print(f"Processed {i+1}/{sample_size} papers...")

# 创建词典和语料库
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

# 训练LDA模型
lda_model = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)

# 保存结果到文件
with open(output_file, 'w') as f:
    for i, (paper_id, citations, num_references) in enumerate(paper_stats):
        # 获取主题分布
        topics = lda_model[corpus[i]]
        # 找到概率最大的主题
        main_topic = max(topics, key=lambda x: x[1])
        f.write(f"{paper_id} {citations} {num_references} {main_topic[0]}\n")

print(f"Paper statistics and main topics have been saved to {output_file}")

