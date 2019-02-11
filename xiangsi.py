#比较两篇文档的相似度

import math
import numpy as np
import jieba
from collections import Counter
import time

#开始
starttime = time.time()


# 两篇待比较的文档的路径
sourcefile = '1.txt'
s2 = '2.txt'

#设置停用词词库
#其实可以不用停用词，越是停用词，越能反映文档的相似性
fenci = open(r'stopwords.txt', 'r', encoding='utf-8')
# 将停用次以列表的方式导入，方便使用
stopkey = [line.strip() for line in fenci.readlines()]

# 去停用词
def stopwords(seglist):

    stayed_word=[]
    for word in seglist:
        if word not in stopkey:
            stayed_word.append(word)
    return stayed_word


# 关键词统计和词频统计，以列表形式返回
def Count(resfile):

    with open(resfile,'r',encoding='utf-8') as f:
        seg_list = list(jieba.cut(f.read()))
    seg_list=stopwords(seg_list)  # 去停用词

    dic=Counter(seg_list)  #统计词频

    return (dic)

def MergeWord(T1, T2):  #求并集

    return list(set(list(T1.keys())).union(set(list(T2.keys()))))

# 得出文档向量
def CalVector(T1, mergeWord):
    TF1=[]
    for ch in mergeWord:
        if ch in T1:
            TF1.append(T1[ch])
        else:
            TF1.append(0)
    return TF1

def CalConDis(v1, v2, lengthVector):

    a1 = np.asarray(v1)
    a2 = np.asarray(v2)
    A = math.sqrt(np.sum(a1**2)) * math.sqrt(np.sum(a1**2))
    B=np.sum(a1*a2)

    return format(float(B) / A, ".3f")


T1 = Count(sourcefile)
# print("文档1的词频统计如下：")

T2 = Count(s2)
# print("文档2的词频统计如下：")

# 合并两篇文档的关键词
mergeword = MergeWord(T1, T2)
# print('合并两篇文档的关键词',mergeword)

# 得出文档向量
v1 = CalVector(T1, mergeword)
# print("文档1向量化得到的向量如下：")

v2 = CalVector(T2, mergeword)
# print("文档2向量化得到的向量如下：")

# 计算余弦距离
print('两篇文章的相似度 = ',CalConDis(v1, v2, len(mergeword)))

#结束
endtime = time.time()
print('耗时： ',format(endtime - starttime,'.3f'),'  秒')